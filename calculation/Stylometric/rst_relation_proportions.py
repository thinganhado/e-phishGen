"""Coarse RST relation proportions from already parsed relation labels."""

from collections import Counter


COARSE_RELATIONS = (
    "Attribution.N", "Attribution.S", "Background.N", "Background.S", "Cause.N", "Cause.S",
    "Comparison.N", "Comparison.S", "Condition.N", "Condition.S", "Contrast.N", "Contrast.S",
    "Elaboration.N", "Elaboration.S", "Enablement.N", "Enablement.S", "Evaluation.N", "Evaluation.S",
    "Explanation.N", "Explanation.S", "Joint.N", "Manner-Means.N", "Manner-Means.S",
    "Topic-Comment.N", "Topic-Comment.S", "Summary.N", "Summary.S", "Temporal.N", "Temporal.S",
    "Same-unit.N", "Textual-organization.N", "None",
)


FINE_TO_COARSE = {}
for coarse, fine_labels in {
    "Background": ("background", "circumstance"), "Cause": ("cause", "result", "consequence"),
    "Comparison": ("comparison", "preference", "analogy", "proportion"),
    "Condition": ("condition", "hypothetical", "contingency", "otherwise"),
    "Contrast": ("contrast", "concession", "antithesis"),
    "Elaboration": ("elaboration", "example", "definition"),
    "Enablement": ("purpose", "enablement"), "Evaluation": ("evaluation", "interpretation", "conclusion"),
    "Explanation": ("evidence", "explanation", "reason"), "Joint": ("list", "disjunction"),
    "Manner-Means": ("manner", "means"),
    "Topic-Comment": ("problem", "question", "statement", "topic", "comment", "rhetorical"),
    "Summary": ("summary", "restatement"), "Temporal": ("temporal", "sequence", "inverted"),
}.items():
    for suffix in ("N", "S"):
        for fine in fine_labels:
            # Match create_RST_discourse_vectors.py exactly: some fine
            # relations have no S-side mapping in the original source.
            if (coarse, fine, suffix) in {
                ("Contrast", "contrast", "S"),
                ("Comparison", "proportion", "S"),
                ("Temporal", "sequence", "S"),
                ("Temporal", "inverted", "S"),
            }:
                continue
            FINE_TO_COARSE[fine + "." + suffix] = coarse + "." + suffix
for name in ("attribution", "same_unit", "textualorganization"):
    suffixes = ("N", "S") if name == "attribution" else ("N",)
    for suffix in suffixes:
        FINE_TO_COARSE[name + "." + suffix] = {"attribution": "Attribution", "same_unit": "Same-unit", "textualorganization": "Textual-organization"}[name] + "." + suffix


def rst_relation_proportions(relations):
    coarse = Counter()
    for relation in relations:
        if relation in (None, "", "[[]]", "None"):
            coarse["None"] += 1
        else:
            coarse[FINE_TO_COARSE.get(relation, relation)] += 1
    total = sum(coarse.values())
    return {relation: (coarse[relation] / float(total) if total else 0.0) for relation in COARSE_RELATIONS}
