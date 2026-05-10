"""
editor_server.py
================
포트폴리오 HTML을 브라우저에서 직접 텍스트 편집 후 저장하는 로컬 서버.

실행:
    python editor_server.py              # 최신 버전 자동 선택
    python editor_server.py --ver 2.6.3  # 특정 버전 지정

브라우저:  http://localhost:8765
저장:      [저장 Ctrl+S]        → 현재 파일 덮어쓰기
버전업:    [v2.6.4로 저장 Ctrl+Shift+S] → 다음 패치 버전으로 새 파일 생성 후 자동 새로고침
종료:      터미널에서 Ctrl+C
"""

import os, sys, glob, json, re, threading, webbrowser
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

BASE     = Path(__file__).parent
HTML_DIR = BASE / "html"
PORT     = 8765

# ── 편집할 파일 선택 ────────────────────────────────────
def pick_file(ver=None):
    if ver:
        p = HTML_DIR / f"portfolio_김의현_v{ver}.html"
        if p.exists(): return p
        sys.exit(f"❌ 파일 없음: {p}")
    files = sorted(HTML_DIR.glob("portfolio_김의현_v*.html"),
                   key=os.path.getmtime, reverse=True)
    if not files:
        sys.exit(f"❌ html/ 안에 portfolio_*.html 없음")
    return files[0]

# ── 다음 패치 버전 계산 ─────────────────────────────────
VER_RE = re.compile(r'^portfolio_김의현_v(\d+)\.(\d+)(?:\.(\d+))?\.html$')

def next_patch_version(current_path):
    """현재 파일에서 v{major}.{minor}.{patch} 파싱 후, 존재하지 않는 다음 patch 번호를 반환.

    예) v2.6.html      → v2.6.1
        v2.6.3.html    → v2.6.4 (없으면), v2.6.5 (있으면) ...

    Returns: (Path, version_str)
    """
    m = VER_RE.match(current_path.name)
    if not m:
        raise ValueError(f"버전 파싱 실패: {current_path.name}")
    major = int(m.group(1))
    minor = int(m.group(2))
    patch = int(m.group(3)) if m.group(3) else 0
    while True:
        patch += 1
        candidate = HTML_DIR / f"portfolio_김의현_v{major}.{minor}.{patch}.html"
        if not candidate.exists():
            return candidate, f"{major}.{minor}.{patch}"

# ── 툴바 잔재 제거 ──────────────────────────────────────
# 클라이언트가 저장 직전 toolbar div를 제거하지만, style/script 잔재가 남는 경우가 있어
# 서버 측에서 정규식으로 한 번 더 청소한다.
TOOLBAR_CLEANUP = [
    # 1) toolbar div (방어용 — 보통 클라이언트가 이미 제거)
    re.compile(r'<div\s+id="_edit-toolbar"[\s\S]*?</button>\s*</div>\s*', re.IGNORECASE),
    # 2) toolbar 전용 <style> 블록
    re.compile(
        r'<style\b[^>]*>(?:(?!</style>)[\s\S])*?#_edit-toolbar(?:(?!</style>)[\s\S])*?</style>\s*',
        re.IGNORECASE,
    ),
    # 3) toolbar 전용 <script> 블록 (식별자 기준)
    re.compile(
        r'<script\b[^>]*>(?:(?!</script>)[\s\S])*?'
        r'(?:_saveDoc|_saveAsDoc|_EDIT_FILE|_NEXT_VERSION|_edit-toolbar)'
        r'(?:(?!</script>)[\s\S])*?</script>\s*',
        re.IGNORECASE,
    ),
]

def clean_toolbar(html: str) -> str:
    for pat in TOOLBAR_CLEANUP:
        html = pat.sub('', html)
    return html

