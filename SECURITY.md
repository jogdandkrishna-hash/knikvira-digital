# 🔐 Payment & Content Security — Knikvira Digital

This document explains how the Razorpay payment flow and the study-content
delivery are secured, what you must configure, and how to verify it works.

---

## How checkout works now

1. Buyer clicks **Buy Now** on any product/bundle page.
2. Razorpay checkout opens (client-side, using the **public** `key`).
3. On success, the popup's `handler` reads `razorpay_payment_id` and redirects to:

   ```
   /download-smart.html?slug=<product>&pid=<payment_id>
   ```

4. `download-smart.html` calls the verification function **before** showing any
   link:

   ```
   GET /api/verify-payment?pid=<payment_id>&slug=<product>
   ```

5. Only if that returns `{ ok: true }` does it reveal a link to the protected
   content endpoint:

   ```
   GET /api/get-content?slug=<product>&pid=<payment_id>
   ```

6. `get-content` re-verifies the payment **server-side** and, only on success,
   streams the study content (HTML or PDF). Without a valid, captured,
   correct-amount payment it returns **403 Access Denied**.

### What verification requires (in both functions)

- `status === "captured"` (money actually taken),
- `currency === "INR"`,
- `amount` **exactly** matches the product's price.

This prevents a ₹49 payment from unlocking a ₹199 kit, rejects failed or
fabricated payment ids, and closes the "just change the URL" bypass.

---

## How content is protected

The 20 study-content pages and the bundle delivery pages were moved out of the
public web root into **`api/_content/`**. Vercel serves the `api/` directory
**only as serverless functions** — files inside it are not exposed as static
assets — so the study material can no longer be opened directly by URL. The
only way to reach it is through `api/get-content.js`, which gates on payment.

The handwritten-notes PDFs were moved into `api/_content/downloads/` and are
served the same way (a single verified payment unlocks all 3 language PDFs).

---

## ⚙️ REQUIRED — Configure your Razorpay secret (once)

In **Vercel → your project → Settings → Environment Variables**, add:

| Name | Value |
|---|---|
| `RAZORPAY_KEY_ID` | `rzp_live_TSQwgbmf1nyZxY` (your live key id) |
| `RAZORPAY_KEY_SECRET` | your live **secret** from Razorpay Dashboard → Settings → API Keys |

Then redeploy. Until `RAZORPAY_KEY_SECRET` is set, the functions **fail closed**
(return `ok: false` / 403), so nothing is served — this is intentional and safe,
but you must set the variable before going live.

> ⚠️ The public `key` (`rzp_live_TSQwgbmf1nyZxY`) already in the HTML is fine to
> keep public — that is how Razorpay is designed. The **secret** is the sensitive
> value; never commit it or share it in chat.

---

## ✅ How to verify it works (after deploy)

1. On a product page, click **Buy Now** and complete a ₹1 test payment
   (temporarily lower a price, or use Razorpay test mode keys).
2. You should land on `download-smart.html` and, after "Verifying…", get the
   download link.
3. Open the link — it must serve the study page (URL starts with
   `/api/get-content`).
4. Try opening the old public URL directly (e.g.
   `/mpsc-rajyaseva-study-kit.html`) — it must now return **404**.
5. Try `/api/get-content?slug=mpsc-rajyaseva-study-kit&pid=madeup` — it must
   return **403 Access Denied**.

---

## Files involved

- `api/_lib/catalog.js` — single source of truth: prices + content file map.
- `api/_lib/verify.js` — shared payment verification.
- `api/verify-payment.js` — public check endpoint (used by the confirmation page).
- `api/get-content.js` — protected content delivery.
- `api/_content/` — the study material (HTML + PDF), not publicly served.
- `download-smart.html` — verifies, then links to the protected endpoint.
- All `*-info.html`, `products.html`, `knikvira_pro.html` — handlers forward `razorpay_payment_id`.
- `package.json` — minimal Node manifest so Vercel treats `/api` as functions.
