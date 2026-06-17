# Start Audit Protocol

Status: CURRENT
Project: Trading System
Last updated: 2026-06-17

## Zweck

Diese Datei definiert den Startmodus fuer zukuenftige Read-only-Architektur-Audits.

Sie ersetzt keine fachliche Spezifikation. Sie legt fest, wie bestehende Specs, Schnittstellen, Modulgrenzen und Chat-beschlossene Regeln gegen harte Architektur-Invarianten geprueft werden.

## Grundsatz

Jedes bestehende Artefakt ist im Audit zunaechst eine Hypothese.

Es erhaelt keine Autoritaet durch Historie, Plausibilitaet, bisherige Nutzung oder eloquente Begruendung.

Geprueft wird nicht, ob die aktuelle Loesung erklaerbar ist, sondern ob sie strukturell sauber, state-sicher, alternativensensibel und beweisbar ist.

## Audit-Grenzen

Das Audit ist read-only.

Es darf:

- Specs, Index, Handoff-Dateien, Reports, Config und Golden Cases lesen
- Architekturgrenzen bewerten
- Befunde klassifizieren
- fehlende Beweise benennen
- bessere Architektur-Alternativen vorschlagen

Es darf nicht:

- Dateien aendern
- Code reparieren
- Specs umschreiben
- Golden Cases veraendern
- Optimierungen im Vorbeigehen einbauen
- bestehende Artefakte stillschweigend als gueltig behandeln

## Pflichtfilter

A) Harte vs. scheinbare Constraints

- Ist die Grenze technisch, regulatorisch oder fachlich zwingend?
- Oder ist sie Altlast, Bequemlichkeit, Werkzeuggrenze oder unbelegte Annahme?

B) Alternativenpflicht

- Wurde mindestens eine bessere, schlankere oder robustere Alternative aktiv geprueft?
- Wenn nein: Befund ALT oder WARN, je nach Risiko.

C) State-Leak-Pruefung

- Kann ein hypothetischer, simulierter, abgeleiteter oder geplanter Zustand versehentlich offizieller State werden?
- Was State veraendert, muss eindeutig Reconciliation / Official State zugeordnet sein.

D) Autoritaets-Trennung

- LLM/probabilistisch: darf vorschlagen, interpretieren, begruenden.
- Risk/Guardrail/Validator/deterministisch: muss harte Grenzen pruefen und erzwingen.
- Simulator/quantitativ: darf rechnen und Constraints liefern, aber keinen offiziellen State erzeugen.

E) Beweisfilter

- Welche Datei, welcher Contract, welcher Golden Case oder welcher deterministische Test beweist die Grenze?
- Was nicht beweisbar getrennt ist, gilt als potenziell vermischt.

## Erste Audit-Schwerpunkte

A) Execution Simulator <-> Final Risk Logic

- Simulator darf Execution-Szenarien und Constraints liefern.
- Simulator darf niemals Portfolio-State erzeugen.
- Simulationsergebnisse duerfen Risikologik beeinflussen, aber nicht Reconciliation oder CURRENT_CONFIRMED ersetzen.

B) LLM <-> Guardrails

- LLM darf keine harten Risikogrenzen ersetzen.
- Harte Regeln duerfen nicht nur in Prompt-/LLM-Logik versteckt sein.

C) Reconciliation <-> Portfolio State

- Nur echte Broker-/Exchange-Fills duerfen ueber Reconciliation offiziellen State aktualisieren.
- SIMULATED_POST_EXECUTION darf nie automatisch CURRENT_CONFIRMED werden.

D) Golden Cases / Testbarkeit

- Architekturentscheidungen muessen durch Contracts, Enums, Zustandsuebergaenge oder Golden Cases pruefbar sein.

## Befundklassifikation

PASS = Grenze ist sauber spezifiziert und beweisbar.

WARN = Grenze ist begrifflich oder strukturell unscharf; spaeterer State-Leak oder Autoritaets-Leak moeglich.

FAIL = echte logische Vermischung, State-Leak, Autoritaets-Konfusion oder nicht erlaubte Mutation.

ALT = bessere Architektur-Alternative wurde nicht sichtbar geprueft oder vorschnell verworfen.

## Minimaler Auditbericht

Jeder Auditbericht enthaelt mindestens:

A) Scope
B) Gelesene Artefakte
C) Gepruefte Architekturgrenzen
D) PASS/WARN/FAIL/ALT-Befunde
E) Beweisstelle oder fehlender Beweis
F) Harte Constraints vs. scheinbare Constraints
G) Gegenentwurf oder Alternative, falls relevant
H) Entscheidungsvorschlag: behalten / aendern / verschieben / streichen

## Verhaeltnis zu Frozen State

`specs/96_frozen_project_state.md` enthaelt kompakte, uebergabekritische Chat-Entscheidungen.

Dieses Audit-Protokoll definiert, wie solche Entscheidungen und alle anderen Artefakte in zukuenftigen Architektur-Audits geprueft werden.
