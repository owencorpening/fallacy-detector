import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from core.classifier import build_prompt, parse_response
from core.fallacies import FALLACIES, FallacyResult


# --- parse_response ---

def test_parse_valid_result():
    raw = '{"fallacy": "Straw Man", "confidence": 0.91, "trigger_phrase": "so you want to ban all guns"}'
    result = parse_response(raw)
    assert isinstance(result, FallacyResult)
    assert result.name == "Straw Man"
    assert result.confidence == 0.91
    assert result.trigger_phrase == "so you want to ban all guns"


def test_parse_null_string():
    assert parse_response("null") is None


def test_parse_empty_string():
    assert parse_response("") is None


def test_parse_whitespace_null():
    assert parse_response("  null  ") is None


def test_parse_invalid_json_returns_none():
    assert parse_response("not json at all") is None


def test_parse_missing_key_returns_none():
    assert parse_response('{"fallacy": "Straw Man"}') is None


def test_parse_confidence_as_string():
    raw = '{"fallacy": "Ad Hominem", "confidence": "0.75", "trigger_phrase": "he went bankrupt"}'
    result = parse_response(raw)
    assert result.confidence == 0.75


def test_result_str_format():
    r = FallacyResult(name="Straw Man", confidence=0.87, trigger_phrase="so you're saying...")
    assert str(r) == '[STRAW MAN 0.87] "so you\'re saying..."'


# --- build_prompt ---

def test_prompt_contains_all_fallacy_names():
    prompt = build_prompt("test transcript", [])
    for f in FALLACIES:
        assert f.name in prompt


def test_prompt_contains_transcript():
    prompt = build_prompt("politicians always lie", [])
    assert "politicians always lie" in prompt


def test_prompt_includes_context():
    prompt = build_prompt("current text", ["previous chunk one", "previous chunk two"])
    assert "previous chunk one" in prompt
    assert "previous chunk two" in prompt


def test_prompt_no_context_omits_context_block():
    prompt = build_prompt("only current", [])
    assert "PREVIOUS CONTEXT" not in prompt


def test_prompt_instructs_null_for_clean():
    prompt = build_prompt("clean statement", [])
    assert "null" in prompt


# --- coverage across all 10 fallacies ---

ALL_FALLACY_NAMES = [f.name for f in FALLACIES]


def test_all_ten_fallacies_defined():
    assert len(FALLACIES) == 10


def test_each_fallacy_has_examples():
    for f in FALLACIES:
        assert len(f.examples) >= 2, f"{f.name} needs at least 2 examples"
