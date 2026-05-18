# Execution Simulator Core v1.0

Status: DRAFT
Version: v1.0
Architecture: v1.6.1
Last updated: 2026-05-17
Owner: Trading System Project

## A) Rolle und Abgrenzung

Der Execution Simulator ist ein nachgelagertes What-If-Modul nach Station 8. Er simuliert ausschließlich die hypothetische Ausführung einer von Station 8 validierten Orderliste.

Er ist keine Station 9 und kein Bestandteil der Validierungs-Pipeline.

Er darf: simulieren, berechnen, berichten und auditieren.

Er darf nicht: Orders erzeugen, Orders verändern, Orders reparieren, Orders optimieren, Station 8 überstimmen, target_weights verändern, delta_weights verändern, position_change_plan verändern, die Portfolio Engine ersetzen, Live-Broker-Interaktion durchführen oder Pipeline-/Systemstatus setzen.

## B) Input

Pflicht-Input:

- run_id
- validated_order_list
- current_portfolio
- market_data_snapshot
- fee_structure
- slippage_model
- simulation_timestamp
- station_8_validation_ref

validated_order_list enthält ausschließlich Orders, die durch Station 8 freigegeben wurden.

station_8_validation_ref ist Top-Level-Pflichtfeld des Simulator-Inputs und wird nicht pro Order in validated_order_list wiederholt.

Mindestfelder pro Order:

- asset_id
- order_ref
- symbol
- side
- order_type
- quantity
- limit_price nullable
Für short-fähige SELL-Orders zusätzlich:

- allow_short: true
- short_authorization_ref
- max_authorized_short_quantity optional

## C) Output / Report Contract

Der Output ist ein strukturiertes, auditierbares Simulationsergebnis. Der Execution Simulator gibt genau ein Simulationsergebnis pro run_id und station_8_validation_ref zurück.

A) Top-Level-Output: Pflichtfelder sind run_id, simulation_timestamp, station_8_validation_ref, input_order_count, simulated_fills, post_execution_portfolio, execution_report, simulation_status, reason nullable.

Bei simulation_status = FAILED ist reason nicht nullable und enthält mindestens kurzen technischen Kontext zur Fehlerursache, betroffenen Phase oder fehlenden Datenbasis.

B) simulated_fills: Jeder simulierte Fill enthält station_8_validation_ref, asset_id, symbol, source_order_ref, side, order_type, requested_quantity, filled_quantity, fill_status, fill_price nullable, fill_timestamp, slippage_per_unit, commission, execution_cost, reason nullable.

fill_status: FULL – vollständig simuliert, PARTIAL – teilweise simuliert, NO_FILL – korrekt simuliert ohne Ausführung, FAILED – nicht belastbar simulierbar.

Traceability-Regel: station_8_validation_ref + source_order_ref verweist eindeutig auf validated_order_list[].order_ref innerhalb der zugehörigen Station-8-Validierung.

C) post_execution_portfolio: Pflichtfelder sind cash_after, positions, total_portfolio_value, asset_weight, cash_weight, effective_exposure, effective_leverage, HHI, max_single_asset_exposure_pct.

Konsistenzregel: post_execution_portfolio.total_portfolio_value = cash_after + Summe(position_market_values). Wenn diese Gleichung nicht belastbar herstellbar ist: simulation_status = FAILED.

D) execution_report: Pflichtfelder sind turnover_pct, fill_rate_avg, filled_order_count, partial_fill_count, no_fill_count, failed_fill_count, total_commission, total_slippage_cost, total_execution_cost, estimated_pnl_impact, slippage_summary, cost_summary, reason_summary nullable.

simulation_status: SUCCESS – alle Orders FULL, PARTIAL – mindestens PARTIAL oder NO_FILL und kein FAILED, FAILED – mindestens ein FAILED oder globale Simulationsbasis unbrauchbar.

E) FAILED-Output: Auch bei simulation_status = FAILED muss ein minimal auditierbarer Output erzeugt werden: run_id, simulation_timestamp, station_8_validation_ref nullable, input_order_count nullable, simulation_status = FAILED, reason, execution_report.

