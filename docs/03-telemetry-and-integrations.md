# Real-Time Telemetry, Live APIs, and Serverless SVG Endpoints

This document provides complete architectures and deployable code for streaming real-time metrics—including Spotify playback, WakaTime coding activity, and system uptime—directly into your GitHub profile.

---

## 1. The Real-Time Architecture: Overcoming Camo & Rate Limits

Because GitHub Markdown cannot execute client-side JavaScript, live streaming requires an image tag pointing to an edge function that generates a dynamic SVG response in real time:

```text
Visitor loads Profile 
         │
         ▼
GitHub UI queries: 
https://camo.githubusercontent.com/...
         │
         ▼
Camo requests:
https://telemetry.yourdomain.workers.dev/spotify.svg
         │
         ├── Edge Worker reads Spotify API / KV Store
         ├── Renders inline SVG with dynamic track & equalizer animation
         └── Returns response with `Cache-Control: max-age=0, no-cache`
         ▼
Live SVG renders on Visitor's screen (< 150ms)
```

---

## 2. Spotify Live Telemetry: Edge Worker Implementation

This production-ready **Cloudflare Worker** connects to the Spotify Web API using an OAuth2 refresh token, retrieves the currently playing song (or most recent track), and returns a dynamic SVG card with an animated audio equalizer.

### Cloudflare Worker Script (`worker.js` / `src/index.ts`)

```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);

    if (url.pathname !== "/spotify.svg") {
      return new Response("Not Found", { status: 404 });
    }

    try {
      const track = await getNowPlaying(env);
      const svg = renderSpotifySVG(track);

      return new Response(svg, {
        headers: {
          "Content-Type": "image/svg+xml; charset=utf-8",
          "Cache-Control": "no-cache, no-store, must-revalidate, max-age=0, s-maxage=0",
          "Pragma": "no-cache",
          "Expires": "0",
          "Surrogate-Control": "no-store",
          "Access-Control-Allow-Origin": "*"
        }
      });
    } catch (err) {
      const fallbackSvg = renderSpotifySVG({
        isPlaying: false,
        title: "Offline / Sleeping",
        artist: "No active stream",
        progressMs: 0,
        durationMs: 1
      });

      return new Response(fallbackSvg, {
        headers: {
          "Content-Type": "image/svg+xml; charset=utf-8",
          "Cache-Control": "max-age=60"
        }
      });
    }
  }
};

interface TrackData {
  isPlaying: boolean;
  title: string;
  artist: string;
  progressMs: number;
  durationMs: number;
}

interface Env {
  SPOTIFY_CLIENT_ID: string;
  SPOTIFY_CLIENT_SECRET: string;
  SPOTIFY_REFRESH_TOKEN: string;
}

async function getAccessToken(env: Env): Promise<string> {
  const basic = btoa(`${env.SPOTIFY_CLIENT_ID}:${env.SPOTIFY_CLIENT_SECRET}`);
  const response = await fetch("https://accounts.spotify.com/api/token", {
    method: "POST",
    headers: {
      "Authorization": `Basic ${basic}`,
      "Content-Type": "application/x-www-form-urlencoded"
    },
    body: new URLSearchParams({
      grant_type: "refresh_token",
      refresh_token: env.SPOTIFY_REFRESH_TOKEN
    })
  });

  const data: any = await response.json();
  return data.access_token;
}

async function getNowPlaying(env: Env): Promise<TrackData> {
  const token = await getAccessToken(env);
  const response = await fetch("https://api.spotify.com/v1/me/player/currently-playing", {
    headers: { "Authorization": `Bearer ${token}` }
  });

  if (response.status === 204 || response.status > 400) {
    return {
      isPlaying: false,
      title: "Not Playing",
      artist: "Spotify Inactive",
      progressMs: 0,
      durationMs: 100
    };
  }

  const item: any = await response.json();
  return {
    isPlaying: item.is_playing,
    title: item.item?.name || "Unknown Track",
    artist: item.item?.artists?.map((a: any) => a.name).join(", ") || "Unknown Artist",
    progressMs: item.progress_ms || 0,
    durationMs: item.item?.duration_ms || 1
  };
}

function renderSpotifySVG(track: TrackData): string {
  const progressPercent = Math.min(100, Math.round((track.progressMs / track.durationMs) * 100));
  const safeTitle = escapeXml(track.title.length > 28 ? track.title.slice(0, 25) + "..." : track.title);
  const safeArtist = escapeXml(track.artist.length > 32 ? track.artist.slice(0, 29) + "..." : track.artist);

  return `
