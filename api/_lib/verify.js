/* ============================================================
   KNIKVIRA DIGITAL — Shared Razorpay payment verification
   ------------------------------------------------------------
   Used by both api/verify-payment.js (public check) and
   api/get-content.js (content gate).

   Returns { ok, status, error }.
   `ok` is true ONLY when the payment is CAPTURED, in INR, and the
   amount exactly matches the product's price.
   ============================================================ */

const { PRICES } = require('./catalog');

module.exports = async function verifyPayment(pid, slug) {
  if (!pid || !slug || !PRICES[slug]) {
    return { ok: false, status: 400, error: 'invalid_request' };
  }

  const keyId = process.env.RAZORPAY_KEY_ID;
  const keySecret = process.env.RAZORPAY_KEY_SECRET;

  if (!keyId || !keySecret) {
    // Fail closed if the server-side secret isn't configured.
    return { ok: false, status: 500, error: 'not_configured' };
  }

  try {
    const auth = Buffer.from(`${keyId}:${keySecret}`).toString('base64');
    const resp = await fetch(
      `https://api.razorpay.com/v1/payments/${encodeURIComponent(pid)}`,
      { headers: { Authorization: `Basic ${auth}` } }
    );

    if (resp.status !== 200) {
      return { ok: false, status: 200, error: 'payment_lookup_failed' };
    }

    const payment = await resp.json();
    const ok =
      payment.status === 'captured' &&
      payment.currency === 'INR' &&
      String(payment.amount) === String(PRICES[slug]);

    return { ok, status: 200 };
  } catch (err) {
    // Never leak internal details.
    return { ok: false, status: 200, error: 'verification_error' };
  }
};
