# Audit-Log-Struktur Core v1.0

Status: FINAL
Version: v1.0
Architecture: v1.6.1
Last updated: 2026-05-16
Owner: Trading System Project

## Kurzbeschreibung

Die Audit-Log-Struktur Core v1.0 ist das zentrale, unveränderliche Protokoll aller Entscheidungen und Aktionen innerhalb der Validierungs-Pipeline Station 1 bis Station 8.

Sie ist die Single Source of Truth für jede Regelprüfung, Korrektur, Ablehnung, Freigabe, Normalisierung und jeden Pipeline-Stopp.

Jedes Audit-Event wird als unveränderlicher Datensatz gespeichert:

- primär als Parquet
- optional als JSON-Export für Prüfung, Debugging und Reports

## Ziele

1. Vollständige Traceability

Jede technische, fachliche, marktbezogene, portfolio- oder orderbezogene Entscheidung ist nachvollziehbar.

2. Sicherheit und Unveränderlichkeit

Keine stillen Änderungen. Jede Mutation, Normalisierung, Downgrade, Rejection oder Blockierung wird protokolliert.

3. Konsistenz

Einheitliche Felder und Statuswerte über Station 1 bis Station 8.

4. Testbarkeit

Golden Cases können exakt gegen Audit-Events validiert werden.

5. Compliance und Self-Analysis

Grundlage für Reports, Backtesting, Fehleranalyse und spätere Self-Analysis.

6. Klare Trennung

Core v1.0 umfasst nur Station 1 bis Station 8.

ML_Optimizer-Audits kommen separat in v1.2.

Keine ML-Felder in Core v1.0.

## Pflicht-Standardfelder

Diese Felder sind in jedem Core-v1-Audit-Event vorhanden.

| Feld | Typ | Nullable | Beschreibung | Beispiel |
|---|---|---:|---|---|
| audit_schema_version | string | Nein | Version des Audit-Log-Schemas | audit_log_core_v1.0 |
| run_id | string | Nein | Eindeutige Run-ID der Tagesanalyse | run_20260516_013045_078 |
| timestamp | datetime UTC als string | Nein | Zeitpunkt des Events | 2026-05-16T01:30:45.123Z |
| station | string | Nein | Name der auslösenden Station | Station_3_TechnicalSchemaValidator |
| rule_id | string / null | Ja | Ausgelöste Regel-ID; null bei reinem Erfolgs-Event | VAL_TSV_002 |
| validator_status | string | Nein | Status der Regel- oder Stationsprüfung | BLOCKED |
| system_status | string | Nein | Gesamtsystemstatus nach dem Event | SAFE_HOLD |
| pipeline_action | string | Nein | Nächste Pipeline-Aktion | STOP |
| asset_id | string / null | Ja | Betroffenes Asset; null bei Portfolio-, System- oder Orderlisten-Event | QQQ |
| reason | string | Nein | Kurze lesbare Begründung, maximal 300 Zeichen | Missing required field strategy_regime |
| event_type | string | Nein | Typ des Audit-Events | RULE_REJECTED |
| event_scope | string | Nein | Scope des Audit-Events | ORDER_LIST |
| audit_hash | string | Nein | SHA-256 Integritäts-Hash des Events | sha256:8f3a9c... |

## Optionale Zusatzfelder

Diese Felder werden nur verwendet, wenn sie fachlich relevant sind.

| Feld | Typ | Verwendung |
|---|---|---|
| original_value | string / null | Bei DOWNGRADED, Normalisierung oder technischer Korrektur |
| enforced_value | string / null | Bei DOWNGRADED, Normalisierung oder technischer Korrektur |
| num_orders_proposed | int / null | Station 8 |
| num_orders_rejected | int / null | Station 8 |
| order_proposal_status | string / null | Station 8: APPROVED / REJECTED |
| rejected_order_details | string / null | Station 8: JSON-Array als String |
| station_8_validation_ref | string / null | Execution Simulator: Referenz zur Station-8-Freigabe |
| simulation_status | string / null | Execution Simulator: SUCCESS / PARTIAL / FAILED |
| input_order_count | int / null | Execution Simulator: Anzahl simulierter Orders |
| full_fill_count | int / null | Execution Simulator: vollständig gefüllte Orders |
| partial_fill_count | int / null | Execution Simulator: teilweise gefüllte Orders |
| no_fill_count | int / null | Execution Simulator: nicht gefüllte Orders |
| failed_fill_count | int / null | Execution Simulator: nicht simulierbare Orders |
| total_execution_cost | string / null | Execution Simulator: Gesamtkosten als Decimal-String |
| total_commission | string / null | Execution Simulator: Gebühren als Decimal-String |
| total_slippage_cost | string / null | Execution Simulator: Slippage-Kosten als Decimal-String |
| execution_report_ref | string / null | Execution Simulator: Referenz auf vollständigen Execution Report |
| post_execution_portfolio_ref | string / null | Execution Simulator: Referenz auf simulierten Portfoliozustand |

