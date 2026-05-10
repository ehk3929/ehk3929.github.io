"""
HTML → PDF 변환 (Playwright + 페이지별 active nav 하이라이트)

[필요 환경]
  pip install playwright pypdf
  playwright install chromium

[사용법]
  $ python convert_pdf.py

[동작]
  - 1280×900 viewport, screen 모드 캡처
  - 1280×1810 px 단위로 페이지 분할
  - 페이지마다 해당 섹션의 nav 링크에 .active 클래스를 부여한 뒤
    그 페이지만 단일-페이지 PDF로 추출 → 모두 병합
  - active 결정 알고리즘: "페이지 내 픽셀 점유가 가장 큰 섹션"
"""
import os, sys, tempfile
from pathlib import Path

BASE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(BASE, 'html', 'portfolio_김의현_v2.6.4.html')
PDF_OUT = os.path.join(BASE, 'pdf', 'portfolio_김의현_v2.6.4.pdf')
os.makedirs(os.path.dirname(PDF_OUT), exist_ok=True)
PAGE_HEIGHT_PX = 1810
VIEWPORT_W = 1280

if not os.path.exists(HTML):
    sys.exit(f"❌ HTML 없음: {HTML}")

try:
    from playwright.sync_api import sync_playwright
    from pypdf import PdfReader, PdfWriter
except ImportError:
    sys.exit("❌ 의존성 미설치: pip install playwright pypdf && playwright install chromium")

