# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 rednakta
"""미니맵 영역 지정 안내용 도식 이미지를 생성한다.

실제 게임 화면 캡처 대신 사용하는 자체 제작 도식이며, 결과물은
docs/screenshots/minimap-region-diagram.png 에 저장된다.

저장소 루트에서 실행: python tools/build_minimap_diagram.py
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent

W, H = 900, 760
BG = (10, 12, 11)
CARD = (20, 22, 21)
PANEL = (28, 31, 34)
MAP_BG = (12, 14, 18)
INK = (236, 238, 240)
MUTED = (150, 156, 162)
RED = (226, 42, 42)

FB = str(ROOT / "assets" / "fonts" / "package" / "src" / "NEXON_Lv2_Gothic_Bold.ttf")
FR = str(ROOT / "assets" / "fonts" / "package" / "src" / "NEXON_Lv2_Gothic.ttf")
f_title = ImageFont.truetype(FB, 30)
f_sub = ImageFont.truetype(FR, 19)
f_tag = ImageFont.truetype(FB, 16)
f_small = ImageFont.truetype(FR, 15)
f_tiny = ImageFont.truetype(FR, 13)

im = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(im)

# 상단 텍스트
d.text((60, 42), "미니맵 영역 지정 예시", font=f_title, fill=INK)
d.text((60, 88), "캡쳐 아이콘 클릭 후, 미니맵만 드래그해서 지정", font=f_sub, fill=MUTED)

# 바깥 카드
d.rounded_rectangle((60, 150, 840, 700), radius=26, fill=CARD)

# 게임 화면 모형 패널
px0, py0, px1, py1 = 215, 205, 690, 632
d.rectangle((px0, py0, px1, py1), fill=PANEL)
d.text((px0 + 14, py0 - 26), "게임 화면 (모형)", font=f_tiny, fill=(110, 116, 122))

# 상단 바: 지역명 + 아이콘 버튼
d.rectangle((px0, py0, px1, py0 + 96), fill=(36, 40, 44))
d.rounded_rectangle((px0 + 14, py0 + 14, px0 + 74, py0 + 74), radius=6,
                    fill=(52, 58, 64), outline=(88, 96, 104), width=2)
d.text((px0 + 88, py0 + 22), "지역명", font=f_tag, fill=INK)
d.text((px0 + 88, py0 + 48), "맵 이름", font=f_small, fill=MUTED)
for i in range(4):
    bx = px1 - 42 - i * 46
    d.rounded_rectangle((bx, py0 + 20, bx + 34, py0 + 54), radius=8,
                        fill=(58, 64, 70), outline=(96, 104, 112), width=1)
    d.ellipse((bx + 12, py0 + 32, bx + 22, py0 + 42), fill=(150, 158, 166))

# 미니맵 영역
mx0, my0, mx1, my1 = px0 + 22, py0 + 172, px1 - 22, py0 + 342
d.rectangle((mx0, my0, mx1, my1), fill=MAP_BG, outline=(70, 76, 84), width=1)
# 지형 선
for y in (my1 - 24, my1 - 62, my1 - 100):
    d.line((mx0 + 24, y, mx1 - 24, y), fill=(46, 52, 62), width=3)
d.line((mx0 + 90, my0 + 34, mx1 - 90, my0 + 34), fill=(46, 52, 62), width=3)
# 마커
d.ellipse((mx0 + 60, my1 - 78, mx0 + 76, my1 - 62), fill=(232, 74, 128))          # 캐릭터
d.ellipse((mx1 - 210, my0 + 24, mx1 - 194, my0 + 40), fill=(240, 206, 72))        # NPC
for cx in (mx0 + 18, mx1 - 34):
    d.ellipse((cx, my1 - 118, cx + 18, my1 - 100), outline=(86, 214, 120), width=3)  # 포탈
# 룬 마커(마름모)
rcx, rcy = (mx0 + mx1) // 2, my1 - 46
d.polygon([(rcx, rcy - 13), (rcx + 13, rcy), (rcx, rcy + 13), (rcx - 13, rcy)],
          fill=(196, 120, 244))

# 빨간 지정 박스
d.rounded_rectangle((mx0 - 12, my0 - 12, mx1 + 12, my1 + 12), radius=4,
                    outline=RED, width=5)

# 라벨 말풍선 (상단 바와 미니맵 사이)
label = "빨간 박스 = 지정할 영역"
tw = d.textlength(label, font=f_tag)
lx0, ly0 = mx0 - 12, py0 + 110
d.rounded_rectangle((lx0, ly0, lx0 + tw + 34, ly0 + 38), radius=19,
                    fill=(18, 20, 22), outline=RED, width=3)
d.text((lx0 + 17, ly0 + 9), label, font=f_tag, fill=INK)
d.line((lx0 + 22, ly0 + 38, lx0 + 22, my0 - 12), fill=RED, width=3)

# 하단 상태 바
bx0, by0, bx1, by1 = px0 + 22, my1 + 40, px0 + 300, my1 + 76
d.rounded_rectangle((bx0, by0, bx1, by1), radius=18, fill=(30, 34, 40))
d.rounded_rectangle((bx0 + 8, by0 + 8, bx1 - 60, by1 - 8), radius=10, fill=(74, 138, 226))
d.text((bx1 + 16, by0 + 8), "체력 / 경험치 바", font=f_small, fill=MUTED)

# 하단 주석
d.text((60, 716), "실제 게임 화면이 아니라 영역 지정 방법을 설명하기 위해 그린 도식입니다.",
       font=f_tiny, fill=(104, 110, 116))

out = ROOT / "docs" / "screenshots" / "minimap-region-diagram.png"
im.save(out)
print("saved", out, im.size)