## Grundregeln

- Alle Werte müssen JSON-serialisierbar sein.
- Decimal-Werte werden als Strings gespeichert.
- datetime-Werte werden als UTC-ISO-Strings gespeichert.
- audit_hash wird nach Befüllung aller anderen Felder berechnet.
- audit_hash wird über das vollständige Event ohne audit_hash berechnet.
- audit_schema_version wird mitgehasht.
- Keine ML-Felder in Core v1.0.

## Schema-Versionierung

Core v1.0 verwendet das Pflichtfeld audit_schema_version.

Wert für Core v1.0:

audit_log_core_v1.0

## Versionsregeln

- Major-Version bei inkompatiblen Änderungen.
- Minor-Version bei neuen optionalen Feldern oder abwärtskompatiblen Erweiterungen.
- Alte Schemata bleiben lesbar.
- Bei Schema-Wechsel wird ein neuer Parquet-Pfad verwendet.
- Core v1.0 verwendet den Pfad audit_logs/core_v1_0.

## Erlaubte Statuswerte

### validator_status

Core v1.0 erlaubt stationenübergreifend folgende Statuswerte:

- PASS
- APPROVED
- BLOCKED
- DOWNGRADED
- REJECTED
- TECHNICAL_ERROR
- PORTFOLIO_PROPOSAL_CREATED
- PORTFOLIO_CONSTRUCTION_FAILED
- POST_TRADE_RISK_REJECTED

### system_status

Core v1.0 erlaubt folgende Systemstatuswerte:

- NORMAL_CONTINUE
- NO_NEW_ACTIONS
- SAFE_HOLD
- CASH_ONLY
- FORCE_CASH_ONLY
- BLOCK_RISK_INCREASE

### pipeline_action

Core v1.0 erlaubt folgende Pipeline-Aktionen:

- CONTINUE
- STOP
- STOP_BEFORE_STATION_7
- STOP_BEFORE_STATION_8
- STOP_BEFORE_EXECUTION_SIMULATION

## Statusregeln

- Technische Integritätsfehler führen zu SAFE_HOLD oder NO_NEW_ACTIONS und stoppen die Pipeline.
- Fachliche Risiko- oder Ausführbarkeitsablehnungen führen zu NO_NEW_ACTIONS und stoppen vor der jeweils nächsten riskanten Stufe.
- DOWNGRADED ist nur erlaubt, wenn die Änderung regelbasiert, risikosenkend oder technisch harmlos ist.
- FORCE_CASH_ONLY darf nur durch echte Markt- oder Risiko-Guardrails ausgelöst werden, nicht durch Station 8.

## Event-Typen

Core v1.0 unterscheidet folgende Audit-Event-Typen:

| event_type | Bedeutung |
|---|---|
| RULE_PASS | Regelprüfung ohne Verstoß |
| RULE_BLOCKED | Technischer oder struktureller Fehler blockiert den Lauf |
| RULE_DOWNGRADED | Regelbasierte risikosenkende oder technisch harmlose Anpassung |
| RULE_REJECTED | Fachliche Ablehnung ohne technische Systemstörung |
| TECHNICAL_ERROR | Technischer Fehler, Datenfehler oder invalider Output |
| PORTFOLIO_PROPOSAL_CREATED | Station 6 hat ein valides Zielportfolio erzeugt |
| PORTFOLIO_CONSTRUCTION_FAILED | Station 6 konnte keine zulässige Zielstruktur berechnen |
| PORTFOLIO_VALIDATED | Station 7 hat das Zielportfolio freigegeben |
| ORDER_LIST_APPROVED | Station 8 hat die Orderliste freigegeben |

## Event-Scope

Jedes Audit-Event muss eindeutig einem Scope zugeordnet sein.