FAILED darf Station 8 nicht invalidieren, keinen Pipeline-Stopp erzeugen und keinen Systemstatus setzen.

F) Audit-Referenzen: Große Detailobjekte werden nicht vollständig ins Audit-Summary-Event geschrieben. Audit-Summary enthält station_8_validation_ref, simulation_timestamp, simulation_status, input_order_count, full_fill_count, partial_fill_count, no_fill_count, failed_fill_count, total_execution_cost, execution_report_ref.

execution_report_ref und andere Detailreferenzen müssen stabil und später auflösbar sein, z. B. über run_id + Suffix oder UUID.

Persistenz: Decimal-Werte dürfen zur Laufzeit numerisch berechnet werden, werden aber persistiert als String. Timestamps werden als UTC-ISO-String persistiert. Große Listen bleiben im Detailreport, nicht im Audit-Summary.
## D) Simulationsannahmen

Der Simulator lädt keine Live-Daten nach. Alle Berechnungen erfolgen sofortig zum simulation_timestamp auf Basis des market_data_snapshot.

Keine mehrperiodige Simulation. Keine Order-Warteschlange. Keine Intraday-Pfadsimulation. Keine Markt-Mikrostruktur.

Orders werden seriell in der von Station 8 vorgegebenen Reihenfolge simuliert. Nach jeder Order werden Cash, Positionen und Kosten hypothetisch aktualisiert.

## E) Fill-Preis-, LIMIT- und Slippage-Regeln

Execution-Fill-Preis:

- BUY: primär ask_price
- SELL: primär bid_price

Bei fehlendem Bid/Ask, aber plausibler mid_price + spread:

bid_price = mid_price - spread / 2

ask_price = mid_price + spread / 2

Fehlt eine plausible direkte oder rekonstruierte Bid/Ask-Basis:

simulation_status = FAILED

LIMIT-Regeln:

- LIMIT BUY: Fill nur, wenn simulated_fill_price <= limit_price
- LIMIT SELL: Fill nur, wenn simulated_fill_price >= limit_price
- Limit nicht erreicht: fill_status = NO_FILL

Slippage: deterministisch aus slippage_model.

Standard:

slippage_per_unit = reference_price * slippage_bps / 10000

Slippage verschlechtert den Preis immer gegen den Trader: BUY teurer, SELL günstiger.

Keine Preisverbesserung durch Slippage.

## F) Cash, Gebühren, Portfolio und Liquidität

Cash wird seriell aktualisiert:

- BUY: Cash sinkt um Fill-Wert + Gebühren
- SELL: Cash steigt um Fill-Wert abzüglich Gebühren

BUY darf keinen negativen Cash erzeugen, außer eine explizite, vorgelagerte Margin-Autorisierung liegt vor.

Wenn BUY den Cash negativ machen würde:

- teilweise finanzierbar: fill_status = PARTIAL
- gar nicht finanzierbar: fill_status = NO_FILL
- gesamt: simulation_status = PARTIAL, sofern keine FAILED-Ursache vorliegt

Gebühren stammen aus fee_structure.

Pflicht-Kostenfelder:

- total_commission
- total_slippage_cost
- total_execution_cost = total_commission + total_slippage_cost

Portfolio-Bewertung nutzt eine eigene Preislogik, getrennt von Execution-Fill-Preisen:

1. mid_price
2. last_price
3. fill_price

Fehlende Bid/Ask-Daten führen bei der Portfolio-Bewertung nicht automatisch zu FAILED, solange ein plausibler Bewertungspreis vorhanden ist.

Pflicht-Konsistenzregel:

post_execution_portfolio.total_portfolio_value = cash_after + Summe(position_market_values)

Wenn diese Gleichung nicht erfüllt werden kann, ist das Simulationsergebnis nicht belastbar.

Dann gilt:

simulation_status = FAILED

Liquidität wird nur zur Fill-Simulation genutzt.

Station 8 prüft harte Liquiditätsgrenzen.

- ausreichende Liquidität: FULL möglich
- eingeschränkte Liquidität: PARTIAL möglich
- fehlende oder unbrauchbare Liquiditätsdaten für Fill-Modell: FAILED

