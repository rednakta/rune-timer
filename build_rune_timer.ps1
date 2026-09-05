$ErrorActionPreference = "Stop"

python -m PyInstaller `
  --noconfirm `
  "rune_timer.spec"
