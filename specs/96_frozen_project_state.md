# Frozen Project State

Status: CURRENT
Project: Trading System
Last updated: 2026-06-18

## Zweck

Diese Datei enthaelt kompakte, uebergabekritische Chat-Entscheidungen.

Sie ist nicht die fachliche Single Source of Truth. Fachliche Wahrheit bleibt GitHub `main` mit den Specs, Golden Cases und Config-Dateien.

## Pflege-Regel

Wenn der Benutzer `frozen` schreibt, wird diese Datei kuratiert geprueft.

Dabei gilt:

- neue Eintraege nur aufnehmen, wenn sie fuer neue Chats wirklich uebergabekritisch sind
- alte Eintraege auf Loeschung, Ersetzung oder Ueberfuehrung in echte Specs pruefen
- keine blinde Ergaenzung
- kompakt bleiben

## Aktive Frozen-State-Eintraege

FS-001 — Chat ist keine Source of Truth
Status: ACTIVE
Regel: Chat ist Diskussions- und Review-Raum, nicht fachliche Wahrheit.

FS-002 — Bestehende Artefakte sind Hypothesen
Status: ACTIVE
Regel: Im Audit gelten bestehende Specs, Pipelines und Modulgrenzen zunaechst als Hypothesen.

FS-003 — Gegenentwurfs-Pflicht
Status: ACTIVE
Regel: Groessere Architekturentscheidungen muessen gegen starke Gegenentwuerfe oder schlankere Alternativen geprueft werden.

FS-004 — Audit mutiert nicht
Status: ACTIVE
Regel: Audit ist read-only und darf nichts reparieren, umschreiben, optimieren oder fortentwickeln.

FS-005 — Testbarkeit hat Vorrang
Status: ACTIVE
Regel: Testbarkeit ist harter Architekturfilter, nicht nachgelagerte Qualitaetssicherung.

FS-006 — Beweisbarkeit ist Pflicht
Status: ACTIVE
Regel: Architekturgrenzen muessen durch Datei, Contract, Golden Case, Enum, Zustandsuebergang oder deterministischen Test beweisbar sein.

FS-007 — Simulator liefert keine offiziellen States
Status: ACTIVE
Regel: Simulator-Ergebnisse duerfen Risikologik beeinflussen, aber niemals offiziellen, bestaetigten oder reconciled Portfolio-State erzeugen.

FS-008 — Simulation vs. Reconciliation
Status: ACTIVE
Regel: SIMULATED_POST_EXECUTION darf gespeichert oder berichtet werden, wird aber nie automatisch CURRENT_CONFIRMED. Offizieller Portfolio-State entsteht nur ueber Reconciliation echter Broker-/Exchange-Fills.

FS-009 — LLM und Guardrails
Status: ACTIVE
Regel: LLM darf Strategie interpretieren und vorschlagen; harte Risiko-, Validierungs- und Guardrail-Entscheidungen muessen deterministisch pruefbar sein.

FS-010 — Core bleibt Zielarchitektur-Subset
Status: ACTIVE
Regel: Core v1 muss ein sauberer Subset der Zielarchitektur bleiben.

FS-011 — Neue Chat-Uebergabe
Status: ACTIVE
Regel: Neue Chats muessen 93, 94, 95, 96, 97, 98, 99 und den aktuellen Gate-Report lesen.

FS-012 — State-Leak-Audit startet mit Suchaudit
Status: ACTIVE
Regel: Beim ersten echten State-Leak-Audit werden zuerst nur read-only Suchtreffer gesammelt und gepostet.

FS-013 — Uebergabe-Kurzbefehl
Status: ACTIVE
Regel: `uebergabe` / `übergabe` startet das New Chat Transition Protocol aus `specs/93_new_chat_transition_protocol.md`.
Wirkung: Das Protokoll erzeugt am Ende einen kurzen Copy-Paste-Prompt fuer den neuen Chat. Dieser verweist auf `specs/97_new_chat_handoff_prompt_v1.md`, die Langform-New-Prompt-Datei.

FS-014 — Uebergabe braucht naechsten fachlichen Arbeitspunkt
Status: ACTIVE
Regel: Bei jeder Uebergabe muss `specs/99_handoff_snapshot_current.md` einen konkreten naechsten fachlichen Arbeitspunkt enthalten.
Wirkung: Fehlt dieser Arbeitspunkt, ist die Uebergabe blockiert und der neue Chat darf keinen eigenen breiten Audit als Ersatz ableiten.
