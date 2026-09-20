# Visual Design, Layout Hacks, and SVG Engineering for GitHub Profile READMEs

This guide covers the technical mechanisms, quirks, and engineering techniques for building visual layouts, responsive themes, animated vector graphics, and navigating GitHub's content rendering pipeline.

---

## 1. GitHub HTML Sanitization Engine

GitHub's Markdown pipeline (`github/markup` and GitHub Flavored Markdown) processes all markdown through an aggressive HTML sanitization filter before rendering it in the browser. Understanding what survives this filter is essential for crafting advanced layouts.

### Whitelisted HTML Elements
* **Structural**: `<div>`, `<span>`, `<p>`, `<h1>` to `<h6>`, `<hr>`, `<br>`, `<blockquote>`, `<pre>`, `<code>`
* **Tabular Layouts**: `<table>`, `<thead>`, `<tbody>`, `<tr>`, `<th>`, `<td>`
* **Lists**: `<ul>`, `<ol>`, `<li>`
* **Media & Links**: `<a>`, `<img>`, `<picture>`, `<source>`
* **Typography & Accents**: `<sub>`, `<sup>`, `<kbd>`, `<b>`, `<strong>`, `<i>`, `<em>`, `<del>`
* **Interactive Disclosures**: `<details>`, `<summary>`

### Stripped or Blocked Elements & Attributes
* **Strictly Scrubbed Tags**: `<style>`, `<script>`, `<iframe>`, `<object>`, `<embed>`, `<form>`, `<input>`, `<button>`, `<svg>` (in raw markdown; SVGs must be embedded via `<img>` or `<picture>`).
* **Scrubbed Inline Attributes**: The `style="..."` attribute is **completely stripped** from all HTML elements. You cannot write `<div style="display: flex;">` or `<td style="border: none;">`.
* **Allowed Layout Attributes**:
  * `align="left | center | right"`
  * `valign="top | middle | bottom"`
  * `width="..."` and `height="..."` (on `<img>`, `<td>`, `<th>`, and `<table>`)
  * `cellspacing="..."` and `cellpadding="..."` (on `<table>`)

---

## 2. Dark and Light Mode Theme Switching

GitHub natively supports switching assets based on the user's active theme (Default Light, Dark Default, Dark High Contrast, Dark Dimmed). There are three distinct architectures for theme-responsive assets:

### Architecture A: HTML5 `<picture>` Element (Recommended for Static Images)
The HTML5 `<picture>` tag is fully supported by GitHub's sanitizer and provides a zero-overhead, native browser mechanism for theme switching.

```html
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/username/username/main/assets/banner-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/username/username/main/assets/banner-light.svg">
    <img alt="Developer Profile Banner" src="https://raw.githubusercontent.com/username/username/main/assets/banner-light.svg" width="100%">
  </picture>
</p>
```

> **Implementation Rule**: Always provide a fallback `<img>` tag inside the `<picture>` element with an appropriate `alt` and default `src`.

---

### Architecture B: GitHub URL Theme Fragments
GitHub's internal stylesheet includes CSS selectors targeting image URL hash fragments (`#gh-dark-mode-only` and `#gh-light-mode-only`). This works cleanly with standard Markdown image syntax:

```markdown
![Architecture Dark](https://raw.githubusercontent.com/username/username/main/assets/architecture-dark.png#gh-dark-mode-only)
![Architecture Light](https://raw.githubusercontent.com/username/username/main/assets/architecture-light.png#gh-light-mode-only)
```

**How GitHub renders this**:
GitHub injects global CSS matching:
```css
[data-color-mode="dark"] [src$="#gh-light-mode-only"],
[data-color-mode="light"] [src$="#gh-dark-mode-only"] {
  display: none !important;
}
```

---

### Architecture C: In-SVG CSS Media Queries (Single Asset, Dual Theme)
When an SVG is embedded via `<img src="badge.svg">`, the browser executes the SVG in an isolated browsing context. The SVG cannot access external CSS or run JavaScript, but it **does** evaluate `@media (prefers-color-scheme: dark)`.