| event_scope | Bedeutung |
|---|---|
| SYSTEM | Gesamtpipeline oder Systemzustand |
| PORTFOLIO | Gesamtportfolio / Zielportfolio |
| ASSET | einzelnes Asset |
| ORDER_LIST | gesamte proposed_order_list |
| ORDER | einzelne betroffene Order innerhalb rejected_order_details |

## Event-Grundregel

Core v1.0 erzeugt keine stillen Entscheidungen.

Wenn eine Regel den Lauf verändert, blockiert, downgraded, rejected oder freigibt, muss mindestens ein Audit-Event existieren.

Station 8 erzeugt ein Summary-Event pro Run und keine separaten Einzel-Order-Events.

Einzelne betroffene Orders stehen nur in rejected_order_details.

## Hash- und Unveränderlichkeitsregeln

Jedes Audit-Event erhält einen SHA-256 Einzel-Event-Integritäts-Hash.

Der Hash dient der Erkennung nachträglicher Änderungen und der eindeutigen Referenzierbarkeit eines Events.

Der Hash ist keine kryptografische Signatur.

Core v1.0 verwendet:

- keine Hash-Chain
- kein previous_audit_hash
- keinen Merkle-Baum
- kein HMAC

Merkle-Baum, Hash-Chain oder HMAC werden auf v1.2 verschoben.

## Hash-Berechnung

Der audit_hash wird wie folgt berechnet:

1. Audit-Event vollständig befüllen.
2. audit_hash entfernen oder leer lassen.
3. Event deterministisch serialisieren.
4. SHA-256 über diese serialisierte Struktur berechnen.
5. audit_hash als Feld einfügen.

## Deterministische Serialisierung

Für die Hash-Berechnung gilt:

- JSON-Keys werden stabil sortiert.
- Decimal-Werte werden als Strings gespeichert.
- datetime-Werte werden als UTC-ISO-Strings gespeichert.
- Keine NaN- oder Infinity-Werte.
- Keine Python-spezifischen Objekte.
- Null-Werte bleiben explizit enthalten, wenn das Feld zum Standardfeldsatz gehört.
- audit_hash wird nie in seine eigene Berechnung einbezogen.
- audit_schema_version wird mitgehasht.

## Unveränderlichkeit

Nach Speicherung darf ein Audit-Event nicht überschrieben werden.

Korrekturen erfolgen nur durch ein neues Audit-Event mit Referenz auf das vorherige Event.

Direktes Editieren bestehender Audit-Events ist verboten.

## Speicherformate

Primäres Speicherformat:

- Parquet

Optionales Exportformat:

- JSON

JSON-Export darf niemals als neue Wahrheit gegen Parquet verwendet werden.

Parquet bleibt die primäre Audit-Quelle.

## Parquet-Kompatibilität

Die Audit-Log-Struktur Core v1.0 ist vollständig Parquet-kompatibel.

## Parquet-Speicherregeln

| Feldtyp | Speicherung in Core v1.0 |
|---|---|
| string | Parquet string |
| int | Parquet int64 |
| bool | Parquet bool |
| nullable string | Parquet string mit null |
| timestamp | UTC-ISO-String |
| Decimal-Werte | string |
| rejected_order_details | JSON-String |
| audit_hash | string |

## Entscheidungen

- timestamp wird in Core v1.0 als UTC-ISO-String gespeichert.
- Decimal-Werte werden immer als Strings gespeichert.
- rejected_order_details wird als JSON-String gespeichert.
- Keine NaN- oder Infinity-Werte erlaubt.
- Alle Events müssen vor Speicherung JSON-serialisierbar sein.
- Parquet ist das primäre Speicherformat.
- JSON ist nur Export-, Debugging- und Prüfungsformat.

## Begründung

Die Speicherung komplexer Felder als JSON-String hält das Parquet-Schema stabil.

Nested Parquet-Strukturen wie list<struct> werden für Core v1.0 bewusst nicht verwendet, um Schema-Drift, Tooling-Komplexität und Golden-Case-Abweichungen zu vermeiden.

Eine spätere Umstellung auf native Nested-Parquet-Strukturen bleibt möglich, ist aber nicht Teil von Core v1.0.

## Parquet-Schema Core v1.0

Core v1.0 verwendet ein bewusst einfaches, hash-stabiles Parquet-Schema.

