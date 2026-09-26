param(
  [string]$PartsDir = (Join-Path $PSScriptRoot "parts"),
  [string]$Out = (Join-Path (Split-Path $PSScriptRoot -Parent) "BOOK-OF-CREATIVITY.md")
)
$ErrorActionPreference = "Stop"
$enc = New-Object System.Text.UTF8Encoding($false)
$EM = [char]0x2014
$MID = [char]0x00B7
$SEP = "`r`n`r`n---`r`n`r`n"

$files = Get-ChildItem $PartsDir -File |
  Where-Object { $_.Name -match '^[0-9]+-.*\.md$' } |
  Sort-Object Name
if (-not $files) { throw "No part files matching [0-9]+-*.md in $PartsDir" }

function Get-Slug([string]$s) {
  $s = $s.ToLowerInvariant()
  $s = $s -replace '[^a-z0-9 -]', ''
  $s = $s -replace ' ', '-'
  $s = $s -replace '-{2,}', '-'
  return $s
}

$parts = @()
foreach ($f in $files) {
  $text = [System.IO.File]::ReadAllText($f.FullName, [System.Text.Encoding]::UTF8)
  $first = ($text -split "`r?`n", 2)[0]
  if ($first -notmatch '^# (Part [0-9]{2} .+)$') { throw "First line of $($f.Name) is not a Part heading: $first" }
  $parts += [pscustomobject]@{
    Name   = $f.Name
    Title  = $Matches[1]
    Slug   = Get-Slug $Matches[1]
    SizeKB = [math]::Round($f.Length / 1024, 1)
    Body   = $text.TrimEnd("`r", "`n")
  }
}

$firstNum = $parts[0].Title.Substring(5, 2)
$lastNum = $parts[-1].Title.Substring(5, 2)

$headerLines = @(
  "# THE BOOK OF CREATIVITY $EM GitHub Profile README Research, Complete"
  ""
  "> **One document to rule them all.** Every finding from the 446-profile survey, the technique catalogue, the three-engine capability matrix, the Profile README Book, the two built profiles, all AI work across every branch, 39 freshly-hunted live profiles in two waves, a verbatim motion-code deep-dive, and 99 generators/tools with embed code $EM assembled by script from nine parallel research agents."
  ">"
  "> Assembled: 2026-09-26 $MID Branch: ``helper/side-person_opencode`` $MID Source parts: ``opencode-research/parts/$firstNum..$lastNum-*.md`` $MID Upstream: https://github.com/hammadshakeelai/github-profile-blueprint"
  ""
  "## Table of Contents"
  ""
  ""
)
$tocLines = foreach ($p in $parts) {
  "- [$($p.Title)](#$($p.Slug)) $EM ``$($p.Name)`` ($($p.SizeKB) KB)"
}

$outText = ($headerLines -join "`r`n") + ($tocLines -join "`r`n") + $SEP +
  (($parts | ForEach-Object { $_.Body }) -join $SEP) + $SEP
[System.IO.File]::WriteAllText($Out, $outText, $enc)

Write-Output "Assembled $($parts.Count) parts -> $Out ($([math]::Round((Get-Item $Out).Length/1024,1)) KB)"
