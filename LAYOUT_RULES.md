# LAYOUT_RULES.md
# PDF 페이지 채움 레이아웃 규칙
# Claude Code는 build 스크립트 수정 시 이 규칙을 반드시 준수한다.

---

## 기본 원칙
- A4 기준 각 섹션은 **한 페이지를 꽉 채우거나 정확히 끊어지도록** 설계
- 섹션 간 여백은 `margin-bottom` 으로만 조정 (padding 혼용 금지)
- 이미지·영상 카드는 반드시 **2열 그리드** (`grid-template-columns: 1fr 1fr`)
- KPI 숫자 블록은 **3열 또는 4열** 균등 분할

---

## 페이지별 목표 구성 (v2.6 PDF 기준)

### Page 1 — Hero + Meta + KPI
| 요소 | 높이 목표 | 규칙 |
|------|-----------|------|
| hero-tag (상단 라벨) | 40px | 고정 |
| hero-grid (제목 + 사진) | 260~300px | 제목 font-size 58~64px |
| hero-meta (경력 3항목) | 60px | flex 가로 나열, 구분선 포함 |
| kpi-section (숫자 6개) | 220~260px | 3열×2행, 숫자 48~56px |
| 합계 | ≈ A4 1장 | 여백 포함 800~900px |

### Page 2 — Track Record (타임라인)
| 요소 | 규칙 |
|------|------|
| 섹션 헤더 | font-size 36~40px, margin-bottom 32px |
| 리드 문단 | 2~3줄 이내, font-size 15px |
| 타임라인 항목 5개 | 각 항목 padding 24px, border-left 2px |
| 페이지 목표 | 항목 5개가 1페이지 안에 들어오도록 각 항목 padding 조정 |

### Page 3 — FrameForge (Recent Work 1)
| 요소 | 규칙 |
|------|------|
| 제품명 + 기간 | 1행, font-size 22px bold |
| 부제 | 1행, font-size 14px gray |
| 설명 문단 | 3~4줄 이내 |
| Platform Preview 이미지 | 2열×2행 그리드, 각 이미지 높이 180~200px |
| KPI 4개 | 4열 균등, 숫자 40px |
| 영상 카드 2개 | 2열, 썸네일 높이 160px |
| 하단 요약 박스 | 배경 #f5f4f0, padding 20px, 1~2줄 |

### Page 4 — MDH (Recent Work 2) + 아티코 시작
| 요소 | 규칙 |
|------|------|
| MDH 설명 문단 | 3줄 이내 |
| MDH KPI 4개 | 4열 |
| MDH 영상 카드 2개 | 2열 |
| 팀 요약 박스 | 배경 강조, 2줄 이내 |
| 아티코 헤더 | 섹션 구분선 후 시작 |

### Page 5 — 아티코 계속 (영상 + B2B 고객사 + 갤러리)
| 요소 | 규칙 |
|------|------|
| 영상 카드 1개 + 지명원 이미지 | 2열 |
| B2B 고객사 목록 | 1열 전체 폭, font-size 13px, line-height 1.8 |
| Selected Works 갤러리 | 4열×2행, 각 이미지 높이 110~130px |
| 조직도 이미지 | 갤러리 마지막 셀 |

### Page 6 — Why + Commitment (마지막)
| 요소 | 규칙 |
|------|------|
| Why 섹션 | 3열 카드 (24년 운영 / AI 7년 / 원점 복귀) |
| Commitment 표 | 4행 (30일/90일/1년/5~6년), 각 행 padding 16px |
| 마무리 일화 | 인용 박스, border-left gold |
| 서명 | 우측 정렬, font-size 14px |

---

## 공통 여백 규칙