# ── 편집기 툴바 주입 ────────────────────────────────────
TOOLBAR = """
<style>
#_edit-toolbar {
  position: fixed; top: 0; right: 0; z-index: 99999;
  display: flex; align-items: center; gap: 10px;
  padding: 10px 18px;
  background: #1e293b; color: #fff;
  font-family: -apple-system, 'Pretendard', sans-serif;
  font-size: 13px; border-bottom-left-radius: 10px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}
#_edit-toolbar .tb-file {
  font-size: 11px; color: rgba(255,255,255,0.5);
  max-width: 260px; overflow: hidden;
  text-overflow: ellipsis; white-space: nowrap;
}
#_edit-toolbar .tb-hint {
  font-size: 11px; color: rgba(255,255,255,0.4);
}
#_edit-btn-save {
  padding: 6px 16px; background: #c8a97e; color: #1a1a1e;
  border: none; border-radius: 6px; font-size: 13px;
  font-weight: 700; cursor: pointer; transition: background 0.15s;
}
#_edit-btn-save:hover { background: #d9ba91; }
#_edit-btn-save.saved { background: #22c55e; color: #fff; }
#_edit-btn-saveas {
  padding: 6px 16px; background: #334155; color: #fff;
  border: none; border-radius: 6px; font-size: 13px;
  font-weight: 700; cursor: pointer; transition: background 0.15s;
}
#_edit-btn-saveas:hover { background: #475569; }
#_edit-btn-saveas.saved { background: #22c55e; color: #fff; }
#_edit-status {
  font-size: 11px; color: #c8a97e; min-width: 80px;
}
[contenteditable]:hover {
  outline: 1px dashed rgba(200,169,126,0.5);
  border-radius: 2px;
}
[contenteditable]:focus {
  outline: 2px solid #c8a97e !important;
  border-radius: 2px;
  background: rgba(200,169,126,0.06) !important;
}
/* 편집 모드: reveal 애니메이션 중립화 (IntersectionObserver 충돌 방지) */
.reveal { opacity: 1 !important; transform: none !important; }
</style>

<div id="_edit-toolbar">
  <div>
    <div style="font-weight:600; margin-bottom:2px;">✏️ 포트폴리오 편집기</div>
    <div class="tb-file" id="_tb-fname"></div>
  </div>
  <div class="tb-hint">텍스트 클릭 → 편집</div>
  <div id="_edit-status"></div>
  <button id="_edit-btn-save" onclick="_saveDoc()">저장 Ctrl+S</button>
  <button id="_edit-btn-saveas" onclick="_saveAsDoc()">버전업 저장</button>
</div>

<script>
(function(){
  // 파일명 + 다음 버전 표시
  document.getElementById('_tb-fname').textContent = window._EDIT_FILE || '';
  const nextVer = window._NEXT_VERSION || '';
  const saveAsBtn = document.getElementById('_edit-btn-saveas');
  saveAsBtn.textContent = nextVer ? ('v' + nextVer + '로 저장') : '버전업 저장';

  // contenteditable 대상 — v2.6.3 클래스 기준 광범위 매칭
  const SELECTORS = [
    // 메인 영역 — 태그 기반
    '.main h1','.main h2','.main h3','.main h4','.main h5','.main h6',
    '.main p','.main li','.main td','.main th',
    '.main blockquote','.main figcaption',
    // 메인 영역 — 클래스 기반 텍스트 컨테이너
    '.hero-tag','.hero-title','.hero-sub','.hero-meta',
    '.kpi-label','.kpi-num','.kpi-desc',
    '.es-label',
    '.section-num','.section-title','.section-sub',
    '.ch-meta','.ch-quote','.ch-body',
    '.t-era','.t-org','.t-res',
    '.work-title','.work-sub','.work-period','.work-prose',
    '.metric-num','.metric-label',
    '.vc-meta','.vc-link','.vc-dur',
    '.gallery-label','.cap','.note',
    '.client-list-title',
    '.commit-row','.why-card','.closing',
    // Commitment 섹션 (실제 클래스: .p-when / .p-what)
    '.p-when','.p-what',
    // 사이드바
    '.sb-brand','.sb-foot','.sb-nav a','.sb-num','.ctc-row'
  ];

  function applyEditable() {
    // reveal 애니메이션 무력화 — 모든 .reveal 요소를 즉시 .revealed 처리
    document.querySelectorAll('.reveal').forEach(el => el.classList.add('revealed'));

    SELECTORS.forEach(sel => {
      document.querySelectorAll(sel).forEach(el => {
        if (el.closest('#_edit-toolbar')) return;
        if (el.querySelector('img,svg,iframe,video')) return;
        el.contentEditable = 'true';
        el.spellcheck = false;
      });
    });

    // 디버그: contenteditable 부여 결과 로그
    const total = document.querySelectorAll('[contenteditable="true"]').length;
    console.log('[editor] contenteditable 적용된 요소: ' + total + '개');
    document.querySelectorAll('.p-when, .p-what').forEach((el, i) => {
      console.log('[editor] .p-' + i, el.contentEditable, el);
    });
  }

  applyEditable();

  // 단축키: Ctrl+S = 저장, Ctrl+Shift+S = 버전업 저장
  document.addEventListener('keydown', e => {
    if ((e.ctrlKey || e.metaKey) && (e.key === 's' || e.key === 'S')) {
      e.preventDefault();
      if (e.shiftKey) _saveAsDoc();
      else _saveDoc();
    }
  });

  // 직렬화 직전: 툴바 제거 + contenteditable 정리 → outerHTML 추출 → 툴바 복원
  function _serialize() {
    const toolbar = document.getElementById('_edit-toolbar');
    const toolbarHTML = toolbar.outerHTML;
    toolbar.remove();

    document.querySelectorAll('[contenteditable]').forEach(el => {
      el.removeAttribute('contenteditable');
      el.removeAttribute('spellcheck');
    });

    const html = '<!DOCTYPE html>\\n' + document.documentElement.outerHTML;

    document.body.insertAdjacentHTML('afterbegin', toolbarHTML);
    document.getElementById('_edit-btn-save').onclick = _saveDoc;
    document.getElementById('_edit-btn-saveas').onclick = _saveAsDoc;
    return html;
  }

  // 두 버튼 모두 잠깐 초록으로
  function _flashSaved(savedLabelMain, savedLabelAs, restoreMs) {
    const btn  = document.getElementById('_edit-btn-save');
    const btn2 = document.getElementById('_edit-btn-saveas');
    const origMain = btn.textContent;
    const origAs   = btn2.textContent;
    btn.classList.add('saved');   btn.textContent  = savedLabelMain;
    btn2.classList.add('saved');  btn2.textContent = savedLabelAs;
    if (restoreMs > 0) {
      setTimeout(() => {
        btn.classList.remove('saved');   btn.textContent  = origMain;
        btn2.classList.remove('saved');  btn2.textContent = origAs;
      }, restoreMs);
    }
  }

  // 덮어쓰기 저장
  window._saveDoc = function() {
    const status = document.getElementById('_edit-status');
    const html = _serialize();
    status.textContent = '저장 중...';
    fetch('/save', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({html: html})
    })
    .then(r => r.json())
    .then(d => {
      if (d.ok) {
        status.textContent = '✅ 저장됨';
        _flashSaved('✅ 저장됨', '✅ 저장됨', 2000);
        setTimeout(() => { status.textContent = ''; }, 2000);
        applyEditable();
      } else {
        status.textContent = '❌ 오류: ' + d.msg;
      }
    })
    .catch(e => { status.textContent = '❌ ' + e; });
  };

  // 버전업 저장 — 새 파일 생성 후 자동 새로고침
  window._saveAsDoc = function() {
    const status = document.getElementById('_edit-status');
    const html = _serialize();
    status.textContent = '버전업 저장 중...';
    fetch('/save_as', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({html: html})
    })
    .then(r => r.json())
    .then(d => {
      if (d.ok) {
        status.textContent = '✅ ' + d.fname + ' — 새로고침 중';
        _flashSaved('✅ 저장됨', '✅ ' + d.fname, 0);
        setTimeout(() => window.location.reload(), 1200);
      } else {
        status.textContent = '❌ 오류: ' + d.msg;
      }
    })
    .catch(e => { status.textContent = '❌ ' + e; });
  };
})();
</script>
"""

