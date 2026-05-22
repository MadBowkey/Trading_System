# Modul 01 – Datenebene

## 1) Zweck und Verantwortung des Moduls
Die Datenebene stellt die technische und fachliche Integritätsbasis für die gesamte Pipeline bereit.

Verantwortung im Systemkontext:
- Bereitstellung konsistenter, zeitlich valider und ausreichend vollständiger Eingabedaten für nachgelagerte Stationen.
- Verhinderung von Pipeline-Fortsetzung bei klarer Dateninvalidität.
- Sicherstellung nachvollziehbarer Datenqualitätszustände.

## 2) Eingaben / Datenquellen
Fest im Repo erkennbare Daten-/Konfigurationsquellen:
- `config/universe.example.yaml`
- `config/indicator_registry.yaml`
- `config/regime_matrix.yaml`
- `config/risk_guardrails.yaml`
- `config/rule_registry.yaml`
- `tests/golden_cases/*.json`

## 3) Ausgaben / Verträge / Abhängigkeiten
- Upstream-Gate für Station 1 → Station 2/3.
- Datenqualitätszustände werden in Core-Artefakten mitgeführt.
- Direkte Abhängigkeiten:
  - Modul 02 (Feature/Signal)
  - Modul 03 (Strategie/Entscheidung)
  - Modul 05 (Risikomanagement)
  - Modul 08 (Backtest/Simulation)

## 4) Risiken / Konflikte / Inkonsistenzen

### Konflikt M01-C01 — Klassifikation: HIGH
- Typ: Governance-/Spezifikationslücke.
- Befund: Projekt enthält umfangreiche Spezifikationen und Golden Cases, aber keine produktive Implementierung der Datenpipeline.
- Wirkung: Fachliche Prüfregeln sind definiert, aber technisch nicht ausführbar/verifizierbar im aktuellen Repo-Stand.

### Konflikt M01-C02 — Klassifikation: MEDIUM
- Typ: Konfigurationsvollständigkeit.
- Befund: `indicator_registry.yaml` und `regime_matrix.yaml` enthalten leere Arrays.

### Konflikt M01-C03 — Klassifikation: LOW
- Typ: Nachvollziehbarkeit/Quellenklarheit.
- Befund: Universe-Datei nur als `universe.example.yaml` sichtbar.

## 5) Architektur- und Sicherheitsbewertung
- Positiv: Klare Spezifikationstiefe und Traceability-Konzept.
- Kritisch: Repo derzeit primär spezifikations-/testfallgetrieben ohne nachweisbare Runtime-Implementierung.
- Restrisiko: Sicherheitsannahmen aktuell dokumentiert, aber nicht empirisch verifiziert.

## 6) Empfehlung / Maßnahmen / offene Punkte
1. HIGH: Minimal ausführbaren Datenebenen-Slice definieren.
2. MEDIUM: `indicator_registry` und `regime_matrix` fachlich befüllen oder explizit als bewusst leer deklarieren.
3. LOW: Konfigurationskonvention dokumentieren (`*.example.yaml` vs produktive `*.yaml`).

Offene Punkte:
- Welche Datei gilt als produktive Universe-Konfiguration?
- Welche Pflichtfelder gelten für `regime_matrix` und `indicator_registry`?
- Soll Station 1 bei leeren, aber formal gültigen Registern blockieren oder warnen?