# Practical New Chat Handoff Steps

Status: CURRENT
Architecture: v1.6.1
Last updated: 2026-05-15

## Zweck

Diese Datei beschreibt die praktische Vorgehensweise, wenn das Projekt in einem neuen Chat fortgesetzt wird.

## Vorgehen im neuen Chat

1. Projekt-ZIP hochladen.

   Das aktuelle ZIP aus dem Backup-Ordner hochladen, z. B.:

   C:\Users\Daily\Documents\TradingSystem\backups\trading_allocator_project_handoff_<timestamp>.zip

2. Inhalt von specs\97_new_chat_handoff_prompt_v1.md als Startprompt verwenden.

   Dieser Prompt erklärt dem neuen Chat, dass die hochgeladenen Dateien die Single Source of Truth sind und nicht aus Erinnerung rekonstruiert werden darf.

3. Neuen Chat anweisen, zuerst diese Dateien zu lesen:

   - specs\98_spec_index.md
   - specs\99_handoff_snapshot_current.md

   Danach soll der neue Chat den aktuellen Stand bestätigen und erst anschließend mit Station 6 — Portfolio Engine — weitermachen.

## Wichtig

Der neue Chat kann lokale Windows-Pfade nicht selbst lesen.

Deshalb reicht ein Pfad wie

C:\Users\Daily\Documents\TradingSystem\trading_allocator_project

allein nicht aus.

Es muss entweder das Projekt-ZIP hochgeladen oder der Inhalt der relevanten Dateien manuell eingefügt werden.