```python
import pyarrow as pa

AUDIT_LOG_SCHEMA_CORE_V1_0 = pa.schema([
    pa.field("audit_schema_version", pa.string(), nullable=False),

    pa.field("run_id", pa.string(), nullable=False),
    pa.field("timestamp", pa.string(), nullable=False),
    pa.field("station", pa.string(), nullable=False),
    pa.field("rule_id", pa.string(), nullable=True),
    pa.field("validator_status", pa.string(), nullable=False),
    pa.field("system_status", pa.string(), nullable=False),
    pa.field("pipeline_action", pa.string(), nullable=False),
    pa.field("asset_id", pa.string(), nullable=True),
    pa.field("reason", pa.string(), nullable=False),

    pa.field("event_type", pa.string(), nullable=False),
    pa.field("event_scope", pa.string(), nullable=False),

    pa.field("audit_hash", pa.string(), nullable=False),

    pa.field("original_value", pa.string(), nullable=True),
    pa.field("enforced_value", pa.string(), nullable=True),
    pa.field("num_orders_proposed", pa.int64(), nullable=True),
    pa.field("num_orders_rejected", pa.int64(), nullable=True),
    pa.field("order_proposal_status", pa.string(), nullable=True),
    pa.field("rejected_order_details", pa.string(), nullable=True),
    pa.field("station_8_validation_ref", pa.string(), nullable=True),
    pa.field("simulation_status", pa.string(), nullable=True),
    pa.field("input_order_count", pa.int64(), nullable=True),
    pa.field("full_fill_count", pa.int64(), nullable=True),
    pa.field("partial_fill_count", pa.int64(), nullable=True),
    pa.field("no_fill_count", pa.int64(), nullable=True),
    pa.field("failed_fill_count", pa.int64(), nullable=True),
    pa.field("total_execution_cost", pa.string(), nullable=True),
    pa.field("total_commission", pa.string(), nullable=True),
    pa.field("total_slippage_cost", pa.string(), nullable=True),
    pa.field("execution_report_ref", pa.string(), nullable=True),
    pa.field("post_execution_portfolio_ref", pa.string(), nullable=True)
])
```

## Partitionierungslogik Core v1.0

Partitionierung erfolgt ausschließlich nach UTC-Datum.

```python
from datetime import datetime, timezone
from typing import Dict


def get_audit_partition_path(timestamp_utc_iso: str) -> Dict[str, str]:
    """
    Extract year/month/day partition values from UTC ISO timestamp.

    Input example:
    2026-05-16T01:30:45.123Z
    """

    ts = datetime.fromisoformat(timestamp_utc_iso.replace("Z", "+00:00"))

    if ts.tzinfo is None:
        raise ValueError("timestamp must include UTC timezone")

    ts_utc = ts.astimezone(timezone.utc)

    return {
        "year": f"{ts_utc.year:04d}",
        "month": f"{ts_utc.month:02d}",
        "day": f"{ts_utc.day:02d}"
    }
```

Zielstruktur:

```text
audit_logs/core_v1_0/year=YYYY/month=MM/day=DD/part-xxxxx.snappy.parquet
```

Core v1.0 verwendet keine Partitionierung nach run_id oder station.

## Audit-Log-Rotation

Core v1.0 verwendet eine einfache, deterministische Tagesrotation.

## Rotationsregel

Audit-Events werden nach UTC-Datum partitioniert.

Zielstruktur:

audit_logs/core_v1_0/year=YYYY/month=MM/day=DD/part-xxxxx.snappy.parquet

Beispiel:

audit_logs/core_v1_0/year=2026/month=05/day=16/part-00000.snappy.parquet

## Rotations-Grundregeln

- Ein Audit-Event wird anhand seines UTC-timestamp dem Tagesordner zugeordnet.
- Innerhalb eines Tages wird in dieselbe Tagespartition geschrieben.
- Es gibt keine Hash-Chain über Dateien hinweg.
- audit_hash bleibt ein Einzel-Event-Hash.
- Bestehende Parquet-Dateien werden nicht editiert, sondern append-only erweitert.
- Korrekturen erfolgen durch neue Audit-Events, nicht durch Änderung alter Events.
- JSON-Exports sind optional und werden aus Parquet erzeugt.
- JSON-Exports sind nicht die primäre Wahrheit.

## Kompatibilitätstabelle Core v1.0

