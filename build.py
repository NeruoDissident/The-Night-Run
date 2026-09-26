"""Build standalone HTML and a GitHub Pages-ready PWA using Python's standard library."""
from pathlib import Path
import base64
import hashlib
import json
import shutil

BASE = Path(__file__).resolve().parent
SOURCE = BASE / 'src'
SITE = BASE / '_site'
SITE.mkdir(exist_ok=True)

html = (SOURCE / 'index.html').read_text(encoding='utf-8')
for name in ('style.css', 'mobile.css'):
    css = (SOURCE / name).read_text(encoding='utf-8')
    html = html.replace(f'<link rel="stylesheet" href="{name}">', f'<style>\n{css}\n</style>')
for name in ('data.js', 'engine.js', 'ui.js', 'pwa.js'):
    js = (SOURCE / name).read_text(encoding='utf-8')
    html = html.replace(f'<script src="{name}"></script>', f'<script>\n{js}\n</script>')
html = html.replace('<!-- PWA_HEAD -->', '''
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" type="image/svg+xml" href="icons/logo.svg">
<link rel="icon" type="image/png" sizes="32x32" href="icons/favicon-32.png">
<link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Night Run">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
''')
mark = base64.b64encode((BASE / 'icons/logo.svg').read_bytes()).decode('ascii')
html = html.replace('<!-- BRAND_MARK -->', f'<img class="brand-icon" src="data:image/svg+xml;base64,{mark}" width="32" height="32" alt="Night Run fractured skyline">')
for output in (BASE / 'index.html', BASE / 'Night Run.html', SITE / 'index.html', SITE / 'Night Run.html'):
    output.write_text(html, encoding='utf-8', newline='\n')

assets = ['index.html', 'manifest.webmanifest', 'apple-touch-icon.png'] + sorted(str(p.relative_to(BASE)).replace('\\', '/') for p in (BASE / 'icons').iterdir() if p.is_file())
worker = (SOURCE / 'sw.template.js').read_text(encoding='utf-8')
digest = hashlib.sha256(worker.encode('utf-8'))
for name in assets:
    digest.update((BASE / name).read_bytes())
    if name != 'index.html':
        dest = SITE / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(BASE / name, dest)
version = digest.hexdigest()[:16]
worker = worker.replace('__BUILD_VERSION__', version).replace('__PRECACHE__', json.dumps(['./' + name for name in assets]))
for output in (BASE / 'sw.js', SITE / 'sw.js'):
    output.write_text(worker, encoding='utf-8', newline='\n')
for output in (BASE / '.nojekyll', SITE / '.nojekyll'):
    output.touch()
print(f'Built Night Run {version}: {len(html.encode("utf-8")):,} bytes, {len(assets)} offline assets.')
