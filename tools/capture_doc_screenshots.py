import ctypes
import sys
import time
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pip_timer_auto_detect_app as appmod


OUT_DIR = Path(__file__).resolve().parents[1] / "docs" / "screenshots"
OUT_DIR.mkdir(parents=True, exist_ok=True)


class RECT(ctypes.Structure):
    _fields_ = [
        ("left", ctypes.c_long),
        ("top", ctypes.c_long),
        ("right", ctypes.c_long),
        ("bottom", ctypes.c_long),
    ]


def hwnd_for_tk(window):
    user32 = ctypes.windll.user32
    hwnd = window.winfo_id()
    parent = user32.GetParent(hwnd)
    return parent or hwnd


def capture_window(window, output_name):
    user32 = ctypes.windll.user32
    gdi32 = ctypes.windll.gdi32

    hwnd = hwnd_for_tk(window)
    rect = RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(rect))
    width = max(1, rect.right - rect.left)
    height = max(1, rect.bottom - rect.top)

    hdc_window = user32.GetWindowDC(hwnd)
    hdc_mem = gdi32.CreateCompatibleDC(hdc_window)
    hbitmap = gdi32.CreateCompatibleBitmap(hdc_window, width, height)
    old_obj = gdi32.SelectObject(hdc_mem, hbitmap)
    user32.PrintWindow(hwnd, hdc_mem, 2)

    bmi = BITMAPINFOHEADER()
    bmi.biSize = ctypes.sizeof(BITMAPINFOHEADER)
    bmi.biWidth = width
    bmi.biHeight = -height
    bmi.biPlanes = 1
    bmi.biBitCount = 32
    bmi.biCompression = 0
    buffer = ctypes.create_string_buffer(width * height * 4)
    gdi32.GetDIBits(hdc_mem, hbitmap, 0, height, buffer, ctypes.byref(bmi), 0)

    image = Image.frombuffer("RGBA", (width, height), buffer, "raw", "BGRA", 0, 1).convert("RGB")
    output_path = OUT_DIR / output_name
    image.save(output_path)

    gdi32.SelectObject(hdc_mem, old_obj)
    gdi32.DeleteObject(hbitmap)
    gdi32.DeleteDC(hdc_mem)
    user32.ReleaseDC(hwnd, hdc_window)
    return output_path


class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [
        ("biSize", ctypes.c_uint32),
        ("biWidth", ctypes.c_int32),
        ("biHeight", ctypes.c_int32),
        ("biPlanes", ctypes.c_uint16),
        ("biBitCount", ctypes.c_uint16),
        ("biCompression", ctypes.c_uint32),
        ("biSizeImage", ctypes.c_uint32),
        ("biXPelsPerMeter", ctypes.c_int32),
        ("biYPelsPerMeter", ctypes.c_int32),
        ("biClrUsed", ctypes.c_uint32),
        ("biClrImportant", ctypes.c_uint32),
    ]


def main():
    appmod.MapleTimerApp._disclaimer_acceptance_required = lambda self: False
    app = appmod.MapleTimerApp()
    app.app_size = appmod.DEFAULT_APP_SIZE
    app.app_position = (80, 80)
    app.root.geometry(f"{appmod.DEFAULT_APP_SIZE[0]}x{appmod.DEFAULT_APP_SIZE[1]}+80+80")
    app._start_main_app_after_disclaimer()
    app.root.update_idletasks()
    app.root.update()
    time.sleep(0.2)
    app.root.update()
    home = capture_window(app.root, "rune-timer-home.png")

    app._show_page("settings")
    app.root.update_idletasks()
    app.root.update()
    time.sleep(0.2)
    app.root.update()
    settings = capture_window(app.root, "rune-timer-settings-manual-mode.png")

    app._show_widget_mode()
    app.root.update_idletasks()
    app.root.update()
    time.sleep(0.2)
    app.root.update()
    app.widget.update()
    widget = capture_window(app.widget, "rune-timer-widget-mode.png")

    print(home)
    print(settings)
    print(widget)
    app._quit_app()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
