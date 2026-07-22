#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Trilingual (Hindi/Marathi/English) Atlas builder.
Outputs ONE self-contained HTML: embedded fonts + language switcher + render engine.
Content pages stored as dicts {topic:{hi,mr,en}, body:{hi,mr,en}}.
"""
import json

FONTS = open('fonts.css', encoding='utf-8').read()

CSS = open('css.txt', encoding='utf-8').read()

# ---- PAGE DATA ----
PAGES = []
def add(t, b, cover=False):
    PAGES.append({"topic":t, "body":b, "cover":cover})

exec(open('content.py', encoding='utf-8').read())

# Move Revision page to the end (it was added 13th)
reorder = [p for p in PAGES if 'Revision' not in p['topic'].get('en','') and 'रिवीज़न' not in p['topic'].get('hi','')]
revision_pages = [p for p in PAGES if 'Revision' in p['topic'].get('en','') or 'रिवीज़न' in p['topic'].get('hi','')]
PAGES[:] = reorder + revision_pages


# ---- BUILD ----
def hdr(t, lang):
    return ('<div class="brand-bar"><div style="display:flex;align-items:center;gap:8px"><span class="bk">K</span>'
            '<span class="bn">KNIKVIRA DIGITAL</span></div><div class="bt">'+t+'</div></div>')
def ftr(n, total, lang):
    return ('<div class="foot-bar"><div class="fl">© Knikvira Digital • knikviradigital.in</div>'
            '<div>Page '+str(n)+' / '+str(total)+' • <span class="fw">WA 8421532744</span> • Krishna Jogdand, Pune</div></div>')

def build_page(pg, idx, total):
    cls = "pg cover" if pg["cover"] else "pg"
    # placeholder divs filled by JS per language
    return ('<div class="'+cls+'" data-page="'+str(idx)+'">'
            '<span class="pg-topic"></span>'
            '<div class="watermark">KNIKVIRA<br>DIGITAL</div>'
            '<div class="content"><span class="pg-body"></span></div>'
            '<span class="pg-foot"></span></div>')

pages_html = "\n".join(build_page(p, i+1, len(PAGES)) for i,p in enumerate(PAGES))
data_json = json.dumps(PAGES, ensure_ascii=False)
total = len(PAGES)

html = '''<!doctype html>
<html lang="hi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>महाराष्ट्र भूगोल व जिल्हावार अटलास | Maharashtra Atlas | Knikvira Digital</title>
<style id="embedded-fonts">__FONTS__</style>
<style>__CSS__</style>
</head>
<body>

<div class="lang-sel">
  <span class="lt">🌐 भाषा / Language:</span>
  <button class="lang-btn active" onclick="setLang('hi')">🇮🇳 हिंदी</button>
  <button class="lang-btn" onclick="setLang('mr')">🇮🇳 मराठी</button>
  <button class="lang-btn" onclick="setLang('en')">🇬🇧 English</button>
</div>

<div id="pages">__PAGES__</div>

<script>
var DATA = __DATA__;
var LANG = 'hi';
function setLang(l){
  LANG = l;
  document.documentElement.lang = l;
  document.querySelectorAll('.lang-btn').forEach(function(b){ b.classList.remove('active'); });
  // mark active
  document.querySelectorAll('.lang-btn').forEach(function(b){
    if((l==='hi'&&b.textContent.indexOf('हिंदी')>=0)||(l==='mr'&&b.textContent.indexOf('मराठी')>=0)||(l==='en'&&b.textContent.indexOf('English')>=0)) b.classList.add('active');
  });
  DATA.forEach(function(pg,i){
    var el = document.querySelector('[data-page="'+(i+1)+'"]');
    if(!el) return;
    var topic = pg.topic[l]||pg.topic.en;
    var body = pg.body[l]||pg.body.en;
    var total = DATA.length;
    var foot = '<div class="foot-bar"><div class="fl">© Knikvira Digital • knikviradigital.in</div><div>Page '+(i+1)+' / '+total+' • <span class="fw">WA 8421532744</span> • Krishna Jogdand, Pune</div></div>';
    var head = '<div class="brand-bar"><div style="display:flex;align-items:center;gap:8px"><span class="bk">K</span><span class="bn">KNIKVIRA DIGITAL</span></div><div class="bt">'+topic+'</div></div>';
    var wm = el.querySelector('.watermark');
    el.innerHTML = head + wm.outerHTML + '<div class="content">'+body+'</div>' + foot;
  });
  try{ localStorage.setItem('knv_lang', l); }catch(e){}
}
(function(){
  try{ var s = localStorage.getItem('knv_lang'); if(s) setLang(s); else setLang('hi'); }catch(e){ setLang('hi'); }
})();
</script>
</body>
</html>'''
html = html.replace('__FONTS__', FONTS).replace('__CSS__', CSS).replace('__PAGES__', pages_html).replace('__DATA__', data_json)
open('talathi-vocabulary-master.html','w',encoding='utf-8').write(html)
print("✅ talathi-vocabulary-master.html built:", len(html), "bytes,", total, "pages")
