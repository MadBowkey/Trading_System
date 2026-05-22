# Modul 01 – Datenebene

## 1) Zweck und Verantwortung des Moduls
Die Datenebene stellt die technische und fachliche Integritätsbasis für die gesamte Pipeline bereit.

Verantwortung im Systemkontext:
- Bereitstellung konsistenter, zeitlich valider und ausreichend vollständiger Eingabedaten für nachgelagerte Stationen.
- Verhinderung von Pipeline-Fortsetzung bei klarer Dateninvalidität (z. B. Stale Data, fehlende Pflichtdaten), da sonst Folgeentscheidungen logisch entwertet werden.
- Sicherstellung, dass Datenzustand und Datenqualität über Audit-/State-Artefakte nachvollziehbar bleiben.

Evidenz:
- Station 1 ist explizit für Integritätsprüfung vor LLM-Aufruf definiert (Datenabriss, fehlende Preise, Universe-/Portfolio-Integrität). `specs/07_station_1_pre_llm_validator.md`
- Architektur definiert Data-Integrity-Gates (Vollständigkeit, Stale Data, falscher Handelstag, Feed-Probleme). `specs/01_architecture_overview_v1_6_1.md`
- Guardrails verlangen Blockierung bei ungültigen Daten (`on_invalid_data`). `specs/04_guardrails_v1.md`

## 2) Eingaben / Datenquellen
Fest im Repo erkennbare Daten-/Konfigurationsquellen (keine Annahmen über externe Provider):
- `config/universe.example.yaml` (Universum-Definition als Beispielkonfiguration).
- `config/indicator_registry.yaml` (Indikator-Registry-Struktur, aktuell leeres `indicators`-Array).
- `config/regime_matrix.yaml` (Regime-Matrix-Struktur, aktuell leeres `regimes`-Array).
- `config/risk_guardrails.yaml` (Guardrail-Konfiguration; im Index als zentrale Konfig referenziert).
- `config/rule_registry.yaml` (Regel-IDs/Trigger inkl. Data-Integrity-bezogener Regeln wie `VAL_ENG_003`, `VAL_PTR_003`, `VAL_ORD_001`).
- `tests/golden_cases/*.json` als verifizierbare Input-/Verhaltensreferenzen für Stationen/Core-Komponenten.

Wichtig: Es gibt im aktuellen Stand keine implementierte Runtime-Datenpipeline im Repo (Codebasis fehlt; Fokus liegt auf Specs/Configs/Golden-Cases). Diese Lücke ist keine Annahme, sondern ein Befund aus der Repo-Struktur.

## 3) Ausgaben / Verträge / Abhängigkeiten
Vertragliche Wirkung der Datenebene auf Folge-Module:
- Upstream-Gate für Station 1 → Station 2/3: bei Integritätsfehlern kein regulärer Fortlauf.
- Datenqualitätszustände werden in Core-Artefakten mitgeführt (z. B. `data_quality_status` im Portfolio State Ledger).
- Nachgelagerte Module sind direkt datenabhängig:
  - Station 3 (Schema/Technik-Validität des LLM-Objekts),
  - Station 5/6/7 (Risiko- und Portfolio-Entscheidungen),
  - Station 8 + Execution Simulator (Order-/Snapshot-Konsistenz),
  - Audit Log Core (Nachvollziehbarkeit bei TECHNICAL_ERROR / BLOCKED).

Explizite Abhängigkeit:
- Wenn Datenebene unklar bleibt, sind Ergebnisse in Risiko, Portfolio und Ausführung nur eingeschränkt belastbar.

## 4) Risiken / Konflikte / Inkonsistenzen
### Konflikt M01-C01 — Klassifikation: HIGH
- Typ: Governance-/Spezifikationslücke.
- Befund: Projekt enthält umfangreiche Spezifikationen und Golden Cases, aber keine produktive Implementierung der Datenpipeline.
- Wirkung: Fachliche Prüfregeln sind definiert, aber technisch nicht ausführbar/verifizierbar im aktuellen Repo-Stand.
- Begründung HIGH (nicht CRITICAL): Struktur- und Governance-Arbeit ist möglich; echter Laufzeitbetrieb jedoch nicht nachweisbar.

### Konflikt M01-C02 — Klassifikation: MEDIUM
- Typ: Konfigurationsvollständigkeit.
- Befund: `config/indicator_registry.yaml` und `config/regime_matrix.yaml` enthalten leere Arrays (`indicators: []`, `regimes: []`).
- Wirkung: Unklar, ob bewusstes Placeholder-Stadium oder fachlich final; Risiko späterer Inkonsistenzen in Stationen, die diese Inputs erwarten.
- Begründung MEDIUM: Kein direkter Laufzeitnachweis für Ausfall hier im Repo, aber klarer Integritäts-/Betriebsrisikoindikator.

### Konflikt M01-C03 — Klassifikation: LOW
- Typ: Nachvollziehbarkeit/Quellenklarheit.
- Befund: Universe-Datei ist als `universe.example.yaml` benannt (Beispielcharakter), ohne im Audit eindeutig definiertes produktives Pendant.
- Wirkung: Risiko von Missverständnissen beim Übergang von Spezifikation zu produktiver Konfiguration.
- Begründung LOW: Lösbar durch klare Konfigurationskonvention.

## 5) Architektur- und Sicherheitsbewertung
Architektur-Bewertung:
- Positiv: Klare Spezifikationstiefe (Pipeline-Regeln, Guardrails, Validator-Stationen, Core-Contracts).
- Positiv: Traceability-Konzept über mehrere Stufen ist dokumentiert (Order-/Audit-Referenzen, Ledger-/Audit-Kerne).
- Kritisch für Reifegrad: Repo ist derzeit primär Spezifikations-/Testfall-getrieben, ohne nachweisbare Runtime-Implementierung; dadurch keine End-to-End-Härtung möglich.

Sicherheits-/Robustheitsbewertung (datenbezogen):
- Positiv: Guardrail-Prinzip blockiert invalid data und verhindert riskante Folgeaktionen.
- Positiv: TECHNICAL_ERROR/BLOCKED-Pfade sind in mehreren Stationen beschrieben.
- Restrisiko: Ohne operative Pipeline-Implementierung sind Sicherheitsannahmen nur dokumentiert, nicht empirisch verifiziert.

## 6) Empfehlung / Maßnahmen / offene Punkte
Empfehlungen (priorisiert):
1. **HIGH**: Minimal ausführbaren Datenebenen-Implementierungs-Slice definieren (Ingest → Quality Checks → Gate-Entscheid), damit Modul-1-Aussagen testbar werden.
2. **MEDIUM**: `indicator_registry` und `regime_matrix` fachlich befüllen oder explizit als bewusst leer (mit Regeln/Fallback) deklarieren.
3. **LOW**: Konfigurationskonvention dokumentieren (`*.example.yaml` vs. produktive `*.yaml`) und Referenzpfad festlegen.

Offene Punkte:
- Welche konkrete Datei gilt als produktive Universe-Konfiguration?
- Welche Pflichtfelder/Minimalinhalte sind für `regime_matrix` und `indicator_registry` vor Pipeline-Start erforderlich?
- Soll Station 1 bereits bei leeren, aber formal gültigen Registern blockieren oder nur warnen?
