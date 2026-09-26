"""Original Night Run vector mark and PNG app icons. Pillow is only needed to regenerate icons."""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'icons'
OUT.mkdir(exist_ok=True)
SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" role="img" aria-label="Night Run: a fractured skyline and a road out">
<defs><linearGradient id="b" x2=".8" y2="1"><stop stop-color="#243b42"/><stop offset="1" stop-color="#0b151f"/></linearGradient></defs>
<path fill="url(#b)" d="M0 0h512v512H0z"/>
<circle cx="344" cy="144" r="34" fill="#e3c18a"/>
<path d="M108 352V216h60v136m32 0V136h72v216m32 0V248h80v104" fill="none" stroke="#93d7b5" stroke-width="22" stroke-linejoin="miter"/>
<path fill="#0e2029" d="m292 112 34 16-66 108 58 52-100 132-42-24 83-105-57-51z"/>
<path d="m311 112-78 125 59 53-94 119" fill="none" stroke="#e3c18a" stroke-width="13" stroke-linejoin="bevel"/>
<path d="M128 242h20m-20 34h20m180 2h34m-34 34h34" stroke="#d0e5d4" stroke-width="10"/>
</svg>'''
(OUT / 'logo.svg').write_text(SVG, encoding='utf-8', newline='\n')
SCALE = 4
im = Image.new('RGB', (512*SCALE, 512*SCALE))
d = ImageDraw.Draw(im)
for y in range(512*SCALE):
    f=y/(512*SCALE-1)
    c=tuple(round(a*(1-f)+b*f) for a,b in zip((36,59,66),(11,21,31)))
    d.line([(0,y),(512*SCALE,y)], fill=c)
def pts(points): return [(round(x*SCALE),round(y*SCALE)) for x,y in points]
def line(points,color,width): d.line(pts(points),fill=color,width=width*SCALE,joint='curve')
d.ellipse([310*SCALE,110*SCALE,378*SCALE,178*SCALE],fill='#e3c18a')
for points in [[(108,352),(108,216),(168,216),(168,352)],[(200,352),(200,136),(272,136),(272,352)],[(304,352),(304,248),(384,248),(384,352)]]:
    line(points,'#93d7b5',22)
d.polygon(pts([(292,112),(326,128),(260,236),(318,288),(218,420),(176,396),(259,291),(202,240)]),fill='#0e2029')
line([(311,112),(233,237),(292,290),(198,409)],'#e3c18a',13)
for x,y,w in [(128,242,20),(128,276,20),(328,278,34),(328,312,34)]:line([(x,y),(x+w,y)],'#d0e5d4',10)
for filename,size in [('icon-192.png',192),('icon-512.png',512),('icon-maskable-512.png',512),('favicon-32.png',32)]:
    im.resize((size,size),Image.Resampling.LANCZOS).save(OUT/filename)
im.resize((180,180),Image.Resampling.LANCZOS).save(ROOT/'apple-touch-icon.png')
print('Generated vector logo, Apple touch icon, favicons, and PWA icons.')