This enables a single SVG file to automatically theme itself without duplicating files:

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 450 120" width="450" height="120">
  <defs>
    <style>
      .canvas {
        fill: #f6f8fa;
        stroke: #d0d7de;
      }
      .title-text {
        fill: #1f2328;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
        font-size: 16px;
        font-weight: 600;
      }
      .subtitle-text {
        fill: #656d76;
        font-family: monospace;
        font-size: 12px;
      }
      .accent-line {
        stroke: #0969da;
        stroke-width: 3;
      }

      /* Dark Mode Media Query */
      @media (prefers-color-scheme: dark) {
        .canvas {
          fill: #0d1117;
          stroke: #30363d;
        }
        .title-text {
          fill: #f0f6fc;
        }
        .subtitle-text {
          fill: #8b949e;
        }
        .accent-line {
          stroke: #2f81f7;
        }
      }
    </style>
  </defs>

  <!-- Background Card -->
  <rect class="canvas" x="2" y="2" width="446" height="116" rx="8" stroke-width="1"/>
  <line class="accent-line" x1="2" y1="2" x2="2" y2="118"/>

  <!-- Content -->
  <text class="title-text" x="24" y="45">Principal Systems Architect</text>
  <text class="subtitle-text" x="24" y="75">STATUS: ONLINE // CLUSTER: US-EAST-1</text>
  <text class="subtitle-text" x="24" y="95">UPTIME: 99.98% // KERNEL: 6.12.4-ARCH</text>
</svg>
```

---

## 3. Layout Engineering & Multi-Column Grids

Because GitHub strips `style="display: flex"` and CSS Grid, responsive multi-column layouts must be implemented using HTML `<table>` elements with layout-specific attributes.

### Dual-Column Card Layout
```html
<table width="100%" cellspacing="0" cellpadding="8" border="0">
  <tr>
    <td width="50%" valign="top">
      <h3>Core Competencies</h3>
      <ul>
        <li>Distributed Consensus (Raft, Paxos)</li>
        <li>High-throughput message brokers (Kafka, NATS)</li>
        <li>Linux kernel telemetry (eBPF, BCC)</li>
      </ul>
    </td>
    <td width="50%" valign="top">
      <h3>Active Research</h3>
      <ul>
        <li>Deterministic simulation testing</li>
        <li>Memory-mapped IPC buffers in Rust</li>
        <li>Low-latency zero-copy networking</li>
      </ul>
    </td>
  </tr>
</table>
```

### Centered Badge & Icon Grids
To prevent jagged wrapping on mobile viewports, organize technology badges in fixed tables:

```html
<p align="center">
  <a href="https://go.dev">
    <img src="https://img.shields.io/badge/Go-00ADD8?style=for-the-badge&logo=go&logoColor=white" alt="Go" height="28">
  </a>
  <a href="https://rust-lang.org">
    <img src="https://img.shields.io/badge/Rust-000000?style=for-the-badge&logo=rust&logoColor=white" alt="Rust" height="28">
  </a>
  <a href="https://kubernetes.io">
    <img src="https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white" alt="K8s" height="28">
  </a>
  <a href="https://ebpf.io">
    <img src="https://img.shields.io/badge/eBPF-E95420?style=for-the-badge&logo=canonical&logoColor=white" alt="eBPF" height="28">
  </a>
</p>
```

### Collapsible Deep-Dive Accordions
Use `<details>` and `<summary>` to tuck away verbose telemetry, full resume histories, or interactive instructions without cluttering the primary viewport:

```html
<details>
  <summary><b>Detailed Cluster Topology & Personal Hardware Specs</b></summary>
  <br>

| Node | Architecture | OS / Kernel | Role | Storage |
| :--- | :--- | :--- | :--- | :--- |
| `helios-01` | AMD EPYC 7763 (64c/128t) | Alpine Linux 3.20 (LTS) | K3s Control Plane | 2TB NVMe ZFS |
| `helios-02` | Dual Intel Xeon Platinum | Debian 12 (Bookworm) | Heavy Worker / CI | 4TB U.2 NVMe |
| `helios-03` | Apple M3 Max (16c) | Asahi Linux (Kernel 6.11) | Local ML / Embedding | 1TB NVMe |

</details>
```

---

## 4. Pure SVG Vector Graphics & Animations

SVGs can execute keyframe CSS animations inside an `<img>` tag without triggering GitHub's script filters. This allows high-tech, living elements on your profile.

### Animated Typing / Blinking Cursor SVG
This SVG creates a looping terminal typing effect and blinking cursor:

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 80" width="600" height="80">
  <defs>
    <style>
      .terminal-bg {
        fill: #090d13;
        stroke: #1b222d;
        stroke-width: 1;
      }
      .prompt {
        font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
        font-size: 15px;
        fill: #27c93f;
      }
      .text-stream {
        font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
        font-size: 15px;
        fill: #d1d5db;
        white-space: pre;
      }
      .cursor {
        fill: #58a6ff;
        animation: blink 0.9s infinite step-end;
      }
      @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0; }
      }
      .typed-text {
        display: inline-block;
        overflow: hidden;
        animation: typeCycle 12s steps(45, end) infinite;
      }
      @keyframes typeCycle {
        0%, 10% { opacity: 0; }
        15%, 45% { opacity: 1; }
        50%, 55% { opacity: 0; }
        60%, 95% { opacity: 1; }
        100% { opacity: 0; }
      }
    </style>
  </defs>

  <rect class="terminal-bg" width="600" height="80" rx="8"/>
  <circle cx="20" cy="18" r="5" fill="#ff5f56"/>
  <circle cx="36" cy="18" r="5" fill="#ffbd2e"/>
  <circle cx="52" cy="18" r="5" fill="#27c93f"/>

  <text x="20" y="52" class="prompt">guest@engineer:~#</text>
  <text x="180" y="52" class="text-stream typed-text">cargo build --release --target=x86_64-unknown-none</text>
  <rect x="555" y="40" width="8" height="15" class="cursor"/>
</svg>
```

