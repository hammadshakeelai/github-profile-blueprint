export interface Env {
  SPOTIFY_CLIENT_ID: string;
  SPOTIFY_CLIENT_SECRET: string;
  SPOTIFY_REFRESH_TOKEN: string;
}

interface TrackData {
  isPlaying: boolean;
  title: string;
  artist: string;
  progressMs: number;
  durationMs: number;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);

    if (url.pathname === "/spotify.svg") {
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

    return new Response("Profile Telemetry Edge Gateway Active. Endpoints: /spotify.svg", {
      headers: { "Content-Type": "text/plain" }
    });
  }
};

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