Diese Tabelle legt fest, wie Audit-Felder zwischen Python, JSON, Parquet und Golden Cases behandelt werden.

| Feld | Python / Runtime | JSON-Export | Parquet Core v1.0 | Golden-Case-Prüfung |
|---|---|---|---|---|
| audit_schema_version | str | string | string | exakter Stringvergleich |
| run_id | str | string | string | exakter Stringvergleich |
| timestamp | str UTC-ISO | string | string | exakter Stringvergleich |
| station | str | string | string | exakter Stringvergleich |
| rule_id | str oder None | string oder null | nullable string | exakter Vergleich inkl. null |
| validator_status | str | string | string | exakter Stringvergleich |
| system_status | str | string | string | exakter Stringvergleich |
| pipeline_action | str | string | string | exakter Stringvergleich |
| asset_id | str oder None | string oder null | nullable string | exakter Vergleich inkl. null |
| reason | str | string | string | contains- oder exakter Vergleich |
| event_type | str | string | string | exakter Stringvergleich |
| event_scope | str | string | string | exakter Stringvergleich |
| audit_hash | str | string | string | Hash-Reproduktion möglich |
| original_value | str oder None | string oder null | nullable string | exakter Stringvergleich |
| enforced_value | str oder None | string oder null | nullable string | exakter Stringvergleich |
| num_orders_proposed | int oder None | number oder null | nullable int64 | exakter Vergleich |
| num_orders_rejected | int oder None | number oder null | nullable int64 | exakter Vergleich |
| order_proposal_status | str oder None | string oder null | nullable string | exakter Vergleich |
| rejected_order_details | list zur Laufzeit, JSON-String bei Speicherung | array oder string-exportiert | nullable string | nach JSON-Deserialisierung prüfbar |
| station_8_validation_ref | str oder None | string oder null | nullable string | Referenz zur Station-8-Freigabe |
| simulation_status | str oder None | string oder null | nullable string | SUCCESS / PARTIAL / FAILED |
| input_order_count | int oder None | number oder null | nullable int64 | Anzahl simulierter Orders |
| full_fill_count | int oder None | number oder null | nullable int64 | vollständig gefüllte Orders |
| partial_fill_count | int oder None | number oder null | nullable int64 | teilweise gefüllte Orders |
| no_fill_count | int oder None | number oder null | nullable int64 | nicht gefüllte Orders |
| failed_fill_count | int oder None | number oder null | nullable int64 | nicht simulierbare Orders |
| total_execution_cost | str oder None | string oder null | nullable string | Decimal-String |
| total_commission | str oder None | string oder null | nullable string | Decimal-String |
| total_slippage_cost | str oder None | string oder null | nullable string | Decimal-String |
| execution_report_ref | str oder None | string oder null | nullable string | Referenz auf vollständigen Execution Report |
| post_execution_portfolio_ref | str oder None | string oder null | nullable string | Referenz auf simulierten Portfoliozustand |

## Kompatibilitätsregeln

- Runtime-Events dürfen intern strukturierte Objekte verwenden.
- Vor Parquet-Speicherung müssen komplexe Felder serialisiert werden.
- rejected_order_details wird in Parquet als JSON-String gespeichert.
- Decimal-Werte werden vor Hashing und Speicherung in Strings normalisiert.
- datetime-Werte werden vor Hashing und Speicherung in UTC-ISO-Strings normalisiert.
- Golden Cases prüfen keine Python-Objekte, sondern kanonische JSON-kompatible Werte.
- Die Hash-Berechnung basiert auf der kanonischen JSON-Repräsentation, nicht auf der Parquet-Binärrepräsentation.

## Nicht erlaubt in Core v1.0

- keine NaN- oder Infinity-Werte
- keine Python-Objekte im finalen Audit-Event
- keine Decimal-Objekte im finalen Audit-Event
- keine datetime-Objekte im finalen Audit-Event
- keine ML-Felder

## Hash- und Verifikationslogik Core v1.0

Core v1.0 verwendet einen Einzel-Event-Integritäts-Hash.

Keine Hash-Chain.

Kein previous_audit_hash.

Kein Merkle-Baum.

Kein HMAC.

Der Hash dient der Integritätsprüfung einzelner Audit-Events. Er ist keine kryptografische Signatur.

