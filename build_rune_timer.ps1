# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 rednakta
$ErrorActionPreference = "Stop"

python -m PyInstaller `
  --noconfirm `
  "rune_timer.spec"
