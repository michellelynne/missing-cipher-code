/* eslint-disable no-unused-vars -- this file is joined with the Apps Script files into one bundle by google-docs.test.cjs, which uses these names. */
// Minimal stand-ins for the parts of DocumentApp, DriveApp, Utilities, Logger the engine uses.
var ElementType = { BODY_SECTION: 'BODY_SECTION', PARAGRAPH: 'PARAGRAPH', LIST_ITEM: 'LIST_ITEM', TEXT: 'TEXT', INLINE_IMAGE: 'INLINE_IMAGE' };
function TextNode(paragraph, text) { this.paragraph = paragraph; this.text = text; this.links = {}; }
TextNode.prototype.getText = function () { return this.text; };
TextNode.prototype.getParent = function () { return this.paragraph; };
TextNode.prototype.getType = function () { return ElementType.TEXT; };
TextNode.prototype.asText = function () { return this; };
TextNode.prototype.deleteText = function (start, endInclusive) { this.text = this.text.slice(0, start) + this.text.slice(endInclusive + 1); };
TextNode.prototype.insertText = function (offset, piece) { this.text = this.text.slice(0, offset) + piece + this.text.slice(offset); };
TextNode.prototype.getAttributes = function () { return {}; };
TextNode.prototype.setAttributes = function () {};
TextNode.prototype.getLinkUrl = function (offset) { return this.links[offset] || null; };
TextNode.prototype.setLinkUrl = function (start, end, url) { this.links[start] = url; };
TextNode.prototype.setText = function (value) { this.text = value; };
function Paragraph(body, text) { this.body = body; this.textNode = new TextNode(this, text); }
Paragraph.prototype.getType = function () { return ElementType.PARAGRAPH; };
Paragraph.prototype.getText = function () { return this.textNode.text; };
Paragraph.prototype.asText = function () { return this.textNode; };
Paragraph.prototype.editAsText = function () { return this.textNode; };
Paragraph.prototype.getParent = function () { return this.body; };
Paragraph.prototype.asParagraph = function () { return this; };
Paragraph.prototype.getHeading = function () { return 'NORMAL'; };
Paragraph.prototype.setHeading = function () {};
Paragraph.prototype.removeFromParent = function () { this.body.children.splice(this.body.children.indexOf(this), 1); };
function Body(lines) { var self = this; this.children = lines.map(function (line) { return new Paragraph(self, line); }); }
Body.prototype.getType = function () { return ElementType.BODY_SECTION; };
Body.prototype.getParent = function () { return null; };
Body.prototype.getNumChildren = function () { return this.children.length; };
Body.prototype.getChild = function (index) { return this.children[index]; };
Body.prototype.getChildIndex = function (child) { return this.children.indexOf(child); };
Body.prototype.insertParagraph = function (index, text) { var paragraph = new Paragraph(this, text); this.children.splice(index, 0, paragraph); return paragraph; };
Body.prototype.findText = function (pattern, from) {
  var regex = new RegExp(pattern);
  var startChild = 0; var startOffset = 0;
  if (from) { startChild = this.children.indexOf(from.getElement().getParent()); startOffset = from.getEndOffsetInclusive() + 1; }
  for (var childIndex = startChild; childIndex < this.children.length; childIndex = childIndex + 1) {
    var node = this.children[childIndex].textNode;
    var offset = childIndex === startChild ? startOffset : 0;
    var rest = node.text.slice(offset);
    var match = rest.match(regex);
    if (match) {
      var start = offset + match.index; var end = start + match[0].length - 1;
      return { getElement: function () { return node; }, getStartOffset: function () { return start; }, getEndOffsetInclusive: function () { return end; } };
    }
  }
  return null;
};
var backups = [];
var DOCS = {};
function makeFile(name) {
  return { getName: function () { return name; }, getId: function () { return name; }, getLastUpdated: function () { return 'today'; },
    makeCopy: function (copyName) { backups.push(copyName); } };
}
var DocumentApp = { ElementType: ElementType, openById: function (id) { return { getBody: function () { return DOCS[id].body; }, saveAndClose: function () {} }; } };
var MimeType = { GOOGLE_DOCS: 'doc' };
var DriveApp = { getFolderById: function () { return { getFilesByType: function () {
  var list = Object.keys(DOCS).map(function (name) { return DOCS[name].file; }); var position = 0;
  return { hasNext: function () { return position < list.length; }, next: function () { position = position + 1; return list[position - 1]; } }; } }; } };
var Utilities = { formatDate: function () { return '2026-11-05_01-00'; } };
var output = [];
var Logger = { log: function (text) { output.push(text); } };
