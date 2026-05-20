# Spec 18 — Portfolio State & Ledger Core v1.0

Status: FINAL
Version: v1.0
Architecture: v1.6.1
Last updated: 2026-05-20
Owner: Trading System Project

## A) Rolle

Portfolio State = verbindlicher Zustand zu einem bestimmten Zeitpunkt.

Portfolio Ledger = append-only Historie aller Zustände.

Spec 18 definiert die Zustands- und Historienbasis für Portfolio, Cash, Positionen, Simulationsergebnisse und spätere Reports.

## B) Architekturposition

Portfolio State & Ledger Core v1.0 ist eine Querschicht.

Sie ist nicht Station 9.

Sie wird von Station 1 bis Station 8, Execution Simulator und später Reports genutzt.

Sie darf nicht:

- Orders erzeugen
- Strategieentscheidungen treffen
- Risikoentscheidungen treffen
- Validator-Status setzen
- Pipeline-Status setzen
- Audit Core ersetzen
- simulierte Zustände automatisch zu echten Zuständen machen

## C) Zentrale Zustandsarten

portfolio_state_type erlaubt in Core v1.0 folgende Werte:

A) CURRENT_CONFIRMED – letzter bestätigter echter Stand.

B) PRE_RUN_SNAPSHOT – Ausgangszustand eines Analyse-Runs.

C) TARGET_PROJECTION – von Station 6 erzeugtes Zielportfolio.

D) POST_TRADE_VALIDATED_TARGET – von Station 7 freigegebenes Zielportfolio.

E) SIMULATED_POST_EXECUTION – hypothetischer, nicht bestätigter Zustand aus dem Execution Simulator.

F) MANUAL_CORRECTION – manuell korrigierter Zustand mit Begründung.

Wichtig:

SIMULATED_POST_EXECUTION wird nie automatisch zu CURRENT_CONFIRMED.

## D) Minimale Pflichtfelder Portfolio State Core v1.0

Jeder Portfolio State enthält mindestens:

- portfolio_state_ref
- parent_portfolio_state_ref nullable
- run_id
- timestamp_utc
- portfolio_state_type
- source
- portfolio_value
- cash
- positions
- data_quality_status
- audit_ref

positions[] enthält mindestens:

- asset_id
- symbol
- quantity
- market_value

## E) Ledger-Regeln

A) Append-only: Bestehende Ledger-Einträge werden nicht aktualisiert oder überschrieben.

B) Jeder Ledger-Eintrag braucht portfolio_state_ref, source und audit_ref.

C) Korrekturen erzeugen einen neuen Ledger-Eintrag mit parent_portfolio_state_ref.

D) Simulierte Zustände bleiben als simuliert markiert.

E) Simulierte Zustände dürfen nicht automatisch bestätigte Echtzustände werden.

F) Bei Widerspruch zwischen abgeleiteten Ansichten und Ledger gilt der Ledger.

## F) Schnittstellen

A) Station 1 nutzt CURRENT_CONFIRMED oder PRE_RUN_SNAPSHOT als Eingang.

B) Station 6 erzeugt TARGET_PROJECTION.

C) Station 7 erzeugt oder bestätigt POST_TRADE_VALIDATED_TARGET.

D) Station 8 erzeugt keinen Portfolio State.

E) Execution Simulator erzeugt SIMULATED_POST_EXECUTION.

F) Audit protokolliert State-Erstellung, Korrektur und Referenzen.

G) Reports lesen den Ledger und schreiben ihn nicht.

## G) Core-v1-Grenzen

Nicht Teil von Portfolio State & Ledger Core v1.0:

- Broker-Live-Sync
- automatische Bestandsübernahme
- Steuerlogik
- ML-Auswertung
- Performance-Attribution im Detail
- automatische Umwandlung von Simulation in Echtbestand
- mehrperiodige Simulation
- neue Portfolio-State-Typen ohne fachlichen Beschluss

## H) Golden Cases Portfolio State & Ledger Core v1.0

| Case | Zweck | Erwartung |
|---|---|---|
| TC_LEDGER_001 | Gültiger CURRENT_CONFIRMED State | State wird akzeptiert und im Ledger gespeichert. |
| TC_LEDGER_002 | Fehlende Pflichtfelder | State wird abgelehnt: CONTRACT_INVALID. |
| TC_LEDGER_003 | SIMULATED_POST_EXECUTION | Bleibt strikt simuliert; keine automatische Umwandlung zu CURRENT_CONFIRMED. |
| TC_LEDGER_004 | MANUAL_CORRECTION | Neuer Ledger-Eintrag mit korrektem parent_portfolio_state_ref. |
| TC_LEDGER_005 | Append-only-Verstoß | Versuch eines Updates oder Overwrites wird abgelehnt. |
| TC_LEDGER_006 | Ledger-Index Rekonstruierbarkeit | Index kann vollständig aus dem Ledger neu erzeugt werden. |
| TC_LEDGER_007 | Index-Widerspruch | Ledger gewinnt immer; Index wird ignoriert. |
| TC_LEDGER_008 | Execution Simulator State | SIMULATED_POST_EXECUTION wird mit audit_ref und run_id korrekt gespeichert, bleibt aber nicht bestätigt. |

