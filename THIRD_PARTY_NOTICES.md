# Third Party Notices

이 저장소에는 앱 실행과 빌드를 위해 외부 라이브러리와 폰트 파일이 포함되거나 사용됩니다.

모든 구성요소의 라이선스 **전문**은 저장소 루트의 `THIRD_PARTY_LICENSES.txt`에 있으며,
실행 파일 배포본에도 같은 파일이 동봉됩니다.

## Python Libraries

실행 파일에 포함되어 재배포되는 라이브러리:

| 구성요소 | 라이선스 | 출처 |
|---|---|---|
| Pillow | MIT-CMU | https://github.com/python-pillow/Pillow |
| NumPy | BSD-3-Clause | https://github.com/numpy/numpy |
| DXcam | MIT | https://github.com/ra1nty/DXcam |
| PyInstaller | GPL-2.0-or-later + Bootloader Exception | https://github.com/pyinstaller/pyinstaller |

PyInstaller가 생성한 exe에는 부트로더가 포함됩니다. PyInstaller의 Bootloader
Exception 조항에 따라 부트로더 포함 자체는 결합 저작물의 라이선스에 제약을
주지 않습니다.

문서 생성 전용 도구(실행 파일에 포함되지 않음): reportlab (BSD-3-Clause),
python-docx (MIT). `tools/` 스크립트에서만 사용합니다.

## Fonts

### NEXON Lv2 Gothic

앱 설정 화면 UI, 그리고 사용자 가이드 PDF 생성에 사용합니다.

- 파일: `assets/fonts/package/src/NEXON_Lv2_Gothic{,_Light,_Medium,_Bold}.ttf` (4종)
- 저작권자: NEXON Korea Corporation
- 사용 조건: [넥슨 폰트 사용정책](https://levelup.nexon.com/index.html#policy) (SPDX 표준 라이선스 아님)
- 배포처: [NEXON LEVEL UP](https://levelup.nexon.com/index.html)
- 포함 경로: npm 패키지 `@kfonts/nexon-lv2-gothic` v0.2.0에서 수정 없이 가져옴

이 폰트는 exe에 번들되어 재배포되고 생성 PDF에 서브셋 임베드됩니다. 포함 경위와
배포 전 확인 항목은 `assets/fonts/package/NOTICE.md`에 정리되어 있습니다.

### Poppins Thin

홈 화면 타이머 숫자 표시용으로 Poppins Thin 폰트를 사용합니다.

- 파일: `assets/fonts/timer/Poppins-Thin.ttf`
- 라이선스: SIL Open Font License, Version 1.1 (OFL-1.1)
- 라이선스 전문: `assets/fonts/timer/OFL.txt` (실행 파일 배포본에도 동일 경로로 포함)
- 원본: https://github.com/itfoundry/Poppins

```
Copyright 2020 The Poppins Project Authors (https://github.com/itfoundry/Poppins)

This Font Software is licensed under the SIL Open Font License, Version 1.1.
This license is copied below, and is also available with a FAQ at:
http://scripts.sil.org/OFL
```

폰트 파일은 수정 없이 원본 그대로 포함하며, 재배포 시 위 저작권 표시와 OFL 전문을 함께 제공합니다.

## Sounds

### TTS 알림 음원

- 파일: `assets/sounds/tts_rune.mp3`, `tts_rune_due.mp3`, `tts_warning.mp3`
- 생성 도구: [TTSMaker](https://ttsmaker.com/) (온라인 TTS 서비스)
- 사용 조건: TTSMaker의 이용약관 및 음성별 저작권 안내를 따릅니다.
  <https://ttsmaker.com/copyright>

이 음원은 직접 녹음한 저작물이 아니라 온라인 TTS 서비스로 생성한 결과물이며,
exe에 번들되어 재배포됩니다. TTSMaker는 음성(voice)별로 사용 조건을 따로 표기하므로,
사용한 음성이 다운로드 배포 앱에 포함되어 재배포될 수 있는지 배포 전에 확인해야
합니다. 확인 항목과 이력은 `assets/sounds/NOTICE.md`를 참고하세요.

## App Assets

앱 아이콘과 UI 이미지는 공개 배포를 고려해 별도로 제작한 앱 전용 자산입니다. 공식 메이플스토리 아이콘, 몬스터 이미지, 클라이언트 리소스를 직접 포함하지 않는 것을 원칙으로 합니다.

문서용 이미지도 같은 원칙을 따릅니다.

- `docs/screenshots/rune-timer-*.png` — 이 앱 자체의 화면 캡처
- `docs/screenshots/minimap-region-diagram.png` — 미니맵 영역 지정 방법을 설명하기
  위해 직접 그린 도식입니다. 게임 화면 캡처가 아니며, `tools/build_minimap_diagram.py`로
  재생성할 수 있습니다.

즉 이 저장소에는 게임 클라이언트 화면 캡처가 포함되어 있지 않습니다.
