/* ============================================================
   KNIKVIRA DIGITAL — Shared product catalog (server-side)
   ------------------------------------------------------------
   Single source of truth for the Razorpay payment amount and the
   protected content file for every product slug.

   ⚠️  PRICES MUST stay in sync with:
       - the payNow(...) amount argument in every *-info.html page,
       - products.html, knikvira_pro.html, and download-smart.html.
   ============================================================ */

// slug -> amount in paise (₹1 = 100 paise)
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

// slug -> protected content file (relative to api/_content/)
const FILES = {
  'mpsc-rajyaseva-study-kit': 'mpsc-rajyaseva-study-kit.html',
  'mpsc-group-c-vyakaran': 'mpsc-group-c-vyakaran.html',
  'mpsc-polity-quick-notes': 'mpsc-polity-quick-notes.html',
  'mpsc-previous-year-questions': 'mpsc-previous-year-questions.html',
  'upsc-prelims-master-book': 'upsc-prelims-master-book.html',
  'upsc-polity-mcq-set': 'upsc-polity-mcq-set.html',
  'upsc-current-affairs-starter': 'upsc-current-affairs-starter.html',
  'police-bharti-complete-guide': 'police-bharti-complete-guide.html',
  'police-bharti-question-bank': 'police-bharti-question-bank.html',
  'talathi-bharti-guide': 'talathi-bharti-guide.html',
  'talathi-vocabulary-master': 'talathi-vocabulary-master.html',
  'maharashtra-gk-revision-pack': 'maharashtra-gk-revision-pack.html',
  'maharashtra-gk-atlas-ebook': 'atlas-tri.html',
  'csat-practice-starter': 'csat-practice-starter.html',
  'ncert-foundation-notes': 'ncert-foundation-notes.html',
  'handwritten-quick-notes': 'handwritten-quick-notes.html',
  'handwritten-vahi-notes-vol2': 'handwritten-vahi-notes-vol2.html',
  'student-study-planner': 'student-study-planner.html',
  '30-days-english-speaking-practice': '30-days-english-speaking-practice.html',
  'job-application-kit-for-freshers': 'job-application-kit-for-freshers.html',
  'bundle-career-ready': 'bundle-career-ready.html',
  'bundle-police-talathi': 'bundle-police-talathi.html',
  'bundle-mpsc-complete': 'bundle-mpsc-complete.html',
  'bundle-upsc-prelims': 'bundle-upsc-prelims.html',
};

// Optional PDF files served for the handwritten-vahi-notes-vol2 product.
// A single verified payment unlocks all three language PDFs.
const PDFS = {
  marathi: 'downloads/handwritten-vahi-notes-vol2.pdf',
  hindi: 'downloads/handwritten-vahi-notes-vol2-hi.pdf',
  english: 'downloads/handwritten-vahi-notes-vol2-en.pdf',
};

module.exports = { PRICES, FILES, PDFS };
