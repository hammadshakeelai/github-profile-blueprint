# seek-capture.ps1 — deterministic frame capture for SUPER-REEL.svg
# Chrome's --virtual-time-budget is flaky with SMIL (often screenshots t=0).
# This harness injects a throwaway <script> into a QA COPY of the SVG (never
# the deliverable), pauses SMIL + CSS timelines, seeks to T ms, then shoots.
# Usage: .\seek-capture.ps1 14500 16500
param(
  [Parameter(Mandatory = $true)][int[]]$Times
)

$ErrorActionPreference = "Stop"
$chrome = "C:\Program Files\Google\Chrome\Application\chrome.exe"
$root   = Split-Path -Parent $MyInvocation.MyCommand.Path
$src    = Join-Path $root "SUPER-REEL.svg"
$shots  = Join-Path $root "shots"
$ud     = Join-Path $env:TEMP "opencode\chromeprofile"

if (-not (Test-Path $shots)) { New-Item -ItemType Directory -Path $shots | Out-Null }

$svgText = [System.IO.File]::ReadAllText($src, [System.Text.Encoding]::UTF8)
$js = @'
<script type="text/javascript"><![CDATA[
(function(){
  var T = __T__;
  function seek(){
    try { var s = document.documentElement; s.pauseAnimations(); s.setCurrentTime(T/1000); } catch(e){}
    try { document.getAnimations().forEach(function(a){ a.pause(); a.currentTime = T; }); } catch(e){}
  }
  seek();
  if (window.requestAnimationFrame) requestAnimationFrame(function(){ requestAnimationFrame(seek); });
})();
]]></script>
'@

foreach ($t in $Times) {
  $qa   = $svgText.Replace("</svg>", ($js.Replace("__T__", "$t")) + "`n</svg>")
  $qf   = Join-Path $shots "qa_$t.svg"
  $out  = Join-Path $shots "seek_$t.png"
  [System.IO.File]::WriteAllText($qf, $qa, (New-Object System.Text.UTF8Encoding($false)))
  $url  = "file:///" + (($qf -replace '\\', '/'))
  & $chrome --headless --disable-gpu --hide-scrollbars --no-first-run --no-default-browser-check `
    --user-data-dir="$ud" --screenshot="$out" --window-size=1280,720 `
    --virtual-time-budget=1200 $url 2>&1 | Out-Null
  Start-Sleep -Milliseconds 600
  if (Test-Path $out) { "seek_$t = $((Get-Item $out).Length) bytes" } else { "seek_$t MISSING" }
}
