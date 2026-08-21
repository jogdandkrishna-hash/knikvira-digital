/* ============================================================
   KNIKVIRA DIGITAL — Razorpay Payment Verification (serverless)
   ------------------------------------------------------------
   Deployed on Vercel at:  GET /api/verify-payment?pid=<payment_id>&slug=<product>

   Required environment variables (set in Vercel → Project Settings → Environment Variables):
     RAZORPAY_KEY_ID      e.g. rzp_live_TKphKiYGjotBE7
     RAZORPAY_KEY_SECRET  (the SECRET key from your Razorpay dashboard — never commit it)

   What it does:
     1. Takes the Razorpay `payment_id` returned by the checkout popup and the product `slug`.
     2. Fetches the payment record from Razorpay's API using the server-side secret.
     3. Returns `{ ok: true }` ONLY if the payment is CAPTURED, in INR,
        and the amount exactly matches the product price (so a ₹49 payment
        cannot unlock a ₹199 kit).

   ⚠️  This verifies the payment and secures the download *confirmation* page.
       It does NOT (by itself) protect the static .html content pages, which are
       served directly by Vercel. See SECURITY.md for the full picture.
   ============================================================ */

// Expected amount in paise for every product slug. MUST stay in sync with
// the payNow(...) calls in the info pages and the PRODUCTS map in download-smart.html.
const PRICES = {
  // MPSC
  'mpsc-rajyaseva-study-kit': 19900,
  'mpsc-group-c-vyakaran': 9900,
  'mpsc-polity-quick-notes': 9900,
  'mpsc-previous-year-questions': 9900,
  // UPSC
  'upsc-prelims-master-book': 14900,
  'upsc-polity-mcq-set': 9900,
  'upsc-current-affairs-starter': 4900,
  // Police & Talathi
  'police-bharti-complete-guide': 14900,
  'police-bharti-question-bank': 14900,
  'talathi-bharti-guide': 14900,
  'talathi-vocabulary-master': 9900,
  // GK & CSAT
  'maharashtra-gk-revision-pack': 4900,
  'maharashtra-gk-atlas-ebook': 9900,
  'csat-practice-starter': 4900,
  'ncert-foundation-notes': 14900,
  // Notes & Planners
  'handwritten-quick-notes': 9900,
  'handwritten-vahi-notes-vol2': 9900,
  'student-study-planner': 4900,
  '30-days-english-speaking-practice': 4900,
  'job-application-kit-for-freshers': 4900,
  // Bundles
  'bundle-career-ready': 9900,
  'bundle-police-talathi': 17900,
  'bundle-mpsc-complete': 14900,
  'bundle-upsc-prelims': 12900,
};

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
  const expected = PRICES[slug];

  if (!pid || !slug || !expected) {
    res.status(400).json({ ok: false, error: 'invalid_request' });
    return;
  }

  const keyId = process.env.RAZORPAY_KEY_ID;
  const keySecret = process.env.RAZORPAY_KEY_SECRET;

  if (!keyId || !keySecret) {
    // Fail closed if the server-side secret isn't configured.
    res.status(500).json({ ok: false, error: 'not_configured' });
    return;
  }

  try {
    const auth = Buffer.from(`${keyId}:${keySecret}`).toString('base64');
    const apiResp = await fetch(
      `https://api.razorpay.com/v1/payments/${encodeURIComponent(pid)}`,
      { headers: { Authorization: `Basic ${auth}` } }
    );

    if (apiResp.status !== 200) {
      res.status(200).json({ ok: false, error: 'payment_lookup_failed' });
      return;
    }

    const payment = await apiResp.json();

    const ok =
      payment.status === 'captured' &&
      payment.currency === 'INR' &&
      String(payment.amount) === String(expected);

    res.status(200).json({ ok });
  } catch (err) {
    // Never leak internal details.
    res.status(200).json({ ok: false, error: 'verification_error' });
  }
};
