"""Minimal Chrome DevTools Protocol client over `websockets`.

Shared by layout.py (measures rendered boxes) and screenshot.py (captures
pages). Launches the local Chrome headless, opens page targets, and correlates
requests with responses. No browser-automation dependency needed.
"""
from __future__ import annotations

import asyncio
import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request
from contextlib import asynccontextmanager
from pathlib import Path

import websockets

CHROME_CANDIDATES = [
    os.environ.get("CHROME", ""),
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser",
]


def chrome() -> str:
    for c in CHROME_CANDIDATES:
        if c and Path(c).exists():
            return c
    sys.exit("Chrome not found; set CHROME=/path/to/chrome")


def free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class Tab:
    """One DevTools page target with request/response correlation."""

    def __init__(self, ws):
        self.ws, self.next_id, self.pending, self.events = ws, 0, {}, asyncio.Queue()
        self.reader = asyncio.create_task(self._read())

    async def _read(self):
        async for raw in self.ws:
            msg = json.loads(raw)
            if "id" in msg and msg["id"] in self.pending:
                self.pending.pop(msg["id"]).set_result(msg)
            elif "method" in msg:
                await self.events.put(msg)

    async def send(self, method: str, params: dict | None = None, timeout: float = 40) -> dict:
        self.next_id += 1
        fut = asyncio.get_running_loop().create_future()
        self.pending[self.next_id] = fut
        await self.ws.send(json.dumps({"id": self.next_id, "method": method, "params": params or {}}))
        return await asyncio.wait_for(fut, timeout)

    async def wait_event(self, name: str, timeout: float) -> bool:
        end = time.monotonic() + timeout
        while (left := end - time.monotonic()) > 0:
            try:
                ev = await asyncio.wait_for(self.events.get(), left)
            except asyncio.TimeoutError:
                return False
            if ev.get("method") == name:
                return True
        return False

    def drain(self) -> None:
        while not self.events.empty():
            self.events.get_nowait()

    async def emulate(self, width: int, height: int, scheme: str = "dark") -> None:
        """Phone-faithful when width < 700: mobile viewport semantics, not just a narrow window."""
        await self.send("Emulation.setDeviceMetricsOverride",
                        {"width": width, "height": height, "deviceScaleFactor": 1, "mobile": width < 700})
        await self.send("Emulation.setEmulatedMedia",
                        {"features": [{"name": "prefers-color-scheme", "value": scheme}]})


@asynccontextmanager
async def browser():
    """Yields a function that opens a new Tab in a throwaway headless Chrome."""
    port, tmp = free_port(), Path(tempfile.mkdtemp(prefix="cdp-"))
    proc = subprocess.Popen([chrome(), "--headless=new", "--no-sandbox", "--disable-gpu",
                             "--disable-dev-shm-usage", "--no-first-run", "--mute-audio",
                             "--hide-scrollbars", f"--remote-debugging-port={port}",
                             f"--user-data-dir={tmp}", "about:blank"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    conns = []
    try:
        for _ in range(60):
            try:
                urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=1)
                break
            except Exception:
                await asyncio.sleep(0.5)

        async def new_tab() -> Tab:
            req = urllib.request.Request(f"http://127.0.0.1:{port}/json/new?about:blank", method="PUT")
            target = json.loads(urllib.request.urlopen(req).read())
            ws = await websockets.connect(target["webSocketDebuggerUrl"], max_size=80_000_000)
            conns.append(ws)
            tab = Tab(ws)
            await tab.send("Page.enable")
            return tab

        yield new_tab
    finally:
        for ws in conns:
            try:
                await ws.close()
            except Exception:
                pass
        proc.terminate()
        try:
            proc.wait(10)
        except subprocess.TimeoutExpired:
            proc.kill()
        shutil.rmtree(tmp, ignore_errors=True)
