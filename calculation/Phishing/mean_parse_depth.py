"""Mean dependency-tree depth from supplied token depths."""
from common import safe_div


def mean_parse_depth(depths):
    values = list(depths)
    return safe_div(sum(values), len(values))