# ── HTTP 핸들러 ─────────────────────────────────────────
class Handler(BaseHTTPRequestHandler):
    target_file = None
    auto_pick   = False  # --ver 미지정 시 매 GET / 마다 최신 mtime 재선택

    def log_message(self, fmt, *args):
        pass  # 로그 억제

    def do_GET(self):
        if urlparse(self.path).path == '/':
            if Handler.auto_pick:
                latest = pick_file(None)
                if latest != Handler.target_file:
                    Handler.target_file = latest

            raw = Handler.target_file.read_text(encoding='utf-8')
            fname = Handler.target_file.name
            try:
                _, next_ver = next_patch_version(Handler.target_file)
            except ValueError:
                next_ver = ''
            inject = (
                f'<script>'
                f'window._EDIT_FILE="{fname}";'
                f'window._NEXT_VERSION="{next_ver}";'
                f'</script>\n' + TOOLBAR
            )
            if '</body>' in raw:
                html = raw.replace('</body>', inject + '\n</body>', 1)
            else:
                html = raw + inject
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        path = urlparse(self.path).path
        if path == '/save':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            try:
                data = json.loads(body)
                html = clean_toolbar(data.get('html', ''))
                Handler.target_file.write_text(html, encoding='utf-8')
                resp = json.dumps({'ok': True}).encode()
            except Exception as e:
                resp = json.dumps({'ok': False, 'msg': str(e)}).encode()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(resp)
        elif path == '/save_as':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            try:
                data = json.loads(body)
                html = clean_toolbar(data.get('html', ''))
                new_path, _ = next_patch_version(Handler.target_file)
                new_path.write_text(html, encoding='utf-8')
                Handler.target_file = new_path
                resp = json.dumps({'ok': True, 'fname': new_path.name}).encode()
            except Exception as e:
                resp = json.dumps({'ok': False, 'msg': str(e)}).encode()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(resp)
        else:
            self.send_response(404)
            self.end_headers()

# ── 메인 ────────────────────────────────────────────────
if __name__ == '__main__':
    ver = None
    if '--ver' in sys.argv:
        idx = sys.argv.index('--ver')
        if idx + 1 < len(sys.argv):
            ver = sys.argv[idx + 1]

    target = pick_file(ver)
    Handler.target_file = target
    Handler.auto_pick   = (ver is None)

    server = HTTPServer(('localhost', PORT), Handler)
    url = f'http://localhost:{PORT}'

    print(f'✅ 편집기 서버 시작')
    print(f'   파일: {target}')
    print(f'   주소: {url}')
    print(f'   종료: Ctrl+C')

    threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n서버 종료.')
