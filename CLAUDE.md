# 포트폴리오 빌드 프로젝트 — Claude Code 컨텍스트

## 목적
김의현 포트폴리오 HTML/PDF 빌드 환경 구성 및 유지

## 디렉토리 구조
```
D:/OneDrive/14_Career/03_Portfolio/my_portfolio/
├── CLAUDE.md              ← 이 파일 (Claude Code 컨텍스트)
├── build_v261.py          ← 메인 빌드 스크립트 (HTML 생성)
├── convert_pdf.py         ← HTML → PDF 변환
├── gallery_b64.json       ← 아티코 갤러리 이미지 base64
├── portfolio_김의현_v2.6.pdf  ← 참고용 PDF (덮어쓰지 말 것)
└── assets/
    ├── 김의현_사진_정장_사진.png
    ├── 01_랜딩페이지.png
    ├── 02_대시보드.png
    ├── 03_스튜디오.png
    ├── 04_갤러리.png
    ├── 목동아티코야경외관.jpg
    ├── 썸네일__주치의.png
    ├── 썸네일_MDH_AI_시뮬레이터.png
    ├── 썸네일_여황제.png
    └── 썸네일__AI_취향분석.png
```

## 빌드 명령
```bash
# 1. HTML 생성
python build_v261.py

# 2. PDF 변환 (wkhtmltopdf 필요)
python convert_pdf.py
```

## 버전 규칙
- 빌드 파일: build_v{버전}.py
- 출력 파일: portfolio_김의현_v{버전}.html / .pdf
- 현재 버전: 2.6.1

## 이미지 경로 탐색 순서 (build 스크립트 내부)
1. `./assets/`
2. `./` (루트)
3. (fallback) 없으면 경고 출력 후 스킵

## 주의사항
- `gallery_b64.json` — 아티코 갤러리 9장 base64 묶음, 수정 금지
- `portfolio_김의현_v2.6.pdf` — 참고용 원본, 덮어쓰기 금지
- 고객사 실명 (MetaCraft·TopcoMedia·HartAI) 코드/문서 내 노출 금지
- 매출·자금 숫자 직접 표기 금지
