# Frozen Project State

Status: CURRENT
Project: Trading System
Last updated: 2026-06-17

## Zweck

Diese Datei friert kompakte, uebergabekritische Chat-Entscheidungen ein, die fuer den Projektstand wichtig sind, aber nicht zwingend in `specs/95_operational_workflow_rules.md`, `specs/97_new_chat_handoff_prompt_v1.md`, `specs/98_spec_index.md` oder `specs/99_handoff_snapshot_current.md` vollstaendig abgebildet werden.

Sie schuetzt neue Chats gegen Kontextverlust durch lange Chatverlaeufe und Token-Verdraengung.

## Abgrenzung

Frozen State ist nicht die fachliche Single Source of Truth.

Fachliche Single Source of Truth bleiben die Specs auf GitHub `main`.

Frozen State enthaelt nur kurze, aktive Regeln und Entscheidungen, die ein neuer Chat zwingend kennen muss, um nicht falsch weiterzuarbeiten.

## Pflege-Regel

Wenn der Benutzer `frozen` schreibt, muss Frozen State geprueft und bei Bedarf aktualisiert werden.

Dabei gilt:

- nicht blind neue Eintraege anhaengen
- zuerst pruefen, ob alte Eintraege geloescht, ersetzt oder in eine echte Spec ueberfuehrt werden koennen
- nur uebergabekritische Regeln aufnehmen
- kompakt bleiben
- Aenderungen kurz berichten: hinzugefuegt / geaendert / geloescht / unveraendert

Die KI muss auch selbst vorschlagen, Frozen State zu aktualisieren, wenn eine neue harte Architekturregel, Audit-Maxime, negative Entscheidung, State-Leak-Sicherung, Gegenentwurfs-Pflicht oder Uebergaberegel beschlossen wird.

## Aktive Frozen-State-Eintraege

FS-001 — Frozen State Rolle
Status: ACTIVE
Regel: Frozen State speichert uebergabekritische Chat-Entscheidungen kompakt und versioniert.
Wirkung: Neue Chats muessen diese Datei lesen, bevor sie fachlich weiterarbeiten.
Nicht tun: Frozen State nicht als langen Handoff-Prompt oder als Ersatz fuer Specs verwenden.

FS-002 — Chat ist keine Source of Truth
Status: ACTIVE
Regel: Der Chat ist Diskussions- und Review-Raum, nicht fachliche Wahrheit.
Wirkung: Chat-Entscheidungen werden erst belastbar, wenn sie in versionierte Projektartefakte ueberfuehrt werden.
Nicht tun: Lange Chatverlaeufe als dauerhafte Architekturquelle behandeln.

FS-003 — Alte Trade-Bot-/GUI-Prototypen
Status: ACTIVE
Regel: Ein frueherer lauffaehiger Trade-Bot- oder GUI-Prototyp gehoert nicht automatisch in die Zielarchitektur.
Wirkung: Solche Prototypen duerfen hoechstens historischer Kontext oder Negativbeispiel sein.
Nicht tun: Bot-artige Direktlogik, vermischte GUI-/Trading-Logik oder unklare Verantwortung in den Core uebernehmen.

FS-004 — Bestehende Artefakte sind Hypothesen
Status: ACTIVE
Regel: Jede bestehende Spezifikation, Pipeline und Modulgrenze gilt im Architektur-Audit zunaechst als Hypothese, nicht als gueltige Architekturentscheidung.
Wirkung: Historie, Plausibilitaet und eloquente Begruendung geben keinen Heimvorteil.
Nicht tun: Nur pruefen, ob die bestehende Loesung erklaerbar ist.

FS-005 — Gegenentwurfs-Pflicht
Status: ACTIVE
Regel: Groessere Architekturentscheidungen muessen gegen mindestens einen starken Gegenentwurf oder eine schlankere Alternative geprueft werden.
Wirkung: Bequeme oder naheliegende Loesungen gelten bis zur Alternativenpruefung als vorlaeufig.
Nicht tun: Die zuerst naheliegende Loesung als Architekturautoritaet behandeln.

FS-006 — Audit mutiert nicht
Status: ACTIVE
Regel: Ein Audit ist read-only und darf nichts reparieren, umschreiben, optimieren oder fortentwickeln.
Wirkung: Audit erzeugt Befunde gegen feste Architektur-Invarianten.
Nicht tun: Audit und Implementierung vermischen.

