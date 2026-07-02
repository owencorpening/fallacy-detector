from core.fallacies import FALLACIES, FallacyResult
import json


def _fallacy_block() -> str:
    return "\n\n".join(
        f"**{f.name}**\n{f.description}\nExamples:\n" + "\n".join(f"  - {e}" for e in f.examples)
        for f in FALLACIES
    )


def build_prompt(transcript: str, context: list[str]) -> str:
    context_block = ""
    if context:
        joined = " [...] ".join(context)
        context_block = f"\nPREVIOUS CONTEXT:\n{joined}\n"

    return f"""You are a logical fallacy detector. Analyze the CURRENT TRANSCRIPT for logical fallacies.

FALLACIES TO DETECT:
{_fallacy_block()}

{context_block}
CURRENT TRANSCRIPT:
{transcript}

If you detect a fallacy, respond with a JSON object only — no explanation, no markdown:
{{"fallacy": "<exact fallacy name from list>", "confidence": <0.0–1.0>, "trigger_phrase": "<short exact quote from transcript>"}}

If no fallacy is detected, respond with exactly: null"""


def build_batch_prompt(transcript: str) -> str:
    return f"""You are a logical fallacy detector. Analyze the TRANSCRIPT below and identify ALL logical fallacies present.

FALLACIES TO DETECT:
{_fallacy_block()}

TRANSCRIPT:
{transcript}

Respond with a JSON array of every fallacy found. Each entry:
{{"fallacy": "<exact name from list>", "confidence": <0.0–1.0>, "trigger_phrase": "<complete sentence or phrase quoted exactly from the transcript>"}}

If no fallacies are found, respond with exactly: []
No explanation, no markdown — only the JSON array or []."""


def parse_batch_response(raw: str, transcript: str) -> list[FallacyResult]:
    raw = raw.strip()
    if not raw or raw == "[]":
        return []
    try:
        data = json.loads(raw)
        if not isinstance(data, list):
            return []
        results = []
        for item in data:
            trigger = item.get("trigger_phrase", "")
            if not trigger or trigger.lower() not in transcript.lower():
                continue
            results.append(FallacyResult(
                name=item["fallacy"],
                confidence=float(item["confidence"]),
                trigger_phrase=trigger,
            ))
        return results
    except (json.JSONDecodeError, KeyError, ValueError):
        return []


def parse_response(raw: str, transcript: str) -> FallacyResult | None:
    raw = raw.strip()
    if raw.lower() == "null" or not raw:
        return None
    try:
        data = json.loads(raw)
        trigger = data["trigger_phrase"]
        if not trigger or trigger.lower() not in transcript.lower():
            return None
        return FallacyResult(
            name=data["fallacy"],
            confidence=float(data["confidence"]),
            trigger_phrase=trigger,
        )
    except (json.JSONDecodeError, KeyError, ValueError):
        return None
