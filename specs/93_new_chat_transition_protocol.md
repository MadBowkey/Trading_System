# New Chat Transition Protocol

Status: CURRENT
Project: Trading System
Last updated: 2026-06-17

## Zweck

Diese Datei definiert das Protokoll fuer geplante Uebergaben in einen neuen Chat.

Sie sorgt dafuer, dass der Uebergang nicht aus einem langen improvisierten Prompt besteht, sondern aus einem versionierten, kurzen New-Chat-Prompt plus Pflichtkontext im Repository.

## Ausloeser

Wenn der Benutzer `uebergabe` oder `übergabe` schreibt, startet dieses Protokoll.

Der Befehl bedeutet nicht: sofort neuen Chat starten.

Der Befehl bedeutet: Uebergabeprozess vorbereiten, pruefen, dokumentieren und erst bei bestandenem Gate freigeben.

## Grundprinzipien

A) Der Chat ist nicht die fachliche Source of Truth.

B) GitHub `main` ist der kanonische technische Projektstand.

C) Specs, Frozen State, Handoff Snapshot, Gate Report und Golden Cases sind die Uebergabegrundlage.

D) Der New-Chat-Prompt bleibt kurz. Detailkontext wird nicht in den Prompt kopiert, sondern ueber Pflichtdateien referenziert.

E) Keine Uebergabe ohne aktuelles bestandenes Pre-Handoff-Gate mit KRITISCH 0 und MITTEL 0.

## Protokollablauf

A) Uebergabe einfrieren

- Keine neue fachliche Spezifikationsarbeit beginnen.
- Keine Implementierung beginnen.
- Keine neuen Architekturentscheidungen versteckt mitziehen.
- Erst den aktuellen Projektstand pruefen.

B) Pflichtkontext lesen

Mindestens lesen:

- README.md
- specs/93_new_chat_transition_protocol.md
- specs/94_start_audit_protocol.md
- specs/95_operational_workflow_rules.md
- specs/96_frozen_project_state.md
- specs/97_new_chat_handoff_prompt_v1.md
- specs/98_spec_index.md
- specs/99_handoff_snapshot_current.md
- letzter Pre-Handoff-Gate-Report

Zusätzlich lesen:

- alle Specs, Golden Cases und Config-Dateien, die vom aktuellen Arbeitspunkt oder vom letzten Gate betroffen sind.

C) Frozen-State-Pruefung

Vor jeder neuen Uebergabe muss geprueft werden:

- Gibt es seit der letzten Aktualisierung neue uebergabekritische Chat-Entscheidungen?
- Muessen alte Frozen-State-Eintraege geloescht, ersetzt oder in echte Specs ueberfuehrt werden?
- Muss `specs/96_frozen_project_state.md` aktualisiert werden?

Keine blinde Ergaenzung.

D) Struktur- und Konsistenzpruefung

Pruefen:

- Pflichtkontext vollstaendig?
- 97/98/99 verweisen auf aktuellen Gate-Report?
- Gate-Status widerspruchsfrei?
- Specs und Golden Cases konsistent?
- Frozen State gegen Specs widerspruchsfrei?
- Start Audit Protocol gegen aktuelle Architekturentscheidungen widerspruchsfrei?
- offene KRITISCH/MITTEL-Befunde vorhanden?

E) Pre-Handoff-Gate erzeugen

Ein neuer Gate-Report wird unter `_codex_reports/` angelegt.

Mindestinhalt:

- Scope
- gelesene Artefakte
- Ergebnis KRITISCH / MITTEL / REDAKTIONELL
- Handoff-Empfehlung JA/NEIN
- offene Befunde
- erforderliche Dateiaenderungen
- finaler Gate-Status

F) Bei Gate-Fehler

Wenn KRITISCH > 0 oder MITTEL > 0:

- Uebergabe ist blockiert.
- 95/97/98/99 werden auf blockierten Gate-Status aktualisiert.
- Kein finaler New-Chat-Start empfohlen.
- Naechster Schritt ist die fachliche Klaerung der offenen Befunde.

G) Bei bestandenem Gate

Wenn KRITISCH = 0 und MITTEL = 0:

- Gate-Report als bestanden dokumentieren.
- 95/97/98/99 auf aktuellen Gate-Status aktualisieren.
- 97 als kurze New-Prompt-Datei aktualisieren.
- 99 als kompakten Handoff Snapshot aktualisieren.
- Uebergabe freigeben.

## New-Prompt-Datei

`specs/97_new_chat_handoff_prompt_v1.md` ist die formale New-Prompt-Datei.

Sie muss kurz bleiben.

Sie enthaelt nur:

- Projektname
- Pflichtkontext
- aktueller Gate-Status
- erste read-only Aufgabe des neuen Chats
- naechster fachlicher Vorschlag

Sie darf nicht:

- lange Projektgeschichte enthalten
- Specs duplizieren
- Frozen State kopieren
- ganze Gate-Reports kopieren
- fachliche Spezifikationen ersetzen

## Abschlussbericht im alten Chat

Nach Ausfuehrung von `uebergabe` berichtet ChatGPT kurz:

A) Gate-Status
B) geaenderte Dateien
C) Handoff freigegeben: JA/NEIN
D) offene Befunde, falls vorhanden
E) zu verwendende New-Prompt-Datei

## Abgrenzung zu anderen Kurzbefehlen

`weiter` = naechster logischer fachlicher Schritt.

`frozen` = Frozen State kuratiert pruefen und aktualisieren.

`uebergabe` / `übergabe` = vollstaendigen New-Chat-Uebergabeprozess nach dieser Datei ausfuehren.