# nav 항목과 매칭되는 섹션 ID (HTML과 일치)
SECTIONS = [
    {'nav_idx': 0, 'sec_id': 'about'},     # 01 About
    {'nav_idx': 1, 'sec_id': 'summary'},   # 02 Executive Summary
    {'nav_idx': 2, 'sec_id': 'track'},     # 03 Track Record
    {'nav_idx': 3, 'sec_id': 'work'},      # 04 Recent Work
    {'nav_idx': 4, 'sec_id': 'why'},       # 05 Why This Move
    {'nav_idx': 5, 'sec_id': 'commit'},    # 06 Commitment
    {'nav_idx': 6, 'sec_id': 'contact'},   # 07 Contact
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': VIEWPORT_W, 'height': 900})
    # ★ 페이지 스크립트 실행 전 미리 주입: KPI 카운트업 옵저버 skip
    page.add_init_script("""
        document.addEventListener('DOMContentLoaded', () => {
            document.querySelectorAll('.kpi-num').forEach(el => el.dataset.animated = 'true');
        });
    """)
    page.goto(Path(HTML).as_uri(), wait_until='networkidle')
    page.emulate_media(media='screen')

    # lazy-load + reveal 즉시 표시
    page.evaluate("""() => {
        // PDF 전용: KPI 카운트업 즉시 완료 처리 (라이브 웹에는 영향 없음)
        document.querySelectorAll('.kpi-num').forEach(el => el.dataset.animated = 'true');
        document.querySelectorAll('img[loading="lazy"]').forEach(i => i.loading='eager');
        document.querySelectorAll('.reveal').forEach(el => el.classList.add('revealed'));
    }""")

    # 스크롤로 IntersectionObserver / lazy-load 트리거
    page.evaluate("""async () => {
        const total = document.documentElement.scrollHeight;
        for (let y=0; y<total; y+=window.innerHeight) {
            window.scrollTo(0, y);
            await new Promise(r => setTimeout(r, 100));
        }
        window.scrollTo(0, 0);
    }""")

    # 이미지 로드 완료 대기 (5초/장 타임아웃)
    page.evaluate("""() => Promise.all(
        Array.from(document.images).filter(i => !i.complete).map(i =>
            Promise.race([
                new Promise(r => { i.onload = i.onerror = r; }),
                new Promise(r => setTimeout(r, 5000))
            ])
        )
    )""")
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(1500)

    # PDF 전용: 간격 압축 + closing break 규칙 완화 (HTML 파일 무수정)
    page.evaluate("""() => {
        const s = document.createElement('style');
        s.textContent = `
            /* Why 섹션을 위로 끌어올리기 — 상단 margin/padding 모두 축소 */
            section + #why { margin-top: 0 !important; }
            #why { margin-top: 0 !important; padding-top: 0 !important; margin-bottom: 24px !important; }
            #why .section-head { margin-bottom: 18px !important; padding-top: 0 !important; }
            #why .section-num { margin-bottom: 12px !important; }
            #why .section-title { margin-bottom: 8px !important; line-height: 1.1 !important; }
            #why .section-sub { margin-top: 8px !important; }
            .why-block { gap: 12px !important; margin: 16px 0 !important; }
            .why-card  { padding: 14px 18px !important; }
            /* 직전 work 섹션 하단 여백 축소 */
            #work { margin-bottom: 0 !important; padding-bottom: 0 !important; }
            #work .work-block:last-child { margin-bottom: 0 !important; }
            /* Commit — p7 여유 공간 활용해 아래로 내리고 항목 여유 있게 */
            #commit { margin-top: 32px !important; padding-top: 24px !important; margin-bottom: 24px !important; }
            #commit .section-head { margin-bottom: 24px !important; }
            #commit .p-row { padding: 20px 0 !important; }
            #commit .p-when { padding: 14px 16px !important; }
            #commit .p-what { padding: 14px 18px !important; }
            /* 우측 갤러리 블록(B2B 고객사 등) 페이지 잘림 방지 */
            .afr-list { page-break-inside: avoid !important; break-inside: avoid !important; }
            .gallery-label { page-break-after: avoid !important; break-after: avoid !important; }
            /* closing: 페이지 분할 강제 해제 (8쪽 유발 원인) */
            .closing { page-break-inside: auto !important; break-inside: auto !important; padding-top: 12px !important; margin-top: 16px !important; }
            .closing-quote { padding: 14px 20px !important; margin-bottom: 14px !important; }
            .closing-final { padding: 12px 0 !important; margin: 12px 0 !important; }
            .signature { margin-top: 16px !important; padding-top: 16px !important; }
        `;
        document.head.appendChild(s);
    }""")

    # 각 섹션의 Y 시작 위치 + 높이 측정
    measure_js = """(sections) => {
        const total_h = document.documentElement.scrollHeight;
        const positions = sections.map(s => {
            if (!s.sec_id) return { nav_idx: s.nav_idx, y: null, h: 0 };
            const el = document.getElementById(s.sec_id);
            if (!el) return { nav_idx: s.nav_idx, y: null, h: 0 };
            const r = el.getBoundingClientRect();
            return {
                nav_idx: s.nav_idx,
                y: Math.round(window.scrollY + r.top),
                h: Math.round(r.height)
            };
        });
        return { positions, total_h };
    }"""
    info = page.evaluate(measure_js, SECTIONS)
    positions = info['positions']
    total_h = info['total_h']
    # ★ 수학 계산 대신 Chromium 실제 페이지 수 사용
    # page-break-inside:avoid 등으로 Chromium이 추가 페이지를 만들 수 있음
    with tempfile.TemporaryDirectory() as _probe_dir:
        _probe_pdf = os.path.join(_probe_dir, 'probe.pdf')
        page.pdf(
            path=_probe_pdf,
            width=f'{VIEWPORT_W}px',
            height=f'{PAGE_HEIGHT_PX}px',
            print_background=True,
            prefer_css_page_size=False,
            display_header_footer=False,
            margin={'top':'0','bottom':'0','left':'0','right':'0'},
        )
        total_pages = len(PdfReader(_probe_pdf).pages)

    # 페이지별 active nav 결정 — "페이지 내 픽셀 점유 최대 섹션"
    nav_labels = ['01 About', '02 Exec Summary', '03 Track Record',
                  '04 Recent Work', '05 Why', '06 Commitment', '07 Contact']
    page_to_nav = []
    for pg in range(total_pages):
        page_start = pg * PAGE_HEIGHT_PX
        page_end   = page_start + PAGE_HEIGHT_PX

        best_nav    = 0
        best_overlap = -1
        fallback_nav = 0  # 이 페이지 이전에 시작한 마지막 섹션

        for sp in positions:
            if sp['y'] is None:
                continue
            sec_y   = sp['y']
            sec_end = sec_y + max(sp.get('h', 0), 1)
            overlap = max(0, min(sec_end, page_end) - max(sec_y, page_start))
            if sec_y <= page_start:
                fallback_nav = sp['nav_idx']
            if overlap > best_overlap:
                best_overlap = overlap
                best_nav = sp['nav_idx']

        # 겹치는 섹션이 없으면 fallback
        if best_overlap <= 0:
            best_nav = fallback_nav

        page_to_nav.append(best_nav)

    print(f"document height: {total_h}px → Chromium 실제 {total_pages}쪽")
    for i, idx in enumerate(page_to_nav, 1):
        print(f"  p{i}: nav[{idx}] = {nav_labels[idx]}")

    # 페이지별로 active 설정 → 해당 1쪽만 PDF로 추출 → 병합
    set_active_js = """(idx) => {
        document.querySelectorAll('.sb-nav a').forEach((a, i) => {
            if (i === idx) a.classList.add('active');
            else a.classList.remove('active');
        });
    }"""

    pdf_files = []
    with tempfile.TemporaryDirectory() as tmpdir:
        for pg, nav_idx in enumerate(page_to_nav):
            page.evaluate(set_active_js, nav_idx)
            tmp_pdf = os.path.join(tmpdir, f'page_{pg+1}.pdf')
            page.pdf(
                path=tmp_pdf,
                width=f'{VIEWPORT_W}px',
                height=f'{PAGE_HEIGHT_PX}px',
                print_background=True,
                prefer_css_page_size=False,
                display_header_footer=True,
                header_template='<span></span>',
                footer_template='<div style="font-size:9px;color:#aaa;width:100%;text-align:right;padding:0 24px 6px;font-family:sans-serif;letter-spacing:0.04em;"><a href="https://ehk3929.github.io" style="color:#aaa;text-decoration:none;">https://ehk3929.github.io</a></div>',
                margin={'top':'0','bottom':'24px','left':'0','right':'0'},
                page_ranges=str(pg + 1),
            )
            pdf_files.append(tmp_pdf)

        writer = PdfWriter()
        for f in pdf_files:
            for src_page in PdfReader(f).pages:
                writer.add_page(src_page)
        with open(PDF_OUT, 'wb') as out:
            writer.write(out)

    browser.close()

sz = os.path.getsize(PDF_OUT) // 1024
print(f"\n✅ PDF: {PDF_OUT}  ({sz} KB / {sz/1024:.2f} MB)")
