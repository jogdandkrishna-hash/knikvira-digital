# -*- coding: utf-8 -*-
"""
Knikvira Digital — Sample PDF Generator
प्रत्येक product साठी 5-पानी sample PDF (cover + अनुक्रमणिका + 3 खरे नमुना पाने).
"""
import os
import re
from fpdf import FPDF

FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
OUT_DIR = "/home/user/knikvira-fix/samples"
os.makedirs(OUT_DIR, exist_ok=True)

# Noto Sans Devanagari = Devanagari + Latin + ₹ only → strip emoji/symbols safely
_KEEP = set("–—₹‘’“”…«»")
def clean(t):
    return "".join(c for c in str(t) if ord(c) < 0x2000 or c in _KEEP)

INDIGO = (79, 70, 229)
VIOLET = (124, 58, 237)
DARK = (31, 41, 55)
GRAY = (107, 114, 128)
AMBER = (245, 158, 11)
LIGHT = (238, 242, 255)
GREEN = (5, 150, 105)

WA_NUMBER = "84215 32744"
SITE = "www.knikviradigital.in"


class SamplePDF(FPDF):
    def __init__(self, title, slug):
        super().__init__("P", "mm", "A4")
        self.ptitle = title
        self.slug = slug
        self.add_font("noto", "", f"{FONT_DIR}/NotoSansDevanagari-Regular.ttf")
        self.add_font("noto", "B", f"{FONT_DIR}/NotoSansDevanagari-Bold.ttf")
        self.add_font("latin", "", f"{FONT_DIR}/dejavu/DejaVuSans.ttf")
        self.add_font("latin", "B", f"{FONT_DIR}/dejavu/DejaVuSans-Bold.ttf")
        self.set_fallback_fonts(["latin"])
        self.set_text_shaping(True)
        self.set_auto_page_break(True, 16)
        self.set_margins(16, 14, 16)

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-13)
        self.set_font("noto", "", 8)
        self.set_text_color(*GRAY)
        self.cell(0, 5, f"Free Sample • {SITE} • WhatsApp {WA_NUMBER}", align="L")
        self.cell(0, 5, f"पान {self.page_no()}", align="R", new_x="LMARGIN", new_y="NEXT")

    def watermark(self):
        # faux alpha: pale indigo; Latin drawn explicitly (text() has no font-fallback)
        self.set_text_color(232, 230, 250)
        with self.rotation(45, 105, 148):
            self.set_font("latin", "B", 40)
            w = self.get_string_width("FREE SAMPLE  ")
            self.text(35, 148, "FREE SAMPLE  ")
            self.set_font("noto", "B", 40)
            self.text(35 + w, 148, "नमुना")

    # ---------- block renderers ----------
    def h2(self, txt):
        txt = clean(txt)
        self.ln(1)
        self.set_font("noto", "B", 13)
        self.set_text_color(*INDIGO)
        self.multi_cell(0, 7, txt)
        self.set_draw_color(*INDIGO)
        self.set_line_width(0.4)
        self.line(self.l_margin, self.get_y(), self.l_margin + 42, self.get_y())
        self.ln(2)

    def p(self, txt):
        txt = clean(txt)
        self.set_font("noto", "", 10.5)
        self.set_text_color(*DARK)
        self.multi_cell(0, 5.6, txt)
        self.ln(1)

    def bullets(self, items):
        self.set_font("noto", "", 10.5)
        self.set_text_color(*DARK)
        for it in items:
            it = clean(it)
            y0 = self.get_y()
            self.set_text_color(*INDIGO)
            self.set_font("latin", "", 10.5)
            self.text(self.l_margin, y0 + 4.4, "•")   # latin font marker (text() no fallback)
            self.set_font("noto", "", 10.5)
            self.set_x(self.l_margin + 5)
            self.set_text_color(*DARK)
            self.multi_cell(0, 5.6, it)
        self.ln(1)

    def note(self, txt, bg=LIGHT, fg=DARK):
        txt = clean(txt)
        self.set_fill_color(*bg)
        self.set_font("noto", "B", 10.5)
        self.set_text_color(*fg)
        self.multi_cell(0, 6.4, txt, fill=True)
        self.ln(2)

    def mcq(self, q, opts, ans_idx, expl):
        q, expl = clean(q), clean(expl)
        opts = [clean(o) for o in opts]
        self.set_font("noto", "B", 10.5)
        self.set_text_color(*DARK)
        self.multi_cell(0, 5.8, q, new_x="LMARGIN", new_y="NEXT")
        self.set_font("noto", "", 10.5)
        for i, o in enumerate(opts):
            mark = "क)" if i == 0 else "ख)" if i == 1 else "ग)" if i == 2 else "घ)"
            self.set_text_color(*DARK)
            self.multi_cell(0, 5.4, f"   {mark} {o}", new_x="LMARGIN", new_y="NEXT")
        self.set_font("noto", "B", 10.5)
        self.set_text_color(*GREEN)
        self.multi_cell(0, 5.6, f"✔ योग्य उत्तर: {chr(2325 + ans_idx)}) {opts[ans_idx]}", new_x="LMARGIN", new_y="NEXT")
        self.set_font("noto", "", 9.5)
        self.set_text_color(*GRAY)
        self.multi_cell(0, 5.2, f"स्पष्टीकरण: {expl}", new_x="LMARGIN", new_y="NEXT")
        self.ln(2.5)

    def table(self, headers, rows, widths=None):
        headers = [clean(h) for h in headers]
        rows = [[clean(c) for c in r] for r in rows]
        widths = widths or [None] * len(headers)
        total = self.w - self.l_margin - self.r_margin
        if widths[0] is None:
            widths = [total / len(headers)] * len(headers)
        else:
            s = sum(widths)
            widths = [total * wdt / s for wdt in widths]
        self.set_font("noto", "B", 9.5)
        self.set_fill_color(*INDIGO)
        self.set_text_color(255, 255, 255)
        for htxt, wdt in zip(headers, widths):
            self.cell(wdt, 6.4, htxt, border=0, fill=True, align="C")
        self.ln()
        self.set_font("noto", "", 9.5)
        fill = False
        for row in rows:
            self.set_fill_color(*LIGHT)
            self.set_text_color(*DARK)
            for cell, wdt in zip(row, widths):
                self.cell(wdt, 6.0, str(cell), border=0, fill=fill, align="L")
            self.ln()
            fill = not fill
        self.ln(2)


