"""
v2.6.1 빌드 — 7장 서사 + 모던 미니멀 디자인 + 좌측 sticky 메뉴
- 다크 인디고 액센트
- Pretendard 풀 시스템
- AI 티 제거 (메타포·italic·장식 X)
- 1973년생·한자 이름 제거
- "꿈" → "목표"
- "오른팔" → "사장의 입장을 아는 사업개발자"
"""
import json, os, base64

# 스크립트 자기 위치 기준 (어디에 두고 실행해도 OK)
BASE = os.path.dirname(os.path.abspath(__file__))
# 프로젝트 지식 파일명 매핑 (동일 파일 그대로 사용)
ASSET_MAP = {
    'profile':         '김의현_사진_정장_사진.png',
    'ff_landing':      '01_랜딩페이지.png',
    'ff_dashboard':    '02_대시보드.png',
    'ff_studio':       '03_스튜디오.png',
    'ff_gallery':      '04_갤러리.png',
    'thumb_atico':     '목동아티코야경외관.jpg',
    'thumb_mdh_full':  '썸네일__AI_취향분석.jpg',
    'thumb_mdh_walk':  '썸네일_MDH_AI_시뮬레이터.png',
    'thumb_ff_juchi':  '썸네일__주치의.png',
    'thumb_ff_yeo':    '썸네일_여황제.png',
}

def find_file(fname):
    """파일을 BASE/assets/, BASE/, /mnt/project/ 순으로 탐색"""
    for d in [os.path.join(BASE, 'assets'), BASE, '/mnt/project']:
        p = os.path.join(d, fname)
        if os.path.exists(p):
            return p
    return None

# 1) 이미지 파일 10개 base64 인코딩
IMG = {}
for key, fname in ASSET_MAP.items():
    path = find_file(fname)
    if path:
        with open(path, 'rb') as f:
            IMG[key] = base64.b64encode(f.read()).decode()
    else:
        print(f"⚠️ 누락: {fname}")

# 2) gallery_b64.json에서 Atico 갤러리 로드 (9개)
gallery_path = find_file('gallery_b64.json')
if gallery_path:
    with open(gallery_path, encoding='utf-8') as f:
        IMG.update(json.load(f))
else:
    print(f"⚠️ gallery_b64.json 없음 (Atico 갤러리 미표시)")

def img_data(key):
    fname = ASSET_MAP.get(key, '')
    mime = 'image/png' if fname.lower().endswith('.png') else 'image/jpeg'
    return f"data:{mime};base64,{IMG[key]}"

VIDS = {
    'atico':    {'id': 'i7kFVOFjOLM', 'title': '목동 플래그십 홈스타일링', 'sub': '17년 자영업의 결과물', 'dur': '1:28'},
    'mdh_full': {'id': 'Ag8PvaRd_uE', 'title': 'AI 취향분석 → 3D 인테리어 자동 생성', 'sub': '풀 사이클 시연', 'dur': '1:42'},
    'mdh_walk': {'id': 'a86ChoE-9VE', 'title': '생성 공간 워크스루 인터랙션', 'sub': '실감형 3D 시뮬레이션', 'dur': '1:55'},
    'ff_juchi': {'id': 'Zask1rh_hMU', 'title': '주치의는 악녀를 고치고 도망쳤다', 'sub': '웹툰 IP 본계약 납품작 · 음성 더빙 완성본', 'dur': '3:04'},
    'ff_yeo':   {'id': 'If1zbZFPlPI', 'title': '여황제 EP.1 완성본', 'sub': '웹툰 IP 본계약 납품작 · 풀 에피소드', 'dur': '3:04'},
}

def vc(key):
    v = VIDS[key]
    thumb_key = f'thumb_{key}'
    thumb_src = f"data:image/jpeg;base64,{IMG[thumb_key]}" if thumb_key in IMG else f"https://i.ytimg.com/vi/{v['id']}/maxresdefault.jpg"
    return f'''<a href="https://youtu.be/{v['id']}" target="_blank" rel="noopener" class="vc">
  <div class="vc-thumb">
    <img src="{thumb_src}" alt="{v['title']}" class="yt-thumb" loading="lazy">
    <div class="vc-overlay">
      <svg class="vc-play" viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <circle cx="40" cy="40" r="38" fill="rgba(0,0,0,0.65)"/>
        <polygon points="33,24 33,56 58,40" fill="white"/>
      </svg>
      <span class="vc-dur">{v['dur']}</span>
    </div>
  </div>
  <div class="vc-meta">
    <strong>{v['title']}</strong>
    <em>{v['sub']}</em>
    <span class="vc-link">youtu.be/{v['id']} ↗</span>
  </div>
</a>'''


