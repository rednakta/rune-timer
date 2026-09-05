# NEXON Lv2 Gothic — 포함 경위 및 사용 조건 기록

## 파일 출처

- 서체명: 넥슨Lv2고딕 (NEXON Lv2 Gothic)
- 저작권자: NEXON Korea Corporation
- 공식 배포처: [NEXON LEVEL UP](https://levelup.nexon.com/index.html)
- 사용정책: [넥슨 폰트 사용정책](https://levelup.nexon.com/index.html#policy)
- 이 저장소에 넣은 경로: npm 패키지 [`@kfonts/nexon-lv2-gothic`](https://www.npmjs.com/package/@kfonts/nexon-lv2-gothic) v0.2.0
  (패키지의 원본 `README.md`와 `metadata.json`을 이 디렉터리에 함께 보존)

포함 파일 (`src/`, 수정 없이 원본 그대로):

| 파일 | Weight |
|---|---|
| `NEXON_Lv2_Gothic_Light.ttf` | 300 |
| `NEXON_Lv2_Gothic.ttf` | 400 |
| `NEXON_Lv2_Gothic_Medium.ttf` | 500 |
| `NEXON_Lv2_Gothic_Bold.ttf` | 700 |

## 이 프로젝트에서의 사용 형태

1. 앱 UI 폰트 — `pip_timer_auto_detect_app.pyw`가 실행 시 TTF를 등록해 설정 화면 등에 사용
2. 실행 파일 번들 — `rune_timer.spec`의 datas로 TTF 4종이 exe에 포함되어 재배포됨
3. 문서 임베딩 — 사용자 가이드 PDF 생성 시 TTF를 로드했으며, 배포된 PDF에는 서브셋 폰트가 임베드되어 있음 (생성 도구는 현재 저장소에 없음)

즉 이 프로젝트는 **폰트 파일 자체를 재배포**하며, 폰트를 수정하거나 폰트 자체를
판매하지 않습니다.

## 라이선스 성격

이 폰트는 OFL/Apache 같은 SPDX 표준 오픈소스 라이선스가 아니라 넥슨이 정한
**자체 사용정책**을 따릅니다. 따라서 이 저장소의 GPL-3.0-or-later는 이 폰트
파일에 적용되지 않으며, 사용 조건의 최종 기준은 위 공식 정책 페이지입니다.

## 확인 이력

정책 내용은 변경될 수 있으므로, 배포 시점마다 아래 표를 갱신하세요.

| 확인일 | 확인자 | 확인한 정책 URL | 결과 |
|---|---|---|---|
| (미확인) | | https://levelup.nexon.com/index.html#policy | 배포 전 확인 필요 |

확인해야 할 항목:

- 폰트 파일을 애플리케이션에 번들해 재배포하는 것이 허용되는지
- 생성 문서(PDF)에 서브셋 임베드하는 것이 허용되는지
- 요구되는 저작권 표시 문구와 표기 위치
- 상업적 이용 및 유료 배포 시 추가 조건
