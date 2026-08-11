"""DetectLLM Log-Rank Ratio."""


def lrr(average_log_probability_value, average_log_rank_value):
    if average_log_rank_value == 0:
        raise ValueError("average_log_rank_value must not be zero")
    return -float(average_log_probability_value) / float(average_log_rank_value)
