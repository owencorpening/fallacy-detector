from dataclasses import dataclass


@dataclass
class FallacyDefinition:
    name: str
    description: str
    examples: list[str]


@dataclass
class FallacyResult:
    name: str
    confidence: float
    trigger_phrase: str

    def __str__(self) -> str:
        return f"[{self.name.upper()} {self.confidence:.2f}] \"{self.trigger_phrase}\""


FALLACIES: list[FallacyDefinition] = [
    FallacyDefinition(
        name="Straw Man",
        description="Misrepresenting someone's argument to make it easier to attack.",
        examples=[
            "Person A: We should have stricter gun laws. Person B: So you want to ban all guns and leave us defenseless.",
            "She said we should cut the defense budget, so she must want no military at all.",
        ],
    ),
    FallacyDefinition(
        name="Ad Hominem",
        description="Attacking the person making the argument rather than the argument itself.",
        examples=[
            "You can't trust his economic policy — he went bankrupt twice.",
            "Why would we listen to her climate advice? She drives an SUV.",
        ],
    ),
    FallacyDefinition(
        name="False Dichotomy",
        description="Presenting only two options when more exist; framing a choice as either/or.",
        examples=[
            "You're either with us or against us.",
            "If you don't support this bill, you support crime.",
        ],
    ),
    FallacyDefinition(
        name="Slippery Slope",
        description="Claiming one event will inevitably lead to extreme consequences without justification.",
        examples=[
            "If we allow same-sex marriage, next people will want to marry animals.",
            "If we raise the minimum wage, businesses will close, the economy will collapse.",
        ],
    ),
    FallacyDefinition(
        name="Appeal to Authority",
        description="Using an authority figure's opinion as evidence without other support, especially outside their domain.",
        examples=[
            "A Nobel Prize winner says vaccines are dangerous, so they must be.",
            "My doctor says astrology is real, so it must have merit.",
        ],
    ),
    FallacyDefinition(
        name="Hasty Generalization",
        description="Drawing a broad conclusion from a small or unrepresentative sample.",
        examples=[
            "I met two rude people from that city — everyone there is rude.",
            "That politician lied once, so all politicians always lie.",
        ],
    ),
    FallacyDefinition(
        name="Circular Reasoning",
        description="Using the conclusion as a premise; the argument assumes what it's trying to prove.",
        examples=[
            "The Bible is true because it says so in the Bible.",
            "He's a criminal because he does criminal things.",
        ],
    ),
    FallacyDefinition(
        name="Red Herring",
        description="Introducing irrelevant information to distract from the actual issue.",
        examples=[
            "Why worry about pollution when people are dying of cancer?",
            "You say I broke the law, but what about all the good I've done for this community?",
        ],
    ),
    FallacyDefinition(
        name="Appeal to Emotion",
        description="Manipulating emotions to substitute for a logical argument.",
        examples=[
            "Think of the children — how can you vote against this?",
            "Our soldiers died for this country. Are you saying their sacrifice meant nothing?",
        ],
    ),
    FallacyDefinition(
        name="Bandwagon",
        description="Arguing something is true or good because many people believe or do it.",
        examples=[
            "Millions of people use this supplement, so it must work.",
            "Everyone supports this candidate — you should too.",
        ],
    ),
]

FALLACY_MAP: dict[str, FallacyDefinition] = {f.name.upper(): f for f in FALLACIES}
