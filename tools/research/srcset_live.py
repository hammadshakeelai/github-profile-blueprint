#!/usr/bin/env python3
"""Track 1, live half: load real profile pages and see which file a relative
`<picture><source srcset>` actually serves.

    python tools/research/srcset.py        # writes the candidate list first
    python tools/research/srcset_live.py

Read-only. Loads public profile pages in headless Chrome at 1280px in the dark
scheme and reads each `<picture>` img's currentSrc. Nothing is edited on any
profile, which is why this question was answerable at all.

A candidate's "wanted" file is the first relative dark source in its README; if
that happens to be a mobile (max-width) source, the desktop pass legitimately
reports a mismatch. Read the filename in the output before believing one.
"""
import asyncio, json, sys
sys.path.insert(0,"tools/survey")
from cdp import browser
C = json.load(open("/tmp/relcands.json"))
JS = """(async()=>{const i=[...document.querySelectorAll('.js-profile-readme picture img, article.markdown-body picture img')];
await Promise.race([Promise.all(i.map(x=>x.complete?0:new Promise(r=>{x.onload=r;x.onerror=r}))),new Promise(r=>setTimeout(r,10000))]);
await new Promise(r=>setTimeout(r,1500));
return JSON.stringify([...document.querySelectorAll('.js-profile-readme picture img, article.markdown-body picture img')].map(x=>({cur:x.currentSrc,ok:x.naturalWidth>0})))})()"""
async def one(new_tab, user, want, sem):
    async with sem:
        t = await new_tab()
        try:
            await t.emulate(1280, 1400, "dark"); t.drain()
            await t.send("Page.navigate", {"url": f"https://github.com/{user}"})
            await t.wait_event("Page.loadEventFired", 30)
            r = await t.send("Runtime.evaluate", {"expression": JS, "awaitPromise": True}, timeout=40)
            rows = json.loads(r["result"]["result"]["value"])
            stem = want.split("?")[0].rsplit("/",1)[-1].lower()
            hit = [x for x in rows if stem in x["cur"].lower()]
            if not rows: return user, "no <picture> found"
            if hit: return user, ("RESOLVED — dark file served" + ("" if hit[0]["ok"] else ", but the file is broken"))
            return user, "MISMATCH — dark file not served; got " + rows[0]["cur"].rsplit("/",1)[-1][:50]
        except Exception as e: return user, f"error {type(e).__name__}"
        finally:
            t.reader.cancel(); await t.ws.close()
async def main():
    sem = asyncio.Semaphore(3)
    async with browser() as nt:
        for u, r in await asyncio.gather(*(one(nt,u,w,sem) for u,w in C.items())):
            print(f"{u:22} {r}")
asyncio.run(main())