```python
import hashlib
import json
from copy import deepcopy
from typing import Any, Dict


SUPPORTED_AUDIT_SCHEMA_VERSION = "audit_log_core_v1.0"

REQUIRED_AUDIT_FIELDS = [
    "audit_schema_version",
    "run_id",
    "timestamp",
    "station",
    "rule_id",
    "validator_status",
    "system_status",
    "pipeline_action",
    "asset_id",
    "reason",
    "event_type",
    "event_scope",
]

NULLABLE_FIELDS = {"rule_id", "asset_id"}


def _validate_required_fields(event: Dict[str, Any]) -> None:
    for field in REQUIRED_AUDIT_FIELDS:
        if field not in event:
            if field in NULLABLE_FIELDS:
                raise ValueError(
                    f"Missing required field: {field}. "
                    "Field must be present even if null."
                )
            if field == "audit_schema_version":
                raise ValueError(
                    "Missing required field: audit_schema_version. "
                    "All Core v1.0 audit events must declare "
                    "'audit_schema_version': 'audit_log_core_v1.0'."
                )
            raise ValueError(f"Missing required audit field: {field}")


def _validate_non_nullable_fields(event: Dict[str, Any]) -> None:
    for field in REQUIRED_AUDIT_FIELDS:
        if field in NULLABLE_FIELDS:
            continue
        if event.get(field) is None:
            raise ValueError(f"Required field must not be null: {field}")


def _validate_schema_version(event: Dict[str, Any]) -> None:
    version = event.get("audit_schema_version")
    if version != SUPPORTED_AUDIT_SCHEMA_VERSION:
        raise ValueError(
            f"Unsupported audit_schema_version: '{version}'. "
            f"Expected exactly '{SUPPORTED_AUDIT_SCHEMA_VERSION}'."
        )


def _validate_reason(event: Dict[str, Any]) -> None:
    reason = event.get("reason")

    if not isinstance(reason, str) or len(reason.strip()) == 0:
        raise ValueError("reason must be a non-empty string")

    if len(reason) > 300:
        raise ValueError("reason must not exceed 300 characters")


def _validate_json_safety(event: Dict[str, Any]) -> None:
    try:
        json.dumps(
            event,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Audit event is not canonical JSON safe: {exc}") from exc


def validate_audit_event_payload(event: Dict[str, Any]) -> None:
    """
    Validates a Core-v1 audit event payload before hash calculation.

    The event must not contain a non-empty audit_hash.
    """

    if not isinstance(event, dict):
        raise TypeError("Audit event must be a dictionary")

    if "audit_hash" in event and event.get("audit_hash") not in (None, ""):
        raise ValueError("audit_hash must be absent or empty before hash calculation")

    _validate_required_fields(event)
    _validate_non_nullable_fields(event)
    _validate_schema_version(event)
    _validate_reason(event)
    _validate_json_safety(event)


def compute_audit_hash(event: Dict[str, Any]) -> str:
    """
    Computes deterministic SHA-256 hash over canonical JSON.

    Important:
    - Validation runs on the original event first.
    - A pre-existing non-empty audit_hash is rejected.
    - audit_hash is removed only after validation for the hash basis.
    """

    validate_audit_event_payload(event)

    event_copy = deepcopy(event)
    event_copy.pop("audit_hash", None)

    canonical_json = json.dumps(
        event_copy,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )

    hash_obj = hashlib.sha256(canonical_json.encode("utf-8"))

    return f"sha256:{hash_obj.hexdigest()}"

def add_audit_hash(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Returns a copy of the event with audit_hash added.

    The original event remains unchanged.
    """

    if not isinstance(event, dict):
        raise TypeError("Event must be a dictionary")

    event_without_hash = deepcopy(event)
    event_without_hash.pop("audit_hash", None)

    event_with_hash = deepcopy(event_without_hash)
    event_with_hash["audit_hash"] = compute_audit_hash(event_without_hash)

    return event_with_hash


def verify_audit_event(stored_event: Dict[str, Any]) -> bool:
    """
    Verifies a stored Core-v1 audit event.

    Returns True if the stored audit_hash matches the recomputed hash.
    Raises ValueError on invalid structure or hash mismatch.
    """

    if not isinstance(stored_event, dict):
        raise TypeError("Stored audit event must be a dictionary")

    stored_hash = stored_event.get("audit_hash")

    if not isinstance(stored_hash, str) or not stored_hash.startswith("sha256:"):
        raise ValueError("Missing or invalid audit_hash in stored event")

    event_without_hash = deepcopy(stored_event)
    event_without_hash.pop("audit_hash", None)

    computed_hash = compute_audit_hash(event_without_hash)

    if computed_hash != stored_hash:
        raise ValueError(
            "Audit hash mismatch. "
            f"Stored: {stored_hash[:20]}... "
            f"Computed: {computed_hash[:20]}..."
        )

    return True
```

