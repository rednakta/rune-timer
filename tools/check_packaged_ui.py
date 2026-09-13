# SPDX-License-Identifier: GPL-3.0-or-later
"""Check packaged assets and first-run launch without changing user preferences."""
from pathlib import Path
import ctypes
from ctypes import wintypes
import os
import json
import subprocess
import tempfile
import time
import psutil
from PyInstaller.archive.readers import CArchiveReader

ROOT = Path(__file__).resolve().parents[1]
user32 = ctypes.windll.user32
user32.GetWindowTextW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
user32.GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
user32.PostMessageW.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
callback_type = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)

for profile, suffix in [('low', 'LowRes'), ('high', 'HighRes')]:
    exe = ROOT / 'dist' / 'RuneTimer.exe'
    archive = CArchiveReader(str(exe))
    names = {name.replace('\\', '/') for name in archive.toc}
    for asset in ('settings_icon.png','nilbox_splash_icon.png','maple_timer_custom_icon.ico'):
        assert f'assets/ui/{profile}/{asset}' in names, asset
    other = 'high' if profile == 'low' else 'low'
    assert any(name.startswith(f'assets/ui/{other}/') for name in names)
    with tempfile.TemporaryDirectory() as home:
        if profile == 'high':
            preferences = Path(home) / 'AppData' / 'Roaming' / 'MapleTimerAutoDetect'
            preferences.mkdir(parents=True)
            (preferences / 'ui-profile.json').write_text(json.dumps(profile), encoding='utf-8')
        env = dict(os.environ, USERPROFILE=home)
        startup = subprocess.STARTUPINFO()
        startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startup.wShowWindow = 0
        process = subprocess.Popen([str(exe)], env=env, startupinfo=startup)
        found = []
        try:
            deadline = time.monotonic() + 45
            while time.monotonic() < deadline and process.poll() is None:
                pids = {process.pid} | {p.pid for p in psutil.Process(process.pid).children(recursive=True)}
                found = []
                @callback_type
                def visit(hwnd, _):
                    pid = wintypes.DWORD()
                    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
                    if pid.value in pids:
                        text = ctypes.create_unicode_buffer(256)
                        user32.GetWindowTextW(hwnd, text, 256)
                        found.append((hwnd, text.value))
                    return True
                user32.EnumWindows(visit, 0)
                if any(title == '이용약관' for _, title in found):
                    break
                time.sleep(0.2)
            assert any(title == '이용약관' for _,title in found), (profile, found, process.poll())
            expected = '저해상도' if profile == 'low' else '고해상도'
            assert any(expected in title for _,title in found), (profile,found)
            for hwnd,title in found:
                if title == '이용약관':
                    user32.PostMessageW(hwnd, 0x0010, 0, 0)
            process.wait(timeout=10)
            assert process.returncode == 0, process.returncode
            print(profile, 'packaged assets, correct profile, first-run UI, clean exit: PASS')
        finally:
            if process.poll() is None:
                parent = psutil.Process(process.pid)
                for child in parent.children(recursive=True):
                    child.kill()
                parent.kill()
                process.wait(timeout=10)
