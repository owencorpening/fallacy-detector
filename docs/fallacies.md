# Fallacies detected

The detector watches for 10 common informal fallacies. Each is defined in `core/fallacies.py` and included verbatim in every LLM prompt.

---

## Straw Man
Misrepresenting someone's argument to make it easier to attack.

> "Person A: We should have stricter gun laws. Person B: So you want to ban all guns and leave us defenseless."

---

## Ad Hominem
Attacking the person making the argument rather than the argument itself.

> "You can't trust his economic policy — he went bankrupt twice."

---

## False Dichotomy
Presenting only two options when more exist; framing a choice as either/or.

> "You're either with us or against us."

---

## Slippery Slope
Claiming one event will inevitably lead to extreme consequences without justification.

> "If we raise the minimum wage, businesses will close, the economy will collapse."

---

## Appeal to Authority
Using an authority figure's opinion as evidence without other support, especially outside their domain.

> "A Nobel Prize winner says vaccines are dangerous, so they must be."

---

## Hasty Generalization
Drawing a broad conclusion from a small or unrepresentative sample.

> "I met two rude people from that city — everyone there is rude."

---

## Circular Reasoning
Using the conclusion as a premise; the argument assumes what it's trying to prove.

> "The Bible is true because it says so in the Bible."

---

## Red Herring
Introducing irrelevant information to distract from the actual issue.

> "You say I broke the law, but what about all the good I've done for this community?"

---

## Appeal to Emotion
Manipulating emotions to substitute for a logical argument.

> "Think of the children — how can you vote against this?"

---

## Bandwagon
Arguing something is true or good because many people believe or do it.

> "Millions of people use this supplement, so it must work."

---

## Output format

When a fallacy is detected, the tool prints one line to stdout:

```
[STRAW MAN 0.87] "so you're saying we should just ban everything"
```

`0.87` is the model's confidence (0.0–1.0). The quoted phrase is the exact trigger phrase from the transcript. Nothing is printed for clean audio.
