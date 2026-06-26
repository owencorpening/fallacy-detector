from core.fallacies import FALLACIES, FallacyResult
import json


def build_prompt(transcript: str, context: list[str]) -> str:
    fallacy_block = "\n\n".join(
        f"**{f.name}**\n{f.description}\nExamples:\n" + "\n".join(f"  - {e}" for e in f.examples)
        for f in FALLACIES
    )

    context_block = ""
    if context:
        joined = " [...] ".join(context)
        context_block = f"\nPREVIOUS CONTEXT:\n{joined}\n"

    return f"""You are a logical fallacy detector. Analyze the CURRENT TRANSCRIPT for logical fallacies.

FALLACIES TO DETECT:
{fallacy_block}

{context_block}
CURRENT TRANSCRIPT:
{transcript}

If you detect a fallacy, respond with a JSON object only — no explanation, no markdown:
{{"fallacy": "<exact fallacy name from list>", "confidence": <0.0–1.0>, "trigger_phrase": "<short exact quote from transcript>"}}

If no fallacy is detected, respond with exactly: null"""


def parse_response(raw: str, transcript: str) -> FallacyResult | None:
    raw = raw.strip()
    if raw.lower() == "null" or not raw:
        return None
    try:
        data = json.loads(raw)
        trigger = data["trigger_phrase"]
        if trigger.lower() not in transcript.lower():
            return None
        return FallacyResult(
            name=data["fallacy"],
            confidence=float(data["confidence"]),
            trigger_phrase=trigger,
        )
    except (json.JSONDecodeError, KeyError, ValueError):
        return None