```css
/* 섹션 간격 */
section + section          { margin-top: 72px; }

/* PDF @media print 전용 (v2.6.4+) */
/* 핵심 원칙: page-break-inside:avoid 를 section 단위에 걸지 말 것.
   Playwright/Chromium이 너무 엄격히 적용해 빈 페이지를 만든다.
   대신 섹션 시작점에 page-break-before:always 로 명시적 끊기. */
@media print {
  /* 섹션 자체는 자유롭게 흐르게 둔다 */
  .section                 { margin-bottom: 24pt; page-break-inside: auto; }
  .exec-summary            { page-break-inside: auto; }   /* 잘려도 됨 */

  /* 명시적 페이지 시작점만 지정 */
  #track                   { page-break-before: always; } /* Track Record */
  #work                    { page-break-before: always; } /* Recent Work */
  #why                     { page-break-before: always; } /* Why */
  #commit                  { page-break-before: avoid;  } /* Why와 같은 페이지 */

  /* 표/카드/행 단위만 보호 (작은 단위만 avoid) */
  .promise                 { page-break-inside: avoid; }  /* 입사 후 약속 표 */
  .p-row                   { page-break-inside: avoid; }  /* 표 행 보호 */
  .vc                      { page-break-inside: avoid; }  /* 영상 카드 */
  .kpi-section             { page-break-inside: avoid; }
  .closing                 { page-break-inside: avoid; }

  body                     { font-size: 14px; }
  .main                    { padding: 0; margin: 0; }
}
```

### Page-break 전략 요약
| 단위 | 규칙 | 이유 |
|------|------|------|
| `.section`, `<section>` | `page-break-inside: auto` | 큰 단위에 avoid를 걸면 Playwright가 빈 페이지를 삽입 |
| `#track`, `#work`, `#why` | `page-break-before: always` | 명시적 페이지 시작점 — 섹션 = 페이지 1:1 매핑 |
| `#commit` | break 없음 | Why 섹션과 같은 페이지에 둔다 |
| `.promise`, `.p-row`, `.vc`, `.kpi-section` | `page-break-inside: avoid` | 표/카드/행 단위 — 작은 단위만 보호 |
| `.exec-summary` 본문 문단 | `auto` | 길어지면 잘려도 됨 |

---

## 페이지 압축 조정 가이드

> **언제 사용**: PDF 페이지 수가 목표보다 많을 때, 또는 특정 섹션이 다음 페이지로 넘어갈 때.
> **원리**: 어떤 페이지를 줄이고 싶은지 → 그 페이지에 속한 셀렉터의 padding/margin/line-height를 우선적으로 줄인다. 폰트 크기는 마지막 수단.

### 페이지별 영향 셀렉터 매핑

| 줄이고 싶은 페이지 | 우선 조정 셀렉터 (큰 효과 → 작은 효과 순) |
|------|------|
| **p1 + p2** (Hero+KPI+Exec Summary) | `.exec-summary` padding → `.kpi-grid` margin → `.exec-summary p` line-height/margin → `.hero` padding → `.hero-meta` margin-top → `.kpi-section` padding |
| **p3 + p4** (Track Record) | `.t-row` padding → `.chapter-block` margin-bottom → `.section-head` margin-bottom → `.t-row` font-size |
| **p5 ~ p8** (Recent Work — FrameForge/MDH/Atico) | `.vc-thumb` height → `.work-block + .work-block` margin-top → `.metrics` margin → `.work-prose p` margin → `.gallery > * img` max-height |
| **p9 + p10** (Why + Commitment) | `.why-card` padding → `#why, #commit` padding → `.p-row > *` padding → `.why-card p` line-height → `.promise` margin → `.closing-quote` padding → `.closing` padding-top |

### 안전 범위 (현재값 → 최소 안전값)

가독성을 보존하면서 줄일 수 있는 하한선. 이 이하로 내리면 답답하거나 텍스트가 겹친다.

