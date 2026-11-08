/**
 * Images: puts images from your images folder into the chapter Docs.
 *
 * Two jobs, each with a preview that writes nothing:
 *
 *   Placing new images
 *     In a Doc, put a paragraph on its own line like this, where the path is inside the images
 *     folder from Settings.gs, and the part after | is the alt text a screen reader reads:
 *         [[IMAGE: chapter-03/pricing-flow.png | Flowchart of the three steps to a price floor]]
 *     1. imagesPlacePreview   lists every placeholder and any image file it can't find.
 *     2. imagesPlace          backs up each Doc, then swaps each placeholder for its image.
 *
 *   Refreshing images you have updated
 *     Every image this tool places remembers its path (as its alt title). After you replace a
 *     file in the images folder with a new version of the same name:
 *     1. imagesRefreshPreview lists the images that would be refreshed.
 *     2. imagesRefresh        backs up each Doc, then swaps in the new file, keeping the width.
 *
 * To work on one Doc only, put its exact name in IMAGES_ONLY_DOC below. Leave it '' for all.
 * If the log says STOPPED, run the same function again; it picks up where it left off.
 */

var IMAGES_ONLY_DOC = '';

var ImagesTool = (function () {

  var TIME_LIMIT_MILLISECONDS = 270000;
  var PLACEHOLDER_PATTERN = /^\[\[IMAGE:\s*([^|\]]+?)\s*(?:\|\s*([^\]]*?)\s*)?\]\]$/;

  function selectedDocs() {
    return EditorEngine.chapterDocs().filter(function (file) {
      return IMAGES_ONLY_DOC === '' || file.getName() === IMAGES_ONLY_DOC;
    });
  }

  /** Finds a file by its path inside the images folder (for example "chapter-03/flow.png"). */
  function imageFile(cache, path) {
    if (cache[path] !== undefined) {
      return cache[path];
    }
    var parts = path.split('/');
    var folder = EditorEngine.folder('imagesFolderId');
    for (var index = 0; index < parts.length - 1 && folder !== null; index = index + 1) {
      var subfolders = folder.getFoldersByName(parts[index]);
      folder = subfolders.hasNext() ? subfolders.next() : null;
    }
    var file = null;
    if (folder !== null) {
      var files = folder.getFilesByName(parts[parts.length - 1]);
      file = files.hasNext() ? files.next() : null;
    }
    cache[path] = file;
    return file;
  }

  function placeholders(body) {
    var range = EditorEngine.chapterRange(body);
    var found = [];
    if (!range.found) {
      return null;
    }
    for (var index = range.first; index <= range.last; index = index + 1) {
      var child = body.getChild(index);
      if (child.getType() !== DocumentApp.ElementType.PARAGRAPH && child.getType() !== DocumentApp.ElementType.LIST_ITEM) {
        continue;
      }
      var match = child.getText().trim().match(PLACEHOLDER_PATTERN);
      if (match) {
        found.push({ paragraph: child, path: match[1], altText: match[2] || '' });
      }
    }
    return found;
  }

  /** Every inline image inside the chapter whose alt title is a path. */
  function placedImages(body) {
    var range = EditorEngine.chapterRange(body);
    var found = [];
    if (!range.found) {
      return null;
    }
    for (var index = range.first; index <= range.last; index = index + 1) {
      var child = body.getChild(index);
      if (!child.findElement) {
        continue;
      }
      var result = child.findElement(DocumentApp.ElementType.INLINE_IMAGE);
      while (result !== null) {
        var image = result.getElement().asInlineImage();
        var path = image.getAltTitle();
        if (path && path.indexOf('/') !== -1) {
          found.push({ image: image, path: path });
        }
        result = child.findElement(DocumentApp.ElementType.INLINE_IMAGE, result);
      }
    }
    return found;
  }

  function targetWidthPixels() {
    return Math.round(EditorEngine.setting('imageWidthCentimeters') / 2.54 * 96);
  }

  function sizeImage(image, widthPixels) {
    var height = Math.round(widthPixels * image.getHeight() / image.getWidth());
    image.setWidth(widthPixels);
    image.setHeight(height);
  }

  function run(job, apply) {
    var startTime = Date.now();
    var cache = {};
    var log = ['=== Images: ' + job + (apply ? '' : ' preview (writes nothing)') + ' ==='];
    var total = 0;
    var docs = selectedDocs();
    for (var docIndex = 0; docIndex < docs.length; docIndex = docIndex + 1) {
      var file = docs[docIndex];
      if (apply && Date.now() - startTime > TIME_LIMIT_MILLISECONDS) {
        log.push('STOPPED before "' + file.getName() + '" to stay under the time limit. Run it again to finish.');
        break;
      }
      var document = DocumentApp.openById(file.getId());
      var body = document.getBody();
      var items = job === 'place' ? placeholders(body) : placedImages(body);
      if (items === null) {
        log.push(file.getName() + ': markers not found, skipped');
        continue;
      }
      var ready = [];
      items.forEach(function (item) {
        item.file = imageFile(cache, item.path);
        if (item.file === null) {
          log.push(file.getName() + ': NO FILE "' + item.path + '" in the images folder (left as it is)');
        } else {
          ready.push(item);
        }
      });
      if (ready.length === 0) {
        continue;
      }
      if (!apply) {
        ready.forEach(function (item) { log.push(file.getName() + ': READY ' + item.path); });
        total = total + ready.length;
        continue;
      }
      try {
        log.push(file.getName() + ': BACKED UP as "' + EditorEngine.backup(file) + '"');
      } catch (error) {
        log.push(file.getName() + ': BACKUP FAILED, nothing changed: ' + error.message);
        continue;
      }
      ready.forEach(function (item) {
        if (job === 'place') {
          item.paragraph.clear();
          var placed = item.paragraph.appendInlineImage(item.file.getBlob());
          sizeImage(placed, targetWidthPixels());
          placed.setAltTitle(item.path);
          placed.setAltDescription(item.altText);
        } else {
          var oldImage = item.image;
          var width = oldImage.getWidth();
          var description = oldImage.getAltDescription();
          var parent = oldImage.getParent();
          var position = parent.getChildIndex(oldImage);
          var container = parent.getType() === DocumentApp.ElementType.LIST_ITEM ? parent.asListItem() : parent.asParagraph();
          var refreshed = container.insertInlineImage(position, item.file.getBlob());
          sizeImage(refreshed, width);
          refreshed.setAltTitle(item.path);
          refreshed.setAltDescription(description);
          oldImage.removeFromParent();
        }
        log.push(file.getName() + ': DONE ' + item.path);
        total = total + 1;
      });
      document.saveAndClose();
    }
    log.push('TOTAL: ' + total + (apply ? ' image(s) changed' : ' image(s) ready'));
    Logger.log(log.join('\n'));
  }

  return { run: run };
})();

function imagesPlacePreview() {
  ImagesTool.run('place', false);
}

function imagesPlace() {
  ImagesTool.run('place', true);
}

function imagesRefreshPreview() {
  ImagesTool.run('refresh', false);
}

function imagesRefresh() {
  ImagesTool.run('refresh', true);
}
