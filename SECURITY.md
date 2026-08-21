# 🔐 Payment Security — Knikvira Digital

This document explains how the Razorpay payment flow is secured, what you must
configure, and the one remaining limitation to be aware of.

---

## How checkout works now

1. Buyer clicks **Buy Now** on any product/bundle page.
2. Razorpay checkout opens (client-side, using the **public** `key`).
3. On success, the popup's `handler` reads `razorpay_payment_id` and redirects to:

   ```
   /download-smart.html?slug=<product>&pid=<payment_id>
   ```

4. `download-smart.html` calls the serverless function **before** revealing the
   download link:

   ```
   GET /api/verify-payment?pid=<payment_id>&slug=<product>
   ```

5. The function verifies the payment server-side against Razorpay's API and
   returns `{ ok: true }` **only if** the payment is:
   - `status === "captured"` (money actually taken),
   - `currency === "INR"`, and
   - `amount` **exactly** matches the product's price.

   This prevents a ₹49 payment from unlocking a ₹199 kit, and rejects failed
   or fabricated payment ids. If verification fails, no download link is shown
   — the buyer is directed to WhatsApp support.

---

## ⚙️ REQUIRED — Configure your Razorpay secret (once)

The verification uses your Razorpay **secret key**, which must live server-side
as an environment variable — **never commit it to the repo.**

In **Vercel → your project → Settings → Environment Variables**, add:

| Name | Value |
|---|---|
| `RAZORPAY_KEY_ID` | `rzp_live_TKphKiYGjotBE7` (your live key id) |
| `RAZORPAY_KEY_SECRET` | your live **secret** from Razorpay Dashboard → Settings → API Keys |

Then redeploy. Until `RAZORPAY_KEY_SECRET` is set, the function **fails closed**
(returns `ok: false`), so no downloads will be served — this is intentional and
safe, but it means you must set the variable before going live.

> ⚠️ The public `key` (`rzp_live_TKphKiYGjotBE7`) that already appears in the
> HTML is fine to keep public — that is how Razorpay is designed. The **secret**
> is the sensitive value.

---

## ⚠️ Remaining limitation (please read)

This verification secures the **download confirmation page**, but the actual
study content is currently delivered as **plain `.html` files** (e.g.
`/mpsc-rajyaseva-study-kit.html`) that Vercel serves directly.

**Consequence:** anyone who knows or guesses those URLs can still open the
content without paying. This is inherent to static hosting — server-side
verification alone cannot hide files that the web server is already serving.

### How to close this hole (recommended next step)

Serve the content **only through the verified endpoint** instead of as public
static files:

1. Move the 20 content `.html` files out of direct public serving (e.g. into a
   folder the function reads, or convert them to real PDFs stored privately).
2. Add a function `GET /api/get-content?pid=<pid>&slug=<slug>` that
   (a) verifies the payment (same logic as `verify-payment`), then (b) streams
   the file with `Content-Disposition: attachment`.
3. Point `download-smart.html` at that endpoint instead of the public `.html`.

This is a larger change (it alters the "Ctrl+P → Save as PDF" download UX), so
it should be a deliberate decision. In the meantime the verification above is
still a meaningful improvement: it stops casual link-sharing of the
`download-smart.html?slug=...` confirmation page and enforces price checks.

---

## Files involved

- `api/verify-payment.js` — serverless verification function.
- `download-smart.html` — now verifies via the API before showing the link.
- All `*-info.html`, `products.html`, `knikvira_pro.html` — checkout handlers
  now forward `razorpay_payment_id`.
- `package.json` — minimal Node manifest so Vercel treats `/api` as functions.
