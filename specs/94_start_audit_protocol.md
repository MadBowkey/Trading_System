# Start Audit Protocol

Status: CURRENT
Project: Trading System
Last updated: 2026-06-17

## Zweck

Diese Datei definiert den Startmodus fuer zukuenftige Read-only-Architektur-Audits.

Sie ersetzt keine fachliche Spezifikation. Sie legt fest, wie bestehende Specs, Schnittstellen, Modulgrenzen und chat-beschlossene Regeln gegen harte Architektur-Invarianten geprueft werden.

## Grundsatz

Jedes bestehende Artefakt ist im Audit zunaechst eine Hypothese.

Es erhaelt keine Autoritaet durch Historie, Plausibilitaet, bisherige Nutzung oder eloquente Begruendung.

Geprueft wird nicht, ob die aktuelle Loesung erklaerbar ist, sondern ob die Architektur beweisen kann, dass sie trotz Alternativen, Constraints und Komponentenuebergaengen strukturell sauber bleibt.

## Audit-Grenzen

Das Audit ist read-only.

Es darf:

- Specs, Index, Handoff-Dateien, Reports, Config und Golden Cases lesen
- Architekturgrenzen bewerten
- Suchtreffer und Befunde klassifizieren
- fehlende Beweise benennen
- bessere Architektur-Alternativen vorschlagen

Es darf nicht:

- Dateien aendern
- Code reparieren
- Specs umschreiben
- Golden Cases veraendern
- Optimierungen im Vorbeigehen einbauen
- bestehende Artefakte stillschweigend als gueltig behandeln

## Harte Audit-Prueffelder

Jedes Audit prueft mindestens diese Felder:

A) Schichten-Trennung

- Python-Guardrails, Risk-Metrics, LLM-Entscheidung, Validator, Execution Simulator, Reconciliation und Portfolio State muessen klare Zustaendigkeiten haben.
- Probabilistische, quantitative und deterministische Komponenten duerfen nicht vermischt werden.

B) Harte Limits vs. scheinbare Limits

- Jede Aussage wie `geht nicht`, `muss so sein` oder `ist alternativlos` wird auf echte technische, regulatorische oder fachliche Notwendigkeit geprueft.
- Altlasten, Werkzeuggrenzen, Bequemlichkeit und unbelegte Annahmen gelten nicht als harte Constraints.

C) Deduktive Regeln vs. ML/LLM

- Feste Finanz- und Risikoregeln muessen als harte Leitplanken, Guardrails, Validatorlogik oder pruefbare Contracts sichtbar sein.
- Sie duerfen nicht nur weich in Prompt- oder LLM-Logik versteckt sein.

D) Core-vs-Zielarchitektur

- Core v1 muss ein sauberer Subset der Zielarchitektur sein.
- Fruehe Abkuerzungen duerfen keinen spaeteren architektonischen Umbau erzwingen.

E) Kontrollierbarkeit

- Jede Entscheidung muss erklaerbar, validierbar und bei Fehlern stoppbar sein.
- Unklare Statuswerte, unklare Verantwortlichkeiten oder nicht stoppbare Entscheidungswege sind WARN oder FAIL.

F) Komplexitaet

- Komplexitaet darf nur dort erhoeht werden, wo sie Struktur, Sicherheit, Testbarkeit oder Erweiterbarkeit verbessert.
- Einfache sichtbare Kompromisse sind zu pruefen, wenn eine bessere strukturelle Alternative moeglich ist.

G) Testbarkeit

- Testbarkeit ist ein eigener harter Auditfilter, nicht nachgelagerte Qualitaetssicherung.
- Erwartet werden Golden Cases, Enum-Pruefungen, Validator-Checks, reproduzierbare Entscheidungsprotokolle, Fehlerklassifikationen und Cross-Reference-Checks.
- Fehlende Testbarkeit ist besonders kritisch, weil ein System sonst plausibel aussehen kann, ohne strukturell beweisbar korrekt zu sein.

H) Alternativenpflicht

- Groessere Architekturentscheidungen muessen gegen starke Gegenentwuerfe oder schlankere Alternativen geprueft werden.
- Wird nur die zuerst naheliegende Loesung ausgearbeitet, ist das mindestens ALT, je nach Risiko auch WARN.

## Beweislast

Eine Architekturentscheidung gilt erst als belastbar, wenn sie durch mindestens eines der folgenden Artefakte beweisbar ist:

