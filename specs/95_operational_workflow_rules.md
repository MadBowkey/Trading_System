# Operational Workflow Rules

Status: CURRENT
Project: Trading System
Last updated: 2026-05-19

## Zweck

Diese Datei dokumentiert die verbindlichen Arbeitsregeln fuer ChatGPT, Codex, GitHub-Rueckkanal, lokale Ausfuehrung und neue Chat-Uebergaben.

## Verbindliche Regeln

A) Projektweite Struktur, Konsistenz, Reports und Sync laufen soweit moeglich ueber Codex plus GitHub-Rueckkanal.

B) Codex-relevante Vorgaenge werden soweit moeglich automatisiert: ChatGPT erstellt GitHub-Issues/PR-Kommentare, liest PRs, Reports, Kommentare und geaenderte Dateien selbst und das Team muss PR-Nummern, Reports oder Diffs nicht manuell suchen oder kopieren. Manuelle Eingriffe sind Ausnahme bei Plattform- oder Berechtigungsgrenzen.

C) Fachliche Spezifikation von Modulen, Schnittstellen, Statuslogik und Architekturentscheidungen erfolgt durch Team plus ChatGPT. Codex darf keine neue fachliche Logik erfinden.

D) Codex darf Golden Cases nur auf Basis bereits beschlossener Specs ergaenzen, konkretisieren oder maschinenlesbarer machen und formale Konsistenz gegen beschlossene Specs pruefen.

E) Der lokale Projektordner und GitHub `main` sind der verbindliche Projektstand. Backend- oder chat-only-Aenderungen gelten nicht als erledigt, solange sie nicht im Repo nachvollziehbar geaendert, geprueft und bei Bedarf gemerged sind.

F) Lokale PowerShell-Dateiaenderungen muessen als ein vollstaendiger ausfuehrbarer Block geliefert werden. Wenn Dateien geschrieben werden, ist explizites `StreamWriter`-Handling mit `Write`, `Close` und `try/finally` Pflicht. Keine kommentierten Einzelfragmente. Nach dem Script folgen erwartete Ausgabe, Nicht-Eintreten-Kriterien und Auswertungsanweisung.

G) Keine Uebergabe, kein ZIP und kein neuer Chat-Handoff vor einer projektweiten Cross-Reference-Pruefung ueber Specs, Config und Golden Cases ohne KRITISCH- oder MITTEL-Befunde.

H) Ein neuer Chat muss zuerst read-only eine projektweite Konsistenz- und Strukturpruefung durchfuehren, Schweregrade berichten und erst danach den naechsten fachlichen Schritt vorschlagen.

I) Lange Reports, Logs und Diffs gehoeren nach GitHub in Reports, Issues oder PRs. Chat-Antworten bleiben kurz: Fazit plus naechste Aktion.

J) `weiter` bedeutet: den naechsten logischen Schritt ausfuehren, nicht mehrere Schritte buendeln, und dabei die Rollenverteilung Team/ChatGPT/Codex einhalten.

## Aktueller Gate-Stand

Pre-Handoff Gate 002 auf aktuellem `main` wurde bestanden:

- KRITISCH: 0
- MITTEL: 0
- REDAKTIONELL: 1, nicht blockierend

Der redaktionelle Hinweis betrifft aeltere Terminologie in `specs/01_architecture_overview_v1_6_1.md` und `specs/06_validator_pipeline_v1.md`; er blockiert die Uebergabe nicht.