HTML = '''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>김의현 — 사업개발 포트폴리오</title>
<link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css" />
<style>
:root {
  --bg:       #ffffff;
  --bg-soft:  #f7f6f2;
  --bg-2:     #ebe8e0;
  --ink:      #0a0a0a;
  --ink-2:    #2a2a2a;
  --gray:     #6b6b6b;
  --gray-2:   #9a9a9a;
  --line:     #e5e2da;
  --line-2:   #f0ede5;
  --accent:   #1e293b;
  --accent-2: #334155;
  --hl:       #fef3c7;
}
* { margin:0; padding:0; box-sizing:border-box; }
html { scroll-behavior:smooth; scroll-padding-top:40px; }
body, p, h1, h2, h3, h4, h5, h6, div, span, li, td, th {
  word-break: keep-all;
  overflow-wrap: break-word;
  line-break: strict;
}
body {
  background:var(--bg); color:var(--ink);
  font-family:'Pretendard',sans-serif; font-size:16px; line-height:1.7;
  -webkit-font-smoothing:antialiased;
  font-feature-settings:"ss01","tnum";
}

/* === 좌측 STICKY 사이드바 === */
.sidebar {
  position:fixed; top:0; left:0; width:240px; height:100vh;
  padding:48px 32px; border-right:1px solid var(--line);
  background:var(--bg);
  display:flex; flex-direction:column; justify-content:space-between;
  z-index:10;
}
.sb-brand {
  font-weight:900; font-size:18px; letter-spacing:-0.02em;
  color:var(--ink); line-height:1.2; margin-bottom:4px;
}
.sb-brand small {
  display:block; font-weight:500; font-size:11px;
  color:var(--gray); letter-spacing:0.06em;
  text-transform:uppercase; margin-top:8px;
}
.sb-divider { height:1px; background:var(--line); margin:32px 0; }
.sb-nav { display:flex; flex-direction:column; gap:2px; }
.sb-nav a {
  display:block; padding:9px 0; text-decoration:none;
  font-size:13.5px; font-weight:500; color:var(--gray);
  letter-spacing:-0.005em; transition:all 0.15s ease;
  border-left:2px solid transparent; padding-left:14px; margin-left:-14px;
}
.sb-nav a:hover { color:var(--ink); border-left-color:var(--accent); }
.sb-nav a.active { color:var(--ink); font-weight:600; border-left-color:var(--accent); }
.sb-nav .sb-num {
  display:inline-block; width:24px; font-weight:600;
  color:var(--gray-2); font-size:11px;
}
.sb-foot {
  font-size:11.5px; color:var(--gray); line-height:1.7;
}
.sb-foot a { color:var(--ink); text-decoration:none; font-weight:500; }
.sb-foot a:hover { color:var(--accent); }
.sb-foot .ctc-row { display:flex; gap:8px; align-items:center; padding:3px 0; }
.sb-foot .ctc-icon {
  display:inline-flex; align-items:center; justify-content:center;
  width:22px; height:22px; color:var(--gray-2); flex-shrink:0;
}

/* === 메인 컨텐츠 === */
.main {
  margin-left:240px; max-width:920px;
  padding:80px 64px 120px;
}

/* === HERO === */
.hero { padding:0 0 64px; }
.hero-tag {
  font-size:12px; font-weight:700; letter-spacing:0.16em;
  color:var(--accent); text-transform:uppercase;
  margin-bottom:32px; display:flex; align-items:center; gap:14px;
}
.hero-tag::before {
  content:''; display:inline-block; width:32px; height:1px;
  background:var(--accent);
}
.hero-grid {
  display:grid; grid-template-columns:1fr 240px;
  gap:48px; align-items:end;
}
.hero-title {
  font-weight:900; font-size:68px; line-height:1.05;
  letter-spacing:-0.045em; color:var(--ink);
  margin-bottom:20px;
}
.hero-title .accent { color:var(--accent); }
.hero-sub {
  font-size:17px; font-weight:500; color:var(--gray);
  line-height:1.65; max-width:560px;
  border-left:2px solid var(--accent); padding-left:18px;
  margin-bottom:8px;
}
.hero-photo {
  width:240px; height:300px; object-fit:cover;
  filter:grayscale(0.05) contrast(1.05);
  border-radius:2px;
  box-shadow:0 12px 40px rgba(10,10,10,0.18);
}
.hero-meta {
  margin-top:48px; display:grid; grid-template-columns:repeat(3,1fr);
  border:1px solid var(--line); border-radius:8px; overflow:hidden;
}
.hero-meta span {
  display:flex; flex-direction:column; gap:5px;
  padding:24px 28px;
  border-right:1px solid var(--line);
  font-size:13px; color:var(--gray); font-weight:400; letter-spacing:0.03em;
}
.hero-meta span:last-child { border-right:none; }
.hero-meta span.hl {
  background:var(--accent); color:rgba(255,255,255,0.55);
  border-right:1px solid transparent;
}
.hero-meta span em {
  display:flex; align-items:baseline; gap:3px;
  font-style:normal;
}
.hero-meta span em b {
  font-size:42px; font-weight:700; line-height:1;
  letter-spacing:-0.03em; color:var(--ink);
}
.hero-meta span em s {
  font-size:16px; font-weight:400; text-decoration:none; color:var(--gray);
}
.hero-meta span.hl em b { color:#ffffff; }
.hero-meta span.hl em s { color:rgba(255,255,255,0.65); }
.hero-meta span small {
  font-size:11px; color:var(--gray-2); margin-top:2px;
}
.hero-meta span.hl small { color:rgba(255,255,255,0.4); }

/* === KPI 5초 박스 === */
.kpi-section { margin:0 0 96px; }
.kpi-label {
  font-size:11px; font-weight:700; letter-spacing:0.18em;
  color:var(--gray); text-transform:uppercase;
  margin-bottom:20px; display:flex; align-items:center; gap:14px;
}
.kpi-label::before {
  content:''; display:inline-block; width:24px; height:1px;
  background:var(--gray);
}
.kpi-grid {
  display:grid; grid-template-columns:repeat(3,1fr);
  border-top:2px solid var(--ink);
  border-bottom:2px solid var(--ink);
}
.kpi {
  padding:32px 24px 28px; border-right:1px solid var(--line);
  border-bottom:1px solid var(--line);
}
.kpi:nth-child(3n) { border-right:none; }
.kpi:nth-child(n+4) { border-bottom:none; }
.kpi-num {
  font-weight:900; font-size:56px; line-height:1;
  color:var(--ink); letter-spacing:-0.045em;
  margin-bottom:14px;
}
.kpi-num small {
  font-weight:700; font-size:22px; color:var(--gray); margin-left:3px;
}
.kpi-num .accent { color:var(--accent); }
.kpi-desc {
  font-size:13px; font-weight:500; color:var(--gray-2);
  letter-spacing:-0.005em; line-height:1.5;
}
.kpi-desc strong { color:var(--ink-2); font-weight:600; }

/* === Executive Summary === */
.exec-summary {
  background:var(--bg-soft); padding:40px 48px;
  margin:0 0 96px; border-left:3px solid var(--accent);
}
.exec-summary .es-label {
  font-size:11px; font-weight:700; letter-spacing:0.16em;
  color:var(--accent); text-transform:uppercase;
  margin-bottom:18px;
}
.exec-summary p {
  font-size:17px; line-height:1.85; color:var(--ink-2);
  font-weight:500; letter-spacing:-0.005em;
}
.exec-summary p strong { color:var(--ink); font-weight:700; }
.exec-summary p + p { margin-top:14px; }

/* === 섹션 === */
.section { margin:0 0 120px; }
.section-head { margin-bottom:48px; }
.section-num {
  font-size:12px; font-weight:700; letter-spacing:0.16em;
  color:var(--accent); text-transform:uppercase;
  margin-bottom:14px; display:flex; align-items:center; gap:14px;
}
.section-num::before {
  content:''; display:inline-block; width:24px; height:1px;
  background:var(--accent);
}
.section-title {
  font-weight:900; font-size:44px; line-height:1.1;
  letter-spacing:-0.035em; color:var(--ink);
  margin-bottom:14px;
}
.section-sub {
  font-size:17px; font-weight:500; color:var(--gray);
  line-height:1.55; max-width:680px;
}

/* === 7장 서사 본문 === */
.chapter-block {
  display:grid; grid-template-columns:120px 1fr;
  gap:32px; padding:32px 0;
  border-top:1px solid var(--line);
}
.chapter-block:last-of-type { border-bottom:1px solid var(--line); }
.chapter-block .ch-meta {
  font-weight:700; font-size:13px; color:var(--accent);
  letter-spacing:0.04em; line-height:1.4;
}
.chapter-block .ch-meta small {
  display:block; font-weight:500; font-size:11px;
  color:var(--gray); margin-top:4px; letter-spacing:0;
}
.chapter-block .ch-body {
  font-size:16px; line-height:1.85; color:var(--ink-2);
}
.chapter-block .ch-body p { margin-bottom:14px; }
.chapter-block .ch-body p:last-child { margin-bottom:0; }
.chapter-block .ch-body strong { color:var(--ink); font-weight:700; }
.chapter-block .ch-quote {
  font-weight:600; font-size:17px; color:var(--ink);
  padding:14px 0 14px 20px; border-left:3px solid var(--accent);
  margin:14px 0; line-height:1.55;
  background:var(--bg-soft);
  padding:18px 22px;
}

/* === 5시대 표 === */
.timeline {
  margin:48px 0 0;
  border-top:2px solid var(--ink);
  border-bottom:2px solid var(--ink);
}
.t-row {
  display:grid; grid-template-columns:160px 1fr 1.4fr;
  padding:24px 0; gap:24px;
  border-bottom:1px solid var(--line);
}
.t-row:last-child { border-bottom:none; }
.t-row .t-era {
  font-weight:800; font-size:20px; color:var(--accent);
  letter-spacing:-0.02em; line-height:1.1;
}
.t-row .t-era small {
  display:block; font-weight:500; font-size:11px;
  color:var(--gray); margin-top:6px; letter-spacing:0.02em;
}
.t-row .t-org {
  font-weight:700; font-size:15px; color:var(--ink); line-height:1.5;
}
.t-row .t-org small { font-weight:500; color:var(--gray); font-size:13px; }
.t-row .t-res {
  color:var(--ink-2); font-size:14.5px; line-height:1.65;
}

/* === 결과물 (Recent Work) === */
.work-block {
  padding:48px 0; border-top:1px solid var(--line);
}
.work-block:first-of-type { border-top:none; padding-top:0; }
.work-head {
  display:flex; justify-content:space-between; align-items:baseline;
  margin-bottom:14px; flex-wrap:wrap; gap:16px;
}
.work-period {
  font-size:12px; font-weight:700; letter-spacing:0.12em;
  color:var(--accent); text-transform:uppercase;
}
.work-title {
  font-weight:800; font-size:30px; letter-spacing:-0.03em;
  color:var(--ink); line-height:1.2; margin-bottom:8px;
}
.work-sub {
  font-size:15px; font-weight:500; color:var(--gray);
  line-height:1.55; margin-bottom:24px; max-width:680px;
}
.work-prose {
  font-size:15.5px; line-height:1.85; color:var(--ink-2);
  margin-bottom:32px; max-width:760px;
}
.work-prose p { margin-bottom:14px; }
.work-prose strong { color:var(--ink); font-weight:700; }

/* 메트릭 (섹션 내) */
.metrics {
  display:grid; grid-template-columns:repeat(4,1fr);
  border-top:1px solid var(--line);
  border-bottom:1px solid var(--line);
  margin:24px 0 32px;
}
.metric {
  padding:20px 16px; text-align:left;
  border-right:1px solid var(--line);
}
.metric:last-child { border-right:none; }
.metric-num {
  font-weight:900; font-size:32px; line-height:1;
  color:var(--ink); letter-spacing:-0.03em;
  margin-bottom:6px;
}
.metric-num small {
  font-weight:700; font-size:14px; color:var(--gray); margin-left:2px;
}
.metric-label {
  font-size:11.5px; color:var(--gray); font-weight:500;
  line-height:1.4; letter-spacing:-0.005em;
}

/* === 영상 카드 === */
.video-grid {
  display:grid; grid-template-columns:repeat(auto-fit,minmax(320px,1fr));
  gap:20px; margin:24px 0;
}
.vc {
  display:block; text-decoration:none; color:inherit;
  background:var(--bg); border:1px solid var(--line);
  transition:all 0.2s ease;
}
.vc:hover {
  border-color:var(--accent);
  box-shadow:0 12px 32px rgba(30,41,59,0.15);
  transform:translateY(-2px);
}
.vc-thumb { position:relative; aspect-ratio:16/9; background:#0a0a0a; overflow:hidden; }
.vc-thumb img {
  width:100%; height:100%; object-fit:cover; display:block;
  transition:transform 0.4s ease;
}
.vc:hover .vc-thumb img { transform:scale(1.04); }
.vc-overlay {
  position:absolute; inset:0; display:flex;
  align-items:center; justify-content:center;
  background:rgba(0,0,0,0.05); transition:background 0.2s ease;
}
.vc:hover .vc-overlay { background:rgba(30,41,59,0.18); }
.vc-play { width:60px; height:60px; filter:drop-shadow(0 2px 8px rgba(0,0,0,0.5)); }
.vc-dur {
  position:absolute; bottom:10px; right:10px;
  background:rgba(0,0,0,0.85); color:white;
  padding:3px 9px; font-size:12px; font-weight:600;
}
.vc-meta { padding:16px 18px 18px; }
.vc-meta strong {
  display:block; font-weight:700; font-size:15.5px; color:var(--ink);
  line-height:1.4; margin-bottom:5px; letter-spacing:-0.01em;
}
.vc-meta em { display:block; font-style:normal; font-size:13px; color:var(--gray); margin-bottom:8px; }
.vc-meta .vc-link {
  display:inline-block; font-size:11px; color:var(--accent);
  font-weight:600; letter-spacing:0.04em;
}

.note {
  background:var(--bg-soft); padding:18px 22px;
  font-size:13.5px; color:var(--ink-2); line-height:1.7;
  border-left:3px solid var(--ink);
  margin:20px 0 0;
}
.note strong { color:var(--ink); font-weight:700; }
.note a { color:var(--accent); text-decoration:none; font-weight:600; border-bottom:1px solid var(--accent); }

/* === 갤러리 (지명원) === */
.gallery-label {
  font-size:11px; font-weight:700; letter-spacing:0.16em;
  color:var(--gray); text-transform:uppercase;
  margin:48px 0 16px; display:flex; align-items:center; gap:14px;
}
.gallery-label::before {
  content:''; display:inline-block; width:24px; height:1px;
  background:var(--gray);
}
.gallery {
  display:grid; grid-template-columns:repeat(2,1fr); gap:16px;
}
.gallery.single { grid-template-columns:1fr; max-width:760px; margin:0 auto; }
.gal-item img {
  width:100%; display:block;
  border:1px solid var(--line); border-radius:1px;
}
.gal-item .cap {
  font-size:12.5px; font-weight:500; color:var(--gray);
  padding-top:8px; line-height:1.5;
}

.client-list {
  background:var(--bg-soft); padding:24px 28px; margin:24px 0;
  border-left:3px solid var(--gray);
  font-size:14px; line-height:1.85; color:var(--ink-2);
}
.client-list-title {
  font-size:11px; font-weight:700; color:var(--gray);
  letter-spacing:0.14em; text-transform:uppercase; margin-bottom:12px;
}
.client-list strong { color:var(--ink); font-weight:600; }

/* === Why This Move (모순 해결 섹션) === */
.why-block {
  display:grid; grid-template-columns:1fr;
  gap:24px;
}
.why-card {
  background:var(--bg-soft); padding:36px 40px;
  border-left:3px solid var(--accent);
}
.why-card h4 {
  font-size:18px; font-weight:800; color:var(--ink);
  letter-spacing:-0.02em; margin-bottom:14px;
}
.why-card p {
  font-size:15.5px; line-height:1.85; color:var(--ink-2);
  margin-bottom:10px;
}
.why-card p:last-child { margin-bottom:0; }
.why-card strong { color:var(--ink); font-weight:700; }

/* === 약속 표 === */
.promise {
  margin:32px 0 0;
  border-top:2px solid var(--ink);
  border-bottom:2px solid var(--ink);
}
.p-row {
  display:grid; grid-template-columns:160px 1fr;
  padding:24px 0; gap:32px;
  border-bottom:1px solid var(--line);
}
.p-row:last-child { border-bottom:none; }
.p-row .p-when {
  font-weight:800; font-size:17px; color:var(--accent);
  letter-spacing:-0.02em;
}
.p-row .p-what {
  font-size:15px; line-height:1.85; color:var(--ink-2);
}
.p-row .p-what strong { color:var(--ink); font-weight:700; }

/* === 클로징 === */
.closing {
  margin:64px 0 0; padding:0;
  text-align:left;
}
.closing-quote {
  font-size:18px; line-height:1.75; color:var(--ink-2);
  margin-bottom:24px;
}
.closing-quote em {
  display:block; font-style:normal; font-weight:700;
  font-size:20px; color:var(--ink); margin:14px 0;
  padding:18px 22px; background:var(--bg-soft);
  border-left:3px solid var(--accent);
}
.closing-final {
  font-weight:800; font-size:30px; line-height:1.3;
  letter-spacing:-0.03em; color:var(--ink);
  margin:40px 0 16px; max-width:680px;
}
.closing-final .accent { color:var(--accent); }
.closing-tail {
  font-size:15px; color:var(--gray); font-weight:500; margin-top:16px;
}
.signature {
  margin-top:48px; padding-top:24px;
  border-top:1px solid var(--line);
  font-weight:700; font-size:15px; color:var(--ink);
}
.signature small {
  display:block; font-weight:500; font-size:13px;
  color:var(--gray); margin-top:5px;
}

/* === 반응형 === */
@media (max-width:980px) {
  .sidebar {
    position:relative; width:100%; height:auto;
    border-right:none; border-bottom:1px solid var(--line);
    padding:24px 32px;
  }
  .sb-divider, .sb-foot { display:none; }
  .sb-nav { flex-direction:row; flex-wrap:wrap; gap:6px 16px; margin-top:14px; }
  .sb-nav a { padding:4px 0; border-left:none; padding-left:0; margin-left:0; font-size:12.5px; }
  .sb-nav .sb-num { display:none; }
  .main { margin-left:0; padding:48px 28px 80px; }
  .hero-grid { grid-template-columns:1fr; gap:32px; }
  .hero-photo { width:200px; height:240px; }
  .hero-title { font-size:44px; }
  .kpi-grid { grid-template-columns:repeat(2,1fr); }
  .kpi:nth-child(3n) { border-right:1px solid var(--line); }
  .kpi:nth-child(2n) { border-right:none; }
  .kpi:nth-child(n+4) { border-bottom:1px solid var(--line); }
  .kpi:nth-child(n+5) { border-bottom:none; }
  .kpi-num { font-size:40px; }
  .section-title { font-size:30px; }
  .chapter-block { grid-template-columns:1fr; gap:8px; }
  .t-row { grid-template-columns:1fr; gap:6px; }
  .metrics { grid-template-columns:repeat(2,1fr); }
  .metric:nth-child(2n) { border-right:none; }
  .gallery { grid-template-columns:1fr; }
  .p-row { grid-template-columns:1fr; gap:8px; }
  .closing-final { font-size:22px; }
}

/* === 인쇄 === */
@media print {
  body { background:white; font-size:10.5pt; line-height:1.55; }
  .sidebar { display:none; }
  .main { margin-left:0; max-width:100%; padding:0; }
  .section { margin-bottom:24pt; page-break-inside:avoid; }
  .hero { padding:0 0 12pt; }
  .kpi-section { margin-bottom:24pt; page-break-inside:avoid; }
  .exec-summary { page-break-inside:avoid; }
  .vc { page-break-inside:avoid; box-shadow:none; }
  .vc-thumb img { filter:grayscale(0.3); }
  .hero-title { font-size:24pt; }
  .section-title { font-size:18pt; }
  .kpi-num { font-size:24pt; }
  a { color:var(--ink); text-decoration:none; }
  .closing { page-break-inside:avoid; }
}

/* ============ PDF PRINT CSS (6페이지 A4) ============ */
@page { size: A4; margin: 13mm 16mm; }
@media print {
  body { font-size: 9.5pt !important; line-height: 1.6 !important; }
  .sidebar { display: none !important; }
  .main { margin-left: 0 !important; max-width: none !important; padding: 0 !important; }
  
  .hero, .kpi-section, .exec-summary { page-break-before: avoid !important; }
  section.section { page-break-before: always !important; }
  .work-block + .work-block { page-break-before: always !important; }
  .work-block { page-break-inside: auto !important; }
  
  .hero-grid { display: block !important; font-size: 0 !important; }
  .hero-grid > div:first-child { display: inline-block !important; width: calc(100% - 60mm) !important; vertical-align: middle !important; padding-right: 6mm !important; font-size: 10pt; box-sizing: border-box !important; }
  .hero-photo { display: inline-block !important; width: 54mm !important; height: auto !important; vertical-align: middle !important; }
  
  .kpi-grid { display: block !important; font-size: 0 !important; border-top: 2px solid #0a0a0a !important; border-bottom: 2px solid #0a0a0a !important; margin: 5mm 0 !important; }
  .kpi { display: inline-block !important; width: 33.33% !important; vertical-align: top !important; padding: 5mm 3mm !important; box-sizing: border-box !important; font-size: 10pt; text-align: center !important; border-right: 1px solid #e5e5e5 !important; }
  .kpi:nth-child(3n) { border-right: none !important; }
  .kpi:nth-child(n+4) { border-top: 1px solid #e5e5e5 !important; }
  .kpi-num { font-size: 24pt !important; line-height: 1 !important; margin-bottom: 2mm !important; }
  .kpi-num small { font-size: 11pt !important; }
  .kpi-desc { font-size: 8pt !important; line-height: 1.4 !important; }
  
  .chapter-block { display: block !important; font-size: 0 !important; margin-bottom: 4mm !important; page-break-inside: avoid !important; }
  .chapter-block > * { display: inline-block !important; vertical-align: top !important; font-size: 10pt; box-sizing: border-box !important; }
  .ch-meta { width: 30mm !important; padding-right: 4mm !important; }
  .ch-body { width: calc(100% - 30mm) !important; padding-left: 4mm !important; border-left: 1px solid #e5e5e5 !important; }
  
  .timeline { display: block !important; }
  .t-row { display: block !important; font-size: 0 !important; padding: 2.5mm 0 !important; border-bottom: 1px solid #e5e5e5 !important; }
  .t-row > * { display: inline-block !important; vertical-align: top !important; font-size: 9pt; box-sizing: border-box !important; }
  .t-era { width: 26mm !important; padding-right: 2mm !important; }
  .t-org { width: 32% !important; padding-right: 2mm !important; }
  .t-result { width: calc(68% - 26mm) !important; }
  
  .metrics { display: block !important; font-size: 0 !important; margin: 4mm 0 !important; border-top: 1px solid #e5e5e5 !important; border-bottom: 1px solid #e5e5e5 !important; }
  .metric { display: inline-block !important; width: 25% !important; vertical-align: top !important; padding: 3mm 2mm !important; box-sizing: border-box !important; font-size: 9pt; text-align: center !important; }
  .metric-num { font-size: 16pt !important; line-height: 1 !important; margin-bottom: 1mm !important; }
  .metric-label { font-size: 7pt !important; line-height: 1.3 !important; }
  
  .video-grid { display: block !important; font-size: 0 !important; margin: 4mm 0 !important; }
  .vc { display: inline-block !important; width: 49% !important; margin-right: 2% !important; margin-bottom: 3mm !important; vertical-align: top !important; border: 1px solid #d4d4d4 !important; border-radius: 3px !important; overflow: hidden !important; text-decoration: none !important; color: inherit !important; page-break-inside: avoid !important; font-size: 9pt; box-sizing: border-box !important; }
  .vc:nth-child(2n) { margin-right: 0 !important; }
  .vc:only-child { width: 100% !important; margin-right: 0 !important; height: 24mm !important; }
  .vc:only-child .vc-thumb { float: left !important; width: 42mm !important; height: 24mm !important; display: block !important; }
  .vc:only-child .vc-meta { margin-left: 42mm !important; padding: 4mm 5mm !important; height: 24mm !important; box-sizing: border-box !important; }
  .vc:only-child .vc-play { width: 9mm !important; height: 9mm !important; }
  
  .vc-thumb { display: block !important; width: 100% !important; height: 33mm !important; background: #1e293b !important; position: relative !important; float: none !important; text-align: center !important; padding: 0 !important; margin: 0 !important; overflow: hidden !important; }
  .vc-thumb img.yt-thumb { display: block !important; width: 100% !important; height: 100% !important; object-fit: cover !important; object-position: center !important; }
  .vc-overlay { position: absolute !important; top: 50% !important; left: 50% !important; transform: translate(-50%, -50%) !important; background: transparent !important; margin: 0 !important; padding: 0 !important; display: block !important; }
  .vc-play { width: 11mm !important; height: 11mm !important; display: block !important; }
  .vc-play circle { fill: white !important; opacity: 0.92 !important; }
  .vc-play polygon { fill: #1e293b !important; }
  .vc-dur { display: none !important; }
  
  .vc-meta { display: block !important; margin: 0 !important; padding: 2.5mm 3.5mm !important; background: white !important; height: auto !important; overflow: hidden !important; }
  .vc-meta strong { display: block !important; font-size: 9pt !important; font-weight: 700 !important; color: #0a0a0a !important; margin-bottom: 1mm !important; line-height: 1.3 !important; }
  .vc-meta em { display: block !important; font-style: normal !important; font-size: 7pt !important; color: #737373 !important; margin-bottom: 1mm !important; line-height: 1.4 !important; }
  .vc-link { display: block !important; font-size: 6.5pt !important; font-weight: 600 !important; color: #1e293b !important; letter-spacing: 0.02em !important; }
  
  .gallery { display: block !important; font-size: 0 !important; margin: 3mm 0 !important; }
  .gallery > * { display: inline-block !important; width: 25% !important; vertical-align: top !important; padding: 0 1mm 3mm !important; box-sizing: border-box !important; font-size: 7.5pt; page-break-inside: avoid !important; }
  .gallery > * img { max-height: 28mm !important; width: 100% !important; object-fit: cover !important; }
  .gallery > * .gallery-caption, .gallery > * > p, .gallery > * > div { font-size: 7pt !important; line-height: 1.3 !important; margin-top: 1mm !important; }
  
  .why-block { display: block !important; font-size: 0 !important; margin: 5mm 0 !important; }
  .why-card { display: inline-block !important; width: 33.33% !important; vertical-align: top !important; padding: 5mm !important; box-sizing: border-box !important; font-size: 9pt; border: 1px solid #e5e5e5 !important; border-right: none !important; background: #fafaf8 !important; }
  .why-card:last-child { border-right: 1px solid #e5e5e5 !important; }
  .why-card h4 { font-size: 10pt !important; margin-bottom: 3mm !important; }
  .why-card p { font-size: 8.5pt !important; line-height: 1.65 !important; }
  
  .promise { display: block !important; border: 1px solid #e5e5e5 !important; }
  .p-row { display: block !important; font-size: 0 !important; border-bottom: 1px solid #e5e5e5 !important; }
  .p-row:last-child { border-bottom: none !important; }
  .p-row > * { display: inline-block !important; vertical-align: top !important; font-size: 9.5pt; box-sizing: border-box !important; }
  .p-when { width: 26mm !important; padding: 3.5mm 4mm !important; background: #1e293b !important; color: white !important; font-weight: 700 !important; font-size: 8.5pt !important; text-align: center !important; }
  .p-what { width: calc(100% - 26mm) !important; padding: 3.5mm 6mm !important; line-height: 1.7 !important; }
  
  section { padding: 5mm 0 !important; margin: 0 !important; }
  .hero { padding: 4mm 0 5mm !important; }
  .kpi-section { padding: 3mm 0 !important; }
  .exec-summary { padding: 9mm 0 !important; margin-top: 5mm !important; }
  .exec-summary .es-label { padding: 0 8mm !important; margin-bottom: 6mm !important; font-size: 7.5pt !important; }
  .exec-summary p { padding: 0 8mm !important; line-height: 1.95 !important; margin: 4.5mm 0 !important; font-size: 10pt !important; }
  .section-head { margin-bottom: 5mm !important; }
  
  .hero-title { font-size: 30pt !important; line-height: 1.05 !important; margin-bottom: 4mm !important; }
  .hero-sub { font-size: 9.5pt !important; margin: 3mm 0 !important; line-height: 1.6 !important; }
  .hero-tag { font-size: 7.5pt !important; }
  .hero-meta { font-size: 8pt !important; margin-top: 5mm !important; padding-top: 4mm !important; }
  
  .section-title { font-size: 22pt !important; line-height: 1.1 !important; margin: 0 !important; }
  .section-num { font-size: 7.5pt !important; letter-spacing: 0.22em !important; margin-bottom: 4mm !important; }
  .section-sub { font-size: 9.5pt !important; line-height: 1.6 !important; margin-top: 3mm !important; }
  
  .work-title { font-size: 16pt !important; }
  .work-meta { font-size: 7.5pt !important; }
  .work-prose p { font-size: 9pt !important; line-height: 1.65 !important; margin: 2mm 0 !important; }
  .work-block .gallery > * img { max-height: 28mm !important; }
  
  #commit { page-break-before: avoid !important; }
  .closing { page-break-before: avoid !important; padding-top: 5mm !important; margin-top: 5mm !important; }
  .closing-quote { font-size: 8.5pt !important; line-height: 1.6 !important; padding: 4mm 5mm !important; margin-bottom: 4mm !important; }
  .closing-quote em { font-size: 9.5pt !important; padding: 1mm 0 !important; display: inline; }
  .closing-final { font-size: 13pt !important; line-height: 1.4 !important; padding: 4mm 0 !important; margin: 3mm 0 !important; }
  .closing-tail { font-size: 8.5pt !important; margin: 3mm 0 !important; }
  .signature { font-size: 9pt !important; margin-top: 4mm !important; padding-top: 4mm !important; }
  .signature small { font-size: 7.5pt !important; }
  
  .promise { margin: 3mm 0 !important; }
  .p-row > * { padding: 2.5mm 4mm !important; }
  .p-when { font-size: 8pt !important; }
  .p-what { font-size: 8.5pt !important; line-height: 1.55 !important; }
  
  .why-card { padding: 3.5mm !important; }
  .why-card h4 { font-size: 9.5pt !important; margin-bottom: 2mm !important; }
  .why-card p { font-size: 8pt !important; line-height: 1.55 !important; }
  
  #why, #commit { padding: 4mm 0 !important; }
  #why .section-head, #commit .section-head { margin-bottom: 4mm !important; }
  
  /* FrameForge Platform Preview — 2x2 */
  .section-head + .work-block .gallery:not(.single) > * { width: 50% !important; padding: 0 2mm 4mm !important; font-size: 9pt !important; }
  .section-head + .work-block .gallery:not(.single) > * img { max-height: 38mm !important; width: 100% !important; object-fit: cover !important; }
  
  /* Atico — 영상 + B2B 고객사 좌우 배치 */
  .atico-feature-row { display: block !important; font-size: 0 !important; margin: 5mm 0 !important; }
  .atico-feature-row > * { display: inline-block !important; vertical-align: top !important; font-size: 9pt; box-sizing: border-box !important; }
  .afr-video { width: 50% !important; padding-right: 3mm !important; }
  .afr-list { width: 50% !important; padding-left: 3mm !important; text-align: center !important; }
  .afr-video .video-grid { margin: 0 !important; }
  .afr-video .vc:only-child { width: 100% !important; height: auto !important; margin: 0 !important; display: block !important; }
  .afr-video .vc:only-child .vc-thumb { float: none !important; display: block !important; width: 100% !important; height: 48mm !important; }
  .afr-video .vc:only-child .vc-meta { margin-left: 0 !important; padding: 3mm 4mm !important; height: auto !important; }
  .afr-video .vc:only-child .vc-play { width: 13mm !important; height: 13mm !important; }
  .afr-list .gallery-label { margin-bottom: 2.5mm !important; font-size: 7.5pt !important; text-align: left !important; padding-left: 0 !important; }
  .afr-list .gallery.single { text-align: center !important; margin: 0 !important; }
  .afr-list .gallery.single > * { width: 100% !important; }
  .afr-list .gallery.single > * img { max-width: 100% !important; max-height: 75mm !important; width: auto !important; height: auto !important; margin: 0 auto !important; display: block !important; }
  .afr-list .gallery.single .cap { margin-top: 1.5mm !important; font-size: 7.5pt !important; }
  
  .gallery.single { text-align: center !important; margin: 5mm 0 !important; font-size: 0 !important; }
  .gallery.single > * { display: inline-block !important; width: auto !important; padding: 0 !important; margin: 0 auto !important; text-align: center !important; font-size: 9pt !important; }
  .gallery.single > * img { max-width: 90mm !important; max-height: 65mm !important; width: auto !important; height: auto !important; object-fit: contain !important; display: block !important; margin: 0 auto !important; }
  .gallery.single .cap { margin-top: 2mm !important; font-size: 8pt !important; }
  
  p { margin: 2mm 0 !important; }
  img:not(.hero-photo):not(.yt-thumb) { max-width: 100% !important; height: auto !important; }
  .work-prose, .timeline, .promise, .why-block { page-break-inside: auto !important; }
}

</style>
</head>
<body>

<!-- ========== STICKY SIDEBAR ========== -->
<aside class="sidebar">
  <div>
    <div class="sb-brand">
      KIM EUI-HYUN
      <small>Business Development</small>
    </div>
    
    <div class="sb-divider"></div>
    
    <nav class="sb-nav">
      <a href="#about"><span class="sb-num">01</span>About</a>
      <a href="#summary"><span class="sb-num">02</span>Executive Summary</a>
      <a href="#track"><span class="sb-num">03</span>Track Record</a>
      <a href="#work"><span class="sb-num">04</span>Recent Work</a>
      <a href="#why"><span class="sb-num">05</span>Why This Move</a>
      <a href="#commit"><span class="sb-num">06</span>Commitment</a>
      <a href="#contact"><span class="sb-num">07</span>Contact</a>
    </nav>
  </div>
  
  <div class="sb-foot">
    <div class="ctc-row">
      <span class="ctc-icon">✉</span>
      <a href="mailto:ehk3929@naver.com">ehk3929@naver.com</a>
    </div>
    <div class="ctc-row">
      <span class="ctc-icon">☎</span>
      <a href="tel:01062853929">010-6285-3929</a>
    </div>
  </div>
</aside>

<!-- ========== MAIN ========== -->
<main class="main">

  <!-- ========== 01 HERO ========== -->
  <section id="about" class="hero">
    <div class="hero-tag">Business Development Portfolio</div>
    
    <div class="hero-grid">
      <div>
        <h1 class="hero-title">
          닫힌 거래처를<br>
          <span class="accent">여는 사업개발자.</span>
        </h1>
        <p class="hero-sub">
          정부청사 · 대한생명 63빌딩 · CJ 5계열사 · 래미안 원베일리 · 웹툰 IP사 — 
          27년간 4번의 새 영역에서 동일한 결과를 만든 B2B 사업개발 패턴.
        </p>
      </div>
      <img src="''' + img_data('profile') + '''" alt="김의현" class="hero-photo">
    </div>
    
    <div class="hero-meta">
      <span>
        <span>B2B 사업개발</span>
        <em><b>28</b><s>년</s></em>
        <small>1997 → 현재</small>
      </span>
      <span class="hl">
        <span>회사 운영 경험</span>
        <em><b>24</b><s>년</s></em>
        <small>대표 · 창업 · 경영</small>
      </span>
      <span>
        <span>AI 신제품</span>
        <em><b>7</b><s>년차</s></em>
        <small>MDH → FrameForge</small>
      </span>
    </div>
  </section>

  <!-- ========== 5초 KPI ========== -->
  <section class="kpi-section">
    <div class="kpi-label">Key Numbers</div>
    <div class="kpi-grid">
      <div class="kpi">
        <div class="kpi-num"><span class="accent">30</span><small>+</small></div>
        <div class="kpi-desc"><strong>대형 거래처 단독 개척</strong><br>전 산업 누적</div>
      </div>
      <div class="kpi">
        <div class="kpi-num"><span class="accent">7,000</span><small>+</small></div>
        <div class="kpi-desc"><strong>누적 고객</strong><br>24년 회사 운영</div>
      </div>
      <div class="kpi">
        <div class="kpi-num"><span class="accent">CJ</span><small> 5사</small></div>
        <div class="kpi-desc"><strong>그룹 계열사 장기 거래</strong><br>단일 영업 → 조직 확장 패턴</div>
      </div>
      <div class="kpi">
        <div class="kpi-num"><span class="accent">2,990</span><small>세대</small></div>
        <div class="kpi-desc"><strong>래미안 원베일리</strong><br>AI 1차 피벗 MVP 안착</div>
      </div>
      <div class="kpi">
        <div class="kpi-num"><span class="accent">7</span><small>건</small></div>
        <div class="kpi-desc"><strong>정부 R&amp;D 과제책임자</strong><br>연속 선정</div>
      </div>
      <div class="kpi">
        <div class="kpi-num"><span class="accent">2</span><small>건</small></div>
        <div class="kpi-desc"><strong>웹툰 IP B2B 본계약</strong><br>AI 영상 SaaS 단독 체결</div>
      </div>
    </div>
  </section>

  <!-- ========== 02 EXECUTIVE SUMMARY ========== -->
  <section id="summary" class="exec-summary">
    <div class="es-label">02 — Executive Summary</div>
    <p>
      <strong>본인은 28년 경력의 B2B 사업개발자입니다.</strong> 
      정부청사·대한생명 63빌딩·CJ 5계열사·반포 래미안 원베일리·국내 웹툰 IP사까지 — 
      4번의 새 영역에 진입할 때마다 닫혀 있던 대형 거래처를 단독으로 열어온 패턴이 일관됩니다.
    </p>
    <p>
      특히 <strong>직접 회사를 운영하며 의사결정 라인을 안에서 경험</strong>했고, 
      최근 7년은 AI 신제품 2종(Meta Design House · FrameForge IFN)을 0에서 상용화까지 직접 빌딩했습니다. 
      MDH 운영 기간 정부 R&amp;D 7건을 과제책임자로 수행했고, 
      FrameForge로 웹툰 IP사 2곳과 B2B 본계약을 단독 체결한 정량 결과를 영상·이미지로 검증할 수 있습니다.
    </p>
    <p>
      <strong>회사 운영과 AI 신제품 빌딩</strong>을 모두 거친 사업개발자로서, 마지막 5~6년을 한 회사 안에서 
      신규 거래처 개척과 본계약 협상에 집중하고자 합니다.
    </p>
  </section>

  <!-- ========== 03 TRACK RECORD ========== -->
  <section id="track" class="section">
    <div class="section-head">
      <div class="section-num">03 — Track Record</div>
      <h2 class="section-title">27년, 다섯 영역, 한 가지 방법</h2>
      <p class="section-sub">
        영역이 바뀌고 산업이 바뀌어도, 작동하는 제안을 들고 거절을 다음 방문의 이유로 삼아 
        신뢰가 계약으로 바뀔 때까지 가는 — 한 가지 방법.
      </p>
    </div>

    <!-- 7장 서사: 1~4장 -->
    <div class="chapter-block">
      <div class="ch-meta">시작점<small>1997</small></div>
      <div class="ch-body">
        <p>
          신입사원으로 입사했을 당시, 분명한 목표가 있었습니다.
        </p>
        <div class="ch-quote">
          "실력과 성과로, 사장님이 가장 믿고 쓸 수 있는 사람이 되자."
        </div>
      </div>
    </div>

    <div class="chapter-block">
      <div class="ch-meta">흔들림<small>1998 · IMF</small></div>
      <div class="ch-body">
        <p>
          IMF가 왔습니다. 사장님은 회사를 떠나셨고, 법정관리인이 왔습니다. 
          본래 목표가 향할 자리가 사라졌습니다.
        </p>
        <p>
          그래도 어렸기에 <strong>부도난 회사의 명함을 들고</strong> 현장을 누볐습니다. 
          하나로통신 IDC, 부래당 사옥, 제1·제3 정부종합청사 — LG를 제외한 신규 프로젝트를 
          따낸 영업직원은 회사 안에서 저 한 명이었습니다. 회사는 빠르게 법정관리를 벗어났지만, 
          사장님은 돌아오지 않으셨습니다.
        </p>
      </div>
    </div>

    <div class="chapter-block">
      <div class="ch-meta">두 번째 시도<small>2000~2001</small></div>
      <div class="ch-body">
        <p>
          삼고초려로 합류한 다음 회사에서 어린 나이에 본부장을 역임했고, 
          <strong>3년간의 거절 끝에 마침내 대한생명(현, 한화생명) 63빌딩의 첫 거래를 열었습니다.</strong> 
          그러나 본래 목표가 향할 자리는 여전히 보이지 않았습니다.
        </p>
      </div>
    </div>

    <div class="chapter-block">
      <div class="ch-meta">결심<small>2001</small></div>
      <div class="ch-body">
        <p>
          결국 <strong>그 자리를 직접 만들어보기로 했습니다.</strong> 
          회사 운영의 시작이었습니다.
        </p>
      </div>
    </div>

    <!-- 5시대 표 -->
    <div class="timeline">
      <div class="t-row">
        <div class="t-era">1998<small>IMF 부도 직후</small></div>
        <div class="t-org">제1·제3 정부종합청사<br><small>하나로통신 · 부래당</small></div>
        <div class="t-res">부도난 회사의 명함으로 단독 수주 — LG 제외 신규 영업 사내 유일</div>
      </div>
      <div class="t-row">
        <div class="t-era">2001<small>어린 본부장 시절</small></div>
        <div class="t-org">대한생명 63빌딩<br><small>현 한화생명</small></div>
        <div class="t-res">3년 거절 끝의 첫 거래 — B2B 영업 패턴이 정립된 자리</div>
      </div>
      <div class="t-row">
        <div class="t-era">2010s<small>17년 회사 운영</small></div>
        <div class="t-org">CJ재단 · CJ 5개 계열사<br><small>한화생명 전국 매뉴얼 1위</small></div>
        <div class="t-res">단일 거래 → 조직적 장기 거래로 확장 패턴 완성</div>
      </div>
      <div class="t-row">
        <div class="t-era">2021<small>AI 1차 피벗</small></div>
        <div class="t-org">반포 래미안 원베일리<small>2,990세대 신축 대장 단지</small></div>
        <div class="t-res">조합 도면 확보 → MVP 안착</div>
      </div>
      <div class="t-row">
        <div class="t-era">2025<small>AI 2차 피벗</small></div>
        <div class="t-org">국내 웹툰 IP사 2곳</div>
        <div class="t-res">AI 영상 본계약 단독 체결 — 25+ 모델 오케스트레이션 SaaS 빌딩</div>
      </div>
    </div>
  </section>

  <!-- ========== 04 RECENT WORK ========== -->
  <section id="work" class="section">
    <div class="section-head">
      <div class="section-num">04 — Recent Work</div>
      <h2 class="section-title">최근 결과물</h2>
      <p class="section-sub">
        (주)아티코 시절의 결과물부터 AI 개발제품 2종까지 — 영상과 자료로 직접 검증 가능합니다.
      </p>
    </div>

    <!-- FrameForge -->
    <div class="work-block">
      <div class="work-head">
        <div>
          <div class="work-title">FrameForge IFN</div>
          <div class="work-sub">AI 영상 자동화 SaaS · 25+ 모델 오케스트레이션 엔진 · 1인 단독 수행</div>
        </div>
        <div class="work-period">2025 — Present</div>
      </div>
      <div class="work-prose">
        <p>
          웹툰·웹소설 IP 1편 영상화에 전통 방식으로 수개월·수천만 원이 소요되는 시장에서, 
          <strong>기획부터 아키텍처 설계·핵심 구현·B2B 영업·본계약 협상까지 1인 단독 수행</strong>한 SaaS입니다.
        </p>
        <p>
          사업개발 + 회사 운영 + 9명 팀 빌딩 경험에 더해, 
          <strong>직접 기획부터 개발까지 가능한 사업개발자</strong>라는 차별화는 
          AI 시대 7년이 만들어낸 가장 큰 자산입니다.
        </p>
        <p>
          <strong>IFN(Infinite Frame Network) 엔진</strong>은 WAN 2.2 · VEO 3 Fast · Gemini 2.5 · 
          Kling 1.6 · Flux Schnell · DALL-E 3 · Sora 2 · GPT-4o 등 25개 이상의 생성AI 모델을 
          오케스트레이션해 텍스트 입력 75초 만에 영상을 출력합니다. 멀티엔진 라우터·LoRA 캐릭터 
          파인튜닝·AutoPilot 4단계 자동화 모듈 포함.
        </p>
      </div>

      <div class="gallery-label">Platform Preview</div>
      <div class="gallery">
        <div class="gal-item"><img src="''' + img_data('ff_landing') + '''" alt="FrameForge Landing"><p class="cap">랜딩 — Transform Images to Videos</p></div>
        <div class="gal-item"><img src="''' + img_data('ff_dashboard') + '''" alt="FrameForge Dashboard"><p class="cap">대시보드 — 5종 AI 워크플로우 모듈</p></div>
        <div class="gal-item"><img src="''' + img_data('ff_studio') + '''" alt="FrameForge Studio"><p class="cap">스튜디오 — 풀 에디팅 워크스페이스</p></div>
        <div class="gal-item"><img src="''' + img_data('ff_gallery') + '''" alt="FrameForge Gallery"><p class="cap">갤러리 — 본계약 IP사 결과물</p></div>
      </div>

      <div class="metrics">
        <div class="metric"><div class="metric-num">25<small>+</small></div><div class="metric-label">생성AI 모델 오케스트레이션</div></div>
        <div class="metric"><div class="metric-num">75<small>sec</small></div><div class="metric-label">텍스트→영상 풀 파이프라인</div></div>
        <div class="metric"><div class="metric-num">2<small>건</small></div><div class="metric-label">웹툰 IP사 B2B 본계약</div></div>
        <div class="metric"><div class="metric-num">2<small>건</small></div><div class="metric-label">특허 출원 (2025.08)</div></div>
      </div>
      <div class="video-grid">
        ''' + vc('ff_yeo') + '''
        ''' + vc('ff_juchi') + '''
      </div>
      <div class="note">
        <strong>대표 1인 단독 수행</strong> — 백엔드 89% / 프론트엔드 88% / AI 엔진 90% 완성 · 
        학습 데이터 22,000건 자체 구축 · MVP 영상 20+ 에피소드 제작
      </div>
    </div>

    <!-- MDH -->
    <div class="work-block">
      <div class="work-head">
        <div>
          <div class="work-title">Meta Design House (MDH)</div>
          <div class="work-sub">AI 3D 인테리어 솔루션 · Unity·Unreal × MobileNet · 풀스택 팀 빌딩 3년</div>
        </div>
        <div class="work-period">2021 — 2024</div>
      </div>
      <div class="work-prose">
        <p>
          평균 3개월·8회 이상 대면 미팅이 필요한 인테리어 시공의 비용·시간 문제를 
          AI 취향분석과 3D 시뮬레이션의 결합으로 해결한 솔루션입니다.
        </p>
        <p>
          사용자 라이프스타일 입력 → MobileNet V2/V3 백본 기반 AI 취향분석 엔진 → 
          Unity·Unreal 3D 공간 시뮬레이터 → 디자이너 메타컨설팅의 3단계 구조. 
          학습 DB는 2D 이미지 30,000장 + 3D 에셋 3,260개를 자체 구축. 
          프로토타입 3종 + 크로스플랫폼 앱 2종 연속 개발 후 반포 래미안 원베일리 2,990세대에 MVP 안착.
        </p>
      </div>
      <div class="metrics">
        <div class="metric"><div class="metric-num">2,990<small>세대</small></div><div class="metric-label">래미안 원베일리 MVP 안착</div></div>
        <div class="metric"><div class="metric-num">30<small>min</small></div><div class="metric-label">공간 모델링 (경쟁사 1~3일)</div></div>
        <div class="metric"><div class="metric-num">7<small>건</small></div><div class="metric-label">정부 R&amp;D 과제책임자</div></div>
        <div class="metric"><div class="metric-num">4<small>건</small></div><div class="metric-label">특허 등록 + 상표 3건</div></div>
      </div>
      <div class="video-grid">
        ''' + vc('mdh_full') + '''
        ''' + vc('mdh_walk') + '''
      </div>
      <div class="note">
        <strong>리딩한 팀 — 9명 인하우스</strong> (개발 4명 + 디자인 4명 + 대표). 
        AI/3D 수석 · 백엔드 · 3D 앱·모델러 · 프론트엔드 수석 · 공간 디자이너 등으로 구성. 
        0에서 풀스택 팀을 빌딩하고 3년간 동행. 
        대-스타 해결사 4차산업 AI 부문 최종 2위(2022) · 공간융합 빅데이터 우수기업상(과기정통부, 2023) · 
        창업성장 R&amp;D 디딤돌 과제책임자(2023)
      </div>
    </div>

    <!-- 아티코 -->
    <div class="work-block">
      <div class="work-head">
        <div>
          <div class="work-title">(주)아티코 — ATICO Design &amp; Furniture</div>
          <div class="work-sub">서울 목동 500평 플래그십 · 2본부 7팀 · 누적 고객 7,000명</div>
        </div>
        <div class="work-period">2001 — 2019</div>
      </div>
      <div class="work-prose">
        <p>
          직접 운영한 인테리어·홈퍼니싱 사업. 영업·시공·MD 다부서 조직을 직접 이끌었고, 
          누적 고객 7,000명의 거래처 데이터로 18년간 제안 영업을 체계화했습니다.
        </p>
        <p>
          대한전문건설협회 회원 · 한국디자인진흥원(KIDP) 산업디자인전문회사 · 한국산업기술진흥협회(KOITA) 
          연구개발전담부서 인정 — 정부 R&amp;D 7건 선정의 원점이 된 인프라를 2001~2011년에 직접 구축했습니다.
        </p>
      </div>
      
      <div class="atico-feature-row">
        <div class="afr-video">
      <div class="video-grid">
        ''' + vc('atico') + '''
      </div>
        </div>
        <div class="afr-list">
      <div class="gallery-label">B2B 고객사</div>
      <div class="gallery single">
        <div class="gal-item">
          <img src="''' + img_data('p17') + '''" alt="B2B 고객사">
          <p class="cap">EHK Design 공식 지명원에서 발췌</p>
        </div>
        </div>
      </div>
      </div>

      <div class="client-list">
        <div class="client-list-title">Major Clients (Selected)</div>
        대한생명 63본사 · 한화손해보험 · CJ재단 · CJ홈쇼핑 · CJ시스템즈 · CJ텔레닉스 · CJ개발 · 
        CJ푸드시스템 · CJ E&amp;M센터 · 삼성전자 · GS건설 · 코오롱글로벌 · 한국가스공사(KOGAS) · 
        하나로텔레콤 · 까사미아 · 광동제약 · 화성산업 · (주)태왕 · 우신건설/우신개발 · 
        한국산업인력공단 · 경기디지털콘텐츠진흥원 · 서울 강남/동부/서부 교육청 · 인천 부평구청 외.
      </div>

      <div class="gallery-label">Selected Works</div>
      <div class="gallery">
        <div class="gal-item"><img src="''' + img_data('p19') + '''" alt="CJ E&M"><p class="cap">CJ E&amp;M Center 14F · 오피스</p></div>
        <div class="gal-item"><img src="''' + img_data('p40') + '''" alt="한화손해보험"><p class="cap">한화손해보험 일산지역단 · 오피스</p></div>
        <div class="gal-item"><img src="''' + img_data('p38') + '''" alt="CJ E&M Center 10F"><p class="cap">CJ E&amp;M Center 10F · 라운지 &amp; 라이브러리</p></div>
        <div class="gal-item"><img src="''' + img_data('p45') + '''" alt="까사미아 아현"><p class="cap">까사미아 아현점 · 최우수 점주 (다이닝)</p></div>
        <div class="gal-item"><img src="''' + img_data('p42') + '''" alt="한화생명 63빌딩 고객센터"><p class="cap">한화생명 63빌딩 · 고객센터</p></div>
        <div class="gal-item"><img src="''' + img_data('p34') + '''" alt="한정식"><p class="cap">한정식 · 산천 봉피양 (용산)</p></div>
        <div class="gal-item"><img src="''' + img_data('p49') + '''" alt="씨제이오쇼핑"><p class="cap">씨제이오쇼핑 · 라이프스타일 매장</p></div>
        <div class="gal-item"><img src="''' + img_data('p09') + '''" alt="조직도"><p class="cap">2본부 7팀 — 영업·시공·MD 다부서 조직 (2011)</p></div>
      </div>
    </div>
  </section>

  <!-- ========== 05 WHY THIS MOVE (모순 해결) ========== -->
  <section id="why" class="section">
    <div class="section-head">
      <div class="section-num">05 — Why This Move</div>
      <h2 class="section-title">왜 다시 회사로</h2>
      <p class="section-sub">
        27년 전의 본래 자리로 돌아갑니다. 다만 그때와 다른 점이 있습니다.
      </p>
    </div>

    <div class="why-block">
      <div class="why-card">
        <h4>24년의 회사 운영이 알려준 것</h4>
        <p>
          직접 회사를 운영하며 최종 의사결정자를 경험했습니다. 
          어떤 거래처가 들어와야 하는지, 어떤 사업개발자가 진짜 필요한 사람인지, 
          어떤 결과가 회사를 다음 단계로 끌고 가는지 — <strong>기업 대표의 입장에서 무게를 알게 되었습니다.</strong>
        </p>
      </div>
      
      <div class="why-card">
        <h4>AI 신제품 7년이 알려준 것</h4>
        <p>
          <strong>MDH (2021~2024)</strong> — 9명 인하우스 팀(개발 4명 + 디자인 4명 + 대표)을 빌딩해 3년간 운영.<br>
          <strong>FrameForge IFN (2025~)</strong> — 새 아이템으로 1인 단독 개발.
        </p>
        <p>
          두 가지 운영 방식을 모두 직접 경험한 끝에 정확히 측정한 것은 —
          <strong>작은 팀과 1인 개발 모두 결국 자원과 조직 규모의 한계가 있다</strong>는 사실입니다.
        </p>
        <p>
          같은 28년의 경험과 7년의 AI 빌딩 경험을 무한한 자원과 성장 가능성을 가진 회사 안에서 쓴다면, 
          결과는 10배·100배가 됩니다.
        </p>
      </div>
      
      <div class="why-card">
        <h4>본래의 원점으로</h4>
        <p>
          27년 전 신입사원 시절의 그 목표 — <strong>"사장님이 가장 믿고 쓸 수 있는 사람이 되자"</strong> — 
          로 돌아갑니다.
        </p>
        <p>
          다른 점은 단 하나. 27년 전과 달리 지금의 저는 <strong>최종 의사결정자의 무게를 아는 사업개발자가 되어 있다</strong>는 것입니다.
        </p>
      </div>
    </div>
  </section>

  <!-- ========== 06 COMMITMENT ========== -->
  <section id="commit" class="section">
    <div class="section-head">
      <div class="section-num">06 — Commitment</div>
      <h2 class="section-title">입사 후 약속</h2>
      <p class="section-sub">
        구체적이고 검증 가능한 단계별 목표 — 30일 / 90일 / 1년 / 5~6년.
      </p>
    </div>

    <div class="promise">
      <div class="p-row">
        <div class="p-when">첫 30일</div>
        <div class="p-what">
          회사의 의사결정 라인·기존 거래처 구조·경쟁사 포지션·내부 자산을 정확히 학습. 
          <strong>새 시장에서 닫힌 거래처를 여는 패턴</strong> — 27년간 4번의 새 영역에서 
          일관되게 작동한 능력이 그대로 회사의 자산입니다.
        </div>
      </div>
      <div class="p-row">
        <div class="p-when">31~90일</div>
        <div class="p-what">
          닫혀 있던 신규 대형 거래처 1~2곳에 첫 미팅 자리를 만듭니다. 
          <strong>제 28년이 가장 잘하는 일입니다.</strong>
        </div>
      </div>
      <div class="p-row">
        <div class="p-when">1년 이내</div>
        <div class="p-what">
          신규 본계약 1건 이상, 또는 기존 거래처에서 의미 있는 확장 1건. 
          정부 R&amp;D·공공 발주가 핵심인 조직이라면 <strong>선정 1건 이상</strong>을 목표로 — 
          7건 연속 선정·과제책임자 수행으로 이미 검증된 능력입니다.
        </div>
      </div>
      <div class="p-row">
        <div class="p-when">5~6년</div>
        <div class="p-what">
          <strong>대표 직속의 신뢰받는 사업개발 책임자로 일하다 은퇴.</strong> 
          27년 경력의 마지막 챕터를 한 회사 안에서 의미 있게 마무리하는 것이 저의 분명한 직업적 결정입니다.
        </div>
      </div>
    </div>

    <!-- 클로징 -->
    <div class="closing">
      <div class="closing-quote">
        오래전 저희 회사의 마케팅 교육을 담당했던 분을 한 데모데이 심사위원으로 우연히 다시 만났습니다. 
        평가 말미에 이런 말씀을 하셨습니다.
        <em>"100을 가지고 계신데 80밖에 표현을 못 하시네요. 120을 표현해 보세요."</em>
        오래전부터 저의 일하는 방식을 봐오신 분의 평가였기에 깊이 새겼지만, 
        저는 여전히 <strong>100을 말하고 120을 보이는 것</strong>이 익숙합니다. 
        과장하지 않습니다. 약속한 것보다 늘 조금 더 가져다드리는 것 — 
        신입 시절부터 한 번도 바뀐 적 없는 일하는 방식입니다.
      </div>
      
      <div class="closing-final">
        드릴 수 있는 가장 정직한 약속은 단 하나입니다.<br>
        <span class="accent">결과로만 증명하겠습니다.</span>
      </div>
      
      <p class="closing-tail">면접 자리에서 뵙기를 청합니다.</p>

      <div class="signature" id="contact">
        — 김의현 드림
        <small>010-6285-3929 · ehk3929@naver.com</small>
      </div>
    </div>
  </section>

</main>

</body>
</html>'''

OUT_DIR = os.path.join(BASE, 'html')
os.makedirs(OUT_DIR, exist_ok=True)
OUT = os.path.join(OUT_DIR, 'portfolio_김의현_v2.6.1.html')
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(HTML)
size_kb = os.path.getsize(OUT) // 1024
print(f"✅ v2.6.1 빌드 완료")
print(f"   파일: {OUT}")
print(f"   크기: {size_kb}KB ({size_kb/1024:.1f}MB)")
