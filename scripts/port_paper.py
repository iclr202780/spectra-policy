"""Port the main paper into the CSP-style page, excluding Related Work.

Requires PyMuPDF for authoring only. The source PDF is never modified or served.
Method prose is transcribed with math in method.html. Other prose is extracted
from recorded source rectangles; only PDF line wraps are normalized.
Run render_math.cjs afterwards to typeset the formulas into static HTML.
"""
from pathlib import Path
import re, html, hashlib, json
import pymupdf as pdf

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'SPECTRA__Force_Gated_Spectral_Diffusionfor_Robot_Manipulation.pdf'
DOC=pdf.open(SOURCE)
SOURCE_HASH=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
CONTENT=[]

def clean(s):
    # Remove only hyphenation introduced by PDF line breaks, not compound hyphens.
    for a,b in [('ex-\ntraction','extraction'),('coef-\nficients','coefficients'),
                ('expecta-\ntion','expectation'),('docu-\nments','documents')]:
        s=s.replace(a,b)
    return ' '.join(re.sub(r'-\n\s*','-',s).split())

def extract(page,y0,y1):
    return clean(DOC[page-1].get_textbox(pdf.Rect(103,y0,510,y1)))

def paragraph(*rects):
    text=' '.join(extract(*r) for r in rects)
    CONTENT.append({'type':'paragraph','source_rects':rects,'text':text})
    return '<p>'+html.escape(text)+'</p>\n'

def bullets(page,y0,y1):
    text=extract(page,y0,y1)
    items=[v.strip() for v in text.split('•') if v.strip()]
    CONTENT.append({'type':'list','source_rects':[(page,y0,y1)],'items':items})
    return '<ul>\n'+''.join('<li>'+html.escape(v)+'</li>\n' for v in items)+'</ul>\n'

def figure(name,page,rect,caption_bounds):
    dest=ROOT/'site/static/media'/f'{name}.png'
    dest.parent.mkdir(parents=True,exist_ok=True)
    pix=DOC[page-1].get_pixmap(matrix=pdf.Matrix(3,3),clip=pdf.Rect(*rect),alpha=False)
    pix.save(dest)
    caption=extract(page,*caption_bounds)
    CONTENT.append({'type':'figure','page':page,'crop':rect,'caption_bounds':caption_bounds,
                    'file':str(dest.relative_to(ROOT)),'caption':caption})
    alt=caption.split('. ')[0]
    return f'<figure><a href="static/media/{name}.png" aria-label="{html.escape(alt)} — full size"><img src="static/media/{name}.png" width="{pix.width}" height="{pix.height}" alt="{html.escape(alt)}" loading="lazy" decoding="async"></a><figcaption>{html.escape(caption)}</figcaption></figure>\n'

def section(key,title,body):
    return f'<section id="{key}" aria-labelledby="{key}-title">\n<h2 id="{key}-title">{title}</h2><hr>\n<div class="section-body">\n{body}</div>\n</section>\n'

abstract=paragraph((1,214,386))
intro=paragraph((1,440,530))+paragraph((1,534,623))+paragraph((1,628,684))
intro+=paragraph((1,688,734),(2,285,341))+bullets(2,346,424)
intro+=figure('overview',2,[108,83,504,230],[236,278])
method=(ROOT/'scripts/method.html').read_text()
CONTENT.append({'type':'method','source_rects':[(3,429,734),(4,82,735),(5,102,209)],
                'source_file':'scripts/method.html','equations':list(range(1,8))})
architecture=figure('architecture',3,[100,81,513,324],[329,380])+method
experiments=paragraph((5,239,263))+bullets(5,268,358)
simulation=paragraph((5,382,482))+'<h3>4.1.1 Baselines and Ablations</h3>\n'+paragraph((5,505,594))
simulation+=figure('simulation-results',6,[108,84,505,433],[436,458])
simulation+='<h3>4.1.2 Results and Analysis</h3>\n'+paragraph((5,616,684))+paragraph((5,688,734),(6,466,533))
normalization=paragraph((6,555,645))+figure('spectral-normalization',7,[107,119,505,214],[84,115])
interaction=paragraph((6,667,723),(7,441,508))+figure('force-bandwidth',7,[108,259,504,380],[391,433])
ablations='<h3>4.1.3 Effect of Spectral Signal-to-Noise Balancing</h3>\n'+normalization+'<h3>4.1.4 Interaction Between Force and Action Bandwidth</h3>\n'+interaction
real=paragraph((7,533,612))+'<h3>4.2.1 Experimental Setup</h3>\n'+paragraph((7,633,734))
real+=figure('real-robot-tasks',8,[108,81,504,500],[503,525])
real+='<h3>4.2.2 Results and Analysis</h3>\n'+paragraph((8,550,595))+(ROOT/'scripts/real_robot_videos.html').read_text()+figure('real-robot-results',9,[108,81,504,200],[209,241])+paragraph((8,599,689))
conclusion=paragraph((9,268,336))+paragraph((9,340,386))
ai=paragraph((10,103,171))
repro=paragraph((10,200,301))
body=''.join([
    section('abstract','Abstract',abstract),
    section('introduction','1 Introduction',intro),
    section('architecture','3 SPECTRA: Force-Aware Spectral Diffusion',architecture),
    section('experiments','4 Experiments',experiments),
    section('simulation','4.1 Simulation Experiments',simulation),
    section('ablations','Ablations',ablations),
    section('real-robot','4.2 Real-Robot Experiments',real),
    section('conclusion','5 Conclusion',conclusion),
    section('ai-use','AI Use Statement',ai),
    section('reproducibility','Reproducibility Statement',repro),
])
index=ROOT/'site/index.html';current=index.read_text()
citation=re.search(r'<section id="BibTeX".*?</section>',current,re.S).group()
current=re.sub(r'<main(?:\s[^>]*)?>.*?</main>',lambda _:'<main>\n'+body+citation+'\n</main>',current,flags=re.S)
current=current.replace('href="#paper"','href="#abstract"')
if 'static/vendor/katex/katex.min.css' not in current:
    current=current.replace('<link rel="stylesheet" href="static/style.css">','<link rel="stylesheet" href="static/vendor/katex/katex.min.css">\n  <link rel="stylesheet" href="static/style.css">')
index.write_text(current)
manifest={'source_sha256':SOURCE_HASH,'scope':'Main paper, pages 1–10; excludes Related Work, References, and Appendices. In-text citations retained. No PDF download.',
          'content':CONTENT}
(ROOT/'paper-port-manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==SOURCE_HASH
assert not list((ROOT/'site').rglob('*.pdf'))
print('Restored section-based page with complete main-paper prose, 7 equations, 5 figures, and 2 tables.')
