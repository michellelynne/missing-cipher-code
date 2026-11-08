# Editor tools for Word

Two Visual Basic modules that make the fixes you approve in a review as **tracked changes**, so
you can accept or reject each one in Word, and count words across your chapters. They work in
Word for Windows and Word for Mac (not Word on the web, which can't run macros).

> **Status:** written to the same design as the Google Docs tools, but not yet tested in Word.
> Try them on a copy of a chapter first.

| Module | What it does | Macros you run |
|---|---|---|
| `EditorTools.bas` | The engine. Import once | `EditorFixesCheck`, `EditorFixesApply`, `EditorWordCount` |
| `EditorBatch.bas` | One batch of approved fixes. Each review gives you a new one to paste in | none |

## Setting it up (once)

1. **Show the Developer tab.**
   - Windows: **File > Options > Customize Ribbon**, tick **Developer**.
   - Mac: **Word > Preferences > Ribbon & Toolbar**, tick **Developer**.
2. **Open the Visual Basic editor**: **Developer > Visual Basic**.
3. **Import both modules.** In the project list on the left, select **Normal** (so the tools work
   in every document), then **File > Import File** and choose `EditorTools.bas`. Do the same for
   `EditorBatch.bas`.
4. **Check the markers.** At the top of `EditorTools`, `START_MARKER` and `END_MARKER` are the
   lines that mark where a chapter starts and ends. Change them to yours, or set both to `""` if
   your files hold only the chapter.
5. **Allow macros** if Word asks. Macros in your Normal template are your own, so they're safe to
   enable.

## Applying a batch of fixes

1. **Paste in the new batch.** In the Visual Basic editor (**Developer > Visual Basic**),
   double-click **EditorBatch** under **Normal > Modules**, select all of its code, and paste the
   new batch over it. Save.
2. **Open the chapter** the batch is for.
3. **Check:** **Developer > Macros**, run `EditorFixesCheck`. A new document lists every fix as
   READY, ALREADY APPLIED, NOT FOUND (fix by hand), FOUND 2 TIMES (fix by hand), or GONE (a
   deletion whose text isn't there: already deleted, or it never matched; check by hand). Nothing in
   the chapter changes.
4. **Apply:** run `EditorFixesApply`. It saves the chapter, copies it to a `Backups` folder next
   to it with the date and time in the name, turns on Track Changes, and makes the READY fixes.
   Track Changes goes back to how you had it afterwards.
5. **Review** the tracked changes (**Review > Next**), accept or reject them, and save.

On a Mac, Word asks once for permission to use the chapter's folder. Choose **Grant Access**;
that's how it saves the backup.

## Counting words

Open any chapter and run `EditorWordCount`. Every `.docx` in the same folder is counted, between
the markers only, and a new document lists the counts and the total. Nothing changes.

## Limits

- **Exact text.** A fix matches its text exactly, case included. Curly and straight quotes are
  different characters.
- **One fix, one place.** If the text appears more than once in the chapter, the fix is skipped so
  the wrong one is never changed. The review makes the search text longer to avoid this.
- **Characters outside plain ASCII** (curly quotes, dashes, accented letters) are written in the
  batch as `ChrW(code)`, because the Visual Basic editor can't read them reliably.

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*
