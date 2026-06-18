# Operational Workflow Rules

Status: CURRENT
Project: Trading System
Last updated: 2026-06-18

## Zweck

Diese Datei dokumentiert die verbindlichen Arbeitsregeln fuer ChatGPT, Codex, GitHub-Rueckkanal, lokale Ausfuehrung und neue Chat-Uebergaben.

Sie enthaelt keine laufenden Gate-Snapshots. Aktueller Gate- und Handoff-Status steht in `specs/99_handoff_snapshot_current.md`.

## Verbindliche Regeln

A) Projektweite Struktur, Konsistenz, Reports und Sync laufen soweit moeglich ueber Codex plus GitHub-Rueckkanal.

B) Codex-relevante Vorgaenge werden soweit moeglich automatisiert: ChatGPT erstellt GitHub-Issues/PR-Kommentare, liest PRs, Reports, Kommentare und geaenderte Dateien selbst. Das Team muss PR-Nummern, Reports oder Diffs nicht manuell suchen oder kopieren. Manuelle Eingriffe sind Ausnahme bei Plattform- oder Berechtigungsgrenzen.

C) Fachliche Spezifikation von Modulen, Schnittstellen, Statuslogik und Architekturentscheidungen erfolgt durch Team plus ChatGPT. Codex darf keine neue fachliche Logik erfinden.

D) Codex darf Golden Cases nur auf Basis bereits beschlossener Specs ergaenzen, konkretisieren oder maschinenlesbarer machen und formale Konsistenz gegen beschlossene Specs pruefen.

E) GitHub `main` ist der kanonische technische Projektstand. Lokale Ordner sind Arbeitskopien, nicht Wahrheit.

F) Lokale PowerShell-Dateiaenderungen muessen als vollstaendiger ausfuehrbarer Block geliefert werden. Wenn Dateien geschrieben werden, ist explizites `StreamWriter`-Handling mit `Write`, `Close` und `try/finally` Pflicht.

G) Keine Uebergabe, kein ZIP und kein neuer Chat-Handoff vor einer projektweiten Cross-Reference-Pruefung ohne KRITISCH- oder MITTEL-Befunde.

H) Jede Uebergabe braucht in `specs/99_handoff_snapshot_current.md` einen konkreten naechsten fachlichen Arbeitspunkt. Fehlt dieser, ist die Uebergabe blockiert.

I) Ein neuer Chat muss zuerst read-only eine Konsistenz- und Strukturpruefung durchfuehren, Schweregrade berichten und erst danach den in 99 gesetzten naechsten fachlichen Schritt vorschlagen.

J) Lange Reports, Logs und Diffs gehoeren nach GitHub in Reports, Issues oder PRs. Chat-Antworten bleiben kurz: Fazit plus naechste Aktion.

K) Nach jedem Codex-PR, Merge oder Abschluss prueft ChatGPT PR-Status, zugehoeriges Issue, offene Codex-Issues und ob ein Folge-Cleanup noetig ist.

L) Nach Abschluss eines Codex- oder lokalen Arbeitsablaufs muss entweder ein PR erstellt oder im zugehoerigen Issue kommentiert werden. Der Rueckkanal nennt PR-Nummer, PR-Link, Branch, geaenderte Dateien und Kurzstatus.

## Kurzbefehle

A) `weiter`

Bedeutung: den naechsten logischen fachlichen Schritt ausfuehren, nicht mehrere Schritte buendeln.

B) `frozen`

Bedeutung: `specs/96_frozen_project_state.md` kuratiert pruefen und bei Bedarf aktualisieren. Dabei alte Eintraege auf Loeschung, Ersetzung oder Ueberfuehrung in echte Specs pruefen. Keine blinde Ergaenzung.

C) `uebergabe` / `übergabe`

Bedeutung: das New Chat Transition Protocol aus `specs/93_new_chat_transition_protocol.md` ausfuehren.

Der Prozess sammelt Pflichtkontext, prueft Frozen State, prueft Struktur/Konsistenz, erstellt einen aktuellen Pre-Handoff-Gate-Report, aktualisiert erforderliche Handoff-Dateien und gibt am Ende den kurzen Copy-Paste-Prompt fuer den neuen Chat aus.

## Audit-Regel

Zukuenftige Architektur-Audits starten nach `specs/94_start_audit_protocol.md`.

Audits sind read-only, behandeln bestehende Artefakte als Hypothesen und klassifizieren Befunde mindestens als PASS, WARN, FAIL oder ALT.
