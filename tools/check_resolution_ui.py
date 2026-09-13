# SPDX-License-Identifier: GPL-3.0-or-later
"""Windows UI smoke checks; isolated settings and no capture/audio workers."""
import sys
from pathlib import Path
import tempfile
import time
import json
import tkinter as tk
from PIL import ImageGrab

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import pip_timer_auto_detect_app as mod

with tempfile.TemporaryDirectory() as temp:
    mod.APP_DIR = Path(temp)
    mod.SETTINGS_PATH = Path(temp) / 'settings.json'
    mod.prepare_sounds = lambda: {}
    mod.MapleTimerApp._sound_loop = lambda self: None
    mod.MapleTimerApp._start_main_app = lambda self: None
    mod.MapleTimerApp._show_startup_splash = lambda self: None
    app = mod.MapleTimerApp()
    errors = []
    app.root.report_callback_exception = lambda *args: errors.append(str(args))
    app.root.overrideredirect(True)
    app.root.deiconify()
    output = ROOT / 'test_outputs' / mod.UI_PROFILE
    output.mkdir(parents=True, exist_ok=True)
    def snapshot(name, win=None):
        win = win or app.root
        win.update_idletasks()
        win.update()
        x,y=win.winfo_rootx(),win.winfo_rooty()
        ImageGrab.grab(bbox=(x,y,x+win.winfo_width(),y+win.winfo_height())).save(output / (name+'.png'))
    for width,height in mod.APP_SIZE_PRESETS:
        app.app_size=(width,height)
        app.root.geometry(f'{width}x{height}+60+60')
        app.root.update()
        app._layout_monitor_page()
        app.root.update()
        x,y,size=app.countdown_card_metrics
        assert x >= 0 and x+size <= app.monitor_backdrop.winfo_width(), (width,'card')
        dock=app.bottom_dock
        assert y + size + int(32 * app._monitor_scale()) + max(4, int(17 * app._monitor_scale())) < dock.winfo_y(), ('gauge overlaps dock',width)
        assert dock.winfo_y()+dock.winfo_height() <= app.monitor_page.winfo_height(), (width,'dock',dock.winfo_y(),dock.winfo_height(),app.monitor_page.winfo_height())
        for region in app.bottom_dock_regions.values():
            assert 0 <= region[0] < region[2] <= dock.winfo_width(), region
            assert 0 <= region[1] < region[3] <= dock.winfo_height(), region
        if (width,height)==mod.APP_SIZE_PRESETS[0]:
            snapshot('minimum-home')
    app.app_size=mod.APP_SIZE_PRESETS[0]
    app.root.geometry(f'{app.app_size[0]}x{app.app_size[1]}+60+60')
    app._show_page('settings')
    app.root.update()
    snapshot('minimum-settings')
    view=app.settings_viewport
    bbox=view.bbox('all')
    assert bbox[0] >= -1 and bbox[2] <= view.winfo_width()+1, ('settings clipped',bbox,view.winfo_width())
    # Wheel events must work over child controls, with no visible native scrollbar.
    assert not any(isinstance(child, tk.Scrollbar) for child in view.master.winfo_children())
    entry = next(child for child in app.settings_stack.winfo_children()[0].winfo_children() if isinstance(child, tk.Frame))
    before = view.yview()[0]
    entry.event_generate('<MouseWheel>', delta=-120)
    app.root.update()
    assert view.yview()[0] > before
    view.yview_moveto(1)
    snapshot('settings-bottom')
    for width, height in mod.APP_SIZE_PRESETS:
        app.root.geometry(f'{width}x{height}+60+60')
        app.root.update()
        x, y = view.coords(app.settings_stack_item)
        assert abs(x - view.winfo_width() / 2) < 1
        content_height = app.settings_stack.winfo_reqheight()
        if (view.master.winfo_height() - content_height) / 2 >= view.winfo_y():
            assert abs(view.winfo_y() + y + content_height / 2 - view.master.winfo_height() / 2) < 1
        if content_height <= view.winfo_height():
            assert view.yview()[0] == 0
    snapshot('large-settings')
    app.root.geometry(f'{app.app_size[0]}x{app.app_size[1]}+60+60')
    app.root.update()
    app._ensure_widget_window()
    app.widget.geometry(f'{mod.WIDGET_WIDTH}x{mod.WIDGET_HEIGHT}+400+60')
    app.widget.attributes('-alpha', 1.0)
    app.widget.deiconify()
    app._draw_widget_mode(force=True)
    snapshot('widget',app.widget)
    for name in ('widget_restore_region','widget_count_region','widget_rune_region'):
        x1,y1,x2,y2=getattr(app,name)
        assert 0<=x1<x2<=mod.WIDGET_WIDTH and 0<=y1<y2<=mod.WIDGET_HEIGHT, (name,x1,y1,x2,y2)
    # Real state transitions with only audio output and process discovery stubbed.
    app._restore_from_widget_mode()
    app.root.update()
    assert not app.widget_mode_active and app.app_size == mod.APP_SIZE_PRESETS[0]
    app._show_page('monitor')
    app._toggle_warning_countdown_pause()
    assert not app.warning_timer_paused
    app.last_stall_alert_at -= 3
    app._toggle_warning_countdown_pause()
    assert app.warning_timer_paused and app.warning_paused_remaining < app.warning_loop_seconds - 2
    for key in ('warning', 'rune', 'tts'):
        setter = getattr(app, '_set_' + key + '_sound_enabled')
        setter(False)
        assert not getattr(app, key + '_sound_enabled')
        setter(True)
    app._set_warning_volume(37)
    app._set_rune_volume(62)
    app._set_rune_cooldown_minutes(10)
    app._set_offline_mode_enabled(True)
    assert app.offline_mode_enabled and not app.rune_capture_active
    app.last_rune_cleared_at = time.monotonic() - 300
    assert 0.49 < app._rune_cooldown_progress() < 0.51
    app._handle_widget_rune_click()
    assert app._rune_cooldown_progress() < 0.01
    app._set_offline_mode_enabled(False)
    app._maplestory_process_is_running = lambda: True
    calls = []
    app._play = calls.append
    app.rune_region = (0, 0, 100, 100)
    app._apply_monitor_result({'minimap_ok': True, 'score': app.rune_threshold + 10})
    assert app.rune_active_visual and app.rune_alert_latched and 'rune' in calls
    app._apply_monitor_result({'minimap_ok': True, 'score': 0})
    assert not app.rune_active_visual and not app.rune_alert_latched
    remaining = app._warning_remaining_float()
    paused = app.warning_timer_paused
    for profile in ('low', 'high'):
        app._set_ui_profile(profile)
        assert mod.load_ui_profile() == profile
        assert app.warning_timer_paused == paused
        assert abs(app._warning_remaining_float() - remaining) < 0.1
    app._save_settings()
    app.warning_volume = 0
    app._load_settings()
    assert app.warning_volume == 37 and app.rune_volume == 62 and app.rune_cooldown_minutes == 10
    assert app.app_size == mod.APP_SIZE_PRESETS[0]
    app._show_disclaimer_dialog(readonly=False)
    snapshot('disclaimer',app.disclaimer_dialog)
    assert not errors, errors
    app.root.destroy()
    print(mod.UI_PROFILE, 'PASS: all sizes, scrolling, widget restore/hit regions, timer pause, audio settings, manual mode, synthetic rune appearance/disappearance, saved preferences')
