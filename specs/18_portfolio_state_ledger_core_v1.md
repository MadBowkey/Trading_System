# Spec 18 — Portfolio State & Ledger Core v1.0

Status: DRAFT
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

## H) Golden Cases

Golden Cases werden später ergänzt.

Für Core v1.0 sind später mindestens zu prüfen:

- gültiger CURRENT_CONFIRMED State
- ungültiger State bei fehlender Pflichtreferenz
- SIMULATED_POST_EXECUTION wird nicht automatisch CURRENT_CONFIRMED
- MANUAL_CORRECTION erzeugt neuen Ledger-Eintrag mit parent_portfolio_state_ref
- Ledger-Index ist aus dem Ledger rekonstruierbar

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
