Attribute VB_Name = "EditorTools"
' Editor tools for Word: the shared engine. Import once; you don't edit this module.
'
' Macros you run (Tools > Macro > Macros, or View > Macros):
'   EditorFixesCheck   Lists READY, ALREADY APPLIED, or NOT FOUND for every fix. Changes nothing.
'   EditorFixesApply   Saves and backs up the chapter, turns on Track Changes, then makes the
'                      fixes, so each one shows as a tracked change you can accept or reject.
'   EditorWordCount    Counts the words between the chapter markers in every .docx in the
'                      chapter's folder. Changes nothing.
' The fixes themselves live in the EditorBatch module, which each review replaces.
'
' From The Missing Cipher by Michelle Brenner, Quill & Coin. MIT License; see skills/editor/LICENSE.md.

Option Explicit

' The lines that mark where a chapter starts and ends. Leave both "" if the file is only the chapter.
Private Const START_MARKER As String = "[START CHAPTER]"
Private Const END_MARKER As String = "[END CHAPTER]"
' Backups go in a folder with this name next to the chapter file.
Private Const BACKUPS_FOLDER_NAME As String = "Backups"
' Word's Find can only search for 255 characters at once; longer fixes are matched in two steps.
Private Const FIND_LIMIT As Long = 255

' ------------------------------------------------------------------------------------------
' Chapter boundaries
' ------------------------------------------------------------------------------------------

' The part of the document between the markers, or Nothing if the markers aren't there.
Private Function ChapterRange(targetDocument As Document) As Range
    Dim wholeRange As Range
    Set wholeRange = targetDocument.Content
    If START_MARKER = "" And END_MARKER = "" Then
        Set ChapterRange = wholeRange
        Exit Function
    End If

    Dim startSearch As Range
    Set startSearch = targetDocument.Content
    If Not FindLiteral(startSearch, START_MARKER) Then
        Set ChapterRange = Nothing
        Exit Function
    End If

    Dim endSearch As Range
    Set endSearch = targetDocument.Range(startSearch.End, wholeRange.End)
    If Not FindLiteral(endSearch, END_MARKER) Then
        Set ChapterRange = Nothing
        Exit Function
    End If

    Set ChapterRange = targetDocument.Range(startSearch.End, endSearch.Start)
End Function

' Searches searchRange for the exact text. On success, searchRange becomes the match.
Private Function FindLiteral(searchRange As Range, literalText As String) As Boolean
    With searchRange.Find
        .ClearFormatting
        ' A caret starts a special code in Word's Find (^p, ^t), so a literal caret is doubled.
        .Text = Replace(literalText, "^", "^^")
        .MatchCase = True
        .MatchWholeWord = False
        .MatchWildcards = False
        .MatchSoundsLike = False
        .MatchAllWordForms = False
        .Forward = True
        .Wrap = wdFindStop
        .Format = False
        FindLiteral = .Execute
    End With
End Function

' ------------------------------------------------------------------------------------------
' Finding every match of a fix inside the chapter
' ------------------------------------------------------------------------------------------

' Every place the exact text appears inside the chapter, as a Collection of Ranges.
Private Function MatchesInChapter(targetDocument As Document, chapter As Range, literalText As String) As Collection
    Dim found As New Collection
    Dim searchPart As String
    searchPart = Left$(literalText, FIND_LIMIT)

    Dim searchStart As Long
    searchStart = chapter.Start
    Do While searchStart < chapter.End
        Dim searchRange As Range
        Set searchRange = targetDocument.Range(searchStart, chapter.End)
        If Not FindLiteral(searchRange, searchPart) Then Exit Do
        If searchRange.End > chapter.End Then Exit Do

        Dim fullMatch As Range
        Set fullMatch = targetDocument.Range(searchRange.Start, searchRange.Start + Len(literalText))
        If fullMatch.End <= chapter.End And fullMatch.Text = literalText Then
            found.Add fullMatch
        End If
        searchStart = searchRange.Start + 1
    Loop
    Set MatchesInChapter = found
End Function

' ------------------------------------------------------------------------------------------
' Status of one fix (changes nothing)
' ------------------------------------------------------------------------------------------

Private Function FixStatus(targetDocument As Document, chapter As Range, findText As String, replaceText As String, ByRef matchRange As Range) As String
    Dim matches As Collection
    Set matches = MatchesInChapter(targetDocument, chapter, findText)
    If matches.Count = 1 Then
        Set matchRange = matches(1)
        FixStatus = "READY"
        Exit Function
    End If
    If matches.Count = 0 Then
        If replaceText = "" Then
            FixStatus = "GONE (already deleted, or the text never matched; check by hand)"
        ElseIf MatchesInChapter(targetDocument, chapter, replaceText).Count >= 1 Then
            FixStatus = "ALREADY APPLIED"
        Else
            FixStatus = "NOT FOUND (the text has changed; fix by hand)"
        End If
        Exit Function
    End If
    FixStatus = "FOUND " & matches.Count & " TIMES (skipped; fix by hand)"
