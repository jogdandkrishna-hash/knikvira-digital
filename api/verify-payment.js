/* ============================================================
   KNIKVIRA DIGITAL — Razorpay Payment Verification (serverless)
   ------------------------------------------------------------
   Public check endpoint:  GET /api/verify-payment?pid=<payment_id>&slug=<product>

   Returns `{ ok: true }` only for a captured, INR payment whose amount
   exactly matches the product price. Used by download-smart.html to
   decide whether to show the download link.

   Required environment variables (Vercel → Settings → Environment Variables):
     RAZORPAY_KEY_ID      e.g. rzp_live_TSQwgbmf1nyZxY
     RAZORPAY_KEY_SECRET  (the SECRET key from your Razorpay dashboard — never commit it)
   ============================================================ */

const verifyPayment = require('./_lib/verify');

function cors(res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Cache-Control', 'no-store');
}

module.exports = async function handler(req, res) {
  cors(res);

  if (req.method === 'OPTIONS') {
    res.status(204).end();
    return;
  }

  if (req.method !== 'GET') {
    res.status(405).json({ ok: false, error: 'method_not_allowed' });
    return;
  }

  const pid = (req.query && req.query.pid) || '';
  const slug = (req.query && req.query.slug) || '';

  const result = await verifyPayment(pid, slug);
  res.status(result.status).json({ ok: result.ok, error: result.error });
};