<svg xmlns="http://www.w3.org/2000/svg" width="400" height="110" viewBox="0 0 400 110">
  <defs>
    <style>
      .card { fill: #0d1117; stroke: #30363d; stroke-width: 1; rx: 8px; }
      .title { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', monospace; font-size: 14px; font-weight: bold; fill: #58a6ff; }
      .artist { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', monospace; font-size: 12px; fill: #8b949e; }
      .status { font-family: monospace; font-size: 10px; fill: #3fb950; text-transform: uppercase; letter-spacing: 1px; }
      .bar-bg { fill: #21262d; rx: 3px; }
      .bar-fill { fill: #1db954; rx: 3px; }
      .eq-bar { fill: #1db954; transform-origin: bottom; }
      @keyframes bounce1 { 0%, 100% { height: 4px; } 50% { height: 16px; } }
      @keyframes bounce2 { 0%, 100% { height: 14px; } 50% { height: 6px; } }
      @keyframes bounce3 { 0%, 100% { height: 8px; } 50% { height: 18px; } }
      .eq1 { animation: bounce1 1.1s infinite ease-in-out; }
      .eq2 { animation: bounce2 0.8s infinite ease-in-out; }
      .eq3 { animation: bounce3 1.3s infinite ease-in-out; }
    </style>
  </defs>

  <rect class="card" x="1" y="1" width="398" height="108"/>

  <!-- Status & Equalizer Icon -->
  <g transform="translate(20, 24)">
    <text class="status" x="0" y="0">${track.isPlaying ? "● LIVE SPOTIFY PLAYBACK" : "○ RECENTLY PLAYED"}</text>
    ${track.isPlaying ? `
      <g transform="translate(180, -10)">
        <rect class="eq-bar eq1" x="0" y="0" width="3" height="12"/>
        <rect class="eq-bar eq2" x="5" y="0" width="3" height="12"/>
        <rect class="eq-bar eq3" x="10" y="0" width="3" height="12"/>
      </g>
    ` : ""}
  </g>

  <!-- Track Title & Artist -->
  <text class="title" x="20" y="52">${safeTitle}</text>
  <text class="artist" x="20" y="72">${safeArtist}</text>

  <!-- Progress Bar -->
  <rect class="bar-bg" x="20" y="86" width="360" height="5"/>
  <rect class="bar-fill" x="20" y="86" width="${(360 * progressPercent) / 100}" height="5"/>
</svg>
`.trim();
}

function escapeXml(unsafe: string): string {
  return unsafe.replace(/[<>&'"]/g, (c) => {
    switch (c) {
      case '<': return '&lt;';
      case '>': return '&gt;';
      case '&': return '&amp;';
      case '\'': return '&apos;';
      case '"': return '&quot;';
      default: return c;
    }
  });
}
```

---

## 3. WakaTime / Code Time Telemetry

WakaTime records editor activity from plugins in Neovim, VS Code, and JetBrains.

### Embedding via Dynamic SVG Badge
```markdown
<p align="center">
  <img src="https://github-readme-stats.vercel.app/api/wakatime?username=your_wakatime_user&layout=compact&theme=tokyonight" alt="WakaTime Stats" />
</p>
```

### Pulling WakaTime Metrics in GitHub Actions (Git-Native)
To prevent reliance on third-party uptime, fetch from WakaTime's REST API during a scheduled GitHub Action:

```bash
# Fetch last 7 days of coding time
curl -s "https://wakatime.com/api/v1/users/current/stats/last_7_days?api_key=${WAKATIME_API_KEY}" \
  | jq -r '.data | {total: .human_readable_total, languages: [.languages[0:3][] | {name: .name, percent: .percent}]}'
```

---

## 4. Homelab / System Uptime & Neovim Status

You can push live status from your local development workstation or server directly to GitHub or a serverless KV store.

### Architecture:
1. **Workstation / Server Hook**: A systemd timer, cron job, or Neovim autocmd (`FocusGained`, `BufEnter`) sends a heartbeat ping to your Cloudflare Worker:
   ```bash
   curl -X POST https://telemetry.yourdomain.workers.dev/heartbeat \
     -H "Authorization: Bearer ${SECRET_PING_KEY}" \
     -d '{"status":"Editing Rust in Neovim","project":"consensus-engine"}'
   ```
2. **Worker Store**: Saves the payload with a 10-minute TTL to Cloudflare KV.
3. **SVG Renderer**: When the profile renders, the worker returns "🟢 Currently active in Neovim: consensus-engine" if the key is live, or "⚪ Away / Offline" if expired.