## G) Short-Positionen

Short-Positionen sind nicht pauschal verboten. Sie können bei bestätigtem Downtrend oder als Hedge ein valides Instrument sein.

Der Simulator darf aber keine unbeabsichtigten Shorts erzeugen.

Shorts dürfen nur simuliert werden, wenn Station 8 die betroffene SELL-Order explizit autorisiert hat.

Pflicht im Input:

- allow_short: true
- short_authorization_ref

Optional:

- max_authorized_short_quantity

SELL-Orders werden kumulativ gegen den aktuellen simulierten Positionsstand geprüft.

Wenn SELL quantity > aktuelle Long-Menge:

A) Short autorisiert + Short-/Margin-Daten plausibel: hypothetische Short-Position darf simuliert werden.

B) Keine Short-Autorisierung: Verkauf nur bis zur vorhandenen Long-Menge; fill_status = PARTIAL oder NO_FILL.

C) Positions-, Short- oder Margin-Daten widersprüchlich: fill_status = FAILED und simulation_status = FAILED.

Der Simulator darf keine Margin-Anforderungen, Borrowing-Kosten, Leihverfügbarkeit, Short-Finanzierungskosten oder Hebelannahmen selbst erfinden.

Solche Angaben müssen vorgelagert validiert oder explizit im Simulationsinput vorhanden sein.

## H) Statuslogik

A) fill_status pro Order:

- FULL: vollständig hypothetisch ausgeführt
- PARTIAL: teilweise hypothetisch ausgeführt
- NO_FILL: technisch korrekt simuliert, aber nicht ausgeführt
- FAILED: technisch oder datenlogisch nicht zuverlässig simulierbar

B) simulation_status gesamt:

- SUCCESS: alle Orders FULL
- PARTIAL: mindestens eine Order PARTIAL oder NO_FILL, keine Order FAILED
- FAILED: mindestens eine Order FAILED oder globale Simulationsbasis unbrauchbar

Wirkung:

- NO_FILL ist kein technischer Fehler.
- PARTIAL ist keine Teilfreigabe.
- FAILED invalidiert Station 8 nicht rückwirkend.
- FAILED stoppt keine Pipeline.
- FAILED löst kein SAFE_HOLD, CASH_ONLY, FORCE_CASH_ONLY oder NO_NEW_ACTIONS aus.

## I) Audit-Log-Anbindung

Der Execution Simulator schreibt ein Summary-Audit-Event pro Simulationslauf.

Keine Einzel-Order-Audit-Events in Core v1.0.

Event-Typen:

- EXECUTION_SIMULATION_SUCCESS
- EXECUTION_SIMULATION_PARTIAL
- EXECUTION_SIMULATION_FAILED

Audit-Mapping:

- validator_status = PASS
- system_status = NORMAL_CONTINUE
- pipeline_action = CONTINUE
- event_scope = ORDER_LIST
- simulation_status separat führen

Pflicht-Summary-Felder:

- station_8_validation_ref
- simulation_timestamp
- simulation_status
- input_order_count
- full_fill_count
- partial_fill_count
- no_fill_count
- failed_fill_count
- total_execution_cost
- execution_report_ref

Optional:

- total_commission
- total_slippage_cost
- post_execution_portfolio_ref
- reason

Nicht vollständig ins Summary-Audit-Event:

- vollständige simulated_fills
- vollständiges post_execution_portfolio
- vollständiger Execution Report
- große Positionslisten
- umfangreiche Orderdetails

Stattdessen: Summary + Referenzen/Hashes auf Detailreports.

Jedes Simulator-Audit-Event läuft durch add_audit_hash() und muss mit verify_audit_event() prüfbar sein.

## J) Golden Cases

Die Golden Cases für Execution Simulator Core v1.0 liegen unter:

tests/golden_cases/execution_simulator_core_v1_cases.json
A) TC_EXEC_001 — Erfolgreiche vollständige Simulation: vollständige validierte Orderliste, ausreichende Liquidität und Cash, gültige Modelle. Erwartung: alle fill_status = FULL, simulation_status = SUCCESS, vollständiger Report, post_execution_portfolio, Audit-Event EXECUTION_SIMULATION_SUCCESS, validator_status = PASS.

