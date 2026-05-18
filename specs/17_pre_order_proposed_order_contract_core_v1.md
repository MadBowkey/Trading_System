# Pre-Order / Proposed Order Contract Core v1.0

Status: DRAFT
Version: v1.0
Architecture: v1.6.1
Position: Vor Station 8

## A) Zweck und Architekturposition

Der Pre-Order / Proposed Order Contract definiert die verbindliche Eingabestruktur für Orders, bevor sie an Station 8 übergeben werden.

Er beschreibt ausschließlich vorgeschlagene Orders.

Er darf keine Order validieren, ausführen, reparieren oder simulieren.

Er ist der Übergabevertrag zwischen strategischer Allokations-/Rebalancing-Logik und Station 8 Order Validator.

## B) Felder einer ProposedOrder

A) Immer Pflicht

- proposed_order_ref – eindeutig innerhalb run_id
- run_id
- asset_id
- symbol
- side – BUY | SELL
- order_type – MARKET | LIMIT
- quantity – Decimal-String, > 0
- limit_price – Decimal-String bei LIMIT, null bei MARKET
- allow_short – bool, immer vorhanden, default false
- proposed_at – UTC-ISO-String
- market_data_snapshot_ref
- portfolio_state_ref

B) Herkunft / Traceability

- decision_ref – Pflicht, wenn die Order direkt aus einer strategischen Entscheidung stammt
- position_change_plan_ref – Pflicht, wenn die Order aus einem Position Change Plan abgeleitet wurde

Regel: Mindestens eine fachliche Herkunftsreferenz muss vorhanden sein.

C) Ausführungsgrenzen

- time_in_force – optional, Default DAY, erlaubt: DAY | GTC
- max_slippage_bps – optionaler Override als Decimal-String
- max_commission_amount – optionaler Override als Decimal-String
- liquidity_check_ref – optional, wenn eine separate Liquiditätsprüfung referenziert wird

Regel: Fehlen optionale Ausführungsgrenzen, nutzt Station 8 die gültige Konfiguration.

D) Short-/Margin

- allow_short – immer vorhanden
- short_authorization_ref – Pflicht nur bei allow_short = true
- max_authorized_short_quantity – Pflicht nur bei allow_short = true

Regeln:

- allow_short = true ist nur für SELL relevant.
- Ohne allow_short = true darf ein SELL-Überhang nicht als autorisierter Short interpretiert werden.

E) Nicht enthalten

- order_ref – entsteht erst durch Station 8
- station_8_validation_ref – entsteht erst durch Station 8
- source_order_ref – gehört zum Execution Simulator
- fill_status – gehört zum Execution Simulator
- simulation_status – gehört zum Execution Simulator
- audit_hash – gehört ins Audit-Event

## C) Grundregeln des Proposed-Order-Contracts

A) Charakter

Eine ProposedOrder ist ein Ordervorschlag, keine validierte oder ausführbare Order. Erst Station 8 kann daraus eine validierte Order erzeugen.

B) Keine Validierungs- oder Reparaturfunktion

Der Contract definiert Form, Mindeststruktur und Referenzen. Er validiert keine Order fachlich, repariert keine Felder und entscheidet nicht über Ausführung, Freigabe oder Ablehnung.

C) Referenzkette / Traceability

proposed_order_ref → source_proposed_order_ref / order_ref → source_order_ref

- proposed_order_ref – ursprünglicher Ordervorschlag
- source_proposed_order_ref – Rückverweis der validierten Order auf die ursprüngliche ProposedOrder
- order_ref – von Station 8 freigegebene validierte Order
- source_order_ref – Execution-Fill verweist auf validierte Order

D) Status- und Audit-Regel

Der Proposed-Order-Contract erzeugt keinen eigenen Pipeline-, System- oder Audit-Sonderstatus. Auditierbar wird die spätere Prüfung durch Station 8.

E) Determinismus

Gleicher Input, gleiche Konfiguration und gleiche Marktdatenreferenz müssen zur gleichen Station-8-Prüfbasis führen.

## D) Erlaubte Werte und Feldregeln

A) side

- BUY – Kauforder
- SELL – Verkaufsorder

Andere Werte sind in Core v1.0 nicht erlaubt.

B) order_type

- MARKET – Ausführung ohne limit_price
- LIMIT – Ausführung nur mit limit_price

Regeln:

- MARKET → limit_price = null
- LIMIT → limit_price muss gesetzt sein

C) quantity

- quantity > 0
- Decimal-String
- keine Float-Werte
- keine negativen Mengen
- keine Nullmenge

D) limit_price

- Decimal-String bei LIMIT
- null bei MARKET
- > 0, wenn gesetzt

E) time_in_force

- DAY – Default
- GTC – erlaubt, wenn vom Broker-/Systemprofil unterstützt

Fehlt time_in_force, gilt DAY.

F) Decimal- und Zeitformat

- Decimal-Werte → als String
- Zeitpunkte → UTC-ISO-String

Beispiele:

- quantity = "12.5000"
- limit_price = "425.75"
- proposed_at = "2026-05-18T08:30:00.000Z"

G) Nicht erlaubte Werte

- side = SHORT
- side = COVER
- order_type = STOP
- order_type = STOP_LIMIT
- quantity als Float
- limit_price als Float
- lokale Zeit ohne UTC-Bezug

## E) Übergabe an Station 8

A) Übergabeobjekt

Station 8 erhält eine Liste von ProposedOrder-Objekten als prüfpflichtige Eingabe.

- proposed_order_list

B) Mindestanforderung

Die Liste darf nur strukturell vollständige ProposedOrder-Objekte enthalten.

- fehlende Pflichtfelder → technischer Eingabefehler
- ungültige Feldwerte → technischer Eingabefehler
- fachlich riskante Order → Prüfung durch Station 8