## Verifikationsregeln

- add_audit_hash() erzeugt ein gespeichertes Event mit audit_hash.
- verify_audit_event() prüft gespeicherte Events nach dem Laden aus Parquet.
- audit_hash wird nie in seine eigene Berechnung einbezogen.
- audit_schema_version ist Pflichtfeld und wird mitgehasht.
- rule_id und asset_id sind Pflichtfelder, dürfen aber null sein.
- Alle anderen Pflichtfelder müssen vorhanden und nicht null sein.
- NaN und Infinity sind verboten.
- Decimal- und datetime-Werte müssen vor Hashing als Strings normalisiert sein.
- Core v1.0 verwendet keine Hash-Chain, keinen Merkle-Baum und kein HMAC.

## Aktueller Status

Diese Audit-Log-Struktur ist fachlich für Core v1.0 spezifiziert.

## Codex-Hinweis

Codex darf diese Struktur später implementieren.

Warum:

Die Audit-Log-Struktur ist eine deterministische Infrastrukturkomponente für Speicherung, Hashing, Verifikation und spätere Auswertung.

Wie:

Codex implementiert später AuditEvent, AuditLogger, Hash Utility, Parquet Writer, JSON Export, Verifikation und Unit Tests exakt nach dieser Spezifikation.

Codex darf keine ML-Felder, keine Hash-Chain, keinen Merkle-Baum, kein HMAC und keine feldweise Verschlüsselung in Core v1.0 ergänzen.

## Audit-Log-Archivierung Core v1.0

Core v1.0 definiert ein einfaches, robustes und wartbares Archivierungskonzept für Audit-Logs.

Ziel ist langfristige Aufbewahrung bei erhaltener Integrität, einfacher Wiederherstellung und minimaler operativer Komplexität.

## Archivierungsprinzip

Core v1.0 verwendet den Copy-Verify-Retention-Ansatz.

Nicht erlaubt ist ein Move-first-Verfahren.

Archivierung bedeutet:

1. Hot-Daten lesen.
2. Zielarchiv schreiben.
3. Zielbestand vollständig oder stichprobenbasiert verifizieren.
4. Anzahl und Hash-Integrität prüfen.
5. Quelle nur nach erfolgreicher Prüfung manuell zur Bereinigung freigeben.

## Archiv-Ebenen

| Ebene | Pfad | Zeitraum | Zweck | Komprimierung |
|---|---|---:|---|---|
| Hot | audit_logs/core_v1_0/ | ca. 90 Tage | aktuelle Analysen, Debugging, Golden-Case-Prüfung | Snappy |
| Warm | archive/core_v1_0/year=YYYY/ | ca. 1 Jahr | Reports, Nachanalyse, Backtesting | Snappy oder optional Zstd |
| Cold | archive/core_v1_0/cold/ | unbegrenzt | langfristige Aufbewahrung | optional Zstd + Parquet |

## Archivierungsregeln

- Core v1.0 löscht keine Audit-Events automatisch.
- Archivierung ist ein manueller oder später externer Offline-Prozess.
- Archivierung darf keine Audit-Events inhaltlich verändern.
- audit_schema_version bleibt unverändert erhalten.
- audit_hash bleibt unverändert erhalten.
- Das Parquet-Schema bleibt identisch.
- Komplexe Felder bleiben in ihrer Core-v1.0-Speicherform erhalten.
- Vor Archivierung muss das Quellmaterial lesbar sein.
- Nach Archivierung muss das Zielmaterial verifizierbar sein.
- Quelle wird nicht automatisch gelöscht.
- Manuelle Löschung ist erst nach erfolgreicher Zielprüfung zulässig.

## Vertiefter Archivierungsablauf

### 1. Export / Kopie

Events werden aus Hot gelesen.

Filterung kann erfolgen nach:

- year
- month
- day
- run_id
- station
- event_type

### 2. Ziel schreiben

