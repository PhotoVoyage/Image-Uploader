' -*- coding: utf-8 -*-
Option Explicit

Dim WshShell
Set WshShell = CreateObject("WScript.Shell")

' Function to display a message box with given title and message
Sub ShowMessageBox(message, title, style)
    MsgBox message, style, title
End Sub

' Function to run a Python script
Sub RunPythonScript(scriptPath)
    Dim command
    command = "pythonw """ & scriptPath & """"
    WshShell.Run command, 0, False
End Sub

' Main function
Sub Main()
    ' Construct the message with additional information
    Dim message
    message = "This script will execute the Image Uploader program." & vbCrLf & vbCrLf & _
              "Make sure the program is properly configured and all necessary files are available." & vbCrLf & vbCrLf & _
              "Click OK to proceed."

    ' Display warning message with additional information
    ShowMessageBox message, "Attention", vbInformation + vbOKOnly

    ' Get the username and construct the path to the Python script
    Dim username, pythonScriptPath
    username = WshShell.ExpandEnvironmentStrings("%USERNAME%")
    pythonScriptPath = "C:\Users\" & username & "\Desktop\Image Uploader\app\index.py"

    ' Execute the Python script
    RunPythonScript pythonScriptPath
End Sub

' Run the main function
Main

Set WshShell = Nothing