### Radar / Pulse Status Dot SVG
Creates an animated telemetry dot (green for online, amber for in meeting, red for focus):

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 30" width="200" height="30">
  <defs>
    <style>
      .beacon {
        fill: #238636;
      }
      .wave {
        fill: none;
        stroke: #238636;
        stroke-width: 2;
        transform-origin: 15px 15px;
        animation: pulse 2.2s infinite ease-out;
      }
      .label {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', monospace;
        font-size: 12px;
        font-weight: 600;
        fill: #3fb950;
      }
      @keyframes pulse {
        0% {
          r: 4px;
          opacity: 0.9;
        }
        100% {
          r: 12px;
          opacity: 0;
        }
      }
    </style>
  </defs>

  <circle class="wave" cx="15" cy="15" r="4"/>
  <circle class="beacon" cx="15" cy="15" r="4"/>
  <text x="32" y="19" class="label">LIVE: DEPLOYING CLUSTER</text>
</svg>
```

---

## 5. GitHub Camo Proxy Deep-Dive & Cache Invalidation

### What is GitHub Camo?
All external images linked in GitHub markdown files are rewritten to proxy through `https://camo.githubusercontent.com/<digest>/<hex_url>`.

```text
Markdown Source:
https://api.mytelemetry.com/status.svg

Rendered Browser Image Source:
https://camo.githubusercontent.com/9f7a8b6.../68747470733a2f2f6170692e...
```

**Why GitHub does this**:
1. **IP Anonymization**: Prevents external image servers from logging the IP addresses and user agents of visitors viewing GitHub repositories.
2. **Mixed Content Elimination**: Ensures all assets are delivered over secure HTTPS.
3. **SSRF Mitigation**: Validates that target resources are strictly images and do not trigger internal server-side exploits.

### The Camo Caching Trap
Camo caches images aggressively at GitHub's edge (using Fastly CDN). In default configurations, Camo ignores standard origin `Cache-Control: max-age=60` and can cache SVGs for hours or even days.

### Four Solutions for Live Dynamic SVGs

#### Strategy 1: The Canonical Origin Header Stack
If hosting an external serverless function (Vercel, Cloudflare Worker, AWS Lambda), return **all** of the following headers:

```http
Content-Type: image/svg+xml; charset=utf-8
Cache-Control: no-cache, no-store, must-revalidate, max-age=0, s-maxage=0
Pragma: no-cache
Expires: 0
Surrogate-Control: no-store
```

#### Strategy 2: Cache-Busting Query Parameter via CI
Because Camo generates its proxy URL by hashing the exact target URL string, modifying the query parameter creates a distinct Camo cache key:

```markdown
<!-- README template updated by GitHub Actions -->
<img src="https://my-api.com/badge.svg?v=202609202249">
```
Updating this timestamp inside your GitHub Actions workflow forces Camo to fetch fresh content on every commit.

#### Strategy 3: Issuing an HTTP PURGE Request
Fastly and Camo support the HTTP `PURGE` method. If you know the Camo URL, you can trigger an explicit cache wipe:

```bash
# Calculate or extract the Camo URL and purge it
CAMO_URL="https://camo.githubusercontent.com/<digest>/<hex_encoded_target>"
curl -s -X PURGE "$CAMO_URL"
```

You can automate this in GitHub Actions using community steps like `Angrido/Purge-Camo-Cache` or a custom bash one-liner.

#### Strategy 4: Git-Native Generation (The Gold Standard)
The most resilient and performant architecture bypasses external endpoints completely:
1. A GitHub Actions workflow runs on a schedule or event.
2. It fetches the required telemetry and renders an SVG file directly onto disk: `./assets/dynamic-status.svg`.
3. It commits the SVG into the repository.
4. The README references the local file via a relative path:
   ```markdown
   ![Status](./assets/dynamic-status.svg)
   ```
Relative assets are served from GitHub's raw storage cluster, which invalidates immediately whenever the commit hash changes. This yields **0ms third-party API latency**, **100% uptime reliability**, and **zero Camo caching delays**.
