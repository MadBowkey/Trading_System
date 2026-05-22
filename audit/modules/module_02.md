# Modul 02 – LLM Meta-Manager (Feature/Signal-Interpretation)

## 1) Zweck
Modul 02 überführt den von Modul 01 freigegebenen technischen/fachlichen Kontext in eine strukturierte strategische Absicht (LLMMetaManagerOutput).

Rolle im Gesamtsystem:
- Interpretation (nicht Berechnung) von vorberechneten Markt-, Trend-, Risiko- und Portfoliodaten.
- Ausgabe eines strukturierten Objekts als Input für Modul 03.
- Keine Erzeugung finaler Orders und keine finale Handelsentscheidung.

## 2) Schnittstellen (Input/Output/Annahmen + referenzierte Module)
Input (vorgelagert):
- Freigegebener Kontext aus Modul 01 (u. a. Marktdatenstatus, Trend/Regime, Risikozustände, Universe/Portfolio-Kontext).
- Prompt-/Regelkontext (System-Prompt, deduktive Regeln, Few-Shot-Beispiele, Structured-Output-Schema, API-Konfiguration).

Output (nachgelagert):
- Structured Output im Zielformat `LLMMetaManagerOutput` für Modul 03.

Verhaltensannahmen laut Spezifikation:
- Bei API-/Timeout-/Leerantwortfehlern: SAFE_HOLD / NO_NEW_ACTIONS und Pipeline-Stopp.
- Modul 02 erzeugt strategische Absicht, aber keine technische Schema-Freigabe (diese liegt bei Modul 03).

Referenzierte Module:
- Upstream: Modul 01 (Datenebene/Pre-Validation-Gate).
- Downstream: Modul 03 (Technical Schema Validator), indirekt Modul 04+.

## 3) Gefundene Konflikte (CRITICAL/HIGH/MEDIUM/LOW)

### Konflikt M02-C01 — Klassifikation: HIGH
- Problemcluster: Umsetzungsfähigkeit / Betriebsreife.
- Befund: Für Modul 02 liegt eine fachliche Spezifikation vor, im aktuellen Repo-Stand jedoch keine nachweisbare produktive Laufzeitimplementierung (LLM-Client/Structured-Output-Aufruf/Fehlerpfad).
- Implikation: Der definierte Station-2-Output kann operativ nicht reproduzierbar erzeugt werden; die End-to-End-Kette bleibt auf Dokument-/Testartefakte beschränkt.
- Bewertung: Dringend, da Modul 02 auf dem kritischen Pfad zwischen Datenfreigabe und Validierung liegt; Wichtigkeit nach Bewertungsregel als HIGH.
- Aufwand: Mittel bis hoch (technische Infrastruktur, robustes Fehlerhandling, Auditierbarkeit).

### Konflikt M02-C02 — Klassifikation: MEDIUM
- Problemcluster: Schnittstellenklarheit / Governance.
- Befund: Die Spezifikation trennt fachlich zwischen Modul 02 (Intent-Erzeugung) und Modul 03 (Schema-Validierung), aber es fehlt im Repo ein verbindlicher, ausführbarer Übergabevertrag (z. B. versionierter Contract-Artefakt im Laufzeitpfad).
- Implikation: Erhöhtes Risiko für uneinheitliche Interpretation des Hand-offs (rohes JSON vs. bereits geparstes Objekt) und damit inkonsistente Fehlerbehandlung zwischen Modulen.
- Bewertung: Wichtig für Stabilität und Nachvollziehbarkeit, aber nicht unmittelbar blocker-kritisch ohne Implementierungsstand; daher MEDIUM.
- Aufwand: Mittel (Contract-Fixierung, Übergabe- und Fehlerpfaddefinition).

### Konflikt M02-C03 — Klassifikation: LOW
- Problemcluster: Nachweisbarkeit / Traceability.
- Befund: Geforderte Fehlerwirkungen (SAFE_HOLD / NO_NEW_ACTIONS bei API-/Timeout-Fehlern) sind spezifiziert, aber ohne produktive Artefakte nicht empirisch nachweisbar.
- Implikation: Auditfähigkeit für Ausnahmefälle bleibt eingeschränkt; Risiko liegt primär in fehlender Verifikation statt in widersprüchlicher Fachlogik.
- Bewertung: Beobachtungsrelevant, aktuell nachrangig gegenüber Umsetzungs- und Schnittstellenlücken; daher LOW.
- Aufwand: Niedrig bis mittel (Nachweis-/Test- und Loggingpfade).

## 4) Begründung der Einstufung
- Einstufung nach vorgegebenem Schema:
  - HIGH = dringend, aber nicht wichtig.
  - MEDIUM = wichtig, aber nicht dringend.
  - LOW = Rest/Beobachtung.
- M02-C01 ist dringend, weil Modul 02 ein Kernübergang der Pipeline ist und ohne Implementierung der Kettenbetrieb nicht belastbar ist.
- M02-C02 ist primär wichtig (Governance/Robustheit), aber zeitlich nachgeordnet gegenüber der Basis-Umsetzbarkeit.
- M02-C03 ist nachrangig, da es auf Nachweislücken statt auf direkte fachliche Widersprüche zielt.

## 5) Abhängigkeitseffekt (betroffene Module)
- Direkt betroffen:
  - Modul 03 (Schema-Validator) durch unklare/faktisch nicht laufende Übergabe.
- Indirekt betroffen:
  - Modul 04–10, da alle Folgeprüfungen von einem stabilen, strukturierten Station-2-Output abhängen.
- Querbezug zu bestehendem Cluster aus Modul 01:
  - M01-C01 (fehlende produktive Pipelinebasis) verstärkt M02-C01 unmittelbar.

## 6) Vorläufige Maßnahme (jetzt klären / in Matrix entscheiden)
- M02-C01: in Matrix zu entscheiden.
- M02-C02: in Matrix zu entscheiden.
- M02-C03: in Matrix zu entscheiden.
