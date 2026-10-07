"""Génère les visuels Instagram Ashler & Manson (1080x1350) à partir d'un posts.json.

Usage : python3 outils/build.py 2026-11
  - lit 2026-11/posts.json
  - écrit 2026-11/<slug>.png et 2026-11/<slug>.jpg (le .jpg est celui envoyé à Metricool)
Prérequis (une fois par session) : cd outils && npm i @fontsource/cormorant-garamond @fontsource/manrope
"""
import base64, json, pathlib, sys
from playwright.sync_api import sync_playwright
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent
F = ROOT / 'node_modules/@fontsource'
SEAL = (ROOT / 'logo_seal.svg').read_text()
MARINE, PIERRE, LAITON, ARDOISE = '#16233B', '#E9E1D2', '#A8875A', '#56607A'

def font(fam, path, w, style='normal'):
    b = base64.b64encode((F / path).read_bytes()).decode()
    return f"@font-face{{font-family:'{fam}';src:url(data:font/woff2;base64,{b}) format('woff2');font-weight:{w};font-style:{style};}}"

FONTS = ''.join([
    font('Corm', 'cormorant-garamond/files/cormorant-garamond-latin-300-normal.woff2', 300),
    font('Corm', 'cormorant-garamond/files/cormorant-garamond-latin-500-normal.woff2', 500),
    font('Corm', 'cormorant-garamond/files/cormorant-garamond-latin-400-italic.woff2', 400, 'italic'),
    font('Man', 'manrope/files/manrope-latin-400-normal.woff2', 400),
    font('Man', 'manrope/files/manrope-latin-500-normal.woff2', 500),
])
BASE = """
*{margin:0;padding:0;box-sizing:border-box}
body{font-variant-numeric:lining-nums;width:1080px;height:1350px;overflow:hidden}
.p{width:1080px;height:1350px;padding:96px 100px 84px;display:flex;flex-direction:column}
.rub{font-family:Man;font-weight:500;font-size:27px;letter-spacing:.02em;display:flex;align-items:center;gap:22px}
.rub:before{content:'';width:56px;height:2px;background:%s}
.foot{margin-top:auto;display:flex;justify-content:space-between;align-items:flex-end}
.seal{width:150px;height:150px}.seal svg{display:block}
.tag{font-family:Man;font-size:21px;opacity:.7;text-align:right;line-height:1.5}
.src{font-family:Man;font-size:22px;line-height:1.55;opacity:.72;max-width:760px}
.body{font-family:Corm;font-weight:500;font-size:48px;line-height:1.3;max-width:880px}
""" % LAITON

def page(bg, fg, rub, body):
    return f"""<html><head><meta charset=utf-8><style>{FONTS}{BASE}</style></head><body>
<div class=p style="background:{bg};color:{fg}"><div class=rub>{rub}</div>{body}
<div class=foot><div class=seal style="color:{fg}">{SEAL}</div><div class=tag>Courtier en crédit immobilier<br>Bordeaux, depuis 2003</div></div></div></body></html>"""

# --- Les 4 gabarits (rubriques). Le texte peut contenir &nbsp; pour éviter les veuves. ---
def chiffre(p):   # fond marine. champs : grand (ex. "1 sur 2", court !), phrase, source
    return page(MARINE, PIERRE, 'Le chiffre', f"""
<div style="margin-top:140px;font-family:Corm;font-weight:300;font-size:{p.get('taille',330)}px;line-height:.85;letter-spacing:-.02em">{p['grand']}</div>
<div style="margin-top:70px;font-family:Corm;font-weight:500;font-size:60px;line-height:1.18;max-width:820px">{p['phrase']}</div>
<div class=src style="margin-top:56px">{p['source']}</div>""")

def mot(p):       # fond pierre. champs : mot, definition (ligne italique), texte
    return page(PIERRE, MARINE, 'Le mot juste', f"""
<div style="margin-top:120px;font-family:Corm;font-weight:500;font-size:{p.get('taille',300)}px;line-height:.85">{p['mot']}</div>
<div style="margin-top:40px;font-family:Corm;font-style:italic;font-size:46px;color:{ARDOISE}">{p['definition']}</div>
<div class=body style="margin-top:56px;font-size:50px;max-width:850px">{p['texte']}</div>""")

def idee(p):      # fond marine. champs : citation (idée reçue, barrée), verdict ("Faux."/"Vrai, mais…"), texte
    return page(MARINE, PIERRE, 'L’idée reçue', f"""
<div style="margin-top:120px;font-family:Corm;font-style:italic;font-size:64px;line-height:1.3;max-width:840px;opacity:.8;text-decoration:line-through;text-decoration-color:{LAITON};text-decoration-thickness:3px">« {p['citation']} »</div>
<div style="margin-top:80px;font-family:Corm;font-weight:300;font-size:210px;line-height:.9">{p['verdict']}</div>
<div class=body style="margin-top:46px">{p['texte']}</div>""")

def pierre(p):    # fond pierre. champs : titre, texte, svg (optionnel : dessin au trait marine/laiton, viewBox 0 0 880 430)
    svg = p.get('svg') or ''
    if svg:
        svg = f'<div style="margin-top:60px;width:880px;height:400px">{svg}</div>'
    return page(PIERRE, MARINE, 'Bordeaux, côté pierre', f"""{svg}
<div style="margin-top:{6 if svg else 200}px;font-family:Corm;font-weight:500;font-size:120px;line-height:1">{p['titre']}</div>
<div class=body style="margin-top:46px">{p['texte']}</div>""")

GABARITS = {'chiffre': chiffre, 'mot': mot, 'idee': idee, 'pierre': pierre}

def main(mois):
    d = ROOT.parent / mois
    posts = json.loads((d / 'posts.json').read_text())
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1350})
        for post in posts:
            pg.set_content(GABARITS[post['rubrique']](post['visuel'])); pg.wait_for_timeout(300)
            png = d / f"{post['slug']}.png"
            pg.screenshot(path=str(png))
            Image.open(png).convert('RGB').save(d / f"{post['slug']}.jpg", quality=90, optimize=True)
            print('ok', post['slug'])
        b.close()
    # planche de contrôle (à regarder avant de publier)
    ims = [Image.open(d / f"{p['slug']}.png") for p in posts]
    W = Image.new('RGB', (1080 * 2, 1350 * ((len(ims) + 1) // 2)), 'white')
    for i, im in enumerate(ims):
        W.paste(im, ((i % 2) * 1080, (i // 2) * 1350))
    W.resize((W.width // 2, W.height // 2)).save(d / '_planche.png')

if __name__ == '__main__':
    main(sys.argv[1])
