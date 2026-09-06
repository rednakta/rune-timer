# SPDX-License-Identifier: GPL-3.0-or-later
"""Generate the two distribution asset sets from the original UI artwork."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSETS = {
    'settings_icon.png': (48, 128),
    'nilbox_splash_icon.png': (96, 192),
    'nilbox_splash_icon_blur.png': (96, 192),
    'rune_timer_diamond_icon.png': (64, 256),
}

def main():
    for index, profile in enumerate(('low', 'high')):
        target = ROOT / 'assets' / 'ui' / profile
        target.mkdir(parents=True, exist_ok=True)
        for name, sizes in ASSETS.items():
            with Image.open(ROOT / name) as source:
                image = source.convert('RGBA')
                image.thumbnail((sizes[index], sizes[index]), Image.Resampling.LANCZOS)
                image.save(target / name)
        with Image.open(ROOT / 'maple_timer_custom_icon.ico') as source:
            image = source.convert('RGBA')
            sizes = (16, 24, 32, 48, 64) if profile == 'low' else (16, 24, 32, 48, 64, 128, 256)
            image.save(target / 'maple_timer_custom_icon.ico', sizes=[(n, n) for n in sizes])

if __name__ == '__main__':
    main()