End Function

' ------------------------------------------------------------------------------------------
' Making one change as a small tracked change
' ------------------------------------------------------------------------------------------

' Replaces only the characters that differ, so the tracked change is as small as possible and
' formatting on the rest of the phrase stays as it is.
Private Sub ReplaceMinimally(targetDocument As Document, matchRange As Range, newText As String)
    Dim oldText As String
    oldText = matchRange.Text

    Dim prefixLength As Long
    prefixLength = 0
    Do While prefixLength < Len(oldText) And prefixLength < Len(newText)
        If Mid$(oldText, prefixLength + 1, 1) <> Mid$(newText, prefixLength + 1, 1) Then Exit Do
        prefixLength = prefixLength + 1
    Loop

    Dim suffixLength As Long
    suffixLength = 0
    Do While suffixLength < Len(oldText) - prefixLength And suffixLength < Len(newText) - prefixLength
        If Mid$(oldText, Len(oldText) - suffixLength, 1) <> Mid$(newText, Len(newText) - suffixLength, 1) Then Exit Do
        suffixLength = suffixLength + 1
    Loop

    Dim changeRange As Range
    Set changeRange = targetDocument.Range(matchRange.Start + prefixLength, matchRange.End - suffixLength)
    changeRange.Text = Mid$(newText, prefixLength + 1, Len(newText) - prefixLength - suffixLength)
End Sub

' ------------------------------------------------------------------------------------------
' Backups
' ------------------------------------------------------------------------------------------

' Saves the document, then copies the saved file to the Backups folder next to it as
' "Name_YYYY-MM-DD_HH-MM.docx". Returns the backup's path, or "" if it couldn't be made.
Private Function BackupDocument(targetDocument As Document) As String
    BackupDocument = ""
    If targetDocument.Path = "" Then
        MsgBox "Save the chapter as a file first, then run this again.", vbExclamation, "Editor tools"
        Exit Function
    End If
    If Not targetDocument.Saved Then targetDocument.Save

    Dim separator As String
    separator = Application.PathSeparator
    Dim backupsFolder As String
    backupsFolder = targetDocument.Path & separator & BACKUPS_FOLDER_NAME

    Dim baseName As String
    Dim extension As String
    baseName = targetDocument.Name
    extension = ""
    If InStrRev(baseName, ".") > 0 Then
        extension = Mid$(baseName, InStrRev(baseName, "."))
        baseName = Left$(baseName, InStrRev(baseName, ".") - 1)
    End If
    Dim backupPath As String
    backupPath = backupsFolder & separator & baseName & "_" & Format$(Now, "yyyy-mm-dd_hh-nn") & extension

    On Error GoTo BackupFailed
#If Mac Then
    ' Word for Mac asks once for permission to write in the chapter's folder.
    If Not GrantAccessToMultipleFiles(Array(targetDocument.Path, backupsFolder)) Then GoTo BackupFailed
#End If
    If Dir(backupsFolder, vbDirectory) = "" Then MkDir backupsFolder
#If Mac Then
    FileCopy targetDocument.FullName, backupPath
#Else
    ' FileCopy can't copy a file Word has open on Windows, so use the file system object.
    CreateObject("Scripting.FileSystemObject").CopyFile targetDocument.FullName, backupPath
#End If
    If Dir(backupPath) = "" Then GoTo BackupFailed
    BackupDocument = backupPath
    Exit Function

BackupFailed:
    MsgBox "Couldn't make a backup in " & backupsFolder & ", so nothing was changed." & vbCr & Err.Description, vbExclamation, "Editor tools"
    BackupDocument = ""
End Function

' ------------------------------------------------------------------------------------------
' Reports
' ------------------------------------------------------------------------------------------

' Opens a new document with the report, so long results are easy to read and save.
Private Sub ShowReport(title As String, lines As Collection)
    Dim report As Document
    Set report = Documents.Add
    report.Content.Text = title
    Dim lineIndex As Long
    For lineIndex = 1 To lines.Count
        report.Content.InsertParagraphAfter
        report.Content.InsertAfter lines(lineIndex)
    Next lineIndex
End Sub

' ------------------------------------------------------------------------------------------
' Fixes
' ------------------------------------------------------------------------------------------

