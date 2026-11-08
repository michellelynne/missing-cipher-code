Attribute VB_Name = "EditorBatch"
' Editor tools for Word: one batch of approved fixes.
'
' Each review gives you a new batch as text. Open the Visual Basic editor, double-click
' EditorBatch, select all of its code, and paste the new batch over it. Then run
' EditorFixesCheck and EditorFixesApply.
'
' Each fix is Array(id, find, replace). The find text must appear exactly once between the
' chapter markers; an empty replace ("") deletes the text. Text inside quotation marks here
' doubles any straight quotation mark it contains ("" for one "). Every character outside plain
' ASCII (curly quotes, apostrophes, dashes, accented letters) is written as ChrW(code), for
' example "it" & ChrW(8217) & "s", because the Visual Basic editor can't read them reliably.

Option Explicit

' The chapter this batch is for. The macro warns if a different document is open.
Public Function EditorBatchDocument() As String
    EditorBatchDocument = "Chapter 3 Pricing That Pays the Rent"
End Function

Public Function EditorBatchName() As String
    EditorBatchName = "Example batch (replace with the batch from your review)"
End Function

Public Function EditorBatchFixes() As Collection
    Dim fixes As New Collection
    fixes.Add Array("P1-1", "In order to price labor honestly", "To price labor honestly")
    fixes.Add Array("P1-2", "Does the store front count?", "Does the storefront count?")
    fixes.Add Array("P1-3", "Now that we've covered costs, let's turn to pricing. ", "")
    Set EditorBatchFixes = fixes
End Function
