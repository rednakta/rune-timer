param(
    [int]$DurationSeconds = 10800,
    [int]$IntervalSeconds = 10
)

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$outDir = Join-Path $root "benchmark_logs"
New-Item -ItemType Directory -Path $outDir -Force | Out-Null

$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$rawPath = Join-Path $outDir "resource_log_$stamp.csv"

"timestamp,process_name,pid,cpu_percent,private_mb,working_set_mb" | Out-File -LiteralPath $rawPath -Encoding utf8

$previousCpu = @{}
$endAt = (Get-Date).AddSeconds($DurationSeconds)

while ((Get-Date) -lt $endAt) {
    $now = Get-Date
    $processes = Get-Process | Where-Object {
        $_.ProcessName -eq "룬 타이머" -or
        $_.ProcessName -like "*Rune*" -or
        $_.ProcessName -like "*chrome*" -or
        $_.ProcessName -like "*msedge*"
    }

    foreach ($p in $processes) {
        $key = "$($p.Id)"
        $cpuSeconds = if ($null -ne $p.CPU) { [double]$p.CPU } else { 0.0 }
        $cpuPercent = 0.0
        if ($previousCpu.ContainsKey($key)) {
            $cpuDelta = [Math]::Max(0.0, $cpuSeconds - $previousCpu[$key])
            $cpuPercent = [Math]::Round(($cpuDelta / $IntervalSeconds) * 100.0, 2)
        }
        $previousCpu[$key] = $cpuSeconds

        $privateMb = [Math]::Round($p.PrivateMemorySize64 / 1MB, 2)
        $workingSetMb = [Math]::Round($p.WorkingSet64 / 1MB, 2)
        $line = '"{0}","{1}",{2},{3},{4},{5}' -f $now.ToString("s"), $p.ProcessName, $p.Id, $cpuPercent, $privateMb, $workingSetMb
        Add-Content -LiteralPath $rawPath -Value $line -Encoding utf8
    }

    Start-Sleep -Seconds $IntervalSeconds
}

Write-Output "saved: $rawPath"