Diese acht Fälle decken die Kernschutzregeln von Spec 18 ab: Append-only, Trennung simuliert/echt, Referenzintegrität und Index-Rekonstruierbarkeit.

## I) Codex-Hinweis

Codex darf später implementieren:

- Portfolio-State-Datenmodell
- Ledger-Append-Only-Writer
- Referenzprüfung für portfolio_state_ref und parent_portfolio_state_ref
- Persistenzstruktur
- einfache Golden Cases nach beschlossener Spec
- Ledger-Index als rekonstruierbare abgeleitete Navigationsstruktur

Codex darf nicht ergänzen:

- Broker-Live-Sync
- automatische Bestandsübernahme
- steuerliche Logik
- Performance-Attribution
- ML-Auswertung
- automatische Umwandlung von SIMULATED_POST_EXECUTION zu CURRENT_CONFIRMED
- neue Portfolio-State-Typen ohne fachlichen Beschluss
- neue fachliche Ledger-Statuslogik ohne beschlossene Spec

## J) Ledger-Index Core v1.0

Der Ledger-Index ist eine abgeleitete Navigationsstruktur über dem append-only Portfolio Ledger.

Er ist nicht die fachliche Wahrheit – diese bleibt immer der Ledger selbst.

Zweck:

- schneller Zugriff auf den aktuellen CURRENT_CONFIRMED State
- Zuordnung von run_id zu den verschiedenen portfolio_state_type
- Nachvollziehbarkeit von Korrekturen über parent_portfolio_state_ref
- Verknüpfung zwischen Execution Simulator, States und Audit

Minimale Index-Schlüssel:

- portfolio_state_ref
- parent_portfolio_state_ref nullable
- run_id
- portfolio_state_type
- timestamp_utc
- source
- audit_ref

Regeln:

- Der Index muss vollständig aus dem Ledger rekonstruierbar sein.
- Bei Widerspruch gilt immer der Ledger.
- Der Index darf gelöscht und neu aufgebaut werden.
- Der Index darf keine States erzeugen, ändern oder bestätigen.
- Der Index enthält keine zusätzlichen fachlichen Informationen.

## K) Ledger Operation Outcomes Core v1.0

Ledger Operation Outcomes beschreiben nur das Ergebnis einer Portfolio-State-/Ledger-Operation.

Sie sind keine Pipeline-Statuswerte, keine Systemstatuswerte und keine Audit-Core-Statuswerte.

Erlaubte Outcomes in Core v1.0:

A) APPEND_ACCEPTED – ein neuer Portfolio-State-Eintrag wurde erfolgreich append-only in den Ledger aufgenommen.

B) REJECTED – eine Ledger-Operation wurde abgelehnt; der Ledger bleibt unverändert.

C) CONTRACT_INVALID – eine Ledger-Operation wurde wegen fehlender Pflichtfelder, ungültiger Felder oder ungültiger Struktur abgelehnt.

D) APPEND_ONLY_VIOLATION – eine Operation versucht, einen bestehenden Ledger-Eintrag zu ändern, zu überschreiben oder zu löschen; die Operation wird abgelehnt.

Regeln:

- Jeder REJECTED-, CONTRACT_INVALID- oder APPEND_ONLY_VIOLATION-Fall darf keinen bestehenden Ledger-Eintrag verändern.
- CONTRACT_INVALID ist ein technischer Contract-Fehler der Ledger-Operation, kein fachlicher Portfolio- oder Risikoreject.
- APPEND_ONLY_VIOLATION ist ein Integritätsverstoß gegen die Ledger-Regel, kein Pipeline-Stopp.
- Audit Core bleibt unverändert; die Ledger-Operation referenziert Audit über audit_ref.
- Ledger Operation Outcomes erzeugen keine neuen pipeline_action-, system_status- oder validator_status-Werte.

Minimale data_quality_status-Werte in Core v1.0:

- VALID – bestätigter oder formal gültiger Zustand.
- SIMULATED – hypothetischer simulierter Zustand.
- VALID_CORRECTED – gültiger manuell korrigierter Zustand.

data_quality_status ist State-Metadatum. Es ersetzt keinen Ledger Operation Outcome und keinen Audit-Status.