B) TC_EXEC_002 — LIMIT-Preis nicht erreicht: LIMIT-Order, simulierter Preis verfehlt Limit. Erwartung: fill_status = NO_FILL, simulation_status = PARTIAL, keine Order-Änderung, Audit-Event EXECUTION_SIMULATION_PARTIAL.

C) TC_EXEC_003 — Begrenzte Liquidität: Order innerhalb Station-8-Grenze, Liquiditätsmodell erlaubt nur Teilfüllung. Erwartung: fill_status = PARTIAL, simulation_status = PARTIAL, Portfolio nur auf Basis gefüllter Menge.

D) TC_EXEC_004 — BUY mit unzureichendem Cash: BUY würde Cash negativ machen, keine Margin-Autorisierung. Erwartung: fill_status = PARTIAL oder NO_FILL, simulation_status = PARTIAL, kein negativer Cash.

E) TC_EXEC_005 — SELL-Überhang ohne Short-Autorisierung: SELL > Long-Menge, keine Short-Autorisierung. Erwartung: fill_status = PARTIAL oder NO_FILL, simulation_status = PARTIAL, keine unbeabsichtigte Short-Position.

F) TC_EXEC_006 — Autorisierte Short-Simulation: SELL > Long-Menge, allow_short: true, short_authorization_ref, plausible Short-/Margin-Annahmen. Erwartung: hypothetische Short-Position erlaubt, keine erfundenen Margin-/Borrowing-Werte, simulation_status = SUCCESS oder PARTIAL.

G) TC_EXEC_007 — Technischer Simulationsfehler / fehlende Pflichtreferenz: fehlendes/ungültiges slippage_model, fee_structure, Marktdaten oder fehlende station_8_validation_ref. Erwartung: simulation_status = FAILED, Audit-Event EXECUTION_SIMULATION_FAILED, keine Pipeline-Wirkung, Station 8 bleibt gültig.

H) TC_EXEC_008 — Audit-Hash & Portfolio-Konsistenz: gültiges Simulationsergebnis. Erwartung: audit_hash korrekt, verify_audit_event() erfolgreich, validator_status = PASS, simulation_status separat vorhanden, Portfolio-Konsistenzregel erfüllt.

## K) Order-/Fill-Rückverfolgbarkeit

A) station_8_validation_ref: Referenziert die von Station 8 freigegebene Orderliste.

B) validated_order_list[].order_ref: Pflichtfeld je validierter Order. order_ref ist innerhalb station_8_validation_ref eindeutig.

C) simulated_fills[].station_8_validation_ref: Pflichtfeld je simuliertem Fill und identisch mit der zugehörigen Station-8-Validierung.

D) simulated_fills[].source_order_ref: Pflichtfeld je simuliertem Fill. source_order_ref verweist auf validated_order_list[].order_ref innerhalb derselben station_8_validation_ref.

E) Referenzkette: station_8_validation_ref → validated_order_list[].order_ref → simulated_fills[].station_8_validation_ref + simulated_fills[].source_order_ref.

F) Eindeutigkeitsregel: station_8_validation_ref + source_order_ref verweist eindeutig auf die validierte Ursprungsorder aus Station 8.

G) Zweck: Jeder simulierte Fill muss eindeutig auf die von Station 8 validierte Ursprungsorder zurückführbar sein.

## L) Codex-Hinweis

Codex implementiert später Execution Simulator, Fill-Simulation, Cash-/Positionsfortschreibung, Kostenberechnung, Portfolio-Projektion, Audit-Event-Erzeugung und Golden Cases exakt nach dieser Spezifikation.

Codex darf nicht ergänzen:

- Live-Broker-Interaktion
- Order-Reparatur
- Order-Neuerzeugung
- Portfolio-Optimierung
- Pipeline-Systemstatus-Wechsel
- implizite Margin-/Borrowing-Annahmen
- nicht validierte Short-Erzeugung
