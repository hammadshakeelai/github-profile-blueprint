# Edge Telemetry Worker: Live Spotify & Activity SVG Endpoint

This serverless Cloudflare Worker provides real-time SVG generation for GitHub Profile READMEs, engineered with specific origin headers to bypass GitHub Camo caching.

---

## 🚀 Quick Deployment Guide

### 1. Prerequisites
* [Node.js](https://nodejs.org) (v18+)
* [Cloudflare Account](https://cloudflare.com)
* [Spotify Developer App](https://developer.spotify.com/dashboard)

### 2. Configure Spotify API Credentials
1. Create an app in the Spotify Developer Dashboard.
2. Add `http://localhost:8888/callback` as a Redirect URI.
3. Obtain your **Client ID**, **Client Secret**, and generate a **Refresh Token** with the `user-read-currently-playing` and `user-read-recently-played` scopes.

### 3. Deploy to Cloudflare Workers
```bash
cd edge-telemetry-worker
npm install

# Authenticate wrangler with Cloudflare
npx wrangler login

# Set secret environment variables
npx wrangler secret put SPOTIFY_CLIENT_ID
npx wrangler secret put SPOTIFY_CLIENT_SECRET
npx wrangler secret put SPOTIFY_REFRESH_TOKEN

# Deploy to global edge
npm run deploy
```

### 4. Embed in GitHub Profile README
Once deployed, Cloudflare will output your worker URL (e.g. `https://profile-telemetry.yoursubdomain.workers.dev`). Embed it directly:

```markdown
<p align="center">
  <img src="https://profile-telemetry.yoursubdomain.workers.dev/spotify.svg" alt="Spotify Live Stream" width="400"/>
</p>
```
