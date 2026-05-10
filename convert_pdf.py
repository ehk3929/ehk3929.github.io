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
    page.goto(Path(HTML).as_uri(), wait_until='networkidle')
    page.emulate_media(media='screen')

    # lazy-load + reveal 즉시 표시
    page.evaluate("""() => {
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
    total_pages = (total_h + PAGE_HEIGHT_PX - 1) // PAGE_HEIGHT_PX

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

    print(f"document height: {total_h}px → {total_pages}쪽")
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
                display_header_footer=False,
                margin={'top':'0','bottom':'0','left':'0','right':'0'},
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
