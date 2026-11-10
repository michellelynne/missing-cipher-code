# Editor tools for Google Docs

An Apps Script project that makes the fixes you approve in a review, counts words across your
chapters, and places or refreshes images. You set it up once in your Google account; after that,
each review hands you a new batch of fixes to paste in and run.

Nothing runs on its own. You choose each function and press Run, and every tool that changes a
Doc has a preview that writes nothing. Before any change, the Doc is copied to your backups folder
with a timestamp in its name.

## What's in it

| File | What it does | Functions you run |
|---|---|---|
| `appsscript.json` | The project's settings and the permissions it asks for | none |
| `Settings.gs` | Your folders, time zone, and chapter markers. The only file you edit by hand | none |
| `Editor.gs` | The shared engine the other files use | none |
| `Fixes.gs` | Applies a batch of approved fixes | `fixesCheck`, `fixesPreview`, `fixesApply` |
| `WordCount.gs` | Counts words in every chapter, between the markers | `wordCountRun` |
| `Images.gs` | Swaps image placeholders for images, and refreshes updated images | `imagesPlacePreview`, `imagesPlace`, `imagesRefreshPreview`, `imagesRefresh` |

## Setting it up (once, about ten minutes)

1. **Make three folders in Google Drive** if you don't have them: one for your chapter Docs, one
   for backups, and one for images. Keep each chapter as its own Doc in the chapters folder.
2. **Create the project.** Go to [script.google.com](https://script.google.com), choose
   **New project**, and rename it (click "Untitled project") to something like *Editor tools*.
3. **Show the settings file.** Click the gear (**Project Settings**) and tick **Show
   "appsscript.json" manifest file in editor**. Go back to the editor (the `< >` icon), open
   `appsscript.json`, replace everything in it with the contents of this folder's
   `appsscript.json`, and change `timeZone` to yours.
4. **Add the script files.** For each `.gs` file in this folder, click **+** next to **Files**,
   choose **Script**, type the name without `.gs` (for example `Settings`), and paste the file's
   contents in. Name them exactly as here. Delete the starter `Code.gs` file (the three dots next
   to it, then **Delete**).
5. **Fill in `Settings.gs`.** Paste in your three folder IDs. A folder's ID is the part of its
   address after `/folders/`. Set your chapter start and end markers, or leave both as `''` if
   your Docs hold only the chapter.
6. **Save** (Ctrl+S or Cmd+S).
7. **Give it permission.** Choose `wordCountRun` in the function menu at the top and press
   **Run**. Google asks you to authorize it:
   - Choose **Review permissions** and pick your account.
   - Google warns that it hasn't verified this app. That's because you wrote it, not a company.
     Choose **Advanced**, then **Go to Editor tools (unsafe)**.
   - Allow it to see and edit your Docs and your Drive files. It needs Docs access to read and
     change chapters, and Drive access to find the chapters folder and save backup copies.
8. **Read the result.** The **Execution log** opens below the code. You should see a word count
   for each chapter. If you see "Fill in ... in Settings.gs first", a folder ID is missing.

## Applying a batch of fixes

Each time you approve fixes, the review gives you a `FIX_BATCH`. Then:

1. Open `Fixes.gs` and replace everything between the `BATCH START` and `BATCH END` lines with the
   new batch. Save.
2. Run `fixesCheck`. Every fix shows one of:
   - **READY**: it will be applied.
   - **ALREADY APPLIED**: the chapter already has it, so it is skipped.
   - **NOT FOUND**: the text has changed since the review. Fix it by hand.
   - **FOUND 2 TIMES** (or more): the search text isn't unique, so it is skipped. Fix it by hand.
   - **GONE**: a deletion whose text isn't there. Either it was already deleted or the text never
     matched (often a curly versus straight quote). Check it by hand.
3. Run `fixesPreview` to see each READY fix's before and after text.
4. Run `fixesApply`. Each Doc is backed up before its first change. If the log says STOPPED, run
   it again; finished fixes show ALREADY APPLIED and are skipped.
5. Run `fixesCheck` once more to confirm, and send the review the log if anything needs a hand
   fix.

## Adding your own scripts

Every `.gs` file in a project shares one global space. If two files each declare the same
top-level name (`const SETTINGS`, `function backup()`), one silently replaces the other or the
project stops running. To add a script without breaking the others:

- **Wrap your code in one object** with a name no other file uses, the way these files do:
  `var MyTool = (function () { ... return { run: run }; })();`
- **Give the functions you run a unique prefix** (`myToolRun`), and keep everything else inside
  your object.
- **Don't use another file's values at the top level** of yours. Files load in an order you don't
  control; inside a function is fine.
- Functions whose names end in `_` are hidden from the Run menu, which is a good way to keep
  helpers out of the way.

Your tools can use the engine: `EditorEngine.chapterDocs()`, `EditorEngine.backup(file)`,
`EditorEngine.chapterRange(body)`, and `EditorEngine.runFixes(batch, mode)`.

## Limits

- **No suggestions.** Apps Script can't make edits in Suggesting mode, so changes are direct.
  That's why every Doc is backed up first. **File > Version history** in the Doc is a second way
  back.
- **Six minutes per run.** Google stops a run after six minutes. These tools stop themselves just
  before that and tell you to run again.
- **One paragraph at a time.** A search can't match text that crosses a paragraph break.
- **Exact text.** A fix matches the text exactly, except that a space also matches a nonbreaking
  space. Curly and straight quotes are different characters.

## Undoing a change

Open your backups folder, find the copy named after the Doc with the time of the run, and either
copy what you need back or rename it to replace the chapter. Version history in the Doc works too.

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. The code is MIT and this guide is [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); see
[the Editor's license](../../LICENSE.md).*
