# -*- mode: python ; coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 rednakta


a = Analysis(
    ['pip_timer_auto_detect_app.pyw'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets/ui', 'assets/ui'),
        ('.\\THIRD_PARTY_LICENSES.txt', '.'),
        ('.\\LICENSE', '.'),
        ('.\\assets\\sounds', 'assets\\sounds'),
        ('.\\assets\\fonts\\package\\src', 'assets\\fonts\\package\\src'),
        ('.\\assets\\fonts\\timer\\Poppins-Thin.ttf', 'assets\\fonts\\timer'),
        ('.\\assets\\fonts\\timer\\OFL.txt', 'assets\\fonts\\timer'),
    ],
    hiddenimports=['numpy'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'pandas', 'polars', 'scipy'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='RuneTimer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['assets/ui/high/maple_timer_custom_icon.ico'],
)
