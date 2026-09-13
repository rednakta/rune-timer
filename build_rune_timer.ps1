# SPDX-License-Identifier: GPL-3.0-or-later
$ErrorActionPreference = 'Stop'
Push-Location $PSScriptRoot
try {
    python tools/build_ui_assets.py
    if ($LASTEXITCODE -ne 0) { throw 'UI asset build failed' }
    python -m PyInstaller --noconfirm --workpath build/unified rune_timer.spec
    if ($LASTEXITCODE -ne 0) { throw 'Build failed' }
} finally {
    Pop-Location
}
