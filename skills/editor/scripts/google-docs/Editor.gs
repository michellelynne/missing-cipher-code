/**
 * Editor: the shared engine the other tools use. You never edit or run this file directly.
 *
 * Everything here lives inside one object, EditorEngine, so none of its names can clash with
 * another file in the project. (All .gs files in a project share one global space: two files
 * that each declare the same top-level name break each other.)
 */

var EditorEngine = (function () {

  var TIME_LIMIT_MILLISECONDS = 270000; // stop cleanly before the 6-minute Apps Script limit

  // ---------------------------------------------------------------------------------------
  // Settings, folders, and Docs
  // ---------------------------------------------------------------------------------------

  function setting(name) {
    var value = EDITOR_SETTINGS[name];
    if (value === undefined || String(value).indexOf('PASTE_') === 0) {
      throw new Error('Fill in "' + name + '" in Settings.gs first.');
    }
    return value;
  }

  function folder(settingName) {
    try {
      return DriveApp.getFolderById(setting(settingName));
    } catch (error) {
      throw new Error('Could not open the folder in "' + settingName + '" (Settings.gs). Check the ID. ' + error.message);
    }
  }

  /** Every Google Doc in the chapters folder, sorted by name. */
  function chapterDocs() {
    var files = folder('chaptersFolderId').getFilesByType(MimeType.GOOGLE_DOCS);
    var found = [];
    while (files.hasNext()) {
      found.push(files.next());
    }
    found.sort(function (first, second) {
      return first.getName().localeCompare(second.getName(), undefined, { numeric: true });
    });
    return found;
  }

  /**
   * The one Doc in the chapters folder with exactly this name. Stops if there is none or more
   * than one, because editing the wrong copy is worse than not editing.
   */
  function docByName(docName) {
    var matches = chapterDocs().filter(function (file) {
      return file.getName() === docName;
    });
    if (matches.length === 1) {
      return { file: matches[0] };
    }
    if (matches.length === 0) {
      return { error: 'NO DOC NAMED "' + docName + '" in the chapters folder' };
    }
    var details = matches.map(function (file) {
      return file.getId() + ' (last changed ' + file.getLastUpdated() + ')';
    });
    return { error: matches.length + ' DOCS NAMED "' + docName + '" (fix by hand or remove the extra copy): ' + details.join('; ') };
  }

  function timestamp() {
    return Utilities.formatDate(new Date(), setting('timeZone'), 'yyyy-MM-dd_HH-mm');
  }

  /** Copies the Doc to the backups folder as "Name_YYYY-MM-DD_HH-MM". Throws if it cannot. */
  function backup(file) {
    var backupName = file.getName() + '_' + timestamp();
    file.makeCopy(backupName, folder('backupsFolderId'));
    return backupName;
  }

  // ---------------------------------------------------------------------------------------
  // Chapter boundaries
  // ---------------------------------------------------------------------------------------

  function markerIndex(body, markerText) {
    for (var index = 0; index < body.getNumChildren(); index = index + 1) {
      if (body.getChild(index).getText && body.getChild(index).getText().trim() === markerText) {
        return index;
      }
    }
    return -1;
  }

  /** The range of top-level body children that is the chapter, between the markers. */
  function chapterRange(body) {
    var lastIndex = body.getNumChildren() - 1;
    var startMarker = EDITOR_SETTINGS.startMarker || '';
    var endMarker = EDITOR_SETTINGS.endMarker || '';
    if (startMarker === '' && endMarker === '') {
      return { first: 0, last: lastIndex, found: true };
    }
    var startIndex = markerIndex(body, startMarker);
    var endIndex = markerIndex(body, endMarker);
    if (startIndex === -1 || endIndex === -1 || endIndex < startIndex) {
      return { first: 0, last: -1, found: false };
    }
    return { first: startIndex + 1, last: endIndex - 1, found: true };
  }

  function topLevelIndex(body, element) {
    var current = element;
    while (current.getParent() !== null && current.getParent().getType() !== DocumentApp.ElementType.BODY_SECTION) {
      current = current.getParent();
    }
    return current.getParent() === null ? -1 : body.getChildIndex(current);
  }

  function insideChapter(body, element, range) {
    var index = topLevelIndex(body, element);
    return index >= range.first && index <= range.last;
  }

  // ---------------------------------------------------------------------------------------
  // Finding text
  // ---------------------------------------------------------------------------------------

  /** Turns literal text into a search pattern. A space also matches a nonbreaking space. */
  function searchPattern(literalText) {
    var escaped = literalText.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    return escaped.replace(/ /g, '[  ]');
  }

  function sameText(first, second) {
    return first.replace(/ /g, ' ') === second.replace(/ /g, ' ');
  }

  /** Every exact-case match of the text inside the chapter. */
  function matches(body, literalText, range) {
    var pattern = searchPattern(literalText);
    var results = [];
    var found = body.findText(pattern);
    while (found !== null) {
      var element = found.getElement();
      var matchedText = element.asText().getText().substring(found.getStartOffset(), found.getEndOffsetInclusive() + 1);
      if (sameText(matchedText, literalText) && insideChapter(body, element, range)) {
        results.push(found);
      }
      found = body.findText(pattern, found);
    }
    return results;
  }

  function isTextBlock(element) {
    var type = element.getType();
    return type === DocumentApp.ElementType.PARAGRAPH || type === DocumentApp.ElementType.LIST_ITEM;
  }

  /** Top-level paragraphs inside the chapter whose whole text, trimmed, is exactly this. */
  function paragraphsExactly(body, wantedText, range) {
    var found = [];
    for (var index = range.first; index <= range.last; index = index + 1) {
      var child = body.getChild(index);
      if (isTextBlock(child) && sameText(child.getText().trim(), wantedText.trim())) {
        found.push({ element: child, index: index });
      }
    }
    return found;
  }

  // ---------------------------------------------------------------------------------------
  // Changing text without losing formatting
  // ---------------------------------------------------------------------------------------

  function commonPrefixLength(first, second) {
    var length = 0;
    while (length < first.length && length < second.length && first.charAt(length) === second.charAt(length)) {
      length = length + 1;
    }
    return length;
  }

  function commonSuffixLength(first, second, prefixLength) {
    var length = 0;
    while (length < first.length - prefixLength && length < second.length - prefixLength
      && first.charAt(first.length - 1 - length) === second.charAt(second.length - 1 - length)) {
      length = length + 1;
    }
    return length;
  }

  /**
   * Changes only the characters that differ, so italics, bold, links, and superscripts on the
   * rest of the phrase stay as they are. New characters copy the style of the text they replace.
   */
  function replaceRangeMinimally(textElement, startOffset, endOffset, newText) {
    var currentText = textElement.getText().substring(startOffset, endOffset + 1);
    var prefixLength = commonPrefixLength(currentText, newText);
    var suffixLength = commonSuffixLength(currentText, newText, prefixLength);
    var deleteStart = startOffset + prefixLength;
    var deleteEnd = endOffset - suffixLength;
    var insertText = newText.substring(prefixLength, newText.length - suffixLength);
    var styleOffset = deleteStart;
    if (deleteStart > deleteEnd) {
      styleOffset = Math.max(startOffset, deleteStart - 1);
    }
    var attributes = textElement.getAttributes(styleOffset);
    if (deleteStart <= deleteEnd) {
      textElement.deleteText(deleteStart, deleteEnd);
    }
    if (insertText.length > 0) {
      textElement.insertText(deleteStart, insertText);
      textElement.setAttributes(deleteStart, deleteStart + insertText.length - 1, attributes);
    }
  }

  // ---------------------------------------------------------------------------------------
  // Fix kinds: status (writes nothing) and apply
  // ---------------------------------------------------------------------------------------

  function replaceStatus(fix, body, range) {
    var found = matches(body, fix.find, range);
    if (found.length === 1) {
      return { state: 'READY', match: found[0] };
    }
    var alreadyThere = fix.replace !== '' && matches(body, fix.replace, range).length >= 1;
    if (found.length === 0 && alreadyThere) {
      return { state: 'ALREADY APPLIED' };
    }
    if (found.length === 0 && fix.replace === '') {
      return { state: 'GONE (already deleted, or the text never matched; check by hand)' };
    }
    if (found.length === 0) {
      return { state: 'NOT FOUND (the text has changed; fix by hand)' };
    }
    return { state: 'FOUND ' + found.length + ' TIMES (skipped; make the search text longer, or fix by hand)' };
  }

  function replaceAllStatus(fix, body, range) {
    var found = matches(body, fix.find, range);
    if (found.length >= 1) {
      return { state: 'READY', count: found.length };
    }
    return { state: 'ALREADY APPLIED' };
  }

  function insertAfterStatus(fix, body, range) {
    if (paragraphsExactly(body, fix.text, range).length >= 1) {
      return { state: 'ALREADY APPLIED' };
    }
    var anchors = paragraphsExactly(body, fix.after, range);
    if (anchors.length === 1) {
      return { state: 'READY', anchor: anchors[0] };
    }
    if (anchors.length === 0) {
      return { state: 'NOT FOUND (no paragraph is exactly the "after" text; fix by hand)' };
    }
    return { state: 'FOUND ' + anchors.length + ' TIMES (skipped; fix by hand)' };
  }

  function deleteParagraphStatus(fix, body, range) {
    var found = paragraphsExactly(body, fix.text, range);
    if (found.length === 1) {
      return { state: 'READY', block: found[0] };
    }
    if (found.length === 0) {
      return { state: 'GONE (already deleted, or the paragraph never matched; check by hand)' };
    }
    return { state: 'FOUND ' + found.length + ' TIMES (skipped; fix by hand)' };
  }

  function linkStatus(fix, body, range) {
    var found = matches(body, fix.text, range);
    if (found.length !== 1) {
      return found.length === 0
        ? { state: 'NOT FOUND (the link text has changed; fix by hand)' }
        : { state: 'FOUND ' + found.length + ' TIMES (skipped; fix by hand)' };
    }
    var match = found[0];
    if (match.getElement().asText().getLinkUrl(match.getStartOffset()) === fix.url) {
      return { state: 'ALREADY APPLIED' };
    }
    return { state: 'READY', match: match };
  }

  var KINDS = {
    replace: {
      status: replaceStatus,
      describe: function (fix) { return '"' + fix.find + '"\n      becomes "' + fix.replace + '"'; },
      apply: function (fix, status) {
        var match = status.match;
        replaceRangeMinimally(match.getElement().asText(), match.getStartOffset(), match.getEndOffsetInclusive(), fix.replace);
      }
    },
    replaceAll: {
      status: replaceAllStatus,
      describe: function (fix, status) { return '"' + fix.find + '" becomes "' + fix.replace + '" everywhere (' + status.count + ' times)'; },
      apply: function (fix, status, body, range) {
        var remaining = matches(body, fix.find, range);
        var guard = 0;
        while (remaining.length > 0 && guard < 1000) {
          var match = remaining[0];
          replaceRangeMinimally(match.getElement().asText(), match.getStartOffset(), match.getEndOffsetInclusive(), fix.replace);
          guard = guard + 1;
          remaining = fix.replace.indexOf(fix.find) === -1 ? matches(body, fix.find, range) : [];
        }
      }
    },
    insertAfter: {
      status: insertAfterStatus,
      describe: function (fix) { return 'adds after "' + fix.after + '":\n      "' + fix.text + '"'; },
      apply: function (fix, status, body) {
        var anchor = status.anchor.element;
        var inserted;
        if (anchor.getType() === DocumentApp.ElementType.LIST_ITEM) {
          inserted = body.insertListItem(status.anchor.index + 1, anchor.copy().asListItem());
          inserted.editAsText().setText(fix.text);
        } else {
          inserted = body.insertParagraph(status.anchor.index + 1, fix.text);
          inserted.setHeading(anchor.asParagraph().getHeading());
        }
      }
    },
    deleteParagraph: {
      status: deleteParagraphStatus,
      describe: function (fix) { return 'deletes the paragraph "' + fix.text + '"'; },
      apply: function (fix, status) { status.block.element.removeFromParent(); }
    },
    link: {
      status: linkStatus,
      describe: function (fix) { return 'links "' + fix.text + '" to ' + fix.url; },
      apply: function (fix, status) {
        var match = status.match;
        match.getElement().asText().setLinkUrl(match.getStartOffset(), match.getEndOffsetInclusive(), fix.url);
      }
    }
  };

  function kindOf(fix) {
    var kindName = fix.kind || 'replace';
    if (!KINDS[kindName]) {
      throw new Error('Fix ' + fix.id + ' has an unknown kind "' + kindName + '". Use one of: ' + Object.keys(KINDS).join(', '));
    }
    return KINDS[kindName];
  }

  // ---------------------------------------------------------------------------------------
  // Running a batch of fixes
  // ---------------------------------------------------------------------------------------

  function groupByDoc(fixes) {
    var groups = {};
    var order = [];
    fixes.forEach(function (fix) {
      if (!groups[fix.doc]) {
        groups[fix.doc] = [];
        order.push(fix.doc);
      }
      groups[fix.doc].push(fix);
    });
    return order.map(function (docName) {
      return { docName: docName, fixes: groups[docName] };
    });
  }

  /**
   * mode is 'check' (status only), 'preview' (status plus before and after), or 'apply'.
   * Nothing is written unless mode is 'apply'. Each Doc is backed up before its first change.
   */
  function runFixes(batch, mode) {
    var startTime = Date.now();
    var counts = {};
    var log = ['=== ' + mode.toUpperCase() + ': ' + batch.name + (mode === 'apply' ? '' : ' (writes nothing)') + ' ==='];

    function count(state) {
      var key = state.split(' (')[0];
      counts[key] = (counts[key] || 0) + 1;
    }

    var groups = groupByDoc(batch.fixes);
    for (var groupIndex = 0; groupIndex < groups.length; groupIndex = groupIndex + 1) {
      var group = groups[groupIndex];
      if (mode === 'apply' && Date.now() - startTime > TIME_LIMIT_MILLISECONDS) {
        log.push('STOPPED before "' + group.docName + '" to stay under the time limit. Run it again to finish; finished fixes show ALREADY APPLIED.');
        break;
      }
      var lookup = docByName(group.docName);
      if (lookup.error) {
        log.push(lookup.error + ': ' + group.fixes.length + ' fix(es) skipped');
        group.fixes.forEach(function () { count('SKIPPED'); });
        continue;
      }
      var document = DocumentApp.openById(lookup.file.getId());
      var body = document.getBody();
      var range = chapterRange(body);
      if (!range.found) {
        log.push('"' + group.docName + '": the start and end markers in Settings.gs were not found; ' + group.fixes.length + ' fix(es) skipped');
        group.fixes.forEach(function () { count('SKIPPED'); });
        continue;
      }
      log.push('--- ' + group.docName + ' ---');
      var backedUp = false;
      var changed = 0;
      for (var fixIndex = 0; fixIndex < group.fixes.length; fixIndex = fixIndex + 1) {
        var fix = group.fixes[fixIndex];
        var kind = kindOf(fix);
        var status;
        try {
          status = kind.status(fix, body, range);
        } catch (error) {
          status = { state: 'ERROR (' + error.message + ')' };
        }
        if (mode !== 'apply' || status.state !== 'READY') {
          count(status.state);
          log.push(status.state + ': ' + fix.id);
          if (mode === 'preview' && status.state === 'READY') {
            log.push('      ' + kind.describe(fix, status));
          }
          continue;
        }
        if (!backedUp) {
          try {
            log.push('BACKED UP as "' + backup(lookup.file) + '"');
            backedUp = true;
          } catch (error) {
            log.push('BACKUP FAILED, so nothing in this Doc was changed: ' + error.message);
            for (var skippedIndex = fixIndex; skippedIndex < group.fixes.length; skippedIndex = skippedIndex + 1) {
              count('SKIPPED');
            }
            break;
          }
        }
        try {
          kind.apply(fix, status, body, range);
          changed = changed + 1;
          count('APPLIED');
          log.push('APPLIED: ' + fix.id);
        } catch (error) {
          count('ERROR');
          log.push('ERROR: ' + fix.id + ': ' + error.message);
        }
      }
      if (changed > 0) {
        document.saveAndClose();
      }
    }
    log.push('TOTALS: ' + JSON.stringify(counts));
    if (mode === 'apply') {
      log.push('Run the check again: every fix should now show ALREADY APPLIED or need a hand fix.');
    }
    Logger.log(log.join('\n'));
    return counts;
  }

  // ---------------------------------------------------------------------------------------
  // What the other files may use
  // ---------------------------------------------------------------------------------------

  return {
    setting: setting,
    folder: folder,
    chapterDocs: chapterDocs,
    backup: backup,
    timestamp: timestamp,
    chapterRange: chapterRange,
    runFixes: runFixes
  };
})();