- Spec-Contract
- eindeutige Schnittstelle
- Enum oder Statusmodell
- harter Zustandsuebergang
- Golden Case
- deterministischer Test
- Cross-Reference-Check
- Audit- oder Entscheidungsprotokoll

Ohne Beweis bleibt das Audit auf Argumentationsniveau.

## Execution-Simulator-State-Leak-Audit

Dieser Spezialfall ist vorrangig zu pruefen, weil der State-Leak leise entstehen kann.

Harte Invarianten:

A) Der Execution Simulator darf keine finale Risikoentscheidung treffen.

B) Die finale Risikologik darf simulierte Ausfuehrungen nicht als echte Zustaende behandeln.

C) Der Execution Simulator darf keinen PortfolioState, Ledger-State, Reconciliation-State, CASH_ONLY-Status oder Risk-Regime final setzen.

D) Final Risk darf SimulationReport, Partial Fill, No Fill oder Slippage nicht als echte Position, echten Fill oder echten Risk-State verbuchen.

E) Nur Reconciliation echter Broker-/Exchange-Fills darf offiziellen Portfolio-State aktualisieren.

Erlaubter Simulator-Rueckkanal:

- ExecutionConstraint
- SimulationReport
- liquidity_status
- max_executable_quantity
- expected_slippage_bps
- residual_quantity_risk
- scenario_type: FULL_FILL / PARTIAL_FILL / NO_FILL / SLIPPAGE_CASE / STALE_ORDERBOOK

Verbotener Rueckkanal:

- PortfolioState.update aus Simulation
- Ledger/Reconciliation-State aus Simulation
- echte Position aus SimulationReport
- echter Fill aus SimulationReport
- finaler Risk-State aus SimulationReport
- interne Weiterrechnung auf simuliertem offiziellen State

Soll-Kette:

Official Snapshot
-> Strategy / LLM Candidate
-> Risk Precheck
-> Execution Simulator
-> ExecutionConstraint / SimulationReport
-> Final Risk Scenario Validation
-> OrderTicket
-> Exchange
-> Real FillEvent
-> Reconciliation
-> Official PortfolioState Update

Verbotene Kette:

Execution Simulator
-> PortfolioState Update

oder:

SimulationReport
-> echte Position / echter Fill / echter Risk-State

## State-Leak-Golden-Case-Pflicht

Mindestens diese Faelle muessen existieren oder als fehlend gemeldet werden:

A) FULL_FILL: Order moeglich, State bleibt bis Reconciliation unveraendert.

B) PARTIAL_FILL: Simulator meldet Teilfuellbarkeit, State bleibt unveraendert, neuer isolierter Plan / Reduce / Block.

C) NO_FILL: keine State-Aenderung, Order blockiert oder neu geplant.

D) HIGH_SLIPPAGE: keine State-Aenderung, Order reduziert oder blockiert.

E) STALE_ORDERBOOK: Simulation ungueltig, keine Risikoentscheidung auf Basis dieser Simulation.

## Erster Schritt im State-Leak-Audit

Zuerst nur read-only Suchaudit laufen lassen und Treffer posten.

Danach werden die Fundstellen gezielt klassifiziert.

Nicht sofort Code, Specs oder Golden Cases umschreiben.

## Befundklassifikation

PASS = Grenze ist sauber spezifiziert und beweisbar.

WARN / MITTEL = Grenze ist begrifflich oder strukturell unscharf; spaeterer State-Leak oder Autoritaets-Leak moeglich.

FAIL / KRITISCH = echte logische Vermischung, State-Leak, Autoritaets-Konfusion oder nicht erlaubte Mutation.

ALT = bessere Architektur-Alternative wurde nicht sichtbar geprueft oder vorschnell verworfen.

## Minimaler Auditbericht

Jeder Auditbericht enthaelt mindestens:

A) Scope
B) gelesene Artefakte
C) gepruefte Architekturgrenzen
D) Suchtreffer, falls Suchaudit
E) PASS/WARN/FAIL/ALT-Befunde
F) Beweisstelle oder fehlender Beweis
G) harte Constraints vs. scheinbare Constraints
H) Gegenentwurf oder Alternative, falls relevant
I) Entscheidungsvorschlag: behalten / aendern / verschieben / streichen

## Verhaeltnis zu Frozen State

`specs/96_frozen_project_state.md` enthaelt kompakte, uebergabekritische Chat-Entscheidungen.

Dieses Audit-Protokoll definiert, wie solche Entscheidungen und alle anderen Artefakte in zukuenftigen Architektur-Audits geprueft werden.