C) Keine Vorentscheidung

Die Übergabe an Station 8 bedeutet keine Freigabe.

- ProposedOrder → noch nicht validiert
- ValidatedOrder → erst nach Station-8-Freigabe

D) Referenzweitergabe

Station 8 muss proposed_order_ref erhalten und daraus bei Freigabe ein order_ref erzeugen.

- proposed_order_ref bleibt Rückverweis auf den Vorschlag
- order_ref entsteht erst in Station 8

E) Fehlerwirkung

Der Proposed-Order-Contract setzt keinen system_status und keine pipeline_action.

Technische Strukturfehler dürfen vor Station 8 blockieren. Fachliche Orderfragen gehören in Station 8.

## F) Output / Ergebnis des Proposed-Order-Contracts

A) Primärer Output

Der Contract liefert genau eine proposed_order_list.

Jedes Element entspricht vollständig den Feldern und Regeln aus Abschnitt B–D.

B) Kein Validierungsoutput

Der Proposed-Order-Contract erzeugt nicht:

- APPROVED / REJECTED
- order_ref
- station_8_validation_ref
- validated_order_list

Diese entstehen ausschließlich in Station 8.

C) Technischer Strukturstatus

- CONTRACT_READY – Struktur vollständig und formal korrekt
- CONTRACT_INVALID – Pflichtfeld fehlt oder formal ungültig

CONTRACT_INVALID ist ein technischer Eingabefehler vor Station 8 und kein fachliches Reject von Station 8.

D) Fehlerdetails bei CONTRACT_INVALID

- missing_fields
- invalid_fields
- affected_proposed_order_ref, falls zutreffend
- reason

E) Weitergabe

Bei CONTRACT_READY wird die unveränderte proposed_order_list an Station 8 übergeben.

Keine Reparatur, Normalisierung oder Ergänzung von Feldern.

## G) Golden Cases Proposed-Order-Contract Core v1.0

A) TC_PRE_001 — Gültige LIMIT-BUY Order

Input: Vollständige ProposedOrder mit side = BUY, order_type = LIMIT, limit_price gesetzt und allen Pflichtfeldern.

Erwartung: CONTRACT_READY, unveränderte Weitergabe an Station 8.

B) TC_PRE_002 — MARKET mit limit_price

Input: order_type = MARKET, limit_price gesetzt.

Erwartung: CONTRACT_INVALID, invalid_fields enthält limit_price.

C) TC_PRE_003 — LIMIT ohne limit_price

Input: order_type = LIMIT, limit_price = null.

Erwartung: CONTRACT_INVALID, invalid_fields oder missing_fields enthält limit_price.

D) TC_PRE_004 — Ungültige quantity

Input: quantity ≤ 0, Float statt Decimal-String oder ungültiges Format.

Erwartung: CONTRACT_INVALID, invalid_fields enthält quantity.

E) TC_PRE_005 — Fehlende Herkunftsreferenz

Input: Weder decision_ref noch position_change_plan_ref vorhanden.

Erwartung: CONTRACT_INVALID, reason verweist auf fehlende Traceability.

F) TC_PRE_006 — Unvollständige Short-Autorisierung

Input: allow_short = true, aber short_authorization_ref oder max_authorized_short_quantity fehlt.

Erwartung: CONTRACT_INVALID.

G) TC_PRE_007 — Nicht erlaubter Order-Typ

Input: order_type = STOP, STOP_LIMIT oder ähnlich.

Erwartung: CONTRACT_INVALID.

H) TC_PRE_008 — Traceability-Erhalt

Input: Gültige Liste mit korrekten proposed_order_ref.

Erwartung: proposed_order_ref bleibt unverändert, kein order_ref und keine station_8_validation_ref werden erzeugt.

## H) Abgrenzung / Nicht-Ziele Core v1.0

A) Keine Validierung

Der Contract prüft nur Struktur und formale Feldregeln.

Fachliche, risikobasierte und broker-spezifische Prüfung erfolgt ausschließlich in Station 8.

B) Keine Order-Erzeugung

Der Contract erzeugt keine Orders. Er definiert nur das Format bereits vorgeschlagener Orders.

C) Keine Reparatur oder Normalisierung

Keine Korrektur von Mengen, Preisen, Sides, Typen oder Referenzen.

Keine Tick-Size-, Lot-Size- oder Preisnormalisierung. Diese Prüfung gehört zu Station 8.

D) Keine Execution-Logik

Keine Fills, Slippage-, Gebühren- oder Portfolio-Fortschreibung.

E) Keine Status- oder Audit-Wirkung

Kein system_status, keine pipeline_action, kein APPROVED oder REJECTED.

Kein eigenes Audit-Event.

Auditierung erfolgt durch Station 8.

## I) Codex-Hinweis / Implementierungsgrenzen

A) Codex darf implementieren

Strukturprüfung des ProposedOrder-Contracts, Feldprüfungen, Fehlerdetails und Übergabe der unveränderten proposed_order_list an Station 8.

B) Codex darf nicht ergänzen

Keine fachliche Ordervalidierung, keine Order-Reparatur, keine Normalisierung, keine Execution-Logik, keine Portfolio-Fortschreibung.

C) Statusgrenze

Codex darf nur CONTRACT_READY oder CONTRACT_INVALID für den Contract erzeugen.

Kein APPROVED, kein REJECTED, kein system_status, keine pipeline_action.

D) Referenzgrenze

Codex darf proposed_order_ref prüfen und weitergeben.

order_ref und station_8_validation_ref entstehen ausschließlich in Station 8.

E) Persistenz

Decimal-Werte bleiben Strings. Zeitpunkte bleiben UTC-ISO-Strings.
