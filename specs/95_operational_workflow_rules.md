# Operational Workflow Rules

Status: CURRENT
Project: Trading System
Last updated: 2026-06-17

## Zweck

Diese Datei dokumentiert die verbindlichen Arbeitsregeln fuer ChatGPT, Codex, GitHub-Rueckkanal, lokale Ausfuehrung und neue Chat-Uebergaben.

## Verbindliche Regeln

A) Projektweite Struktur, Konsistenz, Reports und Sync laufen soweit moeglich ueber Codex plus GitHub-Rueckkanal.

B) Codex-relevante Vorgaenge werden soweit moeglich automatisiert: ChatGPT erstellt GitHub-Issues/PR-Kommentare, liest PRs, Reports, Kommentare und geaenderte Dateien selbst und das Team muss PR-Nummern, Reports oder Diffs nicht manuell suchen oder kopieren. Manuelle Eingriffe sind Ausnahme bei Plattform- oder Berechtigungsgrenzen.

C) Fachliche Spezifikation von Modulen, Schnittstellen, Statuslogik und Architekturentscheidungen erfolgt durch Team plus ChatGPT. Codex darf keine neue fachliche Logik erfinden.

D) Codex darf Golden Cases nur auf Basis bereits beschlossener Specs ergaenzen, konkretisieren oder maschinenlesbarer machen und formale Konsistenz gegen beschlossene Specs pruefen.

E) GitHub `main` ist der kanonische technische Projektstand. Der lokale Projektordner ist eine Arbeitskopie und nicht selbst die Wahrheit. Backend-, chat-only- oder lokale Aenderungen gelten erst als erledigt, wenn sie als Repo-Aenderung nachvollziehbar sind und bei Bedarf auf GitHub `main` gemerged wurden.

F) Lokale PowerShell-Dateiaenderungen muessen als ein vollstaendiger ausfuehrbarer Block geliefert werden. Wenn Dateien geschrieben werden, ist explizites `StreamWriter`-Handling mit `Write`, `Close` und `try/finally` Pflicht. Keine kommentierten Einzelfragmente. Nach dem Script folgen erwartete Ausgabe, Nicht-Eintreten-Kriterien und Auswertungsanweisung.

G) Keine Uebergabe, kein ZIP und kein neuer Chat-Handoff vor einer projektweiten Cross-Reference-Pruefung ueber Specs, Config und Golden Cases ohne KRITISCH- oder MITTEL-Befunde.

H) Ein neuer Chat muss zuerst read-only eine projektweite Konsistenz- und Strukturpruefung durchfuehren, Schweregrade berichten und erst danach den naechsten fachlichen Schritt vorschlagen.

I) Lange Reports, Logs und Diffs gehoeren nach GitHub in Reports, Issues oder PRs. Chat-Antworten bleiben kurz: Fazit plus naechste Aktion.

J) `weiter` bedeutet: den naechsten logischen Schritt ausfuehren, nicht mehrere Schritte buendeln, und dabei die Rollenverteilung Team/ChatGPT/Codex einhalten.

K) Nach jedem Codex-PR, Merge oder Abschluss prueft ChatGPT den PR-Status, das zugehoerige Issue, offene Codex-Issues und ob ein Folge-Cleanup noetig ist. Erledigte zugehoerige Issues werden mit `state_reason: completed` geschlossen. Neue Codex-PRs muessen im PR-Body `Closes #<Issue-Nummer>` enthalten. Issue #7 bleibt offen, solange lokaler Sync ein eigener offener Arbeitspunkt ist.

L) Nach Abschluss eines Codex- oder lokalen Arbeitsablaufs muss entweder ein PR erstellt oder im zugehoerigen Issue kommentiert werden. Der Rueckkanal nennt PR-Nummer, PR-Link, Branch, geaenderte Dateien und Kurzstatus. Reine Report-Arbeiten werden als `_codex_reports/...md` per PR eingebracht. Reine lokale Ablaeufe werden als `_codex_reports/local_...md` dokumentiert oder mindestens mit eindeutigem Abschlusskommentar im Issue belegt. Das Team darf PR-Nummern oder Abschlussstatus nicht manuell suchen muessen.

M) Chat-beschlossene, uebergabekritische Architektur- und Arbeitsregeln, die nicht sinnvoll vollstaendig in 95/97/98/99 oder eine Fachspec gehoeren, werden kompakt in `specs/96_frozen_project_state.md` gefuehrt. Der Chat ist nicht die fachliche Source of Truth; Frozen State ist ein versionierter Schutz gegen Kontextverlust.

N) Wenn der Benutzer `frozen` schreibt, muss `specs/96_frozen_project_state.md` geprueft und bei Bedarf aktualisiert werden. Dabei muss ausdruecklich geprueft werden, ob alte Eintraege geloescht, ersetzt oder in eine echte Spec ueberfuehrt werden koennen. Neue Eintraege duerfen nicht blind angehaengt werden. ChatGPT muss auch selbst vorschlagen, Frozen State zu aktualisieren, wenn eine uebergabekritische Regel beschlossen wurde.

O) Zukuenftige Architektur-Audits starten nach `specs/94_start_audit_protocol.md`. Audits sind read-only, behandeln bestehende Artefakte als Hypothesen und klassifizieren Befunde mindestens als PASS, WARN, FAIL oder ALT.

## Aktueller Gate-Stand

Finales Pre-Handoff Gate 004 auf damaligem `main` wurde bestanden:

- KRITISCH: 0
- MITTEL: 0
- REDAKTIONELL: 0 blockierend
- Handoff-Empfehlung: JA

Nach dieser Datei-Aktualisierung muss vor einer neuen Uebergabe erneut ein aktuelles Pre-Handoff-Gate ausgefuehrt werden.
