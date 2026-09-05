# -*- mode: python ; coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 rednakta


a = Analysis(
    ['pip_timer_auto_detect_app.pyw'],
    pathex=[],
    binaries=[],
    datas=[
        ('.\\maple_timer_custom_icon.ico', '.'),
        ('.\\THIRD_PARTY_LICENSES.txt', '.'),
        ('.\\LICENSE', '.'),
        ('.\\settings_icon.png', '.'),
        ('.\\nilbox_splash_icon.png', '.'),
        ('.\\nilbox_splash_icon_blur.png', '.'),
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
    name='룬 타이머',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['maple_timer_custom_icon.ico'],
)
