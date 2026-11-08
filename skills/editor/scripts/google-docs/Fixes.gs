/**
 * Fixes: applies the fixes you approved in a review.
 *
 * Each time you approve fixes (in the conversation, or as FIX marks from an offline review
 * pack), the review gives you a new FIX_BATCH. Replace everything between the two
 * "BATCH" lines below with it, save, and run these in order from the toolbar:
 *
 *   1. fixesCheck     Shows READY, ALREADY APPLIED, or NOT FOUND for every fix. Writes nothing.
 *   2. fixesPreview   Shows each READY fix's before and after text. Writes nothing.
 *   3. fixesApply     Backs up each Doc, then makes the fixes. Running it twice changes nothing.
 *
 * Open the log with View > Logs (or Execution log) to read the results. Anything marked
 * NOT FOUND or FOUND 2 TIMES was skipped for you to fix by hand.
 *
 * Fix kinds (kind is optional; it defaults to replace):
 *   replace          find -> replace. The find text must appear exactly once in the chapter.
 *                    An empty replace ('') deletes the text. Include a few words on each side
 *                    (find 'costs. Now that we... pricing. The', replace 'costs. The') so the
 *                    check can tell a finished deletion from text that never matched.
 *   replaceAll       find -> replace everywhere in the chapter.
 *   insertAfter      adds a new paragraph, text, after the paragraph whose whole text is after.
 *   deleteParagraph  removes the paragraph whose whole text is text.
 *   link             links the text (which must appear once) to url.
 * Search text stays inside one paragraph; a fix can't match across a paragraph break.
 */

// ===== BATCH START: replace from here =====
var FIX_BATCH = {
  name: 'Example batch (replace with the batch from your review)',
  fixes: [
    { id: 'P1-1', doc: 'Chapter 3 Pricing That Pays the Rent', find: 'In order to price labor honestly', replace: 'To price labor honestly' },
    { id: 'P1-2', doc: 'Chapter 3 Pricing That Pays the Rent', kind: 'replaceAll', find: 'store front', replace: 'storefront' },
    { id: 'P1-3', doc: 'Chapter 3 Pricing That Pays the Rent', find: 'Now that we\'ve covered costs, let\'s turn to pricing. ', replace: '' }
  ]
};
// ===== BATCH END: replace to here =====

function fixesCheck() {
  EditorEngine.runFixes(FIX_BATCH, 'check');
}

function fixesPreview() {
  EditorEngine.runFixes(FIX_BATCH, 'preview');
}

function fixesApply() {
  EditorEngine.runFixes(FIX_BATCH, 'apply');
}