Events werden in Warm oder Cold geschrieben.

Dabei bleiben unverändert:

- audit_schema_version
- audit_hash
- run_id
- timestamp
- station
- rule_id
- validator_status
- system_status
- pipeline_action
- asset_id
- reason
- event_type
- event_scope
- optionale Detailfelder

### 3. Integritätsprüfung

Nach dem Schreiben wird der Zielbestand geprüft.

```python
for event in archived_events:
    verify_audit_event(event)
```

### 4. Zusätzliche Konsistenzprüfung

Zusätzlich zur Hash-Prüfung gilt:

- Anzahl der kopierten Events muss mit der Quellmenge übereinstimmen.
- Stichproben-Hash-Vergleich ist empfohlen.
- Für Core v1.0 genügt eine Stichprobe von mindestens 5 Prozent, sofern keine Vollprüfung durchgeführt wird.
- Bei Abweichung gilt die Archivierung als fehlgeschlagen.

### 5. Freigabe zur Bereinigung

Nur nach erfolgreicher Prüfung darf die Quelle manuell zur Bereinigung freigegeben werden.

Core v1.0 führt keine automatische Löschung aus.

## Empfohlene Offline-Skript-Struktur

```python
def archive_events(source_path: str, target_path: str, older_than_days: int):
    """
    Offline archive process for Core-v1.0 audit logs.

    Steps:
    1. Filter old events.
    2. Read source events.
    3. Write events to archive target.
    4. Run verify_audit_event() on archived events.
    5. Compare source and archive event counts.
    6. Write success protocol and metadata.
    7. Allow manual cleanup only after successful verification.
    """
    pass
```

## Nicht Teil von Core v1.0

- kein automatischer Scheduler
- keine automatische Löschung
- keine Kompressionsumwandlung in der normalen Pipeline
- keine Hash-Chain
- kein Merkle-Baum
- kein HMAC
- keine feldweise Verschlüsselung
- kein Move-first-Verfahren

## Review-Fazit

Copy-Verify-Retention ist das verbindliche Archivierungsprinzip für Core v1.0.

Archivierung ist sicher, nachvollziehbar und bewusst offline gehalten.

Hash-Integrität bleibt über verify_audit_event() prüfbar.

Core v1.0 priorisiert Integrität, Wartbarkeit und Wiederherstellbarkeit vor Automatisierung.

## Golden Cases

Die Golden Cases für Audit-Log Core v1.0 liegen unter:

tests/golden_cases/audit_log_core_v1_cases.json

Sie prüfen insbesondere:

- audit_schema_version
- Pflichtfelder und nullable Felder
- Non-Null-Regeln
- Reason-Limit
- Hash-Berechnung
- Hash-Verifikation
- Hash-Mismatch-Erkennung
- Audit-Event-Integrität

## Audit-kompatible Execution-Simulator-Events nach Station 8

A) Zweck: Der Execution Simulator darf nach Station 8 eigene Audit-Events in Audit-Log Core v1.0 schreiben.

B) Abgrenzung: Diese Events sind keine Station-1-bis-8-Validierungsereignisse, keine Station 9 und keine Pipeline-Steuerung.

C) Eigene Event-Typen: EXECUTION_SIMULATION_SUCCESS, EXECUTION_SIMULATION_PARTIAL, EXECUTION_SIMULATION_FAILED.

D) Kein Mapping: Execution-Simulator-Ergebnisse werden nicht auf RULE_PASS, RULE_REJECTED oder TECHNICAL_ERROR gemappt.

E) Statusregeln: validator_status bleibt PASS. simulation_status wird separat geführt. system_status bleibt NORMAL_CONTINUE. pipeline_action bleibt CONTINUE.

F) FAILED-Regel: EXECUTION_SIMULATION_FAILED bedeutet nur, dass die Simulation nicht belastbar war. Es invalidiert Station 8 nicht rückwirkend und stoppt keine Pipeline.

G) Optionale Simulator-Auditfelder: station_8_validation_ref, simulation_status, input_order_count, full_fill_count, partial_fill_count, no_fill_count, failed_fill_count, total_execution_cost, total_commission, total_slippage_cost, execution_report_ref und post_execution_portfolio_ref.

H) Integrität: Jedes Execution-Simulator-Audit-Event läuft durch add_audit_hash() und muss mit verify_audit_event() prüfbar sein.