FS-007 — Testbarkeit hat Vorrang
Status: ACTIVE
Regel: Testbarkeit ist ein harter Architekturfilter, nicht nachgelagerte Qualitaetssicherung.
Wirkung: Golden Cases, Enum-Pruefungen, Validator-Checks, reproduzierbare Entscheidungsprotokolle, Fehlerklassifikationen und Cross-Reference-Checks muessen aktiv geprueft werden.
Nicht tun: Plausible Architektur als ausreichend behandeln, wenn sie nicht beweisbar testbar ist.

FS-008 — Beweisbarkeit ist Pflicht
Status: ACTIVE
Regel: Eine Architekturgrenze gilt erst als belastbar, wenn sie durch Datei, Contract, Golden Case, Enum, Zustandsuebergang oder deterministischen Test beweisbar ist.
Wirkung: Was nicht beweisbar getrennt ist, gilt als potenziell vermischt.
Nicht tun: Nur argumentativ behaupten, dass eine Grenze sauber ist.

FS-009 — Simulator liefert Constraints, keinen State
Status: ACTIVE
Regel: Simulator-Ergebnisse duerfen Risikologik beeinflussen, aber niemals Portfolio-State erzeugen.
Wirkung: Execution Simulator liefert Prognose, Szenario oder ExecutionConstraintReport; Reconciliation bleibt alleiniger Weg zu bestaetigtem State.
Nicht tun: `Simulator -> PortfolioState.update(partial_fill)` oder interne Weiterrechnung auf simuliertem offiziellen State.

FS-010 — Simulation vs. Reconciliation
Status: ACTIVE
Regel: Nur echte Broker-/Exchange-Fills duerfen ueber Reconciliation offiziellen Portfolio-State aktualisieren.
Wirkung: `SIMULATED_POST_EXECUTION` darf nie automatisch `CURRENT_CONFIRMED` werden.
Nicht tun: Partial Fill, No Fill oder Slippage aus Simulation als echten Bestand behandeln.

FS-011 — LLM und Guardrails
Status: ACTIVE
Regel: Das LLM darf Strategie interpretieren und vorschlagen, aber harte Risiko-, Validierungs- und Guardrail-Entscheidungen muessen deterministisch ausserhalb reiner Prompt-Logik pruefbar sein.
Wirkung: Harte Finanz-/Risikoregeln duerfen nicht weich im Prompt versteckt werden.
Nicht tun: LLM als Ersatz fuer Python-Guardrails, Risk-Metrics oder Validatoren behandeln.

FS-012 — Core muss Zielarchitektur-Subset bleiben
Status: ACTIVE
Regel: Core v1 muss ein sauberer Subset der Zielarchitektur sein.
Wirkung: Fruehe Abkuerzungen duerfen keine spaetere architektonische Migration erzwingen.
Nicht tun: Kurzfristige Vereinfachung akzeptieren, wenn sie spaeter Modulgrenzen oder State-Fluss umbaut.

FS-013 — Neue Chat-Uebergabe
Status: ACTIVE
Regel: Neue Chats muessen neben 95/97/98/99 auch `specs/94_start_audit_protocol.md` und diese Datei lesen.
Wirkung: Neue Chats kennen nicht nur formalen Projektstand, sondern auch uebergabekritische Chat-Entscheidungen.
Nicht tun: Nur Handoff-Snapshot lesen und danach chat-beschlossene Architekturregeln ignorieren.

FS-014 — Start Audit Protocol
Status: ACTIVE
Regel: Architektur-Audits starten nach `specs/94_start_audit_protocol.md`.
Wirkung: Audit-Ergebnisse muessen PASS/WARN/FAIL/ALT und einen Beweis- oder Fehlbeweisbezug enthalten.
Nicht tun: Audit als normales Review der bisherigen Loesung behandeln.

FS-015 — State-Leak-Audit startet mit Suchaudit
Status: ACTIVE
Regel: Beim ersten echten State-Leak-Audit werden zuerst nur read-only Suchtreffer gesammelt und gepostet.
Wirkung: Danach werden die Fundstellen gezielt klassifiziert.
Nicht tun: Sofort Code, Specs oder Golden Cases umschreiben.
