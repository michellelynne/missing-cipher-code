/**
 * Word count: counts the words in every chapter Doc in the chapters folder.
 *
 * Run wordCountRun from the toolbar, then open the log. Only the text between the start and end
 * markers in Settings.gs is counted, so notes kept above or below a chapter are left out.
 * Writes nothing.
 */

var WordCountTool = (function () {

  /** Words are runs of letters or digits, with apostrophes and hyphens inside them allowed. */
  function countWords(text) {
    var words = text.match(/[\p{L}\p{N}]+(?:['’-][\p{L}\p{N}]+)*/gu);
    return words === null ? 0 : words.length;
  }

  function chapterText(document) {
    var body = document.getBody();
    var range = EditorEngine.chapterRange(body);
    if (!range.found) {
      return null;
    }
    var pieces = [];
    for (var index = range.first; index <= range.last; index = index + 1) {
      var child = body.getChild(index);
      if (child.getText) {
        pieces.push(child.getText());
      }
    }
    return pieces.join('\n');
  }

  function run() {
    var log = ['=== Word count (writes nothing) ==='];
    var total = 0;
    var counted = 0;
    EditorEngine.chapterDocs().forEach(function (file) {
      var text = chapterText(DocumentApp.openById(file.getId()));
      if (text === null) {
        log.push(file.getName() + ': markers not found, not counted');
        return;
      }
      var words = countWords(text);
      total = total + words;
      counted = counted + 1;
      log.push(file.getName() + ': ' + words.toLocaleString('en-US'));
    });
    log.push('TOTAL across ' + counted + ' Doc(s): ' + total.toLocaleString('en-US'));
    Logger.log(log.join('\n'));
  }

  return { run: run, countWords: countWords };
})();

function wordCountRun() {
  WordCountTool.run();
}
