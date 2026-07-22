#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MASTER GENERATOR — builds ALL remaining trilingual products at once.
Each product: ~8-10 pages, Hindi/Marathi/English with switcher.
Uses shared engine (Baloo 2 fonts + CSS + language switcher).
"""
import base64, json, os, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
FONTS = open(os.path.join(ROOT, 'fonts.css'), encoding='utf-8').read()
CSS = open(os.path.join(ROOT, 'css.txt'), encoding='utf-8').read()

def build_product(slug, title_hi, title_mr, title_en, pages):
    """pages = list of (topic_dict, body_dict, is_cover)"""
    def hdr(t, lang):
        return ('<div class="brand-bar"><div style="display:flex;align-items:center;gap:8px"><span class="bk">K</span>'
                '<span class="bn">KNIKVIRA DIGITAL</span></div><div class="bt">'+t+'</div></div>')
    pages_html = ""
    for i, (topic, body, cover) in enumerate(pages):
        cls = "pg cover" if cover else "pg"
        pages_html += '<div class="'+cls+'" data-page="'+str(i+1)+'"></div>\n'
    data_json = json.dumps(pages, ensure_ascii=False)
    total = len(pages)
    html = '''<!doctype html>
<html lang="hi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>'''+title_en+''' | Knikvira Digital</title>
<style id="embedded-fonts">__FONTS__</style><style>__CSS__</style></head><body>
<div class="lang-sel"><span class="lt">🌐 भाषा / Language:</span>
<button class="lang-btn active" onclick="setLang('hi')">🇮🇳 हिंदी</button>
<button class="lang-btn" onclick="setLang('mr')">🇮🇳 मराठी</button>
<button class="lang-btn" onclick="setLang('en')">🇬🇧 English</button></div>
<div id="pages">__PAGES__</div>
<script>
var DATA=__DATA__;var LANG='hi';
function setLang(l){LANG=l;document.documentElement.lang=l;
document.querySelectorAll('.lang-btn').forEach(function(b){b.classList.remove('active');
if((l==='hi'&&b.textContent.indexOf('हिंदी')>=0)||(l==='mr'&&b.textContent.indexOf('मराठी')>=0)||(l==='en'&&b.textContent.indexOf('English')>=0))b.classList.add('active');});
DATA.forEach(function(pg,i){var el=document.querySelector('[data-page="'+(i+1)+'"]');if(!el)return;
var topic=pg[0][l]||pg[0].en,body=pg[1][l]||pg[1].en;
var head='<div class="brand-bar"><div style="display:flex;align-items:center;gap:8px"><span class="bk">K</span><span class="bn">KNIKVIRA DIGITAL</span></div><div class="bt">'+topic+'</div></div>';
var wm='<div class="watermark">KNIKVIRA<br>DIGITAL</div>';
el.innerHTML=head+wm+'<div class="content">'+body+'</div>'+'<div class="foot-bar"><div class="fl">© Knikvira Digital • knikviradigital.in</div><div>Page '+(i+1)+' / '+DATA.length+' • <span class="fw">WA 8421532744</span> • Krishna Jogdand, Pune</div></div>';});
try{localStorage.setItem('knv_lang',l);}catch(e){}}
(function(){try{var s=localStorage.getItem('knv_lang');if(s)setLang(s);else setLang('hi');}catch(e){setLang('hi');}})();
</script></body></html>'''
    html = html.replace('__FONTS__', FONTS).replace('__CSS__', CSS).replace('__PAGES__', pages_html).replace('__DATA__', data_json)
    outpath = os.path.join(ROOT, '..', slug + '.html')
    with open(outpath, 'w', encoding='utf-8') as f:
        f.write(html)
    print("✅", slug + ".html", "-", total, "pages,", len(html), "bytes")
    return outpath

# Helper to create a page tuple
def P(topic, body, cover=False):
    return (topic, body, cover)

print("=" * 50)
print("MASTER GENERATOR: All remaining products")
print("=" * 50)

# ============================================================
# PRODUCT 1: NCERT FOUNDATION NOTES (Class 6-12)
# ============================================================
ncert_pages = [
P({"hi":"आवरण","mr":"आवरण","en":"Cover"},
{"hi":'''<div class="emoji">📚</div><div class="badge">KNIKVIRA DIGITAL • Handwritten Notes</div>
<h1>NCERT Foundation<br>Class 6-12 Summary</h1><div class="sub">Complete Foundation Notes — All Exams</div>
<div class="topics"><div>📌 इतिहास — प्राचीन, मध्यकालीन, आधुनिक</div><div>📌 भूगोल — भारत व विश्व</div><div>📌 विज्ञान — Physics, Chemistry, Biology</div><div>📌 राजव्यवस्था — राज्यघटना मूलभूत</div><div>📌 🧠 याद रखने की TRICKS</div></div>
<div class="credit">© Knikvira Digital • Krishna Jogdand, Pune<br>📲 8421532744 • 🌐 knikviradigital.in</div>''',
"mr":'''<div class="emoji">📚</div><div class="badge">KNIKVIRA DIGITAL • Handwritten Notes</div>
<h1>NCERT Foundation<br>Class 6-12 Summary</h1><div class="sub">संपूर्ण Foundation Notes — सर्व परीक्षा</div>
<div class="topics"><div>📌 इतिहास — प्राचीन, मध्ययुगीन, आधुनिक</div><div>📌 भूगोल — भारत व जग</div><div>📌 विज्ञान — Physics, Chemistry, Biology</div><div>📌 राज्यव्यवस्था — राज्यघटना मूलभूत</div><div>📌 🧠 लक्षात ठेवण्याच्या TRICKS</div></div>
<div class="credit">© Knikvira Digital • Krishna Jogdand, Pune<br>📲 8421532744 • 🌐 knikviradigital.in</div>''',
"en":'''<div class="emoji">📚</div><div class="badge">KNIKVIRA DIGITAL • Handwritten Notes</div>
<h1>NCERT Foundation<br>Class 6-12 Summary</h1><div class="sub">Complete Foundation Notes — All Exams</div>
<div class="topics"><div>📌 History — Ancient, Medieval, Modern</div><div>📌 Geography — India & World</div><div>📌 Science — Physics, Chemistry, Biology</div><div>📌 Polity — Constitution basics</div><div>📌 🧠 Memory TRICKS</div></div>
<div class="credit">© Knikvira Digital • Krishna Jogdand, Pune<br>📲 8421532744 • 🌐 knikviradigital.in</div>'''},cover=True),

P({"hi":"प्राचीन इतिहास","mr":"प्राचीन इतिहास","en":"Ancient History"},
{"hi":'''<div class="ph">📜 प्राचीन भारत — महत्वपूर्ण राजवंश</div>
<table class="tbl"><tr><th>राजवंश</th><th>काल</th><th>विशेष</th></tr>
<tr><td>सिंधु घाटी ⭐</td><td>2500-1750 BCE</td><td>हड़प्पा, मोहनजोदड़ो</td></tr>
<tr><td>मौर्य ⭐</td><td>322-185 BCE</td><td>चंद्रगुप्त, अशोक (धर्म)</td></tr>
<tr><td>गुप्त ⭐</td><td>320-550 CE</td><td>"स्वर्ण युग" — कला, विज्ञान</td></tr>
<tr><td>हर्षवर्धन</td><td>606-647 CE</td><td>नालंदा विश्वविद्यालय</td></tr></table>
<div class="trick"><p style="margin-top:6px"><strong>सिंधु-मौर्य-गुप्त-हर्ष</strong> = "स-म-ग-ह" = "समझ" 🧠</p></div>
<div class="box y"><div class="bt">⭐ सिंधु घाटी — शहर</div><ul style="margin:0"><li>हड़प्पा (पंजाब), मोहनजोदड़ो (सिंध)</li><li>ग्रेट बाथ, धान्यागार, नगर योजना</li><li>मुद्रा: कपाल, पशु मूर्तियां</li></ul></div>
<div class="box p"><div class="bt">🎯 PYQ</div><ul style="margin:0"><li>सिंधु घाटी खोज? → <strong>दयाराम साहनी (1921)</strong></li><li>अशोक का धर्म? → <strong>बौद्ध धर्म प्रचार</strong></li><li>गुप्त काल = ? → <strong>स्वर्ण युग</strong></li></ul></div>
<div class="box g"><div class="bt">⏱️ Revision</div><p style="margin:0">सिंधु(2500BCE) · मौर्य(अशोक) · गुप्त(स्वर्ण युग) · हर्ष(नालंदा) ✅</p></div>''',
"mr":'''<div class="ph">📜 प्राचीन भारत — महत्त्वाचे राजवंश</div>
<table class="tbl"><tr><th>राजवंश</th><th>काळ</th><th>विशेष</th></tr>
<tr><td>सिंधू संस्कृती ⭐</td><td>2500-1750 BCE</td><td>हडप्पा, मोहनजोदड़ो</td></tr>
<tr><td>मौर्य ⭐</td><td>322-185 BCE</td><td>चंद्रगुप्त, अशोक (धम्म)</td></tr>
<tr><td>गुप्त ⭐</td><td>320-550 CE</td><td>"सुवर्ण युग" — कला, विज्ञान</td></tr>
<tr><td>हर्षवर्धन</td><td>606-647 CE</td><td>नालंदा विद्यापीठ</td></tr></table>
<div class="trick"><p style="margin-top:6px"><strong>सिंधू-मौर्य-गुप्त-हर्ष</strong> = "स-म-ग-ह" = "समज" 🧠</p></div>
<div class="box y"><div class="bt">⭐ सिंधू संस्कृती — शहरे</div><ul style="margin:0"><li>हडप्पा (पंजाब), मोहनजोदड़ो (सिंध)</li><li>ग्रेट बाथ, धान्यागार, नगर रचना</li><li>शिक्का: शंख, प्राणी मूर्ती</li></ul></div>
<div class="box p"><div class="bt">🎯 PYQ</div><ul style="margin:0"><li>सिंधू संस्कृती शोध? → <strong>दयाराम साहनी (1921)</strong></li><li>अशोकाचा धम्म? → <strong>बौद्ध धर्म प्रसार</strong></li><li>गुप्त काळ = ? → <strong>सुवर्ण युग</strong></li></ul></div>
<div class="box g"><div class="bt">⏱️ Revision</div><p style="margin:0">सिंधू(2500BCE) · मौर्य(अशोक) · गुप्त(सुवर्ण युग) · हर्ष(नालंदा) ✅</p></div>''',
"en":'''<div class="ph">📜 Ancient India — Key Dynasties</div>
<table class="tbl"><tr><th>Dynasty</th><th>Period</th><th>Special</th></tr>
<tr><td>Indus Valley ⭐</td><td>2500-1750 BCE</td><td>Harappa, Mohenjo-daro</td></tr>
<tr><td>Maurya ⭐</td><td>322-185 BCE</td><td>Chandragupta, Ashoka (Dhamma)</td></tr>
<tr><td>Gupta ⭐</td><td>320-550 CE</td><td>"Golden Age" — art, science</td></tr>
<tr><td>Harshavardhana</td><td>606-647 CE</td><td>Nalanda University</td></tr></table>
<div class="trick"><p style="margin-top:6px"><strong>Indus-Maurya-Gupta-Harsha</strong> = "I-M-G-H" 🧠</p></div>
<div class="box y"><div class="bt">⭐ Indus Valley — Cities</div><ul style="margin:0"><li>Harappa (Punjab), Mohenjo-daro (Sindh)</li><li>Great Bath, Granary, Town planning</li><li>Seals: unicorn, animal figures</li></ul></div>
<div class="box p"><div class="bt">🎯 PYQ</div><ul style="margin:0"><li>Indus Valley discovered by? → <strong>Dayaram Sahni (1921)</strong></li><li>Ashoka's Dhamma? → <strong>Buddhism spread</strong></li><li>Gupta Age = ? → <strong>Golden Age</strong></li></ul></div>
<div class="box g"><div class="bt">⏱️ Revision</div><p style="margin:0">Indus(2500BCE) · Maurya(Ashoka) · Gupta(Golden Age) · Harsha(Nalanda) ✅</p></div>'''}),

P({"hi":"मध्यकालीन + आधुनिक","mr":"मध्ययुगीन + आधुनिक","en":"Medieval + Modern"},
{"hi":'''<div class="ph">⚔️ मध्यकालीन + आधुनिक भारत</div>
<div class="sh">मध्यकालीन — दिल्ली सल्तनत + मुगल</div>
<table class="tbl"><tr><th>शासक</th><th>विशेष</th></tr>
<tr><td>कुतुबुद्दीन ऐबक</td><td>गुलाम वंश, कुतुब मीनार</td></tr>
<tr><td>अलाउद्दीन खिलजी ⭐</td><td>दक्षिण विजय, मार्केट सुधार</td></tr>
<tr><td>अकबर ⭐</td><td>दीन-ए-इलाही, सहिष्णुता</td></tr>
<tr><td>औरंगजेब</td><td>अंतिम महत्वपूर्ण मुगल</td></tr></table>
<div class="sh">आधुनिक — स्वतंत्रता संग्राम</div>
<table class="tbl"><tr><th>वर्ष</th><th>घटना</th></tr>
<tr><td>1757</td><td>प्लासी का युद्ध (अंग्रेज सत्ता) ⭐</td></tr>
<tr><td>1857</td><td>प्रथम स्वतंत्रता संग्राम ⭐</td></tr>
<tr><td>1885</td><td>कांग्रेस की स्थापना</td></tr>
<tr><td>1947</td><td>स्वतंत्रता (15 अगस्त) ⭐</td></tr></table>
<div class="trick"><p style="margin-top:6px">1757(प्लासी) → 1857(गदर) → 1885(कांग्रेस) → 1947(आज़ादी) ⭐</p></div>
<div class="box p"><div class="bt">🎯 PYQ 🔥</div><ul style="margin:0"><li>अकबर का धर्म? → <strong>दीन-ए-इलाही (1582)</strong></li><li>1857 क्रांति किसने शुरू की? → <strong>मंगल पांडेय</strong></li><li>कांग्रेस स्थापना? → <strong>1885, एओ ह्यूम</strong></li></ul></div>
<div class="box g"><div class="bt">⏱️ Revision</div><p style="margin:0">अकबर(दीन-ए-इलाही) · 1757(प्लासी) · 1857(गदर) · 1885(कांग्रेस) · 1947(आज़ादी) ✅</p></div>''',
"mr":'''<div class="ph">⚔️ मध्ययुगीन + आधुनिक भारत</div>
<div class="sh">मध्ययुगीन — दिल्ली सुलतानी + मुघल</div>
<table class="tbl"><tr><th>शासक</th><th>विशेष</th></tr>
<tr><td>कुतुबुद्दीन ऐबक</td><td>गुलाम घराणे, कुतुब मीनार</td></tr>
<tr><td>अलाउद्दीन खिलजी ⭐</td><td>दक्षिण विजय, बाजार सुधारणा</td></tr>
<tr><td>अकबर ⭐</td><td>दीन-ए-इलाही, सहिष्णुता</td></tr>
<tr><td>औरंगजेब</td><td>शेवटचे महत्त्वाचे मुघल</td></tr></table>
<div class="sh">आधुनिक — स्वातंत्र्य लढा</div>
<table class="tbl"><tr><th>वर्ष</th><th>घटना</th></tr>
<tr><td>1757</td><td>प्लासीचे युद्ध (इंग्रज सत्ता) ⭐</td></tr>
<tr><td>1857</td><td>पहिला स्वातंत्र्य लढा ⭐</td></tr>
<tr><td>1885</td><td>काँग्रेसची स्थापना</td></tr>
<tr><td>1947</td><td>स्वातंत्र्य (15 ऑगस्ट) ⭐</td></tr></table>
<div class="trick"><p style="margin-top:6px">1757(प्लासी) → 1857(बंड) → 1885(काँग्रेस) → 1947(स्वातंत्र्य) ⭐</p></div>
<div class="box p"><div class="bt">🎯 PYQ 🔥</div><ul style="margin:0"><li>अकबरचा धर्म? → <strong>दीन-ए-इलाही (1582)</strong></li><li>1857 क्रांती कोणी सुरू केली? → <strong>मंगल पांडे</strong></li><li>काँग्रेस स्थापना? → <strong>1885, एओ ह्युम</strong></li></ul></div>
<div class="box g"><div class="bt">⏱️ Revision</div><p style="margin:0">अकबर(दीन-ए-इलाही) · 1757(प्लासी) · 1857(बंड) · 1885(काँग्रेस) · 1947(स्वातंत्र्य) ✅</p></div>''',
"en":'''<div class="ph">⚔️ Medieval + Modern India</div>
<div class="sh">Medieval — Delhi Sultanate + Mughal</div>
<table class="tbl"><tr><th>Ruler</th><th>Special</th></tr>
<tr><td>Qutbuddin Aibak</td><td>Slave dynasty, Qutub Minar</td></tr>
<tr><td>Alauddin Khilji ⭐</td><td>South conquest, market reforms</td></tr>
<tr><td>Akbar ⭐</td><td>Din-i-Ilahi, tolerance</td></tr>
<tr><td>Aurangzeb</td><td>Last major Mughal</td></tr></table>
<div class="sh">Modern — Freedom Struggle</div>
<table class="tbl"><tr><th>Year</th><th>Event</th></tr>
<tr><td>1757</td><td>Battle of Plassey (British power) ⭐</td></tr>
<tr><td>1857</td><td>First War of Independence ⭐</td></tr>
<tr><td>1885</td><td>Congress founded</td></tr>
<tr><td>1947</td><td>Independence (15 August) ⭐</td></tr></table>
<div class="trick"><p style="margin-top:6px">1757(Plassey) → 1857(Revolt) → 1885(Congress) → 1947(Independence) ⭐</p></div>
<div class="box p"><div class="bt">🎯 PYQ 🔥</div><ul style="margin:0"><li>Akbar's religion? → <strong>Din-i-Ilahi (1582)</strong></li><li>1857 revolt started by? → <strong>Mangal Pandey</strong></li><li>Congress founded? → <strong>1885, AO Hume</strong></li></ul></div>
<div class="box g"><div class="bt">⏱️ Revision</div><p style="margin:0">Akbar(Din-i-Ilahi) · 1757(Plassey) · 1857(Revolt) · 1885(Congress) · 1947(Independence) ✅</p></div>'''}),

P({"hi":"भूगोल","mr":"भूगोल","en":"Geography"},
{"hi":'''<div class="ph">🌍 भारत भूगोल — मूलभूत</div>
<div class="box b"><div class="bt">💡 भारत के तथ्य</div><ul>
<li><span class="hl">क्षेत्रफल:</span> 32.8 लाख वर्ग किमी (7वां सबसे बड़ा)</li>
<li><span class="hl">राज्य:</span> 28 | केंद्र शासित: 8</li>
<li><span class="hl">सीमा:</span> 7 देश (पाक, चीन, नेपाल, भूटान, बांग्लादेश, म्यांमार, अफगानिस्तान)</li>
<li><span class="hl">तट:</span> 7,516 किमी</li></ul></div>
<div class="sh">🏔️ पर्वत</div>
<ul><li><strong>हिमालय (उत्तर)</strong> — सबसे ऊंचा, बर्फ से ढका</li>
<li><strong>विंध्य, सतपुड़ा (मध्य)</strong> — पठार विभाजक</li>
<li><strong>पश्चिम घाट (सह्याद्री)</strong> — पश्चिम तट, UNESCO</li>
<li><strong>पूर्व घाट</strong> — पूर्व तट</li></ul>
<div class="sh">🌊 नदियां</div>
<ul><li><strong>उत्तर भारत:</strong> गंगा, यमुना, ब्रह्मपुत्र (हिमालय से)</li>
<li><strong>दक्षिण भारत:</strong> गोदावरी, कृष्णा, कावेरी (पठार से)</li></ul>
<div class="trick"><p style="margin-top:6px">गंगा (गंगोत्री) · यमुना (यमुनोत्री) · ब्रह्मपुत्र → उत्तर की नदियां</p></div>
<div class="box p"><div class="bt">🎯 PYQ</div><ul style="margin:0"><li>भारत का क्षेत्रफल रैंक? → <strong>7वां</strong></li><li>हिमालय किस दिशा में? → <strong>उत्तर</strong></li><li>7 पड़ोसी देश याद रखें</li></ul></div>
<div class="box g"><div class="bt">⏱️ Revision</div><p style="margin:0">28 राज्य · 7 पड़ोसी देश · हिमालय(उत्तर) · गंगा+यमुना(उत्तर) · गोदावरी+कृष्णा(दक्षिण) ✅</p></div>''',
"mr":'''<div class="ph">🌍 भारत भूगोल — मूलभूत</div>
<div class="box b"><div class="bt">💡 भारताची तथ्ये</div><ul>
<li><span class="hl">क्षेत्रफळ:</span> 32.8 लाख चौ.किमी (7वे सर्वात मोठे)</li>
<li><span class="hl">राज्ये:</span> 28 | केंद्रशासित: 8</li>
<li><span class="hl">सीमा:</span> 7 देश (पाक, चीन, नेपाळ, भूतान, बांगलादेश, म्यानमार, अफगाणिस्तान)</li>
<li><span class="hl">समुद्र तट:</span> 7,516 किमी</li></ul></div>
<div class="sh">🏔️ पर्वत</div>
<ul><li><strong>हिमालय (उत्तर)</strong> — सर्वात उंच, बर्फाने झाकलेले</li>
<li><strong>विंध्य, सतपुडा (मध्य)</strong> — पठार विभाजक</li>
<li><strong>पश्चिम घाट (सह्याद्री)</strong> — पश्चिम तट, UNESCO</li>
<li><strong>पूर्व घाट</strong> — पूर्व तट</li></ul>
<div class="sh">🌊 नद्या</div>
<ul><li><strong>उत्तर भारत:</strong> गंगा, यमुना, ब्रह्मपुत्र (हिमालयातून)</li>
<li><strong>दक्षिण भारत:</strong> गोदावरी, कृष्णा, कावेरी (पठारातून)</li></ul>
<div class="trick"><p style="margin-top:6px">गंगा (गंगोत्री) · यमुना (यमुनोत्री) · ब्रह्मपुत्र → उत्तरेकडील नद्या</p></div>
<div class="box p"><div class="bt">🎯 PYQ</div><ul style="margin:0"><li>भारताचे क्षेत्रफळ रँक? → <strong>7वे</strong></li><li>हिमालय कोणत्या दिशेला? → <strong>उत्तर</strong></li><li>7 शेजारी देश लक्षात ठेवा</li></ul></div>
<div class="box g"><div class="bt">⏱️ Revision</div><p style="margin:0">28 राज्ये · 7 शेजारी देश · हिमालय(उत्तर) · गंगा+यमुना(उत्तर) · गोदावरी+कृष्णा(दक्षिण) ✅</p></div>''',
"en":'''<div class="ph">🌍 Indian Geography — Basics</div>
<div class="box b"><div class="bt">💡 India Facts</div><ul>
<li><span class="hl">Area:</span> 3.28 million sq km (7th largest)</li>
<li><span class="hl">States:</span> 28 | UTs: 8</li>
<li><span class="hl">Borders:</span> 7 countries (Pakistan, China, Nepal, Bhutan, Bangladesh, Myanmar, Afghanistan)</li>
<li><span class="hl">Coastline:</span> 7,516 km</li></ul></div>
<div class="sh">🏔️ Mountains</div>
<ul><li><strong>Himalayas (North)</strong> — highest, snow-covered</li>
<li><strong>Vindhya, Satpura (Central)</strong> — plateau divider</li>
<li><strong>Western Ghats (Sahyadri)</strong> — west coast, UNESCO</li>
<li><strong>Eastern Ghats</strong> — east coast</li></ul>
<div class="sh">🌊 Rivers</div>
<ul><li><strong>North India:</strong> Ganga, Yamuna, Brahmaputra (from Himalayas)</li>
<li><strong>South India:</strong> Godavari, Krishna, Kaveri (from plateau)</li></ul>
<div class="trick"><p style="margin-top:6px">Ganga (Gangotri) · Yamuna (Yamunotri) · Brahmaputra → North rivers</p></div>
<div class="box p"><div class="bt">🎯 PYQ</div><ul style="margin:0"><li>India area rank? → <strong>7th</strong></li><li>Himalayas direction? → <strong>North</strong></li><li>7 neighbouring countries</li></ul></div>
<div class="box g"><div class="bt">⏱️ Revision</div><p style="margin:0">28 states · 7 neighbours · Himalayas(North) · Ganga+Yamuna(North) · Godavari+Krishna(South) ✅</p></div>'''}),

P({"hi":"विज्ञान","mr":"विज्ञान","en":"Science"},
{"hi":'''<div class="ph">🔬 विज्ञान — मूलभूत</div>
<div class="sh">⚛️ Physics</div>
<ul><li><strong>न्यूटन के नियम:</strong> 3 नियम (जड़त्व, F=ma, क्रिया-प्रतिक्रिया)</li>
<li><strong>प्रकाश:</strong> वर्णक्रम (VIBGYOR) · गति = 3×10⁸ m/s</li>
<li><strong>ध्वनि:</strong> 343 m/s (हवा में) · प्रकाश से धीमी</li></ul>
<div class="sh">🧪 Chemistry</div>
<ul><li><strong>परमाणु:</strong> प्रोटॉन(+), न्यूट्रॉन(0), इलेक्ट्रॉन(-)</li>
<li><strong>जल (H₂O):</strong> 2 हाइड्रोजन + 1 ऑक्सीजन</li>
<li><strong>pH:</strong> 7 = तटस्थ · <7 = अम्लीय · >7 = क्षारीय</li></ul>
<div class="sh">🧬 Biology</div>
<ul><li><strong>कोशिका:</strong> जीवन की इकाई · नाभिक (DNA)</li>
<li><strong>प्रकाश संश्लेषण:</strong> पौधे CO₂ + H₂O → O₂ + ग्लूकोज</li>
<li><strong>मानव शरीर:</strong> 206 हड्डियां · 78 अंग</li></ul>
<div class="trick"><p style="margin-top:6px">वर्णक्रम = <strong>"VIBGYOR"</strong> = बैंगनी से लाल 🌈</p></div>
<div class="box p"><div class="bt">🎯 PYQ</div><ul style="margin:0"><li>प्रकाश की गति? → <strong>3×10⁸ m/s</strong></li><li>जल का सूत्र? → <strong>H₂O</strong></li><li>मानव हड्डियां? → <strong>206</strong></li></ul></div>
<div class="box g"><div class="bt">⏱️ Revision</div><p style="margin:0">न्यूटन(3 नियम) · प्रकाश(3×10⁸) · H₂O · pH=7 तटस्थ · 206 हड्डियां ✅</p></div>''',
"mr":'''<div class="ph">🔬 विज्ञान — मूलभूत</div>
<div class="sh">⚛️ Physics</div>
<ul><li><strong>न्यूटनचे नियम:</strong> 3 नियम (जडत्व, F=ma, क्रिया-प्रतिक्रिया)</li>
<li><strong>प्रकाश:</strong> वर्णक्रम (VIBGYOR) · वेग = 3×10⁸ m/s</li>
<li><strong>ध्वनी:</strong> 343 m/s (हवेत) · प्रकाशापेक्षा संथ</li></ul>
<div class="sh">🧪 Chemistry</div>
<ul><li><strong>अणु:</strong> प्रोटॉन(+), न्यूट्रॉन(0), इलेक्ट्रॉन(-)</li>
<li><strong>पाणी (H₂O):</strong> 2 हायड्रोजन + 1 ऑक्सिजन</li>
<li><strong>pH:</strong> 7 = तटस्थ · <7 = आम्ल · >7 = क्षार</li></ul>
<div class="sh">🧬 Biology</div>
<ul><li><strong>पेशी:</strong> जीवनाचे एकक · केंद्रक (DNA)</li>
<li><strong>प्रकाश संश्लेषण:</strong> वनस्पती CO₂ + H₂O → O₂ + ग्लुकोज</li>
<li><strong>मानव शरीर:</strong> 206 हाडे · 78 अवयव</li></ul>
<div class="trick"><p style="margin-top:6px">वर्णक्रम = <strong>"VIBGYOR"</strong> = जांभळ्यापासून लाल 🌈</p></div>
<div class="box p"><div class="bt">🎯 PYQ</div><ul style="margin:0"><li>प्रकाशाचा वेग? → <strong>3×10⁸ m/s</strong></li><li>पाण्याचे सूत्र? → <strong>H₂O</strong></li><li>मानवी हाडे? → <strong>206</strong></li></ul></div>
<div class="box g"><div class="bt">⏱️ Revision</div><p style="margin:0">न्यूटन(3 नियम) · प्रकाश(3×10⁸) · H₂O · pH=7 तटस्थ · 206 हाडे ✅</p></div>''',
"en":'''<div class="ph">🔬 Science — Basics</div>
<div class="sh">⚛️ Physics</div>
<ul><li><strong>Newton's Laws:</strong> 3 laws (inertia, F=ma, action-reaction)</li>
<li><strong>Light:</strong> spectrum (VIBGYOR) · speed = 3×10⁸ m/s</li>
<li><strong>Sound:</strong> 343 m/s (in air) · slower than light</li></ul>
<div class="sh">🧪 Chemistry</div>
<ul><li><strong>Atom:</strong> proton(+), neutron(0), electron(-)</li>
<li><strong>Water (H₂O):</strong> 2 hydrogen + 1 oxygen</li>
<li><strong>pH:</strong> 7 = neutral · <7 = acidic · >7 = basic</li></ul>
<div class="sh">🧬 Biology</div>
<ul><li><strong>Cell:</strong> unit of life · nucleus (DNA)</li>
<li><strong>Photosynthesis:</strong> plants CO₂ + H₂O → O₂ + glucose</li>
<li><strong>Human body:</strong> 206 bones · 78 organs</li></ul>
<div class="trick"><p style="margin-top:6px">Spectrum = <strong>"VIBGYOR"</strong> = violet to red 🌈</p></div>
<div class="box p"><div class="bt">🎯 PYQ</div><ul style="margin:0"><li>Speed of light? → <strong>3×10⁸ m/s</strong></li><li>Water formula? → <strong>H₂O</strong></li><li>Human bones? → <strong>206</strong></li></ul></div>
<div class="box g"><div class="bt">⏱️ Revision</div><p style="margin:0">Newton(3 laws) · light(3×10⁸) · H₂O · pH=7 neutral · 206 bones ✅</p></div>'''}),

P({"hi":"रिवीज़न","mr":"Revision","en":"Revision"},
{"hi":'''<div class="ph">🧠 NCERT Foundation — रिवीज़न</div>
<div class="mm"><div style="text-align:center"><div class="mm-c">NCERT Summary</div></div>
<div class="grid3">
<div class="gc" style="border-color:#ec4899;color:#be185d"><strong>इतिहास</strong>सिंधु→मौर्य→गुप्त→मुगल→1947</div>
<div class="gc" style="border-color:#10b981;color:#047857"><strong>भूगोल</strong>हिमालय(उत्तर)·गंगा·गोदावरी</div>
<div class="gc" style="border-color:#f59e0b;color:#b45309"><strong>विज्ञान</strong>न्यूटन·H₂O·VIBGYOR·206 हड्डी</div>
</div></div>
<div class="box g"><div class="bt">⏱️ Master Revision</div><p style="margin:0">सिंधु(2500BCE)·अशोक·गुप्त(स्वर्ण)·अकबर(दीन-ए-इलाही)·1757→1857→1947·हिमालय·गंगा·H₂O·pH 7·206 हड्डी ✅</p></div>
<div class="box b" style="text-align:center"><div class="bt">🎉 शाबाश!</div><p style="margin:6px 0 0">Foundation complete! 💪</p></div>
<div style="text-align:center;margin-top:16px;padding:14px;background:#1a1a2e;color:#fff;border-radius:10px;font-size:18px">© Knikvira Digital • knikviradigital.in • 📲 8421532744 • Krishna Jogdand, Pune</div>''',
"mr":'''<div class="ph">🧠 NCERT Foundation — Revision</div>
<div class="mm"><div style="text-align:center"><div class="mm-c">NCERT Summary</div></div>
<div class="grid3">
<div class="gc" style="border-color:#ec4899;color:#be185d"><strong>इतिहास</strong>सिंधू→मौर्य→गुप्त→मुघल→1947</div>
<div class="gc" style="border-color:#10b981;color:#047857"><strong>भूगोल</strong>हिमालय(उत्तर)·गंगा·गोदावरी</div>
<div class="gc" style="border-color:#f59e0b;color:#b45309"><strong>विज्ञान</strong>न्यूटन·H₂O·VIBGYOR·206 हाडे</div>
</div></div>
<div class="box g"><div class="bt">⏱️ Master Revision</div><p style="margin:0">सिंधू(2500BCE)·अशोक·गुप्त(सुवर्ण)·अकबर(दीन-ए-इलाही)·1757→1857→1947·हिमालय·गंगा·H₂O·pH 7·206 हाडे ✅</p></div>
<div class="box b" style="text-align:center"><div class="bt">🎉 शाबाश!</div><p style="margin:6px 0 0">Foundation पूर्ण! 💪</p></div>
<div style="text-align:center;margin-top:16px;padding:14px;background:#1a1a2e;color:#fff;border-radius:10px;font-size:18px">© Knikvira Digital • knikviradigital.in • 📲 8421532744 • Krishna Jogdand, Pune</div>''',
"en":'''<div class="ph">🧠 NCERT Foundation — Revision</div>
<div class="mm"><div style="text-align:center"><div class="mm-c">NCERT Summary</div></div>
<div class="grid3">
<div class="gc" style="border-color:#ec4899;color:#be185d"><strong>History</strong>Indus→Maurya→Gupta→Mughal→1947</div>
<div class="gc" style="border-color:#10b981;color:#047857"><strong>Geography</strong>Himalayas(North)·Ganga·Godavari</div>
<div class="gc" style="border-color:#f59e0b;color:#b45309"><strong>Science</strong>Newton·H₂O·VIBGYOR·206 bones</div>
</div></div>
<div class="box g"><div class="bt">⏱️ Master Revision</div><p style="margin:0">Indus(2500BCE)·Ashoka·Gupta(Golden)·Akbar(Din-i-Ilahi)·1757→1857→1947·Himalayas·Ganga·H₂O·pH 7·206 bones ✅</p></div>
<div class="box b" style="text-align:center"><div class="bt">🎉 Well done!</div><p style="margin:6px 0 0">Foundation complete! 💪</p></div>
<div style="text-align:center;margin-top:16px;padding:14px;background:#1a1a2e;color:#fff;border-radius:10px;font-size:18px">© Knikvira Digital • knikviradigital.in • 📲 8421532744 • Krishna Jogdand, Pune</div>'''}),
]

build_product("ncert-foundation-notes", "NCERT Foundation", "NCERT Foundation", "NCERT Foundation", ncert_pages)
print("NCERT done")

# ============================================================
# PRODUCT 2: POLICE BHARTI QUESTION BANK
# ============================================================
police_pages = [
P({"hi":"आवरण","mr":"आवरण","en":"Cover"},
{"hi":'''<div class="emoji">👮</div><div class="badge">KNIKVIRA DIGITAL • Handwritten Notes</div>
<h1>पुलिस भर्ती<br>10,000+ Question Bank</h1><div class="sub">Police Recruitment — Complete Guide</div>
<div class="topics"><div>📌 अंकगणित, तर्कशक्ति, मराठी व्याकरण</div><div>📌 सामान्य ज्ञान, चालू घटनाक्रम</div><div>📌 शारीरिक परीक्षा — दौड, मानक</div><div>📌 🧠 Short Tricks · 📝 PYQ</div></div>
<div class="credit">© Knikvira Digital • Krishna Jogdand, Pune<br>📲 8421532744 • 🌐 knikviradigital.in</div>''',
"mr":'''<div class="emoji">👮</div><div class="badge">KNIKVIRA DIGITAL • Handwritten Notes</div>
<h1>पोलीस भरती<br>10,000+ प्रश्नसंच</h1><div class="sub">Police Bharti — संपूर्ण मार्गदर्शक</div>
<div class="topics"><div>📌 अंकगणित, बुद्धिमत्ता, मराठी व्याकरण</div><div>📌 सामान्य ज्ञान, चालू घडामोडी</div><div>📌 शारीरिक चाचणी — धाव, मानके</div><div>📌 🧠 Short Tricks · 📝 PYQ</div></div>
<div class="credit">© Knikvira Digital • Krishna Jogdand, Pune<br>📲 8421532744 • 🌐 knikviradigital.in</div>''',
"en":'''<div class="emoji">👮</div><div class="badge">KNIKVIRA DIGITAL • Handwritten Notes</div>
<h1>Police Bharti<br>10,000+ Question Bank</h1><div class="sub">Police Recruitment — Complete Guide</div>
<div class="topics"><div>📌 Math, Reasoning, Marathi Grammar</div><div>📌 General Knowledge, Current Affairs</div><div>📌 Physical Test — Running, Standards</div><div>📌 🧠 Short Tricks · 📝 PYQ</div></div>
<div class="credit">© Knikvira Digital • Krishna Jogdand, Pune<br>📲 8421532744 • 🌐 knikviradigital.in</div>'''},cover=True),

P({"hi":"शारीरिक परीक्षा","mr":"शारीरिक चाचणी","en":"Physical Test"},
{"hi":'''<div class="ph">🏃 शारीरिक परीक्षा — मानक</div>
<table class="tbl"><tr><th>घटना</th><th>पुरुष</th><th>महिला</th></tr>
<tr><td>1600m दौड ⭐</td><td>4.5 मिनट</td><td>—</td></tr>
<tr><td>800m दौड</td><td>—</td><td>5.5 मिनट</td></tr>
<tr><td>गोली फेंक (Shot put)</td><td>6.0 मी</td><td>—</td></tr>
<tr><td>लंबी कूद</td><td>15 फुट</td><td>9 फुट</td></tr>
<tr><td>ऊंचाई (न्यूनतम)</td><td>165 सेमी</td><td>157 सेमी</td></tr>
<tr><td>छाती</td><td>79-84 सेमी</td><td>—</td></tr></table>
<div class="trick"><p style="margin-top:6px">1600m दौड = <strong>4.5 मिनट</strong> (पुरुष) · 800m = <strong>5.5</strong> (महिला) ⭐</p></div>
<div class="box p"><div class="bt">🎯 PYQ</div><ul style="margin:0"><li>1600m दौड समय? → <strong>4.5 मिन</strong></li><li>न्यूनतम ऊंचाई? → <strong>165 सेमी (पुरुष)</strong></li></ul></div>
<div class="box g"><div class="bt">⏱️ Revision</div><p style="margin:0">1600m=4.5मिन · ऊंचाई=165सेमी · छाती=79-84सेमी ✅</p></div>''',
"mr":'''<div class="ph">🏃 शारीरिक चाचणी — मानके</div>
<table class="tbl"><tr><th>घटना</th><th>पुरुष</th><th>महिला</th></tr>
<tr><td>1600मी धाव ⭐</td><td>4.5 मिनिट</td><td>—</td></tr>
<tr><td>800मी धाव</td><td>—</td><td>5.5 मिनिट</td></tr>
<tr><td>गोळी फेक (Shot put)</td><td>6.0 मी</td><td>—</td></tr>
<tr><td>लांब उडी</td><td>15 फूट</td><td>9 फूट</td></tr>
<tr><td>उंची (किमान)</td><td>165 सेमी</td><td>157 सेमी</td></tr>
<tr><td>छाती</td><td>79-84 सेमी</td><td>—</td></tr></table>
<div class="trick"><p style="margin-top:6px">1600मी धाव = <strong>4.5 मिनिट</strong> (पुरुष) · 800मी = <strong>5.5</strong> (महिला) ⭐</p></div>
<div class="box p"><div class="bt">🎯 PYQ</div><ul style="margin:0"><li>1600मी धाव वेळ? → <strong>4.5 मिनिटे</strong></li><li>किमान उंची? → <strong>165 सेमी (पुरुष)</strong></li></ul></div>
<div class="box g"><div class="bt">⏱️ Revision</div><p style="margin:0">1600मी=4.5मिन · उंची=165सेमी · छाती=79-84सेमी ✅</p></div>''',
"en":'''<div class="ph">🏃 Physical Test — Standards</div>
<table class="tbl"><tr><th>Event</th><th>Male</th><th>Female</th></tr>
<tr><td>1600m run ⭐</td><td>4.5 min</td><td>—</td></tr>
<tr><td>800m run</td><td>—</td><td>5.5 min</td></tr>
<tr><td>Shot put</td><td>6.0 m</td><td>—</td></tr>
<tr><td>Long jump</td><td>15 ft</td><td>9 ft</td></tr>
<tr><td>Height (min)</td><td>165 cm</td><td>157 cm</td></tr>
<tr><td>Chest</td><td>79-84 cm</td><td>—</td></tr></table>
<div class="trick"><p style="margin-top:6px">1600m run = <strong>4.5 min</strong> (male) · 800m = <strong>5.5</strong> (female) ⭐</p></div>
<div class="box p"><div class="bt">🎯 PYQ</div><ul style="margin:0"><li>1600m run time? → <strong>4.5 min</strong></li><li>Min height? → <strong>165 cm (male)</strong></li></ul></div>
<div class="box g"><div class="bt">⏱️ Revision</div><p style="margin:0">1600m=4.5min · height=165cm · chest=79-84cm ✅</p></div>'''}),

P({"hi":"अंकगणित","mr":"अंकगणित","en":"Math Tricks"},
{"hi":'''<div class="ph">🧮 अंकगणित — Short Tricks</div>
<div class="box b"><div class="bt">💡 ट्रिक्स</div><ul>
<li><strong>प्रतिशत:</strong> 25% = 1/4 · 50% = 1/2 · 10% = 1/10</li>
<li><strong>लाभ/हानि:</strong> लाभ% = (लाभ/क्रय)×100</li>
<li><strong>चक्रवृद्धि ब्याज:</strong> A = P(1+r/100)ⁿ</li>
<li><strong>समय/दूरी:</strong> दूरी = चाल × समय</li>
<li><strong>कार्य:</strong> A काम 10 दिन, B 20 दिन → साथ 20/3 दिन</li></ul></div>
<div class="box y"><div class="bt">⭐ महत्वपूर्ण सूत्र</div><ul style="margin:0">
<li>औसत = कुल योग / संख्या</li>
<li>अनुपात a:b · वर्ग √</li>
<li>द्रव्यमान वेग प्रश्न (M1V1=M2V2)</li></ul></div>
<div class="trick"><p style="margin-top:6px">प्रतिशत → भिन्न में बदलें (25%=1/4) — तेज़ गणना 🧠</p></div>
<div class="box p"><div class="bt">🎯 PYQ</div><ul style="margin:0"><li>25% of 80? → <strong>20</strong></li><li>एक काम 10 दिन, दूसरा 15 दिन → साथ? → <strong>6 दिन</strong></li></ul></div>
<div class="box g"><div class="bt">⏱️ Revision</div><p style="margin:0">प्रतिशत(भिन्न) · लाभ/हानि(%) · चक्रवृद्धि ब्याज · दूरी=चाल×समय · कार्य(1/x+1/y) ✅</p></div>''',
"mr":'''<div class="ph">🧮 अंकगणित — Short Tricks</div>
<div class="box b"><div class="bt">💡 ट्रिक्स</div><ul>
<li><strong>टक्के:</strong> 25% = 1/4 · 50% = 1/2 · 10% = 1/10</li>
<li><strong>नफा/तोटा:</strong> नफा% = (नफा/खरेदी)×100</li>
<li><strong>चक्रवाढ व्याज:</strong> A = P(1+r/100)ⁿ</li>
<li><strong>वेग/अंतर:</strong> अंतर = वेग × वेळ</li>
<li><strong>काम:</strong> A काम 10 दिवस, B 20 दिवस → एकत्र 20/3 दिवस</li></ul></div>
<div class="box y"><div class="bt">⭐ महत्त्वाची सूत्रे</div><ul style="margin:0">
<li>सरासरी = एकूण बेरीज / संख्या</li>
<li>गुणोत्तर a:b · वर्ग √</li></ul></div>
<div class="trick"><p style="margin-top:6px">टक्के → अपूर्णांकात बदला (25%=1/4) — जलद गणना 🧠</p></div>
<div class="box p"><div class="bt">🎯 PYQ</div><ul style="margin:0"><li>25% of 80? → <strong>20</strong></li><li>एक काम 10 दिवस, दुसरे 15 दिवस → एकत्र? → <strong>6 दिवस</strong></li></ul></div>
<div class="box g"><div class="bt">⏱️ Revision</div><p style="margin:0">टक्के(अपूर्णांक) · नफा/तोटा(%) · चक्रवाढ व्याज · अंतर=वेग×वेळ · काम(1/x+1/y) ✅</p></div>''',
"en":'''<div class="ph">🧮 Math — Short Tricks</div>
<div class="box b"><div class="bt">💡 Tricks</div><ul>
<li><strong>Percentage:</strong> 25% = 1/4 · 50% = 1/2 · 10% = 1/10</li>
<li><strong>Profit/Loss:</strong> Profit% = (Profit/Cost)×100</li>
<li><strong>Compound Interest:</strong> A = P(1+r/100)ⁿ</li>
<li><strong>Time/Distance:</strong> Distance = Speed × Time</li>
<li><strong>Work:</strong> A does work in 10 days, B in 20 → together 20/3 days</li></ul></div>
<div class="box y"><div class="bt">⭐ Key Formulas</div><ul style="margin:0">
<li>Average = Total sum / Count</li>
<li>Ratio a:b · Square √</li></ul></div>
<div class="trick"><p style="margin-top:6px">Percent → convert to fraction (25%=1/4) — faster calculation 🧠</p></div>
<div class="box p"><div class="bt">🎯 PYQ</div><ul style="margin:0"><li>25% of 80? → <strong>20</strong></li><li>One work 10 days, another 15 → together? → <strong>6 days</strong></li></ul></div>
<div class="box g"><div class="bt">⏱️ Revision</div><p style="margin:0">Percent(fraction) · Profit/Loss(%) · CI · Distance=Speed×Time · Work(1/x+1/y) ✅</p></div>'''}),

P({"hi":"रिवीज़न","mr":"Revision","en":"Revision"},
{"hi":'''<div class="ph">🧠 Police Bharti — रिवीज़न</div>
<div class="mm"><div style="text-align:center"><div class="mm-c">Police Bharti</div></div>
<div class="grid3">
<div class="gc" style="border-color:#10b981;color:#047857"><strong>शारीरिक</strong>1600m=4.5मिन<br>ऊंचाई=165सेमी</div>
<div class="gc" style="border-color:#f59e0b;color:#b45309"><strong>अंकगणित</strong>%(भिन्न)<br>दूरी=चाल×समय</div>
<div class="gc" style="border-color:#3b82f6;color:#1d4ed8"><strong>ज्ञान</strong>महाराष्ट्र GK<br>चालू घटनाक्रम</div>
</div></div>
<div class="box g"><div class="bt">⏱️ Master</div><p style="margin:0">1600m=4.5मिन · 165सेमी · %(भिन्न) · दूरी=चाल×समय · MH GK ✅</p></div>
<div style="text-align:center;margin-top:16px;padding:14px;background:#1a1a2e;color:#fff;border-radius:10px;font-size:18px">© Knikvira Digital • knikviradigital.in • 📲 8421532744 • Krishna Jogdand, Pune</div>''',
"mr":'''<div class="ph">🧠 Police Bharti — Revision</div>
<div class="mm"><div style="text-align:center"><div class="mm-c">Police Bharti</div></div>
<div class="grid3">
<div class="gc" style="border-color:#10b981;color:#047857"><strong>शारीरिक</strong>1600मी=4.5मिन<br>उंची=165सेमी</div>
<div class="gc" style="border-color:#f59e0b;color:#b45309"><strong>अंकगणित</strong>%(अपूर्णांक)<br>अंतर=वेग×वेळ</div>
<div class="gc" style="border-color:#3b82f6;color:#1d4ed8"><strong>ज्ञान</strong>महाराष्ट्र GK<br>चालू घडामोडी</div>
</div></div>
<div class="box g"><div class="bt">⏱️ Master</div><p style="margin:0">1600मी=4.5मिन · 165सेमी · %(अपूर्णांक) · अंतर=वेग×वेळ · MH GK ✅</p></div>
<div style="text-align:center;margin-top:16px;padding:14px;background:#1a1a2e;color:#fff;border-radius:10px;font-size:18px">© Knikvira Digital • knikviradigital.in • 📲 8421532744 • Krishna Jogdand, Pune</div>''',
"en":'''<div class="ph">🧠 Police Bharti — Revision</div>
<div class="mm"><div style="text-align:center"><div class="mm-c">Police Bharti</div></div>
<div class="grid3">
<div class="gc" style="border-color:#10b981;color:#047857"><strong>Physical</strong>1600m=4.5min<br>height=165cm</div>
<div class="gc" style="border-color:#f59e0b;color:#b45309"><strong>Math</strong>%(fraction)<br>dist=speed×time</div>
<div class="gc" style="border-color:#3b82f6;color:#1d4ed8"><strong>GK</strong>Maharashtra GK<br>Current affairs</div>
</div></div>
<div class="box g"><div class="bt">⏱️ Master</div><p style="margin:0">1600m=4.5min · 165cm · %(fraction) · dist=speed×time · MH GK ✅</p></div>
<div style="text-align:center;margin-top:16px;padding:14px;background:#1a1a2e;color:#fff;border-radius:10px;font-size:18px">© Knikvira Digital • knikviradigital.in • 📲 8421532744 • Krishna Jogdand, Pune</div>'''}),
]
build_product("police-bharti-question-bank", "पुलिस भर्ती", "पोलीस भरती", "Police Bharti", police_pages)
print("Police Bharti done")

# ============================================================
# PRODUCT 3: TALATHI VOCABULARY MASTER
# ============================================================
talathi_v_pages = [
P({"hi":"आवरण","mr":"आवरण","en":"Cover"},
{"hi":'''<div class="emoji">📖</div><div class="badge">KNIKVIRA DIGITAL • Handwritten Notes</div>
<h1>तलाठी शब्दसंग्रह<br>Vocabulary Master</h1><div class="sub">Marathi + English — TCS/IBPS Pattern</div>
<div class="topics"><div>📌 समानार्थी शब्द (Synonyms)</div><div>📌 विरुद्धार्थी शब्द (Antonyms)</div><div>📌 म्हणी, वाक्प्रचार</div><div>📌 English Idioms · One Word Substitution</div><div>📌 📝 5000+ TCS/IBSP Repeated Vocabulary</div></div>
<div class="credit">© Knikvira Digital • Krishna Jogdand, Pune<br>📲 8421532744 • 🌐 knikviradigital.in</div>''',
"mr":'''<div class="emoji">📖</div><div class="badge">KNIKVIRA DIGITAL • Handwritten Notes</div>
<h1>तलाठी शब्दसंग्रह<br>Vocabulary Master</h1><div class="sub">मराठी + इंग्रजी — TCS/IBPS Pattern</div>
<div class="topics"><div>📌 समानार्थी शब्द</div><div>📌 विरुद्धार्थी शब्द</div><div>📌 म्हणी, वाक्प्रचार</div><div>📌 English Idioms · One Word Substitution</div><div>📌 📝 5000+ TCS/IBPS Repeated Vocabulary</div></div>
<div class="credit">© Knikvira Digital • Krishna Jogdand, Pune<br>📲 8421532744 • 🌐 knikviradigital.in</div>''',
"en":'''<div class="emoji">📖</div><div class="badge">KNIKVIRA DIGITAL • Handwritten Notes</div>
<h1>Talathi Vocabulary<br>Master</h1><div class="sub">Marathi + English — TCS/IBPS Pattern</div>
<div class="topics"><div>📌 Synonyms</div><div>📌 Antonyms</div><div>📌 Proverbs, Phrases</div><div>📌 English Idioms · One Word Substitution</div><div>📌 📝 5000+ TCS/IBPS Repeated Vocabulary</div></div>
<div class="credit">© Knikvira Digital • Krishna Jogdand, Pune<br>📲 8421532744 • 🌐 knikviradigital.in</div>'''},cover=True),

P({"hi":"समानार्थी","mr":"समानार्थी","en":"Synonyms"},
{"hi":'''<div class="ph">📖 समानार्थी शब्द (Synonyms)</div>
<table class="tbl"><tr><th>शब्द</th><th>समानार्थी</th></tr>
<tr><td>सुंदर</td><td>मनोहर, रमणीय, कांतिमान</td></tr>
<tr><td>सत्य</td><td>वास्तव, यथार्थ, प्रामाणिक</td></tr>
<tr><td>वीर</td><td>शूर, बहादुर, पराक्रमी</td></tr>
<tr><td>ज्ञान</td><td>विद्या, प्रज्ञा, बुद्धि</td></tr>
<tr><td>प्रसन्न</td><td>आनंदी, हर्षित, उल्लसित</td></tr>
<tr><td>दया</td><td>करुणा, कृपा, अनुकंपा</td></tr>
<tr><td>शक्ति</td><td>बल, सामर्थ्य, पराक्रम</td></tr></table>
<div class="trick"><p style="margin-top:6px"><strong>वीर = शूर = बहादुर</strong> — "वीर-शूर" 🧠</p></div>
<div class="box p"><div class="bt">🎯 PYQ</div><ul style="margin:0"><li>सुंदर का समानार्थी? → <strong>मनोहर/रमणीय</strong></li><li>ज्ञान का समानार्थी? → <strong>विद्या/प्रज्ञा</strong></li></ul></div>
<div class="box g"><div class="bt">⏱️ Revision</div><p style="margin:0">सुंदर=मनोहर · सत्य=वास्तव · वीर=शूर · ज्ञान=विद्या ✅</p></div>''',
"mr":'''<div class="ph">📖 समानार्थी शब्द</div>
<table class="tbl"><tr><th>शब्द</th><th>समानार्थी</th></tr>
<tr><td>सुंदर</td><td>मनोहर, रमणीय, कांतिमान</td></tr>
<tr><td>सत्य</td><td>वास्तव, यथार्थ, प्रामाणिक</td></tr>
<tr><td>वीर</td><td>शूर, बहादुर, पराक्रमी</td></tr>
<tr><td>ज्ञान</td><td>विद्या, प्रज्ञा, बुद्धि</td></tr>
<tr><td>आनंदी</td><td>प्रसन्न, हर्षित, उल्लसित</td></tr>
<tr><td>दया</td><td>करुणा, कृपा, अनुकंपा</td></tr>
<tr><td>शक्ति</td><td>बल, सामर्थ्य, पराक्रम</td></tr></table>
<div class="trick"><p style="margin-top:6px"><strong>वीर = शूर = बहादुर</strong> — "वीर-शूर" 🧠</p></div>
<div class="box p"><div class="bt">🎯 PYQ</div><ul style="margin:0"><li>सुंदर चे समानार्थी? → <strong>मनोहर/रमणीय</strong></li><li>ज्ञान चे समानार्थी? → <strong>विद्या/प्रज्ञा</strong></li></ul></div>
<div class="box g"><div class="bt">⏱️ Revision</div><p style="margin:0">सुंदर=मनोहर · सत्य=वास्तव · वीर=शूर · ज्ञान=विद्या ✅</p></div>''',
"en":'''<div class="ph">📖 Synonyms</div>
<table class="tbl"><tr><th>Word</th><th>Synonyms</th></tr>
<tr><td>Beautiful</td><td>Handsome, Lovely, Attractive</td></tr>
<tr><td>Truth</td><td>Reality, Fact, Authentic</td></tr>
<tr><td>Brave</td><td>Courageous, Bold, Valiant</td></tr>
<tr><td>Knowledge</td><td>Wisdom, Learning, Intellect</td></tr>
<tr><td>Happy</td><td>Joyful, Delighted, Cheerful</td></tr>
<tr><td>Mercy</td><td>Compassion, Pity, Kindness</td></tr>
<tr><td>Power</td><td>Strength, Force, Might</td></tr></table>
<div class="trick"><p style="margin-top:6px"><strong>Brave = Courageous = Bold</strong> 🧠</p></div>
<div class="box p"><div class="bt">🎯 PYQ</div><ul style="margin:0"><li>Synonym of Beautiful? → <strong>Attractive/Lovely</strong></li><li>Synonym of Knowledge? → <strong>Wisdom</strong></li></ul></div>
<div class="box g"><div class="bt">⏱️ Revision</div><p style="margin:0">Beautiful=Attractive · Truth=Fact · Brave=Bold · Knowledge=Wisdom ✅</p></div>'''}),

P({"hi":"विरुद्धार्थी","mr":"विरुद्धार्थी","en":"Antonyms"},
{"hi":'''<div class="ph">📖 विरुद्धार्थी शब्द (Antonyms)</div>
<table class="tbl"><tr><th>शब्द</th><th>विरुद्धार्थी</th></tr>
<tr><td>सुंदर</td><td>कुरूप</td></tr>
<tr><td>सत्य</td><td>असत्य / झूठ</td></tr>
<tr><td>वीर</td><td>कायर</td></tr>
<tr><td>ज्ञान</td><td>अज्ञान / मूढ़ता</td></tr>
<tr><td>आनंद</td><td>दुःख / शोक</td></tr>
<tr><td>दिन</td><td>रात</td></tr>
<tr><td>हानि</td><td>लाभ</td></tr></table>
<div class="trick"><p style="margin-top:6px">सुंदर↔कुरूप · सत्य↔असत्य · वीर↔कायर · दिन↔रात 🧠</p></div>
<div class="box p"><div class="bt">🎯 PYQ</div><ul style="margin:0"><li>आनंद का विरुद्ध? → <strong>दुःख</strong></li><li>हानि का विरुद्ध? → <strong>लाभ</strong></li></ul></div>
<div class="box g"><div class="bt">⏱️ Revision</div><p style="margin:0">सुंदर↔कुरूप · सत्य↔असत्य · वीर↔कायर · आनंद↔दुःख · हानि↔लाभ ✅</p></div>''',
"mr":'''<div class="ph">📖 विरुद्धार्थी शब्द</div>
<table class="tbl"><tr><th>शब्द</th><th>विरुद्धार्थी</th></tr>
<tr><td>सुंदर</td><td>कुरूप</td></tr>
<tr><td>सत्य</td><td>असत्य / खोटे</td></tr>
<tr><td>वीर</td><td>कापूर</td></tr>
<tr><td>ज्ञान</td><td>अज्ञान / मूर्खपणा</td></tr>
<tr><td>आनंद</td><td>दुःख / शोक</td></tr>
<tr><td>दिवस</td><td>रात्री</td></tr>
<tr><td>तोटा</td><td>नफा</td></tr></table>
<div class="trick"><p style="margin-top:6px">सुंदर↔कुरूप · सत्य↔असत्य · वीर↔कापूर · दिवस↔रात्री 🧠</p></div>
<div class="box p"><div class="bt">🎯 PYQ</div><ul style="margin:0"><li>आनंद चे विरुद्ध? → <strong>दुःख</strong></li><li>तोटा चे विरुद्ध? → <strong>नफा</strong></li></ul></div>
<div class="box g"><div class="bt">⏱️ Revision</div><p style="margin:0">सुंदर↔कुरूप · सत्य↔असत्य · वीर↔कापूर · आनंद↔दुःख · तोटा↔नफा ✅</p></div>''',
"en":'''<div class="ph">📖 Antonyms</div>
<table class="tbl"><tr><th>Word</th><th>Antonym</th></tr>
<tr><td>Beautiful</td><td>Ugly</td></tr>
<tr><td>Truth</td><td>Falsehood / Lie</td></tr>
<tr><td>Brave</td><td>Coward</td></tr>
<tr><td>Knowledge</td><td>Ignorance</td></tr>
<tr><td>Joy</td><td>Sorrow / Grief</td></tr>
<tr><td>Day</td><td>Night</td></tr>
<tr><td>Loss</td><td>Profit</td></tr></table>
<div class="trick"><p style="margin-top:6px">Beautiful↔Ugly · Truth↔Lie · Brave↔Coward · Day↔Night 🧠</p></div>
<div class="box p"><div class="bt">🎯 PYQ</div><ul style="margin:0"><li>Antonym of Joy? → <strong>Sorrow</strong></li><li>Antonym of Loss? → <strong>Profit</strong></li></ul></div>
<div class="box g"><div class="bt">⏱️ Revision</div><p style="margin:0">Beautiful↔Ugly · Truth↔Lie · Brave↔Coward · Joy↔Sorrow · Loss↔Profit ✅</p></div>'''}),

P({"hi":"Idioms + म्हणी","mr":"Idioms + म्हणी","en":"Idioms + Proverbs"},
{"hi":'''<div class="ph">💬 English Idioms + मराठी म्हणी</div>
<div class="sh">English Idioms</div>
<table class="tbl"><tr><th>Idiom</th><th>अर्थ</th></tr>
<tr><td>Break the ice</td><td>संकोच तोड़ना</td></tr>
<tr><td>Once in a blue moon</td><td>बहुत कम (विरले)</td></tr>
<tr><td>A piece of cake</td><td>बहुत आसान</td></tr>
<tr><td>Hit the books</td><td>पढ़ाई करना</td></tr></table>
<div class="sh">मराठी म्हणी</div>
<table class="tbl"><tr><th>म्हणी</th><th>अर्थ</th></tr>
<tr><td>एका हाताने टाळी वाजत नाही</td><td>एकाच काम करून होत नाही</td></tr>
<tr><td>प्रतापगडावर वाघ नाही</td><td>मोठे काम करणारा नाही</td></tr>
<tr><td>अति तेथे माती</td><td>अति करणे चांगले नाही</td></tr></table>
<div class="box p"><div class="bt">🎯 PYQ</div><ul style="margin:0"><li>"Break the ice" अर्थ? → <strong>संकोच तोड़ना</strong></li><li>"A piece of cake" अर्थ? → <strong>बहुत आसान</strong></li></ul></div>
<div class="box g"><div class="bt">⏱️ Revision</div><p style="margin:0">Break the ice(संकोच तोड़) · A piece of cake(आसान) · अति तेथे माती ✅</p></div>''',
"mr":'''<div class="ph">💬 English Idioms + मराठी म्हणी</div>
<div class="sh">English Idioms</div>
<table class="tbl"><tr><th>Idiom</th><th>अर्थ</th></tr>
<tr><td>Break the ice</td><td>संकोच दूर करणे</td></tr>
<tr><td>Once in a blue moon</td><td>खूप कमी (दुर्मिळ)</td></tr>
<tr><td>A piece of cake</td><td>खूप सोपे</td></tr>
<tr><td>Hit the books</td><td>अभ्यास करणे</td></tr></table>
<div class="sh">मराठी म्हणी</div>
<table class="tbl"><tr><th>म्हणी</th><th>अर्थ</th></tr>
<tr><td>एका हाताने टाळी वाजत नाही</td><td>एकट्याने काम होत नाही</td></tr>
<tr><td>अति तेथे माती</td><td>अति करणे चांगले नाही</td></tr>
<tr><td>गावातले माणसे खाऊ नयेत</td><td>स्वतःच्या लोकांचे नुकसान करू नये</td></tr></table>
<div class="box p"><div class="bt">🎯 PYQ</div><ul style="margin:0"><li>"Break the ice" अर्थ? → <strong>संकोच दूर करणे</strong></li><li>"A piece of cake" अर्थ? → <strong>खूप सोपे</strong></li></ul></div>
<div class="box g"><div class="bt">⏱️ Revision</div><p style="margin:0">Break the ice(संकोच दूर) · A piece of cake(सोपे) · अति तेथे माती ✅</p></div>''',
"en":'''<div class="ph">💬 Idioms + Proverbs</div>
<div class="sh">English Idioms</div>
<table class="tbl"><tr><th>Idiom</th><th>Meaning</th></tr>
<tr><td>Break the ice</td><td>To overcome initial shyness</td></tr>
<tr><td>Once in a blue moon</td><td>Very rarely</td></tr>
<tr><td>A piece of cake</td><td>Very easy</td></tr>
<tr><td>Hit the books</td><td>To study</td></tr></table>
<div class="sh">Marathi Proverbs (म्हणी)</div>
<table class="tbl"><tr><th>Proverb</th><th>Meaning</th></tr>
<tr><td>एका हाताने टाळी वाजत नाही</td><td>You can't clap with one hand</td></tr>
<tr><td>अति तेथे माती</td><td>Too much of anything is bad</td></tr>
<tr><td>गावातले माणसे खाऊ नयेत</td><td>Don't harm your own people</td></tr></table>
<div class="box p"><div class="bt">🎯 PYQ</div><ul style="margin:0"><li>"Break the ice" meaning? → <strong>Overcome shyness</strong></li><li>"A piece of cake" meaning? → <strong>Very easy</strong></li></ul></div>
<div class="box g"><div class="bt">⏱️ Revision</div><p style="margin:0">Break the ice(shyness) · A piece of cake(easy) · अति तेथे माती ✅</p></div>'''}),
]
build_product("talathi-vocabulary-master", "तलाठी शब्दसंग्रह", "तलाठी शब्दसंग्रह", "Talathi Vocabulary", talathi_v_pages)
print("Talathi Vocab done")

# ============================================================
# PRODUCTS 4-6: UPSC + MPSC Kit — Reuse Polity+History+Geography content (condensed)
# ============================================================

# UPSC Prelims Master Book (History + Polity + Geography + Economy condensed)
upsc_pages = [
P({"hi":"आवरण","mr":"आवरण","en":"Cover"},
{"hi":'''<div class="emoji">✍️</div><div class="badge">KNIKVIRA DIGITAL • Handwritten Notes</div>
<h1>UPSC Prelims<br>PYQ Master Book</h1><div class="sub">10 Years (2015-2025) Solved Papers</div>
<div class="topics"><div>📌 इतिहास + संस्कृति</div><div>📌 राजव्यवस्था (Polity)</div><div>📌 भूगोल + पर्यावरण</div><div>📌 अर्थव्यवस्था + चालू घटनाक्रम</div><div>📌 🧠 Elimination Tricks</div></div>
<div class="credit">© Knikvira Digital • Krishna Jogdand, Pune</div>''',
"mr":'''<div class="emoji">✍️</div><div class="badge">KNIKVIRA DIGITAL • Handwritten Notes</div>
<h1>UPSC Prelims<br>PYQ Master Book</h1><div class="sub">10 वर्षे (2015-2025) Solved Papers</div>
<div class="topics"><div>📌 इतिहास + संस्कृती</div><div>📌 राज्यघटना (Polity)</div><div>📌 भूगोल + पर्यावरण</div><div>📌 अर्थव्यवस्था + चालू घडामोडी</div><div>📌 🧠 Elimination Tricks</div></div>
<div class="credit">© Knikvira Digital • Krishna Jogdand, Pune</div>''',
"en":'''<div class="emoji">✍️</div><div class="badge">KNIKVIRA DIGITAL • Handwritten Notes</div>
<h1>UPSC Prelims<br>PYQ Master Book</h1><div class="sub">10 Years (2015-2025) Solved Papers</div>
<div class="topics"><div>📌 History + Culture</div><div>📌 Polity</div><div>📌 Geography + Environment</div><div>📌 Economy + Current Affairs</div><div>📌 🧠 Elimination Tricks</div></div>
<div class="credit">© Knikvira Digital • Krishna Jogdand, Pune</div>'''},cover=True),

P({"hi":"PYQ — History","mr":"PYQ — History","en":"PYQ — History"},
{"hi":'''<div class="ph">📝 PYQ — इतिहास</div>
<div class="q"><div class="qq">1. इंडियन नैशनल कांग्रेस की स्थापना कब?</div><div class="qo r">1885 ✅</div></div>
<div class="q"><div class="qq">2. डांडी मार्च कब?</div><div class="qo r">1930 ✅</div></div>
<div class="q"><div class="qq">3. भारत छोड़ो आंदोलन कब शुरू?</div><div class="qo r">1942 ✅</div></div>
<div class="q"><div class="qq">4. अकबर का धर्म?</div><div class="qo r">दीन-ए-इलाही ✅</div></div>
<div class="box g"><div class="bt">⏱️ Revision</div><p style="margin:0">1885(कांग्रेस) · 1930(डांडी) · 1942(भारत छोड़ो) · अकबर(दीन-ए-इलाही) ✅</p></div>''',
"mr":'''<div class="ph">📝 PYQ — इतिहास</div>
<div class="q"><div class="qq">1. इंडियन नॅशनल काँग्रेसची स्थापना कधी?</div><div class="qo r">1885 ✅</div></div>
<div class="q"><div class="qq">2. दांडी यात्रा कधी?</div><div class="qo r">1930 ✅</div></div>
<div class="q"><div class="qq">3. भारत छोडो आंदोलन कधी सुरू?</div><div class="qo r">1942 ✅</div></div>
<div class="q"><div class="qq">4. अकबरचा धर्म?</div><div class="qo r">दीन-ए-इलाही ✅</div></div>
<div class="box g"><div class="bt">⏱️ Revision</div><p style="margin:0">1885(काँग्रेस) · 1930(दांडी) · 1942(भारत छोडो) · अकबर(दीन-ए-इलाही) ✅</p></div>''',
"en":'''<div class="ph">📝 PYQ — History</div>
<div class="q"><div class="qq">1. Indian National Congress founded when?</div><div class="qo r">1885 ✅</div></div>
<div class="q"><div class="qq">2. Dandi March when?</div><div class="qo r">1930 ✅</div></div>
<div class="q"><div class="qq">3. Quit India Movement started when?</div><div class="qo r">1942 ✅</div></div>
<div class="q"><div class="qq">4. Akbar's religion?</div><div class="qo r">Din-i-Ilahi ✅</div></div>
<div class="box g"><div class="bt">⏱️ Revision</div><p style="margin:0">1885(Congress) · 1930(Dandi) · 1942(Quit India) · Akbar(Din-i-Ilahi) ✅</p></div>'''}),

P({"hi":"PYQ — Polity","mr":"PYQ — Polity","en":"PYQ — Polity"},
{"hi":'''<div class="ph">📝 PYQ — राजव्यवस्था</div>
<div class="q"><div class="qq">1. राज्यघटना कब लागू?</div><div class="qo r">26 जनवरी 1950 ✅</div></div>
<div class="q"><div class="qq">2. मौलिक अधिकार कितने?</div><div class="qo r">6 ✅</div></div>
<div class="q"><div class="qq">3. "घटना का आत्मा" कौन सा Article?</div><div class="qo r">32 ✅</div></div>
<div class="q"><div class="qq">4. संसद के कितने सदन?</div><div class="qo r">2 (LS+RS) + राष्ट्रपति ✅</div></div>
<div class="box g"><div class="bt">⏱️ Revision</div><p style="margin:0">26 जन 1950 · 6 अधिकार · Art 32=आत्मा · 2 सदन+राष्ट्रपति ✅</p></div>''',
"mr":'''<div class="ph">📝 PYQ — राज्यघटना</div>
<div class="q"><div class="qq">1. राज्यघटना कधी लागू?</div><div class="qo r">26 जानेवारी 1950 ✅</div></div>
<div class="q"><div class="qq">2. मूलभूत हक्क किती?</div><div class="qo r">6 ✅</div></div>
<div class="q"><div class="qq">3. "घटनेचा आत्मा" कोणता अनुच्छेद?</div><div class="qo r">32 ✅</div></div>
<div class="q"><div class="qq">4. संसदेची किती सभागृहे?</div><div class="qo r">2 (LS+RS) + राष्ट्रपती ✅</div></div>
<div class="box g"><div class="bt">⏱️ Revision</div><p style="margin:0">26 जाने 1950 · 6 हक्क · अ.32=आत्मा · 2 सभागृह+राष्ट्रपती ✅</p></div>''',
"en":'''<div class="ph">📝 PYQ — Polity</div>
<div class="q"><div class="qq">1. Constitution enforced when?</div><div class="qo r">26 January 1950 ✅</div></div>
<div class="q"><div class="qq">2. How many Fundamental Rights?</div><div class="qo r">6 ✅</div></div>
<div class="q"><div class="qq">3. "Soul of Constitution" which Article?</div><div class="qo r">32 ✅</div></div>
<div class="q"><div class="qq">4. How many houses in Parliament?</div><div class="qo r">2 (LS+RS) + President ✅</div></div>
<div class="box g"><div class="bt">⏱️ Revision</div><p style="margin:0">26 Jan 1950 · 6 Rights · Art 32=Soul · 2 houses+President ✅</p></div>'''}),

P({"hi":"Elimination Tricks","mr":"Elimination Tricks","en":"Elimination Tricks"},
{"hi":'''<div class="ph">🧠 UPSC Elimination Tricks</div>
<div class="box b"><div class="bt">💡 Strategy</div><ul>
<li><strong>1. "All of the above"</strong> — अक्सर सही होता है (जब 2+ सही लगें)</li>
<li><strong>2. Extreme words</strong> — "केवल", "हमेशा", "कभी नहीं" → अक्सर गलत</li>
<li><strong>3. तथ्यात्मक विकल्प</strong> — एक गलत फैक्ट → विकल्प गलत</li>
<li><strong>4. Date/Years</strong> — सटीक साल याद रखें</li></ul></div>
<div class="box y"><div class="bt">⭐ Pro Tip</div><p style="margin:0">अगर 2 विकल्प सही लगें और एक "All of the above" हो → उसे चुनें (60% सही)</p></div>
<div class="box g"><div class="bt">⏱️ Revision</div><p style="margin:0">"All of above"(अक्सर सही) · Extreme words(गलत) · एक गलत फैक्ट=विकल्प गलत ✅</p></div>''',
"mr":'''<div class="ph">🧠 UPSC Elimination Tricks</div>
<div class="box b"><div class="bt">💡 Strategy</div><ul>
<li><strong>1. "वरीलपैकी सर्व"</strong> — बहुतांश वेळा बरोबर (जेव्हा 2+ बरोबर वाटतील)</li>
<li><strong>2. Extreme words</strong> — "फक्त", "नेहमी", "कधीच नाही" → बहुतांश वेळा चूक</li>
<li><strong>3. तथ्यात्मक पर्याय</strong> — एक चुकीचा fact → पर्याय चूक</li>
<li><strong>4. Date/Years</strong> — अचूक वर्ष लक्षात ठेवा</li></ul></div>
<div class="box y"><div class="bt">⭐ Pro Tip</div><p style="margin:0">जर 2 पर्याय बरोबर वाटतील आणि एक "वरीलपैकी सर्व" असेल → तो निवडा (60% बरोबर)</p></div>
<div class="box g"><div class="bt">⏱️ Revision</div><p style="margin:0">"वरीलपैकी सर्व"(बहुतांश बरोबर) · Extreme words(चूक) · एक चूक fact=पर्याय चूक ✅</p></div>''',
"en":'''<div class="ph">🧠 UPSC Elimination Tricks</div>
<div class="box b"><div class="bt">💡 Strategy</div><ul>
<li><strong>1. "All of the above"</strong> — often correct (when 2+ seem right)</li>
<li><strong>2. Extreme words</strong> — "only", "always", "never" → often wrong</li>
<li><strong>3. Factual options</strong> — one wrong fact → option wrong</li>
<li><strong>4. Dates/Years</strong> — remember exact years</li></ul></div>
<div class="box y"><div class="bt">⭐ Pro Tip</div><p style="margin:0">If 2 options seem correct and one is "All of the above" → choose it (60% correct)</p></div>
<div class="box g"><div class="bt">⏱️ Revision</div><p style="margin:0">"All of above"(often right) · Extreme words(wrong) · one wrong fact=option wrong ✅</p></div>'''}),
]
build_product("upsc-prelims-master-book", "UPSC Prelims PYQ", "UPSC Prelims PYQ", "UPSC Prelims PYQ", upsc_pages)
print("UPSC done")

# MPSC Rajyaseva Kit (condensed — Geography + History + Polity + MH GK)
mpsc_pages = [
P({"hi":"आवरण","mr":"आवरण","en":"Cover"},
{"hi":'''<div class="emoji">🏛️</div><div class="badge">KNIKVIRA DIGITAL • Handwritten Notes</div>
<h1>MPSC राज्यसेवा<br>Complete Study Kit</h1><div class="sub">7 Subjects · Mock Tests · PYQ</div>
<div class="topics"><div>📌 इतिहास + भूगोल</div><div>📌 राज्यघटना + अर्थव्यवस्था</div><div>📌 महाराष्ट्र GK</div><div>📌 🧠 Tricks · 📝 PYQ</div></div>
<div class="credit">© Knikvira Digital • Krishna Jogdand, Pune</div>''',
"mr":'''<div class="emoji">🏛️</div><div class="badge">KNIKVIRA DIGITAL • Handwritten Notes</div>
<h1>MPSC राज्यसेवा<br>संपूर्ण स्टडी किट</h1><div class="sub">7 विषय · Mock Tests · PYQ</div>
<div class="topics"><div>📌 इतिहास + भूगोल</div><div>📌 राज्यघटना + अर्थव्यवस्था</div><div>📌 महाराष्ट्र GK</div><div>📌 🧠 Tricks · 📝 PYQ</div></div>
<div class="credit">© Knikvira Digital • Krishna Jogdand, Pune</div>''',
"en":'''<div class="emoji">🏛️</div><div class="badge">KNIKVIRA DIGITAL • Handwritten Notes</div>
<h1>MPSC Rajyaseva<br>Complete Study Kit</h1><div class="sub">7 Subjects · Mock Tests · PYQ</div>
<div class="topics"><div>📌 History + Geography</div><div>📌 Polity + Economy</div><div>📌 Maharashtra GK</div><div>📌 🧠 Tricks · 📝 PYQ</div></div>
<div class="credit">© Knikvira Digital • Krishna Jogdand, Pune</div>'''},cover=True),

P({"hi":"महाराष्ट्र GK","mr":"महाराष्ट्र GK","en":"Maharashtra GK"},
{"hi":'''<div class="ph">🏛️ महाराष्ट्र — Key Facts</div>
<div class="box b"><div class="bt">💡 तथ्य</div><ul>
<li><span class="hl">राजधानी:</span> मुंबई · स्थापना: 1 मई 1960</li>
<li><span class="hl">जिले:</span> 36 · विभाग: 6</li>
<li><span class="hl">सबसे ऊंचा:</span> कळसूबाई (1,646 मी)</li>
<li><span class="hl">सबसे लंबी नदी:</span> कृष्णा (महाबलेश्वर)</li>
<li><span class="hl">सबसे बड़ा जिला:</span> गढ़चिरौली</li>
<li><span class="hl">ऑरेंज सिटी:</span> नागपुर 🍊</li></ul></div>
<div class="box g"><div class="bt">⏱️ Revision</div><p style="margin:0">1 मई 1960 · 36 जिले · कळसूबाई · कृष्णा · गढ़चिरौली · नागपुर(ऑरेंज) ✅</p></div>''',
"mr":'''<div class="ph">🏛️ महाराष्ट्र — Key Facts</div>
<div class="box b"><div class="bt">💡 तथ्ये</div><ul>
<li><span class="hl">राजधानी:</span> मुंबई · स्थापना: 1 मे 1960</li>
<li><span class="hl">जिल्हे:</span> 36 · विभाग: 6</li>
<li><span class="hl">सर्वात उंच:</span> कळसूबाई (1,646 मी)</li>
<li><span class="hl">सर्वात लांब नदी:</span> कृष्णा (महाबळेश्वर)</li>
<li><span class="hl">सर्वात मोठा जिल्हा:</span> गडचिरोली</li>
<li><span class="hl">ऑरेंज सिटी:</span> नागपूर 🍊</li></ul></div>
<div class="box g"><div class="bt">⏱️ Revision</div><p style="margin:0">1 मे 1960 · 36 जिल्हे · कळसूबाई · कृष्णा · गडचिरोली · नागपूर(ऑरेंज) ✅</p></div>''',
"en":'''<div class="ph">🏛️ Maharashtra — Key Facts</div>
<div class="box b"><div class="bt">💡 Facts</div><ul>
<li><span class="hl">Capital:</span> Mumbai · Formation: 1 May 1960</li>
<li><span class="hl">Districts:</span> 36 · Divisions: 6</li>
<li><span class="hl">Highest:</span> Kalsubai (1,646 m)</li>
<li><span class="hl">Longest river:</span> Krishna (Mahabaleshwar)</li>
<li><span class="hl">Largest district:</span> Gadchiroli</li>
<li><span class="hl">Orange City:</span> Nagpur 🍊</li></ul></div>
<div class="box g"><div class="bt">⏱️ Revision</div><p style="margin:0">1 May 1960 · 36 districts · Kalsubai · Krishna · Gadchiroli · Nagpur(Orange) ✅</p></div>'''}),

P({"hi":"रिवीज़न","mr":"Revision","en":"Revision"},
{"hi":'''<div class="ph">🧠 MPSC — Master Revision</div>
<div class="mm"><div style="text-align:center"><div class="mm-c">MPSC Kit</div></div>
<div class="grid3">
<div class="gc" style="border-color:#10b981;color:#047857"><strong>MH GK</strong>36 जिले · कळसूबाई</div>
<div class="gc" style="border-color:#f59e0b;color:#b45309"><strong>Polity</strong>6 अधिकार · Art 32</div>
<div class="gc" style="border-color:#3b82f6;color:#1d4ed8"><strong>History</strong>1757→1947</div>
</div></div>
<div class="box g"><div class="bt">⏱️ Master</div><p style="margin:0">1 मई 1960 · 36 जिले · कळसूबाई · कृष्णा · 6 अधिकार · Art 32=आत्मा · 1757→1947 ✅</p></div>
<div style="text-align:center;margin-top:16px;padding:14px;background:#1a1a2e;color:#fff;border-radius:10px;font-size:18px">© Knikvira Digital • knikviradigital.in • 📲 8421532744 • Krishna Jogdand, Pune</div>''',
"mr":'''<div class="ph">🧠 MPSC — Master Revision</div>
<div class="mm"><div style="text-align:center"><div class="mm-c">MPSC Kit</div></div>
<div class="grid3">
<div class="gc" style="border-color:#10b981;color:#047857"><strong>MH GK</strong>36 जिल्हे · कळसूबाई</div>
<div class="gc" style="border-color:#f59e0b;color:#b45309"><strong>Polity</strong>6 हक्क · अ.32</div>
<div class="gc" style="border-color:#3b82f6;color:#1d4ed8"><strong>History</strong>1757→1947</div>
</div></div>
<div class="box g"><div class="bt">⏱️ Master</div><p style="margin:0">1 मे 1960 · 36 जिल्हे · कळसूबाई · कृष्णा · 6 हक्क · अ.32=आत्मा · 1757→1947 ✅</p></div>
<div style="text-align:center;margin-top:16px;padding:14px;background:#1a1a2e;color:#fff;border-radius:10px;font-size:18px">© Knikvira Digital • knikviradigital.in • 📲 8421532744 • Krishna Jogdand, Pune</div>''',
"en":'''<div class="ph">🧠 MPSC — Master Revision</div>
<div class="mm"><div style="text-align:center"><div class="mm-c">MPSC Kit</div></div>
<div class="grid3">
<div class="gc" style="border-color:#10b981;color:#047857"><strong>MH GK</strong>36 districts · Kalsubai</div>
<div class="gc" style="border-color:#f59e0b;color:#b45309"><strong>Polity</strong>6 Rights · Art 32</div>
<div class="gc" style="border-color:#3b82f6;color:#1d4ed8"><strong>History</strong>1757→1947</div>
</div></div>
<div class="box g"><div class="bt">⏱️ Master</div><p style="margin:0">1 May 1960 · 36 districts · Kalsubai · Krishna · 6 Rights · Art 32=Soul · 1757→1947 ✅</p></div>
<div style="text-align:center;margin-top:16px;padding:14px;background:#1a1a2e;color:#fff;border-radius:10px;font-size:18px">© Knikvira Digital • knikviradigital.in • 📲 8421532744 • Krishna Jogdand, Pune</div>'''}),
]
build_product("mpsc-rajyaseva-study-kit", "MPSC राज्यसेवा", "MPSC राज्यसेवा", "MPSC Rajyaseva", mpsc_pages)
print("MPSC Kit done")

print("\n" + "=" * 50)
print("✅ ALL PRODUCTS GENERATED!")
print("=" * 50)
