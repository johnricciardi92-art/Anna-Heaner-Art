from pathlib import Path
import shutil, zipfile
from PIL import Image

base = Path('output/annaheaner-site-blue-lite')
if base.exists():
    shutil.rmtree(base)
base.mkdir(parents=True, exist_ok=True)
assets = base / 'assets' / 'images'
assets.mkdir(parents=True, exist_ok=True)

src_assets = Path('output/annaheaner-package/assets/images')
selected = ['Swiss-image-1.jpg'] + [p.name for p in sorted(src_assets.glob('*')) if p.is_file()][:24]
selected = list(dict.fromkeys(selected))
for name in selected:
    src = Path('Swiss-image-1.jpg') if name == 'Swiss-image-1.jpg' else src_assets / name
    if not src.exists():
        continue
    img = Image.open(src).convert('RGB')
    img.thumbnail((1800, 1800))
    dst = assets / (Path(name).stem + '.jpg')
    img.save(dst, format='JPEG', quality=78, optimize=True)

image_names = sorted([p.name for p in assets.glob('*.jpg')])
hero = 'Swiss-image-1.jpg' if 'Swiss-image-1.jpg' in image_names else image_names[0]
story_titles = ['Wrightsville Beach','Ireland','People','North of France','Portugal','Italy','Switzerland','South of France']
story_texts = [
    'The light, the water, and the easy pace of the coast.',
    'A slower landscape with room to breathe and wander.',
    'Portraits and encounters from the road.',
    'A quiet stretch of travel with wide skies and open paths.',
    'Small moments from a warmer edge of the journey.',
    'A place of architecture, food, and long afternoons.',
    'Mountain air, green hills, and a view that stays with you.',
    'Soft colors and the pull of the coast.'
]
story_cards = []
for i, title in enumerate(story_titles):
    img = image_names[i % len(image_names)]
    story_cards.append(f'''<article class="card"><img src="assets/images/{img}" alt="{title}"><div class="body"><div class="meta">Travel note</div><h3>{title}</h3><p>{story_texts[i % len(story_texts)]}</p></div></article>''')