def build_cover(pdf, d):
    pdf.set_auto_page_break(False, 0)   # cover: never split
    d = {k: (clean(v) if isinstance(v, str) else [clean(x) if isinstance(x, str) else x for x in v] if isinstance(v, list) else v) for k, v in d.items()}
    # indigo hero band
    pdf.set_fill_color(*INDIGO)
    pdf.rect(0, 0, 210, 78, "F")
    pdf.set_fill_color(*VIOLET)
    pdf.rect(105, 0, 105, 78, "F")
    pdf.set_xy(16, 12)
    pdf.set_font("noto", "B", 11)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 6, "KNIKVIRA DIGITAL", new_x="LMARGIN", new_y="NEXT")
    # sample chip
    pdf.set_fill_color(*AMBER)
    pdf.set_xy(16, 20)
    pdf.set_font("noto", "B", 10)
    w = pdf.get_string_width("FREE SAMPLE • नमुना प्रती") + 10
    pdf.cell(w, 8, "FREE SAMPLE • नमुना प्रती", fill=True, new_x="LMARGIN", new_y="NEXT")
    pdf.set_xy(16, 34)
    pdf.set_font("noto", "B", 19)
    pdf.multi_cell(178, 10, d["title"])
    pdf.set_font("noto", "", 10.5)
    pdf.set_xy(16, 62)
    pdf.multi_cell(178, 5.6, "ही 5 पानांची नमुना प्रत आहे — पूर्ण PDF ची शैली, दर्जा व मजकुराची अचूक झलक. खरेदीपूर्वी स्वतः तपासा!")

    pdf.set_y(86)
    pdf.set_text_color(*DARK)
    pdf.set_font("noto", "B", 12.5)
    pdf.cell(0, 8, "या नमुना प्रतीत काय आहे?", new_x="LMARGIN", new_y="NEXT")
    pdf.bullets(d["sample_includes"])

    pdf.set_font("noto", "B", 12.5)
    pdf.set_text_color(*DARK)
    pdf.cell(0, 8, "पूर्ण PDF मध्ये काय मिळेल?", new_x="LMARGIN", new_y="NEXT")
    pdf.bullets(d["full_includes"])

    # price / CTA box
    pdf.ln(3)
    pdf.set_fill_color(236, 253, 245)
    y0 = pdf.get_y()
    pdf.rect(16, y0, 178, 30, "F")
    pdf.set_xy(20, y0 + 4)
    pdf.set_font("noto", "B", 13)
    pdf.set_text_color(*GREEN)
    pdf.cell(0, 7, f"पूर्ण PDF किंमत: फक्त ₹{d['price']}", new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(20)
    pdf.set_font("noto", "", 10)
    pdf.set_text_color(*DARK)
    pdf.multi_cell(170, 5.6, "Razorpay सुरक्षित पेमेंट (UPI / Card / Netbanking) • पेमेंटनंतर लगेच डाउनलोड\nसंपूर्ण PDF हवा? वेबसाइटवर दिलेल्या Buy बटणाने मिळवा किंवा WhatsApp करा")

    pdf.set_y(-24)
    pdf.set_font("noto", "", 9.5)
    pdf.set_text_color(*GRAY)
    pdf.multi_cell(0, 5.2,
        f"{SITE}   •   WhatsApp: {WA_NUMBER}   •   10,000+ विद्यार्थ्यांचा विश्वास\n"
        "© Knikvira Digital — ही प्रत वैयक्तिक अभ्यासासाठी आहे. पुनविक्री/शेअरिंग निषिद्ध.")


def build_toc(pdf, d):
    pdf.set_auto_page_break(True, 16)
    d = {k: (clean(v) if isinstance(v, str) else [clean(x) if isinstance(x, str) else x for x in v] if isinstance(v, list) else v) for k, v in d.items()}
    pdf.add_page()
    pdf.watermark()
    pdf.h2("पूर्ण PDF ची संपूर्ण अनुक्रमणिका")
    pdf.p("खाली पूर्ण PDF मध्ये नेमके काय-काय आहे याची एकूण मांडणी दिली आहे. नमुना प्रतीत पुढील 3 पानांवर यातील काही विषयांची प्रत्यक्ष झलक दिसेल:")
    pdf.set_font("noto", "", 10.5)
    for i, item in enumerate(d["toc"], 1):
        y0 = pdf.get_y()
        pdf.set_text_color(*INDIGO)
        pdf.text(pdf.l_margin, y0 + 4.4, f"{i}.")
        pdf.set_x(pdf.l_margin + 8)
        pdf.set_text_color(*DARK)
        pdf.multi_cell(0, 6.0, item)
    pdf.ln(3)
    pdf.note("लक्षात घ्या: ही फक्त 'रुपरेषा' आहे — पूर्ण PDF मध्ये प्रत्येक टॉपिकवर सविस्तर नोट्स/प्रश्न/उत्तरे दिली आहेत.",
             bg=(254, 243, 199), fg=(120, 53, 15))
    pdf.ln(2)
    pdf.p(d.get("toc_note", "हे अभ्यास साहित्य अनुभवी टीमने तयार केले आहे — परीक्षेच्या ताज्या पॅटर्ननुसार, भाषा सोपी, पॉइंट-वाइज."))


def render_blocks(pdf, blocks):
    for b in blocks:
        kind = b[0]
        if kind == "h2":
            pdf.h2(b[1])
        elif kind == "p":
            pdf.p(b[1])
        elif kind == "bullets":
            pdf.bullets(b[1])
        elif kind == "note":
            pdf.note(b[1])
        elif kind == "mcq":
            pdf.mcq(b[1], b[2], b[3], b[4])
        elif kind == "table":
            pdf.table(b[1], b[2], b[3] if len(b) > 3 else None)
        elif kind == "pagebreak":
            pdf.add_page()
            pdf.watermark()


def build_product(d):
    pdf = SamplePDF(d["title"], d["slug"])
    pdf.add_page()
    build_cover(pdf, d)
    build_toc(pdf, d)
    pdf.add_page()
    pdf.watermark()
    pdf.h2("प्रत्यक्ष नमुना मजकूर (Sample Content)")
    pdf.p("खाली पूर्ण PDF मधीलच काही विषयांची तशीच-तशी झलक दिली आहे:")
    render_blocks(pdf, d["sections"])
    # last CTA strip
    pdf.ln(2)
    pdf.note(f"✅ पूर्ण {d.get('pages','')} PDF — फक्त ₹{d['price']} | {SITE} वर Buy करा किंवा WhatsApp {WA_NUMBER}",
             bg=(236, 253, 245), fg=GREEN)
    out = f"{OUT_DIR}/{d['slug']}-sample.pdf"
    pdf.output(out)
    return out


# ------------------------------------------------------------------
#  PRODUCT CONTENT
# ------------------------------------------------------------------
PRODUCTS = [

dict(slug="mpsc-rajyaseva-study-kit", title="MPSC राज्यसेवा पूर्व परीक्षा 2026 — संपूर्ण स्टडी किट", price=199, pages="180+ पाने",
 sample_includes=[
   "पूर्ण PDF ची मांडणी — 7 विषय कसे विभागले आहेत + प्रत्येकाचे वजन",
   "राज्यघटना विषयाचे 1 खरे नमुना पान (नोट्स शैलीत)",
   "10 प्रश्नांचा सराव टेस्ट — उत्तरतालिका व स्पष्टीकरणासह (तशीच PDF मधली)"],
 full_includes=[
   "7 विषयांचे सविस्तर PDF Booklets (इतिहास, भूगोल, राज्यघटना, अर्थव्यवस्था, विज्ञान, चालू घडामोडी, बुद्धिमत्ता)",
   "10 सोडवलेले Mock Tests + Official Answer Keys",
   "महाराष्ट्र GK व 36 जिल्हा ॲटलास सारांश",
   "PYQ ट्रेंड विश्लेषण (2015–2025) — कोणते टॉपिक किती वेळा विचारले",
   "100% Instant Digital Download — मोबाईल/टॅब/डेस्कटॉपवर वाचता येते"],
 toc=[
   "विषय 1: इतिहास व महाराष्ट्राचा इतिहास (42 प्रकरणे)",
   "विषय 2: भूगोल — भारत व महाराष्ट्र (35 प्रकरणे)",
   "विषय 3: भारतीय राज्यघटना व प्रशासन (38 प्रकरणे)",
   "विषय 4: भारतीय अर्थव्यवस्था (28 प्रकरणे)",
   "विषय 5: सामान्य विज्ञान व तंत्रज्ञान (30 प्रकरणे)",
   "विषय 6: चालू घडामोडी — महिन्यानिहाय अपडेट शीट्स",
   "विषय 7: बुद्धिमत्ता चाचणी व अंकगणित (500+ प्रश्न)",
   "परिशिष्ट A: 10 Mock Tests (प्रत्येकी 100 प्रश्न) + उत्तरतालिका",
   "परिशिष्ट B: 36 जिल्हा Quick ॲटलास व महत्वाचे योजना-संग्रह"],
 sections=[
   ("h2", "विषय 3 नमुना: भारतीय राज्यघटना — मूलभूत हक्क"),
   ("p", "भारतीय राज्यघटनेचा भाग 3 (अनुच्छेद 12 ते 35) मूलभूत हक्कांशी संबंधित आहे. परीक्षेत यावर दरवर्षी सरासरी 3–4 प्रश्न येतात."),
   ("table", ("अनुच्छेद", "तरतूद", "परीक्षेला किती वेळा (2015–25)"),
        [("अनुच्छेद 14", "कायद्यापुढे समानता", "9 वेळा"),
         ("अनुच्छेद 19", "अभिव्यक्ती स्वातंत्र्य (6 स्वातंत्र्ये)", "11 वेळा"),
         ("अनुच्छेद 21", "प्राण व दैनंदिन स्वातंत्र्य", "8 वेळा"),
         ("अनुच्छेद 32", "घटनात्मक उपाय (Dr. अंबेडकर: 'कल्पना-विश्व')", "7 वेळा")],
        (3, 5, 3)),
   ("note", "📌 Shortcut: '12-22 शारीरिक, 23-24 शोषणविरोधी, 25-28 धर्म, 29-30 शिक्षण-संस्कृती' — अशा गटांनी लक्षात ठेवा!"),
   ("mcq", "प्रश्न: 'कायद्यापुढे समानता' ही संकल्पना भारतीय राज्यघटनेत कोणत्या देशाच्या घटनेतून घ्यायला आली?",
        ["अमेरिका", "ब्रिटन", "आयर्लंड", "कॅनडा"], 1,
        "अनुच्छेद 14 — 'Equality before law' ही ब्रिटिश परंपरेतील संकल्पना; 'Equal protection of laws' अमेरिकेतून."),
   ("pagebreak",),
   ("h2", "सराव टेस्ट नमुना (10 पैकी 5 प्रश्न)"),
   ("mcq", "प्र. 1) राज्यसभेची सदस्यसंख्या जास्तीत जास्त किती असू शकते?",
        ["238", "245", "250", "260"], 2,
        "जास्तीत जास्त 250 (राष्ट्रपती 12 मनोनीत + 238 निवडून). सध्या 245."),
   ("mcq", "प्र. 2) महाराष्ट्रातील पहिला मुख्यमंत्री कोण?",
        ["यशवंतराव चव्हाण", "वसंतराव नाईक", "शरद पवार", "वसंतदादा पाटील"], 0,
        "1 मे 1960 — यशवंतराव चव्हाण महाराष्ट्राचे पहिले मुख्यमंत्री."),
   ("mcq", "प्र. 3) 'गोदावरी' नदीचे उगमस्थान कोणते?",
        ["त्र्यंबकेश्वर", "महाबळेश्वर", "अमरकंटक", "भीमाशंकर"], 0,
        "त्र्यंबकेश्वर (नाशिक) — गोदावरी ही दक्षिणेची गंगा/दक्षिण गंगा म्हणून ओळखली जाते."),
   ("mcq", "प्र. 4) कोणत्या अनुच्छेदानुसार राष्ट्रपती 'आर्थिक आपत्काल' घोषित करू शकतात?",
        ["अनुच्छेद 352", "अनुच्छेद 356", "अनुच्छेद 360", "अनुच्छेद 365"], 2,
        "अनुच्छेद 360 — आर्थिक आपत्काल (आजपर्यंत एकदाही घोषित झाला नाही — हेच वधChapter:  अनेकदा विचारतात!)."),
   ("mcq", "प्र. 5) GST परिषदेचे अध्यक्ष कोण असतात?",
        ["राष्ट्रपती", "पंतप्रधान", "केंद्रीय अर्थमंत्री", "निती आयोग उपाध्यक्ष"], 2,
        "अनुच्छेद 279A — GST परिषद, अध्यक्ष: केंद्रीय अर्थमंत्री."),
   ("bullets", ["पूर्ण PDF मध्ये अशे 1000+ प्रश्न + 10 मॉक टेस्ट उत्तरांसह!", "प्रत्येक प्रश्नाखाली एकूल संकल्पना shortcut दिलेला आहे"]) ] ),

dict(slug="upsc-prelims-master-book", title="UPSC Prelims GS-1 & CSAT — 10 Years PYQ Master Book", price=149, pages="350+ पाने",
 sample_includes=[
   "विषयवार वर्गीकरण कसं केले आहे (Blueprint)",
   "2024 च्या 5 प्रश्नांचे सविस्तर स्पष्टीकरणासह उत्तरे",
   "'Elimination Trick' — चुकीचे पर्याय ओळखण्याची पद्धत (पूर्ण पान)"],
 full_includes=[
   "GS Paper-1 व CSAT — 2015 ते 2025 सर्व प्रश्नपत्रिका सोडवलेल्या",
   "प्रत्येक प्रश्नाखाली: उत्तर + सविस्तर स्पष्टीकरण + संकल्पना बॉक्स",
   "विषयवार ट्रेंड टेबल — कोणत्या विषयाला किती वजन (10 वर्षांचे विश्लेषण)",
   "Elimination & Intelligent Guessing तंत्रांचा स्वतंत्र मार्गदर्शक",
   "High-quality PDF — मोबाईलवर सूक्ष्म अक्षरे स्पष्ट वाचता येतात"],
 toc=[
   "Section A: History (Ancient/Medieval/Modern + Art & Culture) — 210 प्रश्न",
   "Section B: Polity & Governance — 185 प्रश्न",
   "Section C: Geography & Environment — 240 प्रश्न",
   "Section D: Economy — 150 प्रश्न",
   "Section E: Science & Tech + Current Affairs — 165 प्रश्न",
   "Section F: CSAT Solved (Comprehension, Reasoning, Quant) — 200 प्रश्न",
   "Appendix: Year-wise Answer Keys (Official UPSC)",
   "Appendix: Cut-off Analysis 2015–2025"],
 sections=[
   ("h2", "नमुना: 2024 GS प्रश्न — स्पष्टीकरणासह"),
   ("mcq", "प्र. 1) 'सिंधु खोऱ्यातील' पुरातत्व संशोधनासाठी पुढीलपैकी कोणते स्थळ प्रसिद्ध आहे?",
        ["लोथल", "कलिंग", "पाटलिपुत्र", "तक्षशिला"], 0,
        "लोथल (गुजरात) — सिंधू संस्कृतीचे प्रसिद्ध बंदरशहर; डॉकयार्ड तिथेच सापडले."),
   ("mcq", "प्र. 2) भारताचे राष्ट्रीय पंचांग (Saka Era) कोणत्या वर्षापासून सुरू होते?",
        ["AD 57", "AD 78", "AD 320", "AD 1947"], 1,
        "शक संवत AD 78 पासून. CPI — राष्ट्रीय पंचांग 1957 मध्ये अंगीकारले (Calendar Reform Committee)."),
   ("note", "🎯 Elimination Trick: पर्याय 'AD 1947' हा ठळकपणे चुकीचा दिसतो — UPSC अशा 'इमोशनल पर्यायां'कडे ट्रॅप म्हणून वापरते. प्रथम हा वगळा, मग 3 राहिलेल्या!"),
   ("pagebreak",),
   ("h2", "नमुना: CSAT — Reasoning"),
   ("mcq", "प्र. 3) एका संख्या मालिकेत पुढील पद ओळखा: 3, 7, 15, 31, 63, ?",
        ["95", "111", "127", "131"], 2,
        "प्रत्येक पद × 2 + 1 → 63×2+1 = 127. (2ⁿ−1 पद्धतीची मालिका)"),
   ("mcq", "प्र. 4) जर CAT = 24 आणি DOG = 26, तर FOX = ?",
        ["42", "45", "48", "50"], 1,
        "अक्षरस्थानांची बेरीज: F(6)+O(15)+X(24) = 45."),
   ("p", "पूर्ण PDF मध्ये Comprehension च्या 40+ solved passages व गणिताचे topic-wise संच आहेत.") ] ),

dict(slug="police-bharti-question-bank", title="पोलीस भरती — 10,000+ जंबो प्रश्नसंच व सराव गाईड", price=149, pages="220 पाने",
 sample_includes=[
   "अंकगणित Short-Trick पान (वर्ग/घन जलद कसे काढायचे)",
   "बुद्धिमत्ता चाचणी — 8 प्रश्न स्पष्टीकरणासह",
   "मराठी व्याकरण व GK चे प्रत्येकी 1 नमुना संच"],
 full_includes=[
   "10,000+ निवडक प्रश्न — अंकगणित, बुद्धिमत्ता, मराठी, GK, संगणक",
   "प्रत्येक विषयाची 'सूत्र-पट्टी' व 1-ओळ Short Tricks",
   "जिल्हानिहाय मागील कट-ऑफ टेबल (Physical व Written)",
   "20 मिनिटांच्या 15 Daily Practice Sets",
   "फिजिकल टेस्ट मार्गदर्शन — उंची/छाती/धावणे तक्ता"],
 toc=[
   "भाग 1: अंकगणित (2,500 प्रश्न — वेग, नफा-तोटा, काळ-काम, सरासरी, %) ",
   "भाग 2: बुद्धिमत्ता (2,200 प्रश्न — मालिका, सांकेतिक भाषा, आकृत्या)",
   "भाग 3: मराठी व्याकरण (1,800 प्रश्न — समानार्थी, समास, संधि, रूढ प्रयोग)",
   "भाग 4: सामान्य ज्ञान (2,500 प्रश्न — महाराष्ट्र GK, घटना, विज्ञान)",
   "भाग 5: संगणक व IT (600 प्रश्न)",
   "भाग 6: 15 Daily Practice Sets (प्रत्येकी 50 प्रश्न, 20 मिनिटे)",
   "अनुबंध: Physical Standards + कट-ऑफ 2023–2025"],
 sections=[
   ("h2", "अंकगणित Short-Trick नमुना"),
   ("p", "85 चा वर्ग 5 सेकंदात: एकक अंक 5 असेल तर → (8 × 9) | 25 = 7225. नियम: पहिले अंक × (तोच + 1), मag 25 जोडा."),
   ("p", "आणखी एक: कुठल्याही 2-अंकी × 11 → मधले अंक = बेरीज. उदा. 43 × 11 = 4|7|3 = 473 (4+3=7 मध्ये)."),
   ("mcq", "सराव: 95 × 95 = ?",
        ["8,925", "9,025", "9,125", "9,525"], 1,
        "(9×10)|25 = 9025 — वरील trick ने 3 सेकंदात!"),
   ("pagebreak",),
   ("h2", "बुद्धिमत्ता चाचणी नमुना (8 पैकी 4)"),
   ("mcq", "प्र. 1) मालिका: AZ, BY, CX, DW, ?",
        ["EV", "EU", "FV", "EX"], 0,
        "पहिले अक्षर +1, दुसरे −1 → EV."),
   ("mcq", "प्र. 2) जर 'POLICE' = 'QPMJDF', तर 'BHARTI' = ?",
        ["CIBSUJ", "CIBSUJ", "DIBSUJ", "CIBTUI"], 0,
        "प्रत्येक अक्षर +1 → CIBSUJ."),
   ("mcq", "प्र. 3) एक माणूस उत्तरेस 5 किमी, नंतर उजवीकडे 3 किमी, पुन्हा उजवीकडे 5 किमी चालतो. आता तो कोणत्या दिशेला आहे?",
        ["उत्तर", "दक्षिण", "पूर्व", "पश्चिम"], 1,
        "उत्तर→(उजवे)पूर्व→(उजवे)दक्षिण. शेवट दक्षिण दिशेने."),
   ("mcq", "प्र. 4) विषम पर्याय ओळखा: 121, 144, 169, 196, 225, 250",
        ["250", "225", "196", "121"], 0,
        "इतर सर्व पूर्ण वर्ग (11²–15²); 250 वर्ग नाही."),
   ("bullets", ["पूर्ण PDF: अशे 2,200 बुद्धिमत्ता प्रश्न विषयवार!", "प्रत्येक संचानंतर 1-ओळ trick दिलेली आहे"]) ] ),

dict(slug="talathi-vocabulary-master", title="तलाठी व सरळसेवा — मराठी + इंग्रजी शब्दसंग्रह मास्टर", price=99, pages="120 पाने",
 sample_includes=[
   "समानार्थी शब्द — 20 वारंवार विचारले जाणारे (TCS pattern)",
   "विरुद्धार्थी शब्द — 10 महत्त्वाचे",
   "English Idioms + One Word Substitution — प्रत्येकी नमुना"],
 full_includes=[
   "5,000+ TCS/IBPS रिपीटेड शब्दसंग्रह — विषयवार वर्गीकरण",
   "समानार्थी 1,200+, विरुद्धार्थी 900+, म्हणी-वाक्प्रचार 600+",
   "English: Idioms 400+, One Word Substitution 350+, Synonyms/Antonyms",
   "प्रत्येक शब्दासोबत वाक्यातील वापर (उदाहरण)",
   "50 'Confusing Pairs' — तडफाने/तडफडाने वगैरे स्पष्टीकरणासह"],
 toc=[
   "भाग 1: समानार्थी शब्द (1,200+) — वर्णमाला क्रमाने",
   "भाग 2: विरुद्धार्थी शब्द (900+)",
   "भाग 3: म्हणी व वाक्प्रचार (600+) — अर्थ + वापर",
   "भाग 4: एक शब्द अनेक अर्थ (350+)",
   "भाग 5: English Idioms (400+) — meaning + example",
   "भाग 6: One Word Substitution (350+)",
   "भाग 7: Confusing Word Pairs (50) — फरक स्पष्ट",
   "भाग 8: TCS-रिपीटेड TOP-500 रेव्हिजन लिस्ट"],
 sections=[
   ("h2", "नमुना: समानार्थी शब्द (TOP-20)"),
   ("table", ("शब्द", "समानार्थी शब्द", "TCS मध्ये (वेळा)"),
        [("अग्नि", "वह्नी, अनल, पावक, हुताशन", "14"),
         ("सूर्य", "रवी, भास्कर, दिनकर, आदित्य", "12"),
         ("चंद्र", "इंदू, शशांक, सोम, निशाकर", "11"),
         ("परवानगी", "सर्व", "9"),
         ("वादळ", "तुफान, आंदडी, चक्रीवादळ", "8"),
         ("शत्रु", "रिपू, वैरी, दुष्मन", "7")],
        (2, 5, 2)),
   ("note", "🧠 Memory Trick: 'रवी-भास्कर आदित्याच्या रथावर दिनकर बनले' — सूर्याचे 4 पर्याय एका वाक्यात!"),
   ("pagebreak",),
   ("h2", "नमुना: English Idioms (5)"),
   ("table", ("Idiom", "Meaning (मराठी)", "वापर"),
        [("A piece of cake", "फार सोपे काम", "The TCS exam was a piece of cake for her."),
         ("Hit the books", "मन लावून अभ्यास करणे", "I need to hit the books for Talathi exam."),
         ("Once in a blue moon", "क्वचितच / कधीच नाहीसे", "He visits us once in a blue moon."),
         ("Break the ice", "संकोच दूर करणे", "The teacher broke the ice with a joke."),
         ("Burn the midnight oil", "रात्रपाळी अभ्यास करणे", "She burnt the midnight oil before MPSC.")],
        (2, 2, 4)),
   ("h2", "नमुना: One Word Substitution"),
   ("mcq", "'जो सर्वजंत माहीत करतो / सर्वशास्त्रज्ञ' — एका शब्दात?",
        ["Polyglot", "Omniscient", "Optimist", "Orator"], 1,
        "Omniscient = सर्वज्ञ. Polyglot = अनेक भाषा जाणणारा, Orator = वकता."),
   ("mcq", "'म्हणीचा उपयोग करा': 'नाच न जाने आंगन टेढे' याचा अर्थ काय?",
        ["काम न करणे", "स्वतःची कमतरता परावर ढकलणे", "नृत्याची आवड", "अभिमान करणे"], 1,
        "स्वतःला न जमलेले दोष परिस्थितीवर ढकलणे — TCS आवडता प्रश्न!") ] ),

dict(slug="maharashtra-gk-atlas-ebook", title="महाराष्ट्र भूगोल व जिल्हावार ॲटलास E-Book 2026", price=99, pages="150 पाने",
 sample_includes=[
   "1 जिल्ह्याचा संपूर्ण नमुना पेजलेआउट (नाशिक — नकाशा-सारांश तक्ता)",
   "नद्या-धरणे टेबल कसे दिले आहे (30 पैकी 6)",
   "36 जिल्हा क्रमवारी trick"],
 full_includes=[
   "36 जिल्ह्यांचे कोटा: नकाशा-वर्णन, नद्या, धरणे, खनिजे, वने, पर्यटन, हवामान",
   "30+ नद्या-धरण तक्ते व 25 कॅलरी ट्रिक्स",
   "रंगीत PDF — मोबाईल Zoom-फ्रेंडली मजकूर",
   "जिल्हा-वाइज मुख्य योजना व पुरस्कार",
   "2024–25 चालू सर्व बदल: नवीन नगरपालिका, मेट्रो, रिंग रोड"],
 toc=[
   "Section 1: महाराष्ट्र — विस्तार, सीमा, हवामान, खनिज भांडार",
   "Section 2: कोकण विभाग (7 जिल्हे) ",
   "Section 3: पश्चिम महाराष्ट्र / देश (पुणे, सातारा, सांगली, कोल्हापूर, सोलापूर)",
   "Section 4: मराठवाडा (8 जिल्हे) ",
   "Section 5: विदर्भ (11 जिल्हे — अमरावती+नागपूर)",
   "Section 6: खानदेश/उत्तर महाराष्ट्र (नाशिक, जळगाव, धुळे, नंदुरबार, अहिल्यानगर)",
   "Section 7: नद्या व धरणे मास्टर तक्ते (30+)",
   "Section 8: राष्ट्रीय उद्याने, अभयारण्य, पर्यटन स्थळे"],
 sections=[
   ("h2", "नमुना पेजलेआउट: नाशिक जिल्हा"),
   ("table", ("घटक", "तपशील"),
        [("मुख्यालय व कोटा", "नाशिक — 'द्राक्षांचे शहर', त्र्यंबकेश्वर (गोदावरी उगम)"),
         ("नद्या", "गोदावरी, दामा, कडवा, गिरणा"),
         ("प्रमुख धरणे", "गंगापूर, कडवा, भडकली"),
         ("खनिज/उद्योग", "द्राक्षे, कांदा, वाइन पार्क, मिसळ, हिंग-उद्योग"),
         ("पर्यटन", "त्र्यंबकेश्वर, पंचवटी, सप्तशृंगी, पांडवलेणी")],
        (2, 6)),
   ("note", "🗺️ 36 जिल्हा क्रम trick: 'कंपास पद्धत' — पश् chokण→देश→खानदेश→मराठवाडा→विदर्भ घड्याळ-दिशेने फिरा, 36 लक्षात राहतात!"),
   ("pagebreak",),
   ("h2", "नमुना: नद्या-धरणे तत्त्पट्टी (30 पैकी 6)"),
   ("table", ("नदी", "उगम", "प्रमुख धरण", "जिल्खा"),
        [("गोदावरी", "त्र्यंबकेश्वर", "जॉयकवाडी (पैठण)", "नाशिक-छ. संभाजीनगर"),
         ("कृष्णा", "महाबळेश्वर", "कोयना, उजनी", "सातारा-सांगली"),
         ("भीमा", "भीमाशंकर", "उजनी (भीमा)", "पुणे-सोलापूर"),
         ("तापी", "मुलताई (बैतूल)", "हतनूर, उकाई", "जळगाव-धुळे"),
         ("मुठा-मुळा", "पुणे परिसर", "खडकवासला, मुळशी", "पुणे"),
         ("वर्धा-वैनगंगा", "MP", "तलकोणा", "वर्धा-चंद्रपूर")],
        (2, 2, 3, 2)),
   ("p", "पूर्ण PDF मध्ये सर्व 36 जिल्हे व 30+ नद्यांचे असे तक्ते + मनाचा नकाशा उजळण्याच्या tricks आहेत.") ] ),

dict(slug="ncert-foundation-notes", title="NCERT व स्टेट बोर्ड — Basic Concepts फाउंडेशन नोट्स (6-12)", price=149, pages="250 पाने",
 sample_includes=[
   "विज्ञान (Cell → Tissue) — 1 प्रकरणाची पूरी नोट",
   "इतिहास टाइमलाइन कशी दिली आहे (1857–1947 तरखापट्टी)",
   "भूगोल मनाचा नकाशा Trick 1"],
 full_includes=[
   "इयत्ता 6-12 सर्व विषयांच्या मूलभूत संकल्पना सारांश",
   "प्रत्येक प्रकरण: 1-पानी Quick Revision Sheet + Keywords box",
   "600+ MCQ — NCERT/बालभारती आधारित",
   "दोन भाषांत कीवर्ड (Marathi + English) — मराठी माध्यमातून English medium परीक्षांसाठी",
   "Maps, Diagrams व Tables — जसे मूळ पाठ्यपुस्तकात, परंतु सारांशित"],
 toc=[
   "Science: Physics 12 प्रकरणे (गति, ऊर्जा, विद्युत...)",
   "Science: Chemistry 11 प्रकरणे (अणू, आम्ल-क्षार, धातू...)",
   "Science: Biology 14 प्रकरणे (पेशी, चयापचय, पुनरुत्पादन...)",
   "History: प्राचीन ते स्वातंत्र्योत्तर — टाइमलाइन पद्धत",
   "Geography: नकाशा-कौशल्य व 20 मनाच्या नकाशा Tricks",
   "Polity/नागरिकशास्त्र: संकल्पना पिरामिड्स",
   "Economics: 10 मूलभूत संकल्पना (मागणी-पुरवठा, बँकिंग)",
   "MCQ परिशिष्ट: 600 प्रश्न + Answer Key"],
 sections=[
   ("h2", "नमुना प्रकरण: पेशी (Cell) — 1 पानी Quick Revision"),
   ("p", "पेशी = शरीराची रचनात्मक व कार्यात्मक एकक (Robert Hooke, 1665 — cork मध्ये शोध)."),
   ("table", ("पेशी-घटक", "कार्य", "Keyword (Eng)"),
        [("पेशीकला", "अंगकांचे घर — राईबोसोम/माइटोकाँड्रिया", "Cytoplasm"),
         ("माइटोकाँड्रिया", "ऊर्जा निर्मिती (ATP)", "Powerhouse of Cell"),
         ("हरितलवक", "प्रकाशसंश्लेषण (फक्त वनस्पती)", "Chloroplast"),
         ("केन्द्रक", "अनुवंशिक माहिती (DNA)", "Nucleus")],
        (3, 3, 2)),
   ("note", "🔑 Exam Keyword Box: 'Powerhouse' = माइटोकाँड्रिया, 'Suicide bags' = लायसोसोम, 'Protein factory' = राईबोसोम — हे 3 परीक्षेत रोज विचारले जातात!"),
   ("pagebreak",),
   ("h2", "नमुना टाइमलाइन: स्वातंत्र्य चळवळ (1857–1947)"),
   ("table", ("वर्ष", "घटना", "सूत्र"),
        [("1857", "पहिला स्वातंत्र्यलढा", "1857-उठाव"),
         ("1885", "काँग्रेस स्थापना", "AO Hume-बांद्रा"),
         ("1905", "बंगाल फाळणी-स्वदेशी", "लॉर्ड कर्झन"),
         ("1930", "मीठ सत्याग्रह", "दांडी मार्च"),
         ("1942", "चले जाव", "ऑगस्ट क्रांती"),
         ("1947", "स्वातंत्र्य", "15 ऑगस्ट")],
        (1, 4, 3)),
   ("p", "अशा 60+ टाइमलाइन टेबल्स पूर्ण PDF मध्ये — प्रत्येकाशी कीवर्ड MCQ देखील!") ] ),

# ---- Featured $49/$99 notes ----
dict(slug="mpsc-polity-quick-notes", title="MPSC Polity Quick Notes", price=49, pages="45 पाने",
 sample_includes=["अनुच्छेद 12-35 ची Quick टेबल (तशीच PDF मधली)","संघराज्य व राज्य यंत्रणा — 1-पानी फ्लोचार्ट","रिव्हिजन Keyword List (20 नमुना)"],
 full_includes=["घटनेचे सर्व महत्त्वाचे अनुच्छेद — टेबल+ट्रिक","संवैधानिक व गैर-संवैधानिक मंडळे तुलना-तक्ते","रिव्हिजन-अष्टौ थोडक्या उल्लेखनीय मुद्दे","PYQ पॉइंटर्स — कोणता अनुच्छेद किती वेळा","Amendments 42/44/73/74 वगैरे 1-ओळ सारांश"],
 toc=["भारतीय घटना — बनावट व वैशिष्ट्ये (Keywords)","करण्यादृष्ट्या अनुच्छेद 'ट्रिक-टेबल' (1-395)","राष्ट्रपती-PM-संसद: अधिकार फ्लोचार्ट","राज्यपाल-CM-विधानमंडळ","घटना दुरुस्त्या (TOP-25)","संघीय/राज्य यंत्रणा (EC, UPSC, AG, CAG)","Panchayat Raj-73/74 स्पेशल"],
 sections=[
   ("h2","नमुना ट्रिक-टेबल: करण्यादृष्ट्या अनुच्छेदे"),
   ("table",("भाग","विषय","अनुच्छेद","Shortcut"),
        [("भाग 3","मूलभूत हक्क","12-35","'३५ मध्ये हक्क संपले'"),
         ("भाग 4","मार्गदर्शक तत्त्वे","36-51","'३६-५१ आयर्लंड'"),
         ("भाग 4A","मूलभूत कर्तव्ये","51A","'४२वी दुरुस्ती-रशिया'"),
         ("भाग 5","संघ यंत्रणा","52-151","'५२-राष्ट्रपती सुरू'"),
         ("भाग 6","राज्य यंत्रणा","152-237","")],
        (2,2,2,3)),
   ("mcq","घटनात्मक दुरुस्ती क्र. 42 ने कोणता भाग जोडला?",["भाग 4A","भाग 9A","भाग 10","भाग 11"],0,
        "42 वी दुरुस्ती (1976) — मूलभूत कर्तव्ये (भाग 4A, अनुच्छेद 51A) जोडली."),
   ("mcq","'GST परिषद' कोणत्या अनुच्छेदान्वये?",["279A","280","263","312"],0,
        "अनुच्छेद 279A — 2016 ची 101 वी दुरुस्ती."),
   ("p","पूर्ण रुद्र PDF मध्ये अशी 45 पाने टेबल्स+ट्रिक्स — रिव्हिजनला 2 तास पुरेसे!")]),

dict(slug="upsc-current-affairs-starter", title="UPSC Current Affairs Starter", price=49, pages="60 पाने",
 sample_includes=["एका महिन्याची खरी Monthly Format (डिसेंबर 2025)","TOP-10 दिवस भरतीच्या घडामोडी टेबल","गती वजन कसे करायचे — PIB Shorts नमुना"],
 full_includes=["महिन्यानिहाय One-Liner + Short Explainer","विषयवार टॅगिंग: Polity/Economy/Env/Sci/India-World","PYQ लिंक — समान मागील UPSC प्रश्न दाखवलेले","'Revision Bullet Box' — फक्त कळी शिपटात","पुढील 12 महिने अपडेट — एकदाच खरेदीवर"],
 toc=["दिलेल्या महिन्याचे TOP-50 One-Liners","राष्ट्रीय — धोरण, योजना, अहवाल","आंतरराष्ट्रीय — करार, शिखर, समारंभ","अर्थव्यवस्था — RBI, रिपोर्ट, सूचकांक","पर्यावरण — निवृत्त प्रकरण, काळी व्हाइल्डलाइफ","सायन्स-टेक — ISRO/DRDO/AI","व्यक्ती/पुरस्कार/क्रीडा","महिन्याचा 25 प्रश्न Self-Test"],
 sections=[
   ("h2","नमुना (डिसेंबर 2025) — One-Liner शैली"),
   ("bullets",["ISRO ने 'Gaganyaan G-2' अक्रू टेस्ट फ्लाइट यशस्वी केली — व्योमी सुरक्षा चाचणी.","RBI ने रेपो दर 6.5% कायम ठेवला — MPC बैठक (गव्हर्नर: संजय मल्होत्रा).","'COP-30' ब्राझीलमध्ये — 1.5°C लक्ष्यवर नवीन कार्यकारी योजना.","भारताने G20 अध्यक्षतेअंतर्गत 'AI सामंजस्य करारा'वर सही."]),
   ("note","📌 Exam Link: ISRO/Gaganyaan — UPSC 2023 मध्ये 'व्योमी मॉड्यूल' विचारले होते. अशी लिंक प्रत्येक घडामोडीखाली दिली आहे!"),
   ("mcq","रिपो दर म्हणजे काय?",["RBI बँकांना देता व्याजदर","बँका RBI कडे ठेवतात दोबार","ग्राहक कर्जदर","सरकारी रोखे दर"],0,
        "Repo = बँकांना RBI अल्पावधी कर्ज दर. Reverse repo = RBI कडे ठेवी."),
   ("p","पूर्ण Monthly PDF मध्ये अशे 50+ One-Liners + सविस्तर Explainers + 25 प्रश्न Self-Test!")]),

dict(slug="mpsc-previous-year-questions", title="MPSC Previous Year Questions (PYQ)", price=99, pages="140 पाने",
 sample_includes=["2015–2025 विषयवार मोड (table)","सोडलेले 8 PYQ उत्तर+टिपासह","रिपीटेड टॉपिक लिस्ट"],
 full_includes=["10 वर्षांच्या प्रश्नपत्रिका विषयवार सोडवलेल्या","प्रत्येक उत्तराखाली 'कनcept Link' — समान प्रश्न कोणत्या वर्षी","रिपीटेड टॉपिक TOP-30 (कádaram घडामोडी)","परीक्षा-विश्लेषण चार्ट्स","उत्तरलेखन मंत्र — वेळेचे नियोजन"],
 toc=["इतिहास व महाराष्ट्र — 190 प्रश्न","राज्यघटना — 230 प्रश्न","भूगोल — 160 प्रश्न","अर्थव्यवस्था — 140 प्रश्न","विज्ञान व तंत्र — 150 प्रश्न","चालू घडामोडी संचित","बुद्धिमत्ता+अंकगणित","रिपीटेड टॉपिक TOP-30"],
 sections=[
   ("h2","नमुना: सोडलेले PYQ"),
   ("mcq","(2023) 'द्रौपदी मुर्मू' यांच्या निवडीबद्दल — राष्ट्रपती निवडणूक मतदान कसं?",["प्रत्यक्ष","अप्रत्यक्ष प्रातिनिधिक","सार्वभौम","प्राधान्य"],1,
        "राष्ट्रपती = अप्रत्यक्ष, प्रातिनिधिक तत्त्ववर एकल संक्रमणीय मतपद्धतीने."),
   ("mcq","(2022) खाजगी क्षेत्राविरोधी — 'श्रमिक कल्याण कोष' कोणत्या कायद्याखाली?",["कामगार कायदा 1948","महाराष्ट्र कल्याण 2017","अपंग 2016","१०वी दुरुस्ती"],1,
        "महाराष्ट्र कल्याण कोष कायदा 2017 — राज्य-विशिष्ट प्रश्न रिपीट!"),
   ("mcq","(2021) 'W-2' उपग्रह म्हणजे?",["पुस्तक","भूप्रेक्षण EOS","दूरव्यवसाय","हवामान"],1,
        "EOS-Nisar प्रेक्षण मालिका — विषय-लिंक: ISRO मोहिमा मोठ्या प्रमाणात."),
   ("h2","रिपीटेड टॉपिक TOP-30 (नमुना 5)"),
   ("table",("टॉपिक","वर्षे (2015-25)","वेळा"),
        [("मूलभूत हक्क","१६,१७,१९,२१,२३","५"),("GST","१७,१८,२०,२२,२४","५"),("गोदावरी घोल","१५,१८,२१,२४","४"),("ISO मानक","१६,१९,२३","३"),("शिवकाळीन कर","१५,१७,२०,२२,२५","५")],(3,4,2)),
   ("p","अशी माहिती 140 पानांत — फक्त जे रिपीट होते, तेच अभ्यासून वेळ वाचवा!")]),

dict(slug="upsc-polity-mcq-set", title="UPSC Polity MCQ Set", price=99, pages="110 पाने",
 sample_includes=["15 अनुक्रमित MCQ उत्तरांसह","स्व-मूल्यमापन स्कोअरशीट","सामान्य चुका-ट्रॅप निर्देश"],
 full_includes=["800+ Topic-wise MCQ (कनstitution फ्रेमवर्क ते Amendments)","प्रत्येक उत्तराखाली 1-ओळ स्पष्टीकरण","प्रत्येक चॅप्टरची 'Trap Alerts'","3 Self-Score शीट्स ट्रॅकिंगसाठी","Prelims Ready-Reckoner ॲपेंडिक्स"],
 toc=["Historical Background & Making","Preamble & Union Territories","Fundamental Rights/Duties","DPSP","President/PM/Parliament","Judiciary","State Govt & Local Bodies","Constitutional Bodies","Amendments & Schedules","800+ प्रश्न + Self-Score"],
 sections=[
   ("h2","नमुना MCQ (15 पैकी 5)"),
   ("mcq","प्रस्तावना '42वी दुरुस्ती' ने कोणते शब्द जोडले?",["समाजवादी, धर्मनिरपेक्ष, अखंडता","लोकशाही, प्रजासत्ताक, धर्म","स्वातंत्र, समता, बंधुता","न्याय स्वातंत्र्य"],0,
        "42 वी दुरुस्ती (1976) — 'Socialist, Secular, Integrity' जोडले."),
   ("mcq","अनुच्छेद 368 — घटना दुरुस्तीची प्रक्रिया?",["साधा बहुमत","विशेष बहुमत","2/3 व अर्धी राज्ये","राज्यपाल"],1,
        "368 — प्रत्येक सभागृहात सदस्यांचे बहुमत व मतदान करणाऱ्यांचे 2/3."),
   ("mcq","'राष्ट्रीय विकास परिषदेचे' अध्यक्ष?",["राष्ट्रपती","PM","केंद्रीय आरआज मंत्री","निती उपाध्यक्ष"],1,
        "NDC — PM अध्यक्ष. (निती आयोगाला PM हेच अध्यक्ष!)"),
   ("mcq","'Money Bill' निर्णय अंतिम कोणाचा?",["राष्ट्रपती","लोकसभा अध्यक्ष","अर्थमंत्री","राज्यसभा सभापती"],1,
        "अनुच्छेद 110(3) — अध्यक्षाचा निर्णय अंतिम."),
   ("mcq","PIL म्हणजे?",["Public Interest Litigation","Private Inquiry List","Public India Law","Principal Int Law"],0,
        "Public Interest Litigation — जनहित याचिका (जस्टीस भागवती)."),
   ("p","पूर्ण PDF: अशे 800+ प्रश्न — Traps टाळून 80%+ गोल करा!")]),

dict(slug="csat-practice-starter", title="CSAT Practice Starter", price=49, pages="70 पाने",
 sample_includes=["Daily Sheet 1 — अशी प्रत्येक पाने","10 सराव प्रश्न (Reasoning+Quant)","Comprehension Shortcut नमुना"],
 full_includes=["60 Daily Practice Sheets (25-30 मिनिटे/दिवस)","Reasoning 400 + Quant 350 + Comprehension 150 प्रश्न","प्रत्येक Sheet ची 10 प्रश्न उत्तर+Hint","CSAT qualifying 33% धोरण स्पष्ट","सूत्र-पट्टी वेगवान वर्गीकरणासाठी"],
 toc=["Daily Sheets 1-60 (वारी मिश्रित)","Reasoning: मालिका/सांकेतिक/दिशा/रक्तसंबंध","Quant: संख्या, सरासरी, %, वेग-वेळ","Comprehension 50 passages","Formula व Shortcut Appendix","7-Day Starter Plan"],
 sections=[
   ("h2","नमुना Daily Sheet — Day 1 (10 प्रश्नांपैकी 5)"),
   ("mcq","प्र.1) मालिका: 2, 6, 12, 20, 30, ?",["36","40","42","44"],2,"n(n+1) → 6×7=42."),
   ("mcq","प्र.2) 20% चा 30% = ?%",["6","15","50","60"],0,"20%×30% = 6%."),
   ("mcq","प्र.3) एका कामात 12 माणसे 8 दिवस, तर 6 माणसे किती?",["14","16","18","20"],1,"M1D1=M2D2 → 16 दिवस."),
   ("mcq","प्र.4) रक्तसंबंध: 'तिच्या बहिणीचा मुलगा माझा भाऊ' — ती माझी कोण?",["आई","मावसी/आत्या","बहीण","मामी"],1,"बहिणीचा मुलगा भाऊ → ती मावसी/आत्या."),
   ("mcq","प्र.5) साठीची 20% सूट — अंतिम दर ₹80 असेल मूळ?",["96","104","100","112"],2,"80 = 80% of 100."),
   ("p","अशी 60 Sheets — रोज 25 मिनिटे, CSAT आरामात qualify!")]),

dict(slug="maharashtra-gk-revision-pack", title="Maharashtra GK Revision Pack", price=99, pages="80 पाने",
 sample_includes=["1-पानी महाराष्ट्र ॲट-ए-ग्लान्स","36 जिल्हा एकलही-ओळी सारांश (नमुना 8)","योजना Quick List"],
 full_includes=["36 जिल्हा 1-ओळ फॅक्ट शीट्स","महाराष्ट्र इतिहास टाइमलाइन (शिवकाळ→समयुक्त→2025)","सरकार योजना TOP-100 व पुरस्कार","GK One-Liner 1,000+","चालू: मुख्यमंत्री/पालकमंत्री/चिन्ह"]
 ,
 toc=["भूगोल: ५ भाग, पर्वत, नदी, हवामान","इतिहास: सातवाहन ते स्वातंत्र्य","राज्य-प्रशासन व घटना-तरतूद","36 जिल्हा 1-ओळ फॅक्ट","योजना TOP-100 व अहवाल","क्रीडा-पुरस्कार व स्मारके","One-Liner Master List (1,000+)"],
 sections=[
   ("h2","नमुना: जिल्हा 1-ओळ फॅक्ट (36 पैकी 8)"),
   ("bullets",["मुंबई-शहर/उपनगर — आर्थिक राजधानी, गेटवे, BSE","पुणे — ऑक्सफर्ड ऑफ ईस्ट, IT/ऑटो हब, खडकवासला","नागपूर — ऑरेंज सिटी, उपराजधानी (हीवाली अधिवेशन)","नाशिक — कुंभमेळा, द्राक्षे, त्र्यंबकेश्वर","छ. संभाजीनगर — अजिंठा-वेरूळ, अजिंठा डोळा","अमरावती — अंबादेवी, चिखलदारा हिलस्टेशन","कोल्हापूर — महालक्ष्मी, पंचगंगा, चप्पल","सातारा — कास पठार (UNESCO), कोयना"]),
   ("h2","शिवकाळीन कर (TOP-5 रिपीटेड)"),
   ("table",("कर","प्रमाण/खाते","उद्देश"),[("चौथ","25%","संरक्षण कर"),("सरदेशमुखी","चौथावर 10%","देशमुखांना"),("बाबती/उदकनी","जमीन-शुल्क","स्थानिक"),("इनाम","मोफत जमीन","धार्मिक/पुरस्कार"),("घासदाणा","इतर कर","गाव खर्च")],(2,2,2)),
   ("p","अशी 80 पाने + 1,000 One-Liners — रिव्हिजनला 1 दिवस पुरेसा!")]),

dict(slug="police-bharti-complete-guide", title="Police Bharti Complete Guide", price=99, pages="130 पाने",
 sample_includes=["फिजिकल स्टँडर्ड तक्ता (तोच PDF मधला)","लेखी सिलॅबस वेगानिर्धारित वजन","8 गुंतागुंती प्रश्न स्पष्टीकरणासह"],
 full_includes=["शारीरिक+लेखी दुहेरी संपूर्ण मार्गदर्शक","1600 मी रन प्लॅन — 4-आठवड्यांचा वैयक्तिक शेड्यूल","लेखी 100 गुण — विषयवार मॉडल पेपर्स","उंची-छाती-वजन टेबल्स","मुलाखत/मेडिकल टिप्स",],
 toc=["भर्ती प्रक्रिया flowchart (10 पायऱ्या)","फिजिकल स्टँडर्ड (पुरुष/महिला)","1600m रन 4-आठवडा प्लॅन","लेखी सिलॅबस वजन-निर्धारण","10 मॉडल पेपर्स (100 गुण)","मेडिकल/डॉक्युमेंट चेकलिस्ट"],
 sections=[
   ("h2","नमुना: फिजिकल स्टँडर्ड तक्ता"),
   ("table",("घटक","पुरुष (Open)","महिला"),[("उंची","165 सेमी","157 सेमी"),("छाती","79-84 सेमी","—"),("वजन","50 किग्रे+","—"),("1600 मी","5:30 मिनि","—"),("800 मी","—","4:00 मिनि"),("शॉटपुट/लांब उडी","7.26 कि / 4 मि","4 कि / 3 मि")],(3,2,2)),
   ("note","⚖️ OBC/SC-ST उंची-सवलत: 5 सेमी — नियम 2024 प्रमाणे; तपशील पूर्ण गाइडमध्ये."),
   ("mcq","सराव: थोडक्यात काडी 6 वाजता घड्याळात — कोन किती?",["180°","175°","165°","150°"],0,"6 वाजता दोन्ही काटे विरुद्ध → 180°."),
   ("mcq","मालिका: 1, 4, 9, 25, 64, ?",["100","121","144","169"],3,"अनुक्रमे 1²,2²,3²,5²,8² (फिबोनाची पाये) → 13²=169."),
   ("p","लेखीचे 10 मॉडल पेपर्स + शारीरिक शेड्यूल एकच PDF मध्ये!")]),

dict(slug="talathi-bharti-guide", title="Talathi Bharti Guide", price=99, pages="120 पाने",
 sample_includes=["सिलॅबस + नमुना महसूल अर्थ","8 सराव प्रश्न","टाकघर-फॉर्म मराठी सूचना"],
 full_includes=["संपूर्ण सिलॅबस विषयवार मार्गदर्शक","महसूल विषय — अन्य/लेखाप्रणाली सोपा","1,500+ प्रश्न उत्तरांसह","TCS Pattern कम्प्युटर टिप्स","कट-ऑफ 2019/2023 विश्लेषण"],
 toc=["तलाठी/महसूल अधिकारी — महीती","सिलॅबस वेब निर्धारण","महसूल विषय मूलभूत (30 प्रकरणे)","मराठी/इंग्रजी/GK/गणित-बुद्धिमत्ता","1,500 प्रश्नसंच","TCS परीक्षा पद्धत मार्गदर्शक"],
 sections=[
   ("h2","नमुना: महसूल विषय मूलभूत"),
   ("p","तलाठी = गावाचा महसूल अधिकारी. मुख्य कामे: मोजमाप (७/१२), जुना-नवीन पुरावा, कळम नोंदी, शुद्धिपत्रक वंत्रतू."),
   ("table",("संज्ञा","अर्थ"),[("७/१२ उतारा","जमीन मालकीचा सारांश पुरावा"),("कळम-नोंद","मालकी/हस्तांतरण बदल नोंद"),("शुद्धिपत्रक","आकारमान दुरुस्ती/चूकांमधील नोंद"),("गट-क्रमांक","गावातील सर्वेक्षण क्र."),("मोजणी","माप प्रक्रिया (Chain/GPS)")],(2,5)),
   ("mcq","७/१२ वर 'इतर हक्क' नोंद कळम कोणती?",["कळम 5","कळम 6","कळम 9","कळम 12"],2,"कळम 9 — इतर हक्क (वारस, कर्ज, इ)."),
   ("mcq","समास: 'चैत्रातला चंद्र' = 'चैत्रचंद्र' — कोणता?",["तत्पुरुष","द्विगू","कर्मधारय","बहुव्रीही"],2,"समान विभक्ती, विशेषण-विशेष्य → कर्मधारय."),
   ("p","महसूल विषय + 1,500 प्रश्न अशा साध्या भाषेत पूर्ण 120 पानांत!")]),

dict(slug="job-application-kit-for-freshers", title="Job Application Kit for Freshers", price=49, pages="50 पाने",
 sample_includes=["ATS-फ्रेंडली Resume टेम्पलेट (1 पान)","5 खास Interview Q&A","Cover Letter फ्रेम"],
 full_includes=["6 ATS Resume टेम्पलेट्स (वर/various मागणी)","50+ Interview Q&A मराठी+इंग्रजी","शब्द-सूची: Action Verbs 100+","Cover-Letter 4 प्रकार","LinkedIn/Offer-लेटर checklists"],
 toc=["ATS म्हणजे काय? + चुका","6 Resume Templates","6 Cover Letter Frames","Interview 50 Q&A","HR Round Secrets","LinkedIn व Job Portals गाइड","Offer बराबर checklist"],
 sections=[
   ("h2","नमुना: STAR Method — Interview"),
   ("p","STAR = Situation → Task → Action → Result. प्रत्येक अनुभव हा मजबूत ठरवा. उदा: 'टीममध्ये काम'चा प्रश्न → कॉलेज प्रोजेक्ट STAR ने सांगा."),
   ("table",("प्रश्न","चुकीचे उत्तर","STAR उत्तर"),[("'Tell about yourself'","संपूर्ण कुटुंब सांगणे","शिक्षण→skills→1 achievement→goal 4-ओळी"),("'Weakness?'","'काहीच नाही'","खरी खूण + सुधारणा-पावले"),("'Why should we hire you?'","'पैसे हवेत'","कौशल्य ↔ कंपनी-गरज जुळवा")],(2,2,3)),
   ("note","💡 Action Verbs: Led, Built, Analyzed, Achieved, Reduced — Resume वाढवतात 40%!"),
   ("mcq","आदर्श Resume लांबी (Fresher)?",["3-4 पाने","2 पाने","1 पान","5 पाने"],2,"Fresher = 1 पान कठोर नियम (ATS friendly)."),
   ("p","50+ अशे Q&A + Templates — पहिल्या नोकरीसाठी सज्ज व्हा!")]),

dict(slug="30-days-english-speaking-practice", title="30 Days English Speaking Practice", price=49, pages="60 पाने",
 sample_includes=["Day-1 Sheet पूरीजशी","50 Daily-use sentences","सामान्य मराठी-चुका Taglish"],
 full_includes=["30 दिवस — रोज 1 पान (Speaking+Listening)","900+ वाक्ये — घर/दुकान/बँक/इंटरव्यू","Self-Record ट्रॅकर शीट्स","Pronunciation टिप्स मराठीत","Common Mistakes कोरrections"],
 toc=["Day 1-10: Basics (Introduction, Daily life)","Day 11-20: Situations (Shop, Bank, Travel)","Day 21-30: Pro Level (Interview, Presentation)","900+ Sentence Bank","Mistake Clinic","Tracker व Motivation"],
 sections=[
   ("h2","नमुना: Day 1 — Introduction Self-Practice"),
   ("table",("मराठी","English","टिप"),[("मी निवडला-समर्थ आहे","I am confident","'मी confident आहे' ⛔"),("मला पुण्यात राहायला आवडते","I like living in Pune","like + -ing"),("तुम्हाला कशी मदत करू?","How may I help you?","May = स्वयंपाकीन नम्र")],(3,3,2)),
   ("p","Daily Routine: 5 वाक्ये मोठ्याने 3 वेळा → आवाज रेकॉर्ड → रात्री स्व-गुण. 30 दिवस = लय बदल!"),
   ("mcq","योग्य इंग्रजी: 'मी काल सिनेमा पाहिला'",["I see movie yesterday","I watched a movie yesterday","I am watching movie tomorrow","Yesterday movie see"],1,"Past tense + article: I watched a movie yesterday."),
   ("p","900+ अशी practical वाक्ये — दररोज 1 पान, बोलायला खरंच सुटते!")]),

dict(slug="student-study-planner", title="Student Study Planner PDF", price=49, pages="40 पाने",
 sample_includes=["Weekly Timetable टेम्पलेट (1 पान)","Goal Tracker नमुना","Rꣁvision Cycle 1-3-7"],
 full_includes=["52 Weekly Planners (Print-ready)","सूत्र 1-3-7 रिव्हिजन चक्र","88-page Goal+Syllabus Trackers","Exam Countdown Sheets","Motivation व Pomodoro Box"],
 toc=["कसे वापरायचे (Start Guide)","Daily Planner 30 पाने","Weekly Timetable 52","Revision 1-3-7 Cycles","Syllabus व Goal Trackers","Exam Countdown + Pomodoro","Motivation Pages"],
 sections=[
   ("h2","नमुना: Weekly Timetable Framework"),
   ("table",("वेळ","सोम-शुक्र","शनि","रवि"),[("05:30-07:30","कठीण विषय (Polity)","PYQ","Mock Test"),("10:00-13:00","विषय 2 + नोट्स","विषय 2","Revision 1-3-7"),("17:00-19:00","GK/Current","Weak topic","Weekly Review"),("21:00-22:00","1-Page रिव्हिजन","प्लॅन अपडेट","Sleep 7h ⏰")],(2,3,2,2)),
   ("note","🔁 1-3-7 Revision Cycle: शिकलेल्या मजकुराची दिवस 1, 3, 7 रिव्हिजन — स्मृति 3X!"),
   ("bullets",["प्रिंट करा किंवा टॅबवर भरा — दोन्ही format","कलर-कोड: कठीण=लाल, मध्यम=पिवळा, सोपा=हिरवा"]),
   ("p","असे 40+ टूल्स — अभ्यास सिस्टीम-बद्द!")]),

dict(slug="mpsc-group-c-vyakaran", title="MPSC Group C — व्याकरण Notes (3 भाषा)", price=99, pages="150 पाने",
 sample_includes=["संधि — नियम+10 उदाहरणे (Mr/Hin/Eng)","समास प्रकार एक-नजर तक्ता","10 सराव प्रश्न उत्तरांसह"],
 full_includes=["संपूर्ण व्याकरण — मराठी+हिंदी+इंग्रजी तिकडी व्याख्या","संधि/समास/अलंकार/वाक्य-प्रकार नियम+उदा","MPSC Group C 2025 PYQ सोडलेले","500+ प्रश्नसंच","TCS ट्रॅप-अलर्ट्स"],
 toc=["वर्ण/विभक्ती/संज्ञा मूलभूत (3 भाषा)","संधि — स्वर/व्यंजन/विसर्ग नियम","समास 6 प्रकार + उदा","अलंकार 12 प्रकार","महणी-वाक्प्रचार-लोकोक्ती","वाक्य-प्रकार व रचना","शुद्धलेखन-सुधारण","500+ PYQ/सराव"],
 sections=[
   ("h2","नमुना: संधि नियम-टेबल (3-भाषा Key)"),
   ("table",("संधि-प्रकार","नियम","उदाहरण","English Rule"),
        [("स्वर संधि","समान/वृद्धि","विद्या+आलय=विद्यालय","Vowel join"),("व्यंजन संधि","परिवर्तन","जगत्+नाथ=जगन्नाथ","Consonant change"),("विसर्ग संधि","स/श/र परिवर्त","निः+शुल्क=निश्शुल्क","Visarga change")],
        (2,2,3,2)),
   ("mcq","'महा+ऋषी' = ?",["महर्षि","महार्षी","म्होर्षी","महऋषि"],0,"आ+ऋ=अर् → महर्षि (गुण स्वर संधि)."),
   ("mcq","'रामायण' कोणता समास?",["तत्पुरुष","बहुव्रीही","कर्मधारय","द्वंद्व"],0,"रामाचे अयन (षष्ठी) → तत्पुरुष."),
   ("note","🎯 Group C-ट्रॅप: 'भिडू' समानार्थी पर्यायात 'भिंडू' अधुरू — शुद्धलेखन प्रश्न स्पेलिंगमध्येच!"),
   ("p","150 पाने: नियम→उदा→सराव हीच methodology 3 भाषांत — एक किट, तीनही परीक्षा!")])
]

if __name__ == "__main__":
    for d in PRODUCTS:
        out = build_product(d)
        print(f"✔ {os.path.basename(out)}  ({os.path.getsize(out)//1024} KB)")
    print(f"\nTotal: {len(PRODUCTS)} sample PDFs in {OUT_DIR}")
