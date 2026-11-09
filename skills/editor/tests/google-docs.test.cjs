// Tests for the Google Docs editor tools, run against a small stand-in for Google Docs.
// Run from this folder: node google-docs.test.cjs
const fs = require('fs');
const path = require('path');
const assert = require('assert');

const toolsFolder = path.join(__dirname, '..', 'scripts', 'google-docs');
const settings = fs.readFileSync(path.join(toolsFolder, 'Settings.gs'), 'utf8')
  .replace('PASTE_THE_CHAPTERS_FOLDER_ID_HERE', 'chapters')
  .replace('PASTE_THE_BACKUPS_FOLDER_ID_HERE', 'backups');
const source = [
  fs.readFileSync(path.join(__dirname, 'google-docs-mock.cjs'), 'utf8'),
  settings,
  fs.readFileSync(path.join(toolsFolder, 'Editor.gs'), 'utf8'),
  fs.readFileSync(path.join(toolsFolder, 'WordCount.gs'), 'utf8'),
  'module.exports = { EditorEngine, WordCountTool, DOCS, Body, makeFile, backups, output };'
].join('\n');
const modulePath = path.join(__dirname, '.google-docs-bundle.cjs');
fs.writeFileSync(modulePath, source);
const tools = require(modulePath);
fs.unlinkSync(modulePath);

const chapterName = 'Chapter 3 Pricing That Pays the Rent';
const chapterLines = fs.readFileSync(path.join(__dirname, 'sample-chapter.md'), 'utf8')
  .split('\n').filter(function (line) { return line.trim() !== ''; });
tools.DOCS[chapterName] = { body: new tools.Body(chapterLines), file: tools.makeFile(chapterName) };

const batch = { name: 'test', fixes: [
  { id: 'replace', doc: chapterName, find: 'In order to price labor honestly', replace: 'To price labor honestly' },
  { id: 'replaceAll', doc: chapterName, kind: 'replaceAll', find: 'store front', replace: 'storefront' },
  { id: 'curly-deletion-never-matched', doc: chapterName, find: 'Now that we’ve covered costs, let’s turn to pricing. ', replace: '' },
  { id: 'deletion', doc: chapterName, find: "Now that we've covered costs, let's turn to pricing. ", replace: '' },
  { id: 'delete-paragraph', doc: chapterName, kind: 'deleteParagraph', text: 'Bread is not a luxury. It is rent.' },
  { id: 'ambiguous', doc: chapterName, find: 'rent', replace: 'lease' },
  { id: 'outside-markers', doc: chapterName, find: 'delve into', replace: 'explore' },
  { id: 'missing-doc', doc: 'No Such Doc', find: 'x', replace: 'y' }
] };

function states(mode) {
  tools.output.length = 0;
  tools.EditorEngine.runFixes(batch, mode);
  const result = {};
  tools.output.join('\n').split('\n').forEach(function (line) {
    const match = line.match(/^([A-Z][A-Z0-9 ]+?)(?: \(.*\))?: (\S+)$/);
    if (match) { result[match[2]] = match[1]; }
  });
  return result;
}

const checked = states('check');
assert.strictEqual(checked.replace, 'READY');
assert.strictEqual(checked.replaceAll, 'READY');
assert.strictEqual(checked['curly-deletion-never-matched'], 'GONE', 'a deletion that never matched must not claim success');
assert.strictEqual(checked.ambiguous, 'FOUND 4 TIMES');
assert.strictEqual(checked['outside-markers'], 'NOT FOUND', 'text outside the chapter markers is never touched');
assert.strictEqual(tools.backups.length, 0, 'check writes nothing');

const applied = states('apply');
assert.strictEqual(applied.replace, 'APPLIED');
assert.strictEqual(applied.deletion, 'APPLIED');
assert.strictEqual(tools.backups.length, 1, 'one backup before the first change');

const again = states('apply');
assert.strictEqual(again.replace, 'ALREADY APPLIED', 'running twice changes nothing');
assert.strictEqual(tools.backups.length, 1, 'no backup when nothing changes');

// A line repeated as its own paragraph can't be made unique by adding words, so "after" picks it out.
const refrainName = 'Refrain Chapter';
const refrainLines = ['[START CHAPTER]', 'The first section.', 'Count it twice.', 'The second section ends here.',
  'Count it twice.', 'The third section.', 'Count it twice.', '[END CHAPTER]'];
tools.DOCS[refrainName] = { body: new tools.Body(refrainLines), file: tools.makeFile(refrainName) };
const refrainBatch = { name: 'refrain', fixes: [
  { id: 'second-refrain', doc: refrainName, find: 'Count it twice.', replace: 'Count it again.', after: 'The second section ends here.' },
  { id: 'missing-anchor', doc: refrainName, find: 'Count it twice.', replace: 'Count it again.', after: 'No such text.' }
] };
function refrainStates(mode) {
  tools.output.length = 0;
  tools.EditorEngine.runFixes(refrainBatch, mode);
  const result = {};
  tools.output.join('\n').split('\n').forEach(function (line) {
    const match = line.match(/^([A-Z][A-Z0-9 ]+?)(?: \(.*\))?: (\S+)$/);
    if (match) { result[match[2]] = match[1]; }
  });
  return result;
}
const refrainChecked = refrainStates('check');
assert.strictEqual(refrainChecked['second-refrain'], 'READY');
assert.strictEqual(refrainChecked['missing-anchor'], 'NOT FOUND', 'a missing "after" text is reported, never guessed');
const refrainApplied = refrainStates('apply');
assert.strictEqual(refrainApplied['second-refrain'], 'APPLIED');
const refrainBody = tools.DOCS[refrainName].body;
const refrainTexts = [2, 4, 6].map(function (index) { return refrainBody.getChild(index).getText(); });
assert.deepStrictEqual(refrainTexts, ['Count it twice.', 'Count it again.', 'Count it twice.'], 'only the line after the "after" text changes');
assert.strictEqual(refrainStates('apply')['second-refrain'], 'ALREADY APPLIED', 'running twice changes nothing');

const body = tools.DOCS[chapterName].body;
assert.ok(body.getChild(0).getText().indexOf('delve') !== -1, 'notes above the start marker are untouched');
assert.strictEqual(tools.WordCountTool.countWords("It's a well-known co-op's rule."), 5);

console.log('google-docs tools: all tests passed');
