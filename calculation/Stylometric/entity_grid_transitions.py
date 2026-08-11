"""Coreference-aware grammatical entity-grid transition proportions."""

TRANSITIONS = tuple(a + b for a in "sox-" for b in "sox-")


def entity_grid_transition_proportions(grid):
    """Calculate the 16 adjacent-row transitions over every entity column."""
    rows = [list(row) for row in grid]
    counts = {transition: 0 for transition in TRANSITIONS}
    for current, following in zip(rows, rows[1:]):
        if len(current) != len(following):
            raise ValueError("all entity-grid rows must have equal width")
        for left, right in zip(current, following):
            transition = str(left) + str(right)
            if transition not in counts:
                raise ValueError("invalid entity-grid symbol: %s" % transition)
            counts[transition] += 1
    total = sum(counts.values())
    return {key: (value / float(total) if total else 0.0) for key, value in counts.items()}
