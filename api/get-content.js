/* ============================================================
   KNIKVIRA DIGITAL — Protected content delivery (serverless)
   ------------------------------------------------------------
   Serves the actual study content ONLY after the payment is verified.

     GET /api/get-content?slug=<product>&pid=<payment_id>
     GET /api/get-content?slug=handwritten-vahi-notes-vol2&pid=<pid>&file=marathi

   The content files live in api/_content/ (NOT served as public static
   files by Vercel — the api/ directory only exposes functions).

   Required environment variables (Vercel → Settings → Environment Variables):
     RAZORPAY_KEY_ID
     RAZORPAY_KEY_SECRET
   ============================================================ */

const path = require('path');
const fs = require('fs');
const { FILES, PDFS } = require('./_lib/catalog');
const verifyPayment = require('./_lib/verify');

const DENIED_HTML = `<!doctype html>
<html lang="mr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Access Denied | Knikvira Digital</title>
<style>
body{min-height:100vh;margin:0;display:flex;align-items:center;justify-content:center;
font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);padding:20px}
.card{background:#fff;border-radius:20px;padding:44px 36px;max-width:460px;width:100%;text-align:center;box-shadow:0 32px 80px rgba(0,0,0,.35)}
h1{font-size:20px;color:#0d1b2a;margin:0 0 10px}
p{font-size:14.5px;color:#475569;line-height:1.7;margin:0 0 20px}
a{display:inline-block;background:#25d366;color:#fff;font-weight:800;text-decoration:none;
padding:13px 22px;border-radius:12px;box-shadow:0 8px 24px rgba(37,211,102,.3)}
</style></head><body>
<div class="card"><h1>⚠️ Access Denied</h1>
<p>हे Notes बघण्यासाठी प्रथम product page वरून <strong>Buy Now</strong> करून payment पूर्ण करा.<br>
या Notes साठी तुम्ही आधीच payment केली असेल तर खालील बटणावर click करा.</p>
<a href="https://wa.me/918421532744" target="_blank">📲 WhatsApp मदत घ्या</a>
</div></body></html>`;

function readContent(rel) {
  // Vercel places the function directory at different paths depending on
  // the runtime; check a few known locations so the file is found reliably.
  const candidates = [
    path.join(__dirname, '_content', rel),
    path.join(process.cwd(), 'api', '_content', rel),
    path.join(process.cwd(), '_content', rel),
  ];
  for (const c of candidates) {
    try { return fs.readFileSync(c); } catch (e) { /* try next */ }
  }
  return null;
}

module.exports = async function handler(req, res) {
  const slug = (req.query && req.query.slug) || '';
  const pid = (req.query && req.query.pid) || '';
  const file = (req.query && req.query.file) || '';

  const v = await verifyPayment(pid, slug);
  if (!v.ok) {
    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    res.setHeader('Cache-Control', 'no-store');
    res.status(403).send(DENIED_HTML);
    return;
  }

  let rel;
  let contentType = 'text/html; charset=utf-8';

  if (file) {
    // PDF variant of the handwritten-vahi-notes-vol2 product.
    if (slug !== 'handwritten-vahi-notes-vol2' || !PDFS[file]) {
      res.status(404).end();
      return;
    }
    rel = PDFS[file];
    contentType = 'application/pdf';
  } else {
    if (!FILES[slug]) {
      res.status(404).end();
      return;
    }
    rel = FILES[slug];
  }

  const buf = readContent(rel);
  if (!buf) {
    res.status(404).end();
    return;
  }

  res.setHeader('Content-Type', contentType);
  res.setHeader('Cache-Control', 'no-store');
  if (contentType === 'application/pdf') {
    res.setHeader(
      'Content-Disposition',
      `inline; filename="${path.basename(rel)}"`
    );
  }
  res.status(200).send(buf);
};
