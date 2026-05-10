"""
preview_launcher.py
===================
my_portfolio/ 안의 portfolio_*.html 파일을 스캔해
버전 런처 페이지를 생성 후 기본 브라우저로 엽니다.

실행:
    python preview_launcher.py
    python preview_launcher.py --open 2.6.1   # 특정 버전 바로 열기
"""

import os, sys, glob, re, webbrowser, tempfile
from datetime import datetime
from pathlib import Path

# ── 경로 ──────────────────────────────────────────────
BASE = Path(__file__).parent   # 스크립트 위치 = my_portfolio/
HTML_DIR = BASE / "html"       # portfolio_*.html 모음

# ── 버전 스캔 ──────────────────────────────────────────
def scan_versions():
    pattern = str(HTML_DIR / "portfolio_김의현_v*.html")
    files = sorted(glob.glob(pattern), key=os.path.getmtime, reverse=True)
    versions = []
    for f in files:
        p = Path(f)
        m = re.search(r'v([\d.]+)\.html$', p.name)
        ver = m.group(1) if m else "?"
        mtime = datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
        size_kb = p.stat().st_size // 1024
        size_str = f"{size_kb:,} KB" if size_kb < 1024 else f"{size_kb/1024:.1f} MB"
        versions.append({
            "ver": ver, "name": p.name, "path": p.as_posix(),
            "mtime": mtime, "size": size_str, "is_latest": False
        })
    if versions:
        versions[0]["is_latest"] = True
    return versions

# ── CLI: 특정 버전 바로 열기 ────────────────────────────
def open_direct(ver_str):
    pattern = str(HTML_DIR / f"portfolio_김의현_v{ver_str}.html")
    matches = glob.glob(pattern)
    if matches:
        webbrowser.open(Path(matches[0]).as_uri())
        print(f"✅ 열림: {matches[0]}")
    else:
        print(f"❌ 파일 없음: portfolio_김의현_v{ver_str}.html")
    sys.exit(0)

# ── 런처 HTML 생성 ─────────────────────────────────────
def make_launcher_html(versions):
    rows = ""
    for v in versions:
        badge = '<span class="badge">최신</span>' if v["is_latest"] else ""
        rows += f"""
        <tr class="{'latest' if v['is_latest'] else ''}">
          <td class="ver">v{v['ver']} {badge}</td>
          <td class="fname">{v['name']}</td>
          <td class="meta">{v['size']}</td>
          <td class="meta">{v['mtime']}</td>
          <td class="action">
            <a href="file:///{v['path']}" target="_blank">열기 ↗</a>
          </td>
        </tr>"""

    empty_msg = """
        <tr><td colspan="5" class="empty">
          portfolio_김의현_v*.html 파일이 없습니다.<br>
          <code>python build_v261.py</code> 를 먼저 실행하세요.
        </td></tr>""" if not versions else ""

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>포트폴리오 런처 — 김의현</title>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{
    font-family: 'Pretendard', -apple-system, 'Apple SD Gothic Neo',
                 'Noto Sans KR', sans-serif;
    background: #f7f6f2; color: #0a0a0a;
    min-height: 100vh; display: flex;
    flex-direction: column; align-items: center;
    justify-content: center; padding: 40px 20px;
  }}
  .card {{
    background: #fff; border: 1px solid #e5e2da;
    border-radius: 12px; width: 100%; max-width: 780px;
    overflow: hidden; box-shadow: 0 2px 16px rgba(0,0,0,0.06);
  }}
  .header {{
    background: #1e293b; color: #fff;
    padding: 28px 36px;
  }}
  .header h1 {{ font-size: 18px; font-weight: 600; letter-spacing: -0.01em; }}
  .header p  {{ font-size: 13px; color: rgba(255,255,255,0.5); margin-top: 6px; }}
  table {{
    width: 100%; border-collapse: collapse;
    font-size: 14px;
  }}
  thead tr {{
    background: #f7f6f2; border-bottom: 1px solid #e5e2da;
  }}
  thead th {{
    padding: 12px 20px; text-align: left;
    font-size: 11px; font-weight: 600;
    letter-spacing: 0.08em; color: #6b6b6b;
    text-transform: uppercase;
  }}
  tbody tr {{
    border-bottom: 1px solid #f0ede5;
    transition: background 0.15s;
  }}
  tbody tr:hover {{ background: #fafaf8; }}
  tbody tr.latest {{ background: #fef9ee; }}
  tbody tr.latest:hover {{ background: #fef3c7; }}
  td {{ padding: 16px 20px; vertical-align: middle; }}
  td.ver {{ font-weight: 700; font-size: 15px; white-space: nowrap; }}
  td.fname {{ font-size: 12.5px; color: #6b6b6b; font-family: monospace; }}
  td.meta {{ font-size: 12px; color: #9a9a9a; white-space: nowrap; }}
  td.action a {{
    display: inline-block; padding: 7px 16px;
    background: #1e293b; color: #fff;
    border-radius: 6px; font-size: 13px;
    font-weight: 500; text-decoration: none;
    transition: background 0.15s;
  }}
  td.action a:hover {{ background: #334155; }}
  .badge {{
    display: inline-block; margin-left: 6px;
    padding: 2px 7px; background: #fef3c7;
    color: #92400e; border-radius: 4px;
    font-size: 10px; font-weight: 700;
    vertical-align: middle; letter-spacing: 0.04em;
  }}
  td.empty {{
    text-align: center; padding: 48px;
    color: #9a9a9a; line-height: 2;
  }}
  td.empty code {{
    background: #f0ede5; padding: 2px 8px;
    border-radius: 4px; font-size: 13px;
  }}
  .footer {{
    padding: 16px 36px; font-size: 12px;
    color: #9a9a9a; background: #f7f6f2;
    border-top: 1px solid #e5e2da;
  }}
</style>
</head>
<body>
<div class="card">
  <div class="header">
    <h1>📄 포트폴리오 버전 런처</h1>
    <p>김의현 · {BASE}</p>
  </div>
  <table>
    <thead>
      <tr>
        <th>버전</th>
        <th>파일명</th>
        <th>크기</th>
        <th>빌드 시각</th>
        <th></th>
      </tr>
    </thead>
    <tbody>
      {rows}{empty_msg}
    </tbody>
  </table>
  <div class="footer">
    새 버전 빌드 후 이 창을 새로고침하면 목록이 업데이트됩니다.
  </div>
</div>
</body>
</html>"""

# ── 메인 ────────────────────────────────────────────────
if __name__ == "__main__":
    # --open 2.6.1 옵션 처리
    if "--open" in sys.argv:
        idx = sys.argv.index("--open")
        if idx + 1 < len(sys.argv):
            open_direct(sys.argv[idx + 1])

    versions = scan_versions()
    html = make_launcher_html(versions)

    # 임시 파일로 저장 후 브라우저 오픈
    tmp = Path(tempfile.gettempdir()) / "_portfolio_launcher.html"
    tmp.write_text(html, encoding="utf-8")
    webbrowser.open(tmp.as_uri())

    print(f"✅ 런처 열림 — {len(versions)}개 버전 발견")
    for v in versions:
        latest_tag = " ← 최신" if v["is_latest"] else ""
        print(f"   v{v['ver']}  {v['size']}  {v['mtime']}{latest_tag}")