Private Sub RunFixes(applyChanges As Boolean)
    If Documents.Count = 0 Then
        MsgBox "Open the chapter first.", vbExclamation, "Editor tools"
        Exit Sub
    End If
    Dim targetDocument As Document
    Set targetDocument = ActiveDocument

    Dim expectedName As String
    expectedName = EditorBatch.EditorBatchDocument()
    If InStr(1, targetDocument.Name, expectedName, vbTextCompare) <> 1 Then
        If MsgBox("This batch is for """ & expectedName & """, but the open document is """ & targetDocument.Name & """. Run it anyway?", vbYesNo + vbQuestion, "Editor tools") <> vbYes Then Exit Sub
    End If

    Dim chapter As Range
    Set chapter = ChapterRange(targetDocument)
    If chapter Is Nothing Then
        MsgBox "The chapter markers " & START_MARKER & " and " & END_MARKER & " weren't found, so nothing was checked.", vbExclamation, "Editor tools"
        Exit Sub
    End If

    Dim fixes As Collection
    Set fixes = EditorBatch.EditorBatchFixes()
    Dim lines As New Collection
    Dim readyCount As Long
    Dim appliedCount As Long
    Dim otherCount As Long

    Dim trackingWas As Boolean
    trackingWas = targetDocument.TrackRevisions
    If applyChanges Then
        Dim backupPath As String
        backupPath = BackupDocument(targetDocument)
        If backupPath = "" Then Exit Sub
        lines.Add "BACKED UP to " & backupPath
        targetDocument.TrackRevisions = True
    End If

    Dim fixIndex As Long
    For fixIndex = 1 To fixes.Count
        Dim fixEntry As Variant
        fixEntry = fixes(fixIndex)
        Dim matchRange As Range
        Set matchRange = Nothing
        Dim state As String
        state = FixStatus(targetDocument, chapter, CStr(fixEntry(1)), CStr(fixEntry(2)), matchRange)
        If state = "READY" And applyChanges Then
            ReplaceMinimally targetDocument, matchRange, CStr(fixEntry(2))
            Set chapter = ChapterRange(targetDocument)
            appliedCount = appliedCount + 1
            lines.Add "APPLIED: " & fixEntry(0)
        ElseIf state = "READY" Then
            readyCount = readyCount + 1
            lines.Add "READY: " & fixEntry(0) & "   """ & fixEntry(1) & """  becomes  """ & fixEntry(2) & """"
        Else
            otherCount = otherCount + 1
            lines.Add state & ": " & fixEntry(0)
        End If
    Next fixIndex

    If applyChanges Then
        targetDocument.TrackRevisions = trackingWas
        lines.Add "TOTAL: " & appliedCount & " applied as tracked changes, " & otherCount & " skipped. Review the tracked changes, then save."
        ShowReport "Editor tools: fixes applied (" & EditorBatch.EditorBatchName() & ")", lines
    Else
        lines.Add "TOTAL: " & readyCount & " ready, " & otherCount & " skipped."
        ShowReport "Editor tools: fixes check, nothing changed (" & EditorBatch.EditorBatchName() & ")", lines
    End If
End Sub

Public Sub EditorFixesCheck()
    RunFixes False
End Sub

Public Sub EditorFixesApply()
    RunFixes True
End Sub

' ------------------------------------------------------------------------------------------
' Word count
' ------------------------------------------------------------------------------------------

Public Sub EditorWordCount()
    If Documents.Count = 0 Or ActiveDocument.Path = "" Then
        MsgBox "Open a saved chapter first; every .docx in its folder is counted.", vbExclamation, "Editor tools"
        Exit Sub
    End If
    Dim folderPath As String
    folderPath = ActiveDocument.Path & Application.PathSeparator
#If Mac Then
    If Not GrantAccessToMultipleFiles(Array(ActiveDocument.Path)) Then Exit Sub
#End If

    Dim fileNames As New Collection
    Dim fileName As String
    fileName = Dir(folderPath)
    Do While fileName <> ""
        If LCase$(Right$(fileName, 5)) = ".docx" And Left$(fileName, 2) <> "~$" Then fileNames.Add fileName
        fileName = Dir()
    Loop

    Dim lines As New Collection
    Dim total As Long
    Dim nameIndex As Long
    For nameIndex = 1 To fileNames.Count
        Dim chapterDocument As Document
        Dim openedHere As Boolean
        openedHere = False
        Set chapterDocument = Nothing
        Dim openIndex As Long
        For openIndex = 1 To Documents.Count
            If Documents(openIndex).FullName = folderPath & fileNames(nameIndex) Then Set chapterDocument = Documents(openIndex)
        Next openIndex
        If chapterDocument Is Nothing Then
            Set chapterDocument = Documents.Open(FileName:=folderPath & fileNames(nameIndex), ReadOnly:=True, AddToRecentFiles:=False, Visible:=False)
            openedHere = True
        End If
        Dim chapter As Range
        Set chapter = ChapterRange(chapterDocument)
        If chapter Is Nothing Then
            lines.Add fileNames(nameIndex) & ": markers not found, not counted"
        Else
            Dim words As Long
            words = chapter.ComputeStatistics(wdStatisticWords)
            total = total + words
            lines.Add fileNames(nameIndex) & ": " & Format$(words, "#,##0")
        End If
        If openedHere Then chapterDocument.Close SaveChanges:=False
    Next nameIndex
    lines.Add "TOTAL across " & fileNames.Count & " file(s): " & Format$(total, "#,##0")
    ShowReport "Editor tools: word count", lines
End Sub