| 셀렉터 / 속성 | 현재값 | 최소 안전값 | 비고 |
|------|------|------|------|
| `.hero` padding | `2mm 0 3mm` | `1mm 0 2mm` | hero-title이 30pt라 더 줄이면 위 여백 부족 |
| `.kpi-section` padding | `1mm 0` | `0` | 더 줄이면 KPI 박스가 위 hero에 붙음 |
| `.kpi-grid` margin | `2mm 0` | `1mm 0` | border-top/bottom과 본문 간 숨통 |
| `.exec-summary` padding | `4mm 0` | `2mm 0` | margin-top:5mm와 합쳐 페이지 내 분리감 |
| `.exec-summary p` line-height | `1.6` | `1.5` | 본문 가독성 마지노선 |
| `.exec-summary p` margin | `2mm 0` | `1mm 0` | 문단 간 호흡 |
| `.hero-meta` margin-top | `2mm` | `1mm` | hero-meta는 작은 메타정보라 여유 적어도 됨 |
| `.vc-thumb` height | `25mm` | `20mm` | YouTube 썸네일 가독성 마지노선 |
| `.work-block + .work-block` margin-top | `4mm` | `2mm` | work block 간 구분선 역할 |
| `.work-prose p` margin | `1mm 0` | `0` | line-height 1.65로 이미 어느 정도 분리됨 |
| `.metrics` margin | `2mm 0` | `1mm 0` | 4-column metric 박스 위아래 |
| `.why-card` padding | `2mm` | `1.5mm` | 더 줄이면 카드 안 텍스트가 border에 붙음 |
| `.why-card p` line-height | `1.4` | `1.35` | 8pt 본문 가독성 |
| `#why, #commit` padding | `2mm 0` | `0` | 섹션 자체 padding |
| `.promise` margin | `1mm 0` | `0` | 표 위아래 |
| `.p-row > *` padding | `1.5mm 3mm` | `1mm 2mm` | 표 셀 안 여백 — 더 줄이면 답답 |
| `.closing` padding-top | `2mm` | `1mm` | 마무리 인용구 위 여백 |
| `.closing-quote` padding | `2mm 4mm` | `1mm 3mm` | 인용구 box 안 여백 |

### 전형적 시나리오

- **"p1+p2가 한 페이지에 안 들어옴"**
  → `.exec-summary` padding과 `.kpi-grid` margin을 먼저 줄인다. 그래도 안 되면 `.exec-summary p` line-height 1.6 → 1.5.
- **"MDH 영상카드와 리딩한 팀이 한 페이지에 안 모임"**
  → `.vc-thumb` height(25→20mm)과 `.work-block + .work-block` margin-top(4→2mm)을 줄인다.
- **"Why와 Commitment가 한 페이지에 안 들어옴"**
  → `.why-card` padding(2→1.5mm) + `.p-row > *` padding(1.5mm 3mm → 1mm 2mm)을 함께 줄인다.
- **모든 안전값에 도달했는데도 페이지가 줄지 않으면**
  → 콘텐츠 자체를 잘라내야 한다 (예: Selected Works 갤러리 항목 수, work-prose 문단 수). CSS만으로는 한계.

### 조정 순서 (실패하지 않는 방법)

1. **한 번에 한 카테고리만 수정** → 빌드 → 페이지 수 확인. 여러 곳 동시 수정하면 어떤 변경이 효과 있었는지 파악 불가.
2. **먼저 padding/margin** → 그 다음 line-height → 마지막 font-size.
3. **테이블/카드 구조(`.p-row`, `.why-card`, `.vc`)는 안전값 근처까지 줄여도 OK** — 작은 단위라 시각적 여백 손실이 적다.
4. **본문 텍스트(`.exec-summary p`, `.work-prose p`)의 line-height는 1.5 미만 금지** — 한국어 한자는 1.5 이하면 답답해진다.

---

## 편집 시 체크리스트 (Claude Code)
- [ ] KPI 숫자가 3열 또는 4열로 균등 분배되는가
- [ ] 이미지 그리드가 2열인가 (1열 금지)
- [ ] 타임라인 항목이 1페이지 안에 들어오는가
- [ ] `@media print` 블록에 `page-break` 규칙이 있는가
- [ ] 섹션 헤더 font-size가 36px 이상인가
- [ ] hero-title font-size가 58px 이상인가

---

## 절대 금지
- 이미지를 1열 전체 폭으로 배치 (갤러리 섹션 제외)
- 섹션 중간에 임의 `<br>` 삽입으로 여백 조정
- `font-size: 12px` 이하 본문 텍스트
- 타임라인 항목 6개 이상을 한 페이지에 배치
