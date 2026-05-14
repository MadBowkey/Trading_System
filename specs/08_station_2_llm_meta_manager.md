# Station 2 — LLM Meta-Manager

Status: DRAFT
Version: v1.0
Architecture: v1.6.1
Last updated: 2026-05-15
Owner: Trading System Project

## Kurzbeschreibung

Diese Station transformiert die aus Station 1 freigegebenen Markt-, Trend-, Risiko- und Portfolio-Kontexte über ein Large Language Model in eine strukturierte strategische Absicht.

Sie berechnet keine finalen Portfoliogewichte und erzeugt keine Orders, sondern bestimmt Regime, Risikomultiplikator und Asset-Absichten im Format LLMMetaManagerOutput.

## Input

Aus Station 1 freigegebene Daten:

- Marktdatenstatus
- Portfolio Status
- User Managed Universe
- Trend Detection Output
- Regime Output
- Risk Metrics
- System-/Analysekonfiguration

Zusätzlich:

- System-Prompt
- deduktive Regeln
- Few-Shot-Beispiele
- Structured-Output-Schema
- API-Konfiguration

## Output

Ein Structured Output Objekt, das dem logischen Pydantic-Schema LLMMetaManagerOutput entsprechen soll und anschließend an Station 3 übergeben wird.

## Fehlerwirkung

Bei API-Fehlern, Timeout, Nichterreichbarkeit oder leerer Antwort:

SAFE_HOLD / NO_NEW_ACTIONS.

Die Pipeline stoppt. Das bestehende Portfolio bleibt unverändert. Es erfolgt keine Marktaktion.

## Wichtig

Diese Station trifft keine finale Handelsentscheidung.

Sie erzeugt nur eine strategische Absicht.

Ob das Objekt technisch gültig ist, prüft erst Station 3.

Ein LLM- oder API-Fehler darf niemals CASH_ONLY auslösen.

## Aktueller Status

Diese Station ist fachlich abgenommen.

## Codex-Hinweis

Codex darf diese Station später teilweise implementieren.

Warum:
API-Wrapper, Structured-Output-Aufruf, Retry-Handling, Fehlerbehandlung und Logging sind technische Infrastruktur.

Wie:
Codex implementiert später den LLM-Client, den Structured-Output-Aufruf, Timeout-Handling, API-Error-Handling und Übergabe an Station 3.

Codex darf keine Prompts, deduktiven Regeln oder Architekturentscheidungen eigenständig ändern.