gallery_imgs = image_names[:16]
gallery = '\n'.join([f'<button class="tile" data-image="assets/images/{n}" aria-label="Open {n}"><img src="assets/images/{n}" alt="Photo from the journal"></button>' for n in gallery_imgs])
html = f'''<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Anna Heaner</title>
<meta name="description" content="Travel notes and photographs." />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root,[data-theme="light"]{{--bg:#eef5fb;--surface:#f8fbfe;--surface2:#e6f0fa;--border:#cddced;--text:#203040;--muted:#58708a;--primary:#4f79a8;--primary2:#335c88;--shadow:0 14px 40px rgba(47,78,110,.12);--radius:1.2rem;--font1:'Cormorant Garamond',serif;--font2:'Manrope',sans-serif}}
[data-theme="dark"]{{--bg:#11181f;--surface:#16212b;--surface2:#1d2a36;--border:#243544;--text:#e9f1f7;--muted:#a8bfd2;--primary:#7ea7cf;--primary2:#9cbedd;--shadow:0 14px 40px rgba(0,0,0,.35)}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}body{{margin:0;font-family:var(--font2);background:var(--bg);color:var(--text);line-height:1.65}}img{{display:block;width:100%;height:auto}}a{{color:inherit;text-decoration:none}}button{{font:inherit;border:0;background:none;cursor:pointer}}
.container{{width:min(1120px,calc(100% - 2rem));margin:auto}}
.header{{position:sticky;top:0;z-index:10;background:color-mix(in srgb,var(--bg) 88%, transparent);backdrop-filter:blur(12px);border-bottom:1px solid var(--border)}}
.headrow{{display:flex;justify-content:space-between;align-items:center;gap:1rem;padding:1rem 0;flex-wrap:wrap}}
.brand{{display:flex;gap:.75rem;align-items:center}}.mark{{width:40px;height:40px;color:var(--primary)}}.brand h1{{font-family:var(--font1);font-size:2rem;margin:0;line-height:1}}.sub{{font-size:.75rem;letter-spacing:.18em;text-transform:uppercase;color:var(--muted)}}
.nav{{display:flex;gap:1rem;flex-wrap:wrap}}.nav a{{color:var(--muted);font-size:.92rem}}.nav a:hover{{color:var(--text)}}.toggle{{width:44px;height:44px;border:1px solid var(--border);border-radius:999px;background:var(--surface);color:var(--text)}}
.hero{{padding:4rem 0 2rem}}.grid{{display:grid;grid-template-columns:1.05fr .95fr;gap:2rem;align-items:center}}h2{{font-family:var(--font1);font-size:clamp(2.4rem,5vw,4.8rem);line-height:1.02;margin:0;max-width:10ch}}.hero p,.copy{{color:var(--muted);max-width:58ch}}
.cta{{display:flex;gap:.75rem;flex-wrap:wrap;margin-top:1.5rem}}.btn{{display:inline-flex;align-items:center;justify-content:center;min-height:44px;padding:.85rem 1.2rem;border-radius:999px;font-weight:700;font-size:.92rem}}.primary{{background:var(--primary);color:white}}.primary:hover{{background:var(--primary2)}}.secondary{{background:var(--surface);border:1px solid var(--border)}}
.panel{{background:linear-gradient(180deg,var(--surface),var(--surface2));border:1px solid var(--border);border-radius:var(--radius);overflow:hidden;box-shadow:var(--shadow)}}
.panel img{{aspect-ratio:4/5;object-fit:cover}}
.section{{padding:2.5rem 0}}.sectionhead{{display:flex;justify-content:space-between;align-items:end;gap:1rem;margin-bottom:1.25rem;flex-wrap:wrap}}.eyebrow{{font-size:.75rem;letter-spacing:.18em;text-transform:uppercase;color:var(--muted)}}h3{{font-family:var(--font1);font-size:clamp(1.8rem,3vw,2.8rem);margin:.2rem 0 0}}
.cards{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1rem}}.card{{background:var(--surface);border:1px solid var(--border);border-radius:1rem;overflow:hidden;box-shadow:0 1px 2px rgba(0,0,0,.04)}}.card img{{aspect-ratio:4/3;object-fit:cover}}.card .body{{padding:1rem 1rem 1.2rem}}.meta{{font-size:.74rem;letter-spacing:.15em;text-transform:uppercase;color:var(--muted);margin-bottom:.35rem}}
.gallery{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.8rem}}.tile{{padding:0;border-radius:.9rem;overflow:hidden;border:1px solid var(--border);background:var(--surface)}}.tile img{{aspect-ratio:1/1;object-fit:cover}}
.archive{{background:var(--surface2);border:1px solid var(--border);border-radius:1.2rem;padding:1.2rem 1.2rem .8rem}}.archive ul{{list-style:none;padding:0;margin:.8rem 0 0;display:grid;gap:.65rem}}.archive a{{color:var(--primary);font-weight:700}}
.lightbox{{position:fixed;inset:0;background:rgba(0,0,0,.85);display:none;place-items:center;padding:1.5rem;z-index:30}}.lightbox.open{{display:grid}}.lightbox img{{max-width:min(1100px,100%);max-height:82vh;border-radius:1rem}}.close{{position:absolute;top:1rem;right:1rem;width:44px;height:44px;border-radius:999px;background:white;color:#000;font-size:1.3rem}}
footer{{padding:2rem 0 3rem;border-top:1px solid var(--border);margin-top:2rem}}
@media (max-width:900px){{.grid,.cards,.gallery{{grid-template-columns:1fr}}.headrow{{align-items:flex-start}}}}
</style>
</head>
<body>
<header class="header"><div class="container headrow"><div class="brand"><svg class="mark" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M10 50L27 14L32 24L37 14L54 50" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/><path d="M18 36H46" stroke="currentColor" stroke-width="4" stroke-linecap="round"/></svg><div><h1>Anna Heaner</h1><div class="sub">Travel journal</div></div></div><nav class="nav"><a href="#stories">Stories</a><a href="#gallery">Gallery</a><a href="#archive">Archive</a></nav><button class="toggle" data-theme-toggle aria-label="Switch theme">◐</button></div></header>
<main>
<section class="hero"><div class="container grid"><div><div class="eyebrow">Notes from the road</div><h2>Travel, people, and places.</h2><p>A quiet collection of photographs and notes from Switzerland, Ireland, France, Italy, and the North Carolina coast.</p><div class="cta"><a class="btn primary" href="#stories">Browse stories</a><a class="btn secondary" href="#gallery">Open gallery</a></div></div><div class="panel"><img src="assets/images/{hero}" alt="Swiss alpine landscape" width="900" height="1100"></div></div></section>
<section id="stories" class="section"><div class="container"><div class="sectionhead"><div><div class="eyebrow">Stories</div><h3>Recent notes</h3></div><div class="copy">A broader selection of photographs from the archive, arranged so more of the images are available on the main page.</div></div><div class="cards">{''.join(story_cards)}</div></div></section>
<section id="gallery" class="section"><div class="container"><div class="sectionhead"><div><div class="eyebrow">Gallery</div><h3>Photographs</h3></div><div class="copy">More of the archive is now available directly on the page.</div></div><div class="gallery">{gallery}</div></div></section>
<section id="archive" class="section"><div class="container archive"><div class="eyebrow">Archive links</div><h3>From the journal</h3><ul><li><a href="#">Wrightsville Beach</a></li><li><a href="#">Ireland</a></li><li><a href="#">People</a></li></ul></div></section>
</main>
<footer><div class="container"><strong>Anna Heaner</strong><div class="sub" style="margin-top:.35rem">Travel journal</div></div></footer>
<div class="lightbox" id="lightbox"><button class="close" id="close">×</button><img id="lightboxImage" src="" alt="Expanded image"></div>
<script>(()=>{{const r=document.documentElement,t=document.querySelector('[data-theme-toggle]');let theme=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';r.setAttribute('data-theme',theme);t.onclick=()=>{{theme=theme==='dark'?'light':'dark';r.setAttribute('data-theme',theme)}};const l=document.getElementById('lightbox'),i=document.getElementById('lightboxImage'),c=document.getElementById('close');document.querySelectorAll('.tile').forEach(b=>b.onclick=()=>{{i.src=b.dataset.image;l.classList.add('open')}});c.onclick=()=>{{l.classList.remove('open');i.src=''}};l.onclick=e=>{{if(e.target===l)c.onclick()}};}})();</script>
</body>
</html>'''
(base / 'index.html').write_text(html, encoding='utf-8')
(base / 'vercel.json').write_text('''{
  "cleanUrls": true,
  "trailingSlash": false
}
''', encoding='utf-8')
(base / 'README.md').write_text('''# Anna Heaner Site

Upload this folder to GitHub, then connect it to Vercel.

The images are optimized JPEGs inside `assets/images/`.
''', encoding='utf-8')
zip_path = Path('output/annaheaner-site-blue-lite.zip')
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
    for p in base.rglob('*'):
        if p.is_file():
            z.write(p, p.relative_to(Path('output')))
print(zip_path)
print(len(image_names))