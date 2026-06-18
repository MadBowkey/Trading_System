# New Chat Transition Protocol

Status: CURRENT
Project: Trading System
Last updated: 2026-06-18

## Zweck

Diese Datei definiert das Protokoll fuer geplante Uebergaben in einen neuen Chat.

Ziel ist eine zweistufige Uebergabe:

A) Im alten Chat wird ein sehr kurzer Copy-Paste-Prompt erzeugt.

B) Dieser kurze Prompt verweist auf die Datei `specs/97_new_chat_handoff_prompt_v1.md`.

Die Datei `specs/97_new_chat_handoff_prompt_v1.md` ist die eigentliche New-Prompt-Datei und enthaelt die Langform-Anweisung fuer den neuen Chat.

## Ausloeser

Wenn der Benutzer `uebergabe` oder `übergabe` schreibt, startet dieses Protokoll.

Der Befehl bedeutet nicht: sofort neuen Chat starten.

Der Befehl bedeutet: Uebergabe vorbereiten, Pflichtkontext sammeln, Frozen State pruefen, Konsistenz pruefen, Gate dokumentieren, Handoff-Dateien aktualisieren und dann den kurzen Copy-Paste-Prompt ausgeben.

## Rollen der Uebergabedateien

A) `specs/93_new_chat_transition_protocol.md`

- definiert diesen Prozess.

B) `specs/95_operational_workflow_rules.md`

- definiert allgemeine Arbeitsregeln und Kurzbefehle.
- enthaelt keinen laufenden Gate-Status.

C) `specs/96_frozen_project_state.md`

- enthaelt kompakte, uebergabekritische Chat-Entscheidungen.
- enthaelt keinen Gate-Snapshot.

D) `specs/97_new_chat_handoff_prompt_v1.md`

- ist die New-Prompt-Datei in Langform.
- der neue Chat liest diese Datei und fuehrt sie aus.

E) `specs/98_spec_index.md`

- ist reiner Datei- und Strukturindex.
- enthaelt keinen laufenden Gate-Status.

F) `specs/99_handoff_snapshot_current.md`

- enthaelt aktuellen Snapshot, aktuellen Gate-Status, aktuellen Gate-Report, zwingend einen konkreten naechsten fachlichen Arbeitspunkt und den kurzen Copy-Paste-Prompt.

## Pflichtpruefung bei Uebergabe

Bei Ausfuehrung des Protokolls liest ChatGPT mindestens:

- README.md
- specs/93_new_chat_transition_protocol.md
- specs/94_start_audit_protocol.md
- specs/95_operational_workflow_rules.md
- specs/96_frozen_project_state.md
- specs/97_new_chat_handoff_prompt_v1.md
- specs/98_spec_index.md
- specs/99_handoff_snapshot_current.md
- den letzten Pre-Handoff-Gate-Report

Zusätzlich liest ChatGPT alle Specs, Golden Cases und Config-Dateien, die vom aktuellen Arbeitspunkt oder vom letzten Gate betroffen sind.

## Frozen-State-Pruefung

Vor jeder neuen Uebergabe muss geprueft werden:

- Gibt es neue uebergabekritische Chat-Entscheidungen?
- Muessen alte Frozen-State-Eintraege geloescht, ersetzt oder in echte Specs ueberfuehrt werden?
- Muss `specs/96_frozen_project_state.md` aktualisiert werden?

Keine blinde Ergaenzung.

## Struktur- und Konsistenzpruefung

Pruefen:

- Pflichtkontext vollstaendig?
- Dateirollen 95 bis 99 ueberschneidungsarm?
- 97 verweist auf 99 und letzten Gate-Report?
- 99 verweist auf den aktuellen Gate-Report?
- 99 enthaelt einen konkreten naechsten fachlichen Arbeitspunkt?
- Gate-Status widerspruchsfrei?
- Specs und Golden Cases konsistent?
- Frozen State gegen Specs widerspruchsfrei?
- Start Audit Protocol gegen aktuelle Architekturentscheidungen widerspruchsfrei?
- offene KRITISCH/MITTEL-Befunde vorhanden?

## Harte Uebergabesperre

Wenn `specs/99_handoff_snapshot_current.md` keinen konkreten naechsten fachlichen Arbeitspunkt enthaelt, ist die Uebergabe blockiert.

In diesem Fall darf kein neuer Chat-Handoff freigegeben werden.

Der fehlende naechste fachliche Arbeitspunkt ist mindestens ein MITTEL-Befund im Pre-Handoff-Gate.

## Pre-Handoff-Gate

Ein neuer Gate-Report wird unter `_codex_reports/` angelegt.

Mindestinhalt:

- Scope
- gelesene Artefakte
- Ergebnis KRITISCH / MITTEL / REDAKTIONELL
- Handoff-Empfehlung JA/NEIN
- offene Befunde
- erforderliche Dateiaenderungen
- finaler Gate-Status

Wenn KRITISCH > 0 oder MITTEL > 0:

- Uebergabe blockiert.
- 99 und 97 werden auf blockierten Status aktualisiert.
- 95, 96 und 98 werden nur aktualisiert, wenn sich ihre Rolleninhalte geaendert haben.

Wenn KRITISCH = 0 und MITTEL = 0:

- Uebergabe freigegeben.
- 99 wird auf aktuellen Gate-Status, aktuellen Gate-Report, naechsten fachlichen Arbeitspunkt und kurzen Copy-Paste-Prompt aktualisiert.
- 97 wird als New-Prompt-Datei aktualisiert, falls sich Startlogik oder Pflichtkontext geaendert haben.
- 95, 96 und 98 werden nur aktualisiert, wenn sich Regeln, Frozen State oder Indexstruktur geaendert haben.

## Kurzprompt fuer den neuen Chat

Nach bestandenem Gate gibt ChatGPT im alten Chat diesen kurzen Copy-Paste-Prompt aus:

```text
Bitte lies im Repository `MadBowkey/Trading_System` auf GitHub `main` die Datei `specs/97_new_chat_handoff_prompt_v1.md` und fuehre sie aus. Beginne mit der dort geforderten Read-only-Pruefung und berichte nur kurz den Projektstand, gefundene Dateien, Konsistenzbefund, Handoff verwendbar Ja/Nein und den naechsten fachlichen Vorschlag.
```

Dieser kurze Prompt ist der einzige Text, der in den neuen Chat kopiert werden soll.

## Abschlussbericht im alten Chat

Nach Ausfuehrung von `uebergabe` berichtet ChatGPT kurz:

A) Gate-Status
B) geaenderte Dateien
C) Handoff freigegeben: JA/NEIN
D) offene Befunde, falls vorhanden
E) zu verwendender Copy-Paste-Prompt

## Abgrenzung zu anderen Kurzbefehlen

`weiter` = naechster logischer fachlicher Schritt.

`frozen` = Frozen State kuratiert pruefen und aktualisieren.

`uebergabe` / `übergabe` = vollstaendigen New-Chat-Uebergabeprozess nach dieser Datei ausfuehren.
