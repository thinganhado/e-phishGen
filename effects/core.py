"""Statistical primitives for the e-phishGen effect-analysis workflow.

The within-dataset model uses centered effect coding::

    metric ~ generation + phishing + generation:phishing + stratum fixed effects

Generation and phishing are coded -0.5/+0.5.  The three corresponding
coefficients are therefore the marginal Generation (G), Phishing (P), and
Interaction (I) effects described in ``phd - 研究步骤指导.pdf``.

Only NumPy and SciPy are used so that the scripts run in the repository's
existing environment without statsmodels.
"""

from __future__ import annotations

import math
from collections import Counter
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
from scipy.optimize import brentq
from scipy.special import gammaln
from scipy.stats import beta as beta_distribution
from scipy.stats import chi2, norm
from scipy.stats import t as student_t


GROUPS = ("HW-B", "HW-P", "MG-B", "MG-P")

# The first four design columns are intercept, G, P, and G:P.  Stratum
# indicators, if any, follow and therefore receive zero contrast weight.
MAIN_EFFECTS = {
    "G": np.array([0.0, 1.0, 0.0, 0.0]),
    "P": np.array([0.0, 0.0, 1.0, 0.0]),
    "I": np.array([0.0, 0.0, 0.0, 1.0]),
}
SIMPLE_EFFECTS = {
    "G_B": np.array([0.0, 1.0, 0.0, -0.5]),
    "G_P": np.array([0.0, 1.0, 0.0, 0.5]),
    "P_HW": np.array([0.0, 0.0, 1.0, -0.5]),
    "P_MG": np.array([0.0, 0.0, 1.0, 0.5]),
}
ALL_CONTRASTS = {**MAIN_EFFECTS, **SIMPLE_EFFECTS}


def is_finite_scalar(value: Any) -> bool:
    """Return True only for finite JSON-style numeric scalars (not booleans)."""

    return (
        isinstance(value, (int, float, np.integer, np.floating))
        and not isinstance(value, (bool, np.bool_))
        and math.isfinite(float(value))
    )


def effect_codes(group: str) -> tuple[float, float]:
    """Return centered generation and phishing codes for a four-cell label."""

    if group not in GROUPS:
        raise ValueError(f"Unsupported group {group!r}; expected one of {GROUPS}")
    generation = 0.5 if group.startswith("MG-") else -0.5
    phishing = 0.5 if group.endswith("-P") else -0.5
    return generation, phishing


def factorial_support(
    rows: Sequence[Mapping[str, Any]], min_cell_n: int = 2
) -> tuple[list[str], dict[str, dict[str, int]]]:
    """Check four-cell support within every stratum.

    Returns a list of human-readable problems and the complete count table.
    """

    counts: dict[str, Counter[str]] = {}
    for row in rows:
        stratum = str(row.get("match_stratum", "__all__"))
        counts.setdefault(stratum, Counter())[str(row["group"])] += 1
    table = {
        stratum: {group: int(cell_counts.get(group, 0)) for group in GROUPS}
        for stratum, cell_counts in sorted(counts.items())
    }
    problems = []
    for stratum, cell_counts in table.items():
        deficient = [
            f"{group}={cell_counts[group]}"
            for group in GROUPS
            if cell_counts[group] < min_cell_n
        ]
        if deficient:
            problems.append(
                f"stratum {stratum!r} lacks factorial support "
                f"(minimum {min_cell_n}; {', '.join(deficient)})"
            )
    return problems, table


def supported_rows(
    rows: Sequence[Mapping[str, Any]], min_cell_n: int = 2
) -> tuple[list[Mapping[str, Any]], list[str]]:
    """Keep only strata containing the requested minimum in all four cells."""

    _, table = factorial_support(rows, min_cell_n=min_cell_n)
    supported = {
        stratum
        for stratum, counts in table.items()
        if all(counts[group] >= min_cell_n for group in GROUPS)
    }
    kept = [
        row
        for row in rows
        if str(row.get("match_stratum", "__all__")) in supported
    ]
    dropped = sorted(set(table) - supported)
    return kept, dropped


def design_matrix(
    rows: Sequence[Mapping[str, Any]],
    weighting: str = "sample",
    covariates: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray, list[str], str]:
    """Build the effect-coded fixed-stratum design and observation weights.

    ``sample`` gives every document equal weight. ``equal_stratum`` gives every
    stratum-by-group cell equal total weight, which is a useful robustness
    estimand when a few strata dominate the dataset.
    """

    if not rows:
        raise ValueError("Cannot build a design matrix with no rows")
    strata = sorted({str(row.get("match_stratum", "__all__")) for row in rows})
    baseline = strata[0]
    matrix = []
    for row in rows:
        generation, phishing = effect_codes(str(row["group"]))
        stratum = str(row.get("match_stratum", "__all__"))
        matrix.append(
            [
                1.0,
                generation,
                phishing,
                generation * phishing,
                *[float(stratum == item) for item in strata[1:]],
            ]
        )
    x = np.asarray(matrix, dtype=float)
    if covariates is not None:
        covariates = np.asarray(covariates, dtype=float)
        if covariates.ndim == 1:
            covariates = covariates[:, None]
        if covariates.ndim != 2 or covariates.shape[0] != len(rows):
            raise ValueError("Additional covariates must have one row per observation")
        if not np.all(np.isfinite(covariates)):
            raise ValueError("Additional covariates must be finite")
        x = np.column_stack([x, covariates])

    if weighting == "sample":
        weights = np.ones(len(rows), dtype=float)
    elif weighting == "equal_stratum":
        counts = Counter(
            (str(row.get("match_stratum", "__all__")), str(row["group"]))
            for row in rows
        )
        weights = np.asarray(
            [
                1.0
                / counts[
                    (str(row.get("match_stratum", "__all__")), str(row["group"]))
                ]
                for row in rows
            ],
            dtype=float,
        )
        # Normalization does not change beta or leverage, but keeps the weighted
        # residual scale comparable with an ordinary residual standard deviation.
        weights *= len(weights) / weights.sum()
    else:
        raise ValueError(f"Unknown weighting {weighting!r}")
    return x, weights, strata, baseline


def _padded_contrast(contrast: np.ndarray, width: int) -> np.ndarray:
    if len(contrast) > width:
        raise ValueError("Contrast is wider than the fitted design")
    return np.pad(np.asarray(contrast, dtype=float), (0, width - len(contrast)))


def hedges_correction(df: int) -> float:
    """Exact Hedges small-sample correction J(df)."""

    if df <= 1:
        return float("nan")
    return float(
        math.exp(
            gammaln(df / 2.0)
            - 0.5 * math.log(df / 2.0)
            - gammaln((df - 1.0) / 2.0)
        )
    )


def fit_factorial(
    x: np.ndarray,
    y: np.ndarray,
    weights: np.ndarray | None = None,
    clusters: Sequence[Any] | None = None,
) -> dict[str, Any]:
    """Fit weighted least squares with HC3 or CR1 robust covariance."""

    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if x.ndim != 2 or y.ndim != 1 or len(x) != len(y):
        raise ValueError("Incompatible design/outcome dimensions")
    n, width = x.shape
    if weights is None:
        weights = np.ones(n, dtype=float)
    weights = np.asarray(weights, dtype=float)
    if weights.shape != (n,) or np.any(weights <= 0) or not np.all(np.isfinite(weights)):
        raise ValueError("Weights must be finite, positive, and match the rows")

    root_w = np.sqrt(weights)
    x_star = x * root_w[:, None]
    y_star = y * root_w
    rank = int(np.linalg.matrix_rank(x_star))
    if rank != width:
        raise ValueError(
            f"Rank-deficient factorial design: rank {rank}, columns {width}"
        )
    condition_number = float(np.linalg.cond(x_star))
    bread = np.linalg.inv(x_star.T @ x_star)
    beta = bread @ x_star.T @ y_star
    residual = y - x @ beta
    transformed_residual = root_w * residual
    leverage = np.sum((x_star @ bread) * x_star, axis=1)
    df_residual = n - rank
    if df_residual <= 1:
        raise ValueError(f"Insufficient residual degrees of freedom: {df_residual}")
    residual_sd = math.sqrt(float(np.sum(weights * residual**2) / df_residual))
    warnings: list[str] = []
    if condition_number > 1e8:
        warnings.append(
            f"Design condition number is {condition_number:.3g}; estimates may be numerically unstable"
        )

    if clusters is None:
        adjusted = transformed_residual / np.maximum(1.0 - leverage, 1e-10)
        meat = (x_star * adjusted[:, None]).T @ (x_star * adjusted[:, None])
        covariance = bread @ meat @ bread
        covariance_method = "HC3"
        inference_df = df_residual
        cluster_count = None
    else:
        cluster_values = np.asarray([str(value) for value in clusters], dtype=object)
        if cluster_values.shape != (n,):
            raise ValueError("Cluster IDs must match the fitted rows")
        unique_clusters = sorted(set(cluster_values.tolist()))
        cluster_count = len(unique_clusters)
        if cluster_count < 4:
            raise ValueError(
                f"Cluster-robust inference needs at least 4 clusters; found {cluster_count}"
            )
        meat = np.zeros((width, width), dtype=float)
        for cluster in unique_clusters:
            mask = cluster_values == cluster
            score = x[mask].T @ (weights[mask] * residual[mask])
            meat += np.outer(score, score)
        correction = (cluster_count / (cluster_count - 1.0)) * (
            (n - 1.0) / (n - rank)
        )
        covariance = correction * (bread @ meat @ bread)
        covariance_method = "CR1"
        inference_df = cluster_count - 1
        if cluster_count < 20:
            warnings.append(
                f"Only {cluster_count} clusters; CR1/t inference may be unstable"
            )
        if cluster_count == n:
            warnings.append(
                "Every row is its own cluster; use HC3 unless this cluster definition is intentional"
            )

    covariance = (covariance + covariance.T) / 2.0
    if residual_sd <= 1e-14 or not math.isfinite(residual_sd):
        warnings.append("Residual variance is zero or numerically degenerate")
    high_leverage_threshold = 2.0 * rank / n
    return {
        "beta": beta,
        "covariance": covariance,
        "residual": residual,
        "residual_sd": residual_sd,
        "rank": rank,
        "n": n,
        "df_residual": df_residual,
        "inference_df": inference_df,
        "condition_number": condition_number,
        "leverage": leverage,
        "max_leverage": float(np.max(leverage)),
        "high_leverage_threshold": float(high_leverage_threshold),
        "high_leverage_count": int(np.sum(leverage > high_leverage_threshold)),
        "covariance_method": covariance_method,
        "cluster_count": cluster_count,
        "weights": weights,
        "warnings": warnings,
    }


def equivalence_test(
    estimate: float,
    standard_error: float,
    df: int,
    bound: float,
    alpha: float = 0.05,
) -> dict[str, Any]:
    """Two one-sided tests (TOST) for equivalence to zero within +/- bound."""

    if bound <= 0:
        raise ValueError("Equivalence bound must be positive")
    if standard_error <= 0 or not math.isfinite(standard_error):
        return {
            "bound": bound,
            "ci90_low": None,
            "ci90_high": None,
            "p_lower": None,
            "p_upper": None,
            "p_tost": None,
            "q_tost": None,
            "equivalent": False,
        }
    critical = float(student_t.ppf(1.0 - alpha, df))
    ci_low = estimate - critical * standard_error
    ci_high = estimate + critical * standard_error
    statistic_lower = (estimate + bound) / standard_error
    statistic_upper = (estimate - bound) / standard_error
    p_lower = float(student_t.sf(statistic_lower, df))
    p_upper = float(student_t.cdf(statistic_upper, df))
    p_tost = max(p_lower, p_upper)
    return {
        "bound": float(bound),
        "ci90_low": float(ci_low),
        "ci90_high": float(ci_high),
        "p_lower": p_lower,
        "p_upper": p_upper,
        "p_tost": p_tost,
        "q_tost": None,
        "equivalent": bool(p_tost < alpha),
    }


def contrast_statistics(
    fit: Mapping[str, Any],
    contrast: np.ndarray,
    alpha: float = 0.05,
    equivalence_bound: float | None = None,
) -> dict[str, Any]:
    """Calculate raw and Hedges-standardized statistics for one contrast."""

    beta = np.asarray(fit["beta"], dtype=float)
    covariance = np.asarray(fit["covariance"], dtype=float)
    vector = _padded_contrast(contrast, len(beta))
    estimate = float(vector @ beta)
    variance = max(0.0, float(vector @ covariance @ vector))
    standard_error = math.sqrt(variance)
    inference_df = int(fit["inference_df"])
    critical = float(student_t.ppf(1.0 - alpha / 2.0, inference_df))
    statistic = estimate / standard_error if standard_error > 0 else float("nan")
    p_value = (
        float(2.0 * student_t.sf(abs(statistic), inference_df))
        if math.isfinite(statistic)
        else (0.0 if estimate else 1.0)
    )
    raw = {
        "estimate": estimate,
        "se": standard_error,
        "ci_low": estimate - critical * standard_error,
        "ci_high": estimate + critical * standard_error,
        "t": statistic if math.isfinite(statistic) else None,
        "df": inference_df,
        "p": p_value,
        "q": None,
    }

    residual_sd = float(fit["residual_sd"])
    correction = hedges_correction(int(fit["df_residual"]))
    if residual_sd > 1e-14 and math.isfinite(correction):
        standardized_estimate = correction * estimate / residual_sd
        # Delta approximation includes uncertainty from the estimated residual
        # scale. This is documented in the output for downstream meta-analysis.
        standardized_variance = (
            correction**2 * variance / residual_sd**2
            + standardized_estimate**2 / (2.0 * int(fit["df_residual"]))
        )
        standardized_se = math.sqrt(max(0.0, standardized_variance))
        standardized = {
            "estimate": standardized_estimate,
            "se": standardized_se,
            "ci_low": standardized_estimate - critical * standardized_se,
            "ci_high": standardized_estimate + critical * standardized_se,
            "hedges_j": correction,
            "method": (
                "model residual SD; Hedges J; approximate delta-method SE "
                "with residual-scale independence approximation"
            ),
        }
    else:
        standardized = {
            "estimate": None,
            "se": None,
            "ci_low": None,
            "ci_high": None,
            "hedges_j": correction if math.isfinite(correction) else None,
            "method": "not estimable because residual SD is degenerate",
        }

    result: dict[str, Any] = {"raw": raw, "standardized": standardized}
    if equivalence_bound is not None:
        if standardized["estimate"] is None:
            result["equivalence"] = {
                "bound": equivalence_bound,
                "ci90_low": None,
                "ci90_high": None,
                "p_lower": None,
                "p_upper": None,
                "p_tost": None,
                "q_tost": None,
                "equivalent": False,
            }
        else:
            result["equivalence"] = equivalence_test(
                float(standardized["estimate"]),
                float(standardized["se"]),
                inference_df,
                equivalence_bound,
                alpha=alpha,
            )
    return result


def analyze_outcome(
    rows: Sequence[Mapping[str, Any]],
    values: Sequence[float],
    weighting: str = "sample",
    alpha: float = 0.05,
    equivalence_bound: float = 0.2,
    clusters: Sequence[Any] | None = None,
    covariates: np.ndarray | None = None,
    covariate_names: Sequence[str] | None = None,
) -> dict[str, Any]:
    """Fit one scalar feature and return all PDF factorial contrasts."""

    if covariates is None:
        covariate_width = 0
    else:
        candidate_covariates = np.asarray(covariates)
        covariate_width = 1 if candidate_covariates.ndim == 1 else candidate_covariates.shape[1]
    if covariate_names is not None and len(covariate_names) != covariate_width:
        raise ValueError("Covariate names do not match the additional covariate columns")
    x, weights, strata, baseline = design_matrix(
        rows, weighting=weighting, covariates=covariates
    )
    y = np.asarray(values, dtype=float)
    fit = fit_factorial(x, y, weights=weights, clusters=clusters)
    contrasts = {}
    for name, contrast in ALL_CONTRASTS.items():
        contrasts[name] = contrast_statistics(
            fit,
            contrast,
            alpha=alpha,
            equivalence_bound=equivalence_bound if name in MAIN_EFFECTS else None,
        )

    raw_cell_summary = {}
    for group in GROUPS:
        cell = y[np.asarray([row["group"] == group for row in rows])]
        raw_cell_summary[group] = {
            "n": int(len(cell)),
            "mean": float(np.mean(cell)),
            "sd": float(np.std(cell, ddof=1)) if len(cell) > 1 else None,
            "median": float(np.median(cell)),
            "q25": float(np.quantile(cell, 0.25)),
            "q75": float(np.quantile(cell, 0.75)),
        }

    # Least-squares cell means average all included strata equally. They are
    # intended for interaction plots; factorial contrasts remain authoritative.
    adjusted_means = {}
    for group in GROUPS:
        generation, phishing = effect_codes(group)
        reference = np.asarray(
            [
                1.0,
                generation,
                phishing,
                generation * phishing,
                *([1.0 / len(strata)] * (len(strata) - 1)),
                *([0.0] * covariate_width),
            ],
            dtype=float,
        )
        adjusted_means[group] = float(reference @ fit["beta"])

    diagnostics = {
        "minimum": float(np.min(y)),
        "maximum": float(np.max(y)),
        "mean": float(np.mean(y)),
        "sd": float(np.std(y, ddof=1)),
        "zero_fraction": float(np.mean(y == 0)),
        "unique_values": int(len(np.unique(y))),
        "n": int(len(y)),
    }
    return {
        "weighting": weighting,
        "n": int(fit["n"]),
        "n_strata": len(strata),
        "strata": strata,
        "baseline_stratum": baseline,
        "additional_covariates": list(covariate_names or []),
        "df_residual": int(fit["df_residual"]),
        "inference_df": int(fit["inference_df"]),
        "residual_sd": float(fit["residual_sd"]),
        "covariance_method": fit["covariance_method"],
        "cluster_count": fit["cluster_count"],
        "condition_number": float(fit["condition_number"]),
        "max_leverage": float(fit["max_leverage"]),
        "high_leverage_threshold": float(fit["high_leverage_threshold"]),
        "high_leverage_count": int(fit["high_leverage_count"]),
        "raw_cell_summary": raw_cell_summary,
        "adjusted_means": adjusted_means,
        "diagnostics": diagnostics,
        "contrasts": contrasts,
        "warnings": list(fit["warnings"]),
    }


def benjamini_hochberg(p_values: Sequence[float | None]) -> list[float | None]:
    """Benjamini-Hochberg FDR adjustment, preserving missing positions."""

    adjusted: list[float | None] = [None] * len(p_values)
    valid = sorted(
        (float(value), index)
        for index, value in enumerate(p_values)
        if value is not None and math.isfinite(float(value))
    )
    running = 1.0
    for rank, (value, index) in reversed(list(enumerate(valid, 1))):
        running = min(running, value * len(valid) / rank)
        adjusted[index] = min(1.0, running)
    return adjusted


def classify_feature(
    contrasts: Mapping[str, Mapping[str, Any]],
    alpha: float = 0.05,
    minimum_effect: float = 0.2,
) -> str:
    """Convenience taxonomy; estimates and uncertainty remain authoritative."""

    def supported(name: str) -> bool:
        effect = contrasts[name]
        estimate = effect["standardized"]["estimate"]
        q_value = effect["raw"].get("q")
        return (
            estimate is not None
            and q_value is not None
            and q_value < alpha
            and abs(float(estimate)) >= minimum_effect
        )

    def equivalent(name: str) -> bool:
        equivalence = contrasts[name].get("equivalence", {})
        q_value = equivalence.get("q_tost")
        return q_value is not None and q_value < alpha

    interaction = contrasts["I"]["standardized"]["estimate"]
    interaction_q = contrasts["I"]["raw"].get("q")
    interaction_detected = bool(
        interaction is not None
        and interaction_q is not None
        and interaction_q < alpha
    )
    if interaction_detected and abs(float(interaction)) >= minimum_effect:
        return "interaction_dependent"
    if equivalent("I"):
        generation = supported("G")
        phishing = supported("P")
        if generation and phishing:
            return "stable_dual"
        if generation:
            return "stable_generation"
        if phishing:
            return "stable_phishing"
        if equivalent("G") and equivalent("P"):
            return "uninformative_within_bounds"
        return "no_supported_stable_main_effect"
    if interaction_detected:
        return "detectable_but_small_interaction"
    return "inconclusive_interaction"


def paule_mandel_tau2(effects: np.ndarray, variances: np.ndarray) -> float:
    """Estimate random-effects variance with the Paule-Mandel equation."""

    effects = np.asarray(effects, dtype=float)
    variances = np.asarray(variances, dtype=float)
    if len(effects) < 2:
        return 0.0

    def generalized_q(tau2: float) -> float:
        weights = 1.0 / (variances + tau2)
        mean = float(np.sum(weights * effects) / np.sum(weights))
        return float(np.sum(weights * (effects - mean) ** 2))

    target = len(effects) - 1.0
    if generalized_q(0.0) <= target:
        return 0.0
    upper = max(float(np.var(effects, ddof=1)), float(np.max(variances)), 1e-8)
    while generalized_q(upper) > target and upper < 1e12:
        upper *= 2.0
    return float(brentq(lambda value: generalized_q(value) - target, 0.0, upper))


def _clopper_pearson(successes: int, total: int, alpha: float) -> tuple[float, float]:
    if total <= 0:
        return float("nan"), float("nan")
    low = (
        0.0
        if successes == 0
        else float(beta_distribution.ppf(alpha / 2.0, successes, total - successes + 1))
    )
    high = (
        1.0
        if successes == total
        else float(beta_distribution.ppf(1.0 - alpha / 2.0, successes + 1, total - successes))
    )
    return low, high


def random_effects_summary(
    effects: Sequence[float],
    standard_errors: Sequence[float],
    labels: Sequence[str] | None = None,
    alpha: float = 0.05,
    neutral_bound: float = 0.0,
    equivalence_bound: float = 0.2,
    include_lodo: bool = True,
) -> dict[str, Any]:
    """Paule-Mandel random-effects meta-analysis and stability diagnostics."""

    y = np.asarray(effects, dtype=float)
    se = np.asarray(standard_errors, dtype=float)
    if y.shape != se.shape or y.ndim != 1:
        raise ValueError("Effects and standard errors must be one-dimensional peers")
    valid = np.isfinite(y) & np.isfinite(se) & (se > 0)
    y, se = y[valid], se[valid]
    if labels is None:
        study_labels = [str(index) for index in range(len(valid))]
    else:
        study_labels = [str(label) for label, keep in zip(labels, valid) if keep]
    k = len(y)
    if k == 0:
        raise ValueError("No finite effect/standard-error pairs")
    variances = se**2

    fixed_weights = 1.0 / variances
    fixed_mean = float(np.sum(fixed_weights * y) / np.sum(fixed_weights))
    q_statistic = float(np.sum(fixed_weights * (y - fixed_mean) ** 2))
    q_df = k - 1
    q_p = float(chi2.sf(q_statistic, q_df)) if q_df > 0 else None
    i2 = (
        max(0.0, (q_statistic - q_df) / q_statistic) * 100.0
        if q_statistic > 0 and q_df > 0
        else 0.0
    )
    tau2 = paule_mandel_tau2(y, variances) if k > 1 else 0.0
    random_weights = 1.0 / (variances + tau2)
    pooled = float(np.sum(random_weights * y) / np.sum(random_weights))

    warnings = []
    if k == 1:
        pooled_se = float(se[0])
        inference_df = None
        critical = float(norm.ppf(1.0 - alpha / 2.0))
        pooled_p = float(2.0 * norm.sf(abs(pooled / pooled_se)))
        warnings.append("One dataset: heterogeneity and transferability are not estimable")
    else:
        hk_scale = max(
            1.0,
            float(np.sum(random_weights * (y - pooled) ** 2) / (k - 1.0)),
        )
        pooled_se = math.sqrt(hk_scale / float(np.sum(random_weights)))
        inference_df = k - 1
        critical = float(student_t.ppf(1.0 - alpha / 2.0, inference_df))
        pooled_p = float(2.0 * student_t.sf(abs(pooled / pooled_se), inference_df))
        if k < 5:
            warnings.append(
                f"Only {k} independent datasets; heterogeneity estimates are unstable"
            )
    ci_low = pooled - critical * pooled_se
    ci_high = pooled + critical * pooled_se

    if k >= 3:
        prediction_critical = float(student_t.ppf(1.0 - alpha / 2.0, k - 2))
        prediction_half_width = prediction_critical * math.sqrt(tau2 + pooled_se**2)
        prediction_low = pooled - prediction_half_width
        prediction_high = pooled + prediction_half_width
    else:
        prediction_low = prediction_high = None
        warnings.append("Prediction interval requires at least three independent datasets")

    positive = y > neutral_bound
    negative = y < -neutral_bound
    neutral = ~(positive | negative)
    n_positive, n_negative, n_neutral = map(
        int, (np.sum(positive), np.sum(negative), np.sum(neutral))
    )
    nonneutral = n_positive + n_negative
    dominant_positive = n_positive >= n_negative
    dominant_count = max(n_positive, n_negative)
    sign_consistency = dominant_count / nonneutral if nonneutral else None
    sign_low, sign_high = _clopper_pearson(dominant_count, nonneutral, alpha)
    dominant_mask = positive if dominant_positive else negative
    nonneutral_weight = float(np.sum(random_weights[positive | negative]))
    weighted_consistency = (
        float(np.sum(random_weights[dominant_mask]) / nonneutral_weight)
        if nonneutral_weight > 0
        else None
    )

    equivalence = equivalence_test(
        pooled,
        pooled_se,
        inference_df if inference_df is not None else 10**9,
        equivalence_bound,
        alpha=alpha,
    )
    equivalence["prediction_interval_inside_bounds"] = bool(
        prediction_low is not None
        and prediction_low > -equivalence_bound
        and prediction_high < equivalence_bound
    )

    lodo = None
    if include_lodo and k >= 3:
        omitted = []
        for index, label in enumerate(study_labels):
            mask = np.ones(k, dtype=bool)
            mask[index] = False
            summary = random_effects_summary(
                y[mask],
                se[mask],
                [item for pos, item in enumerate(study_labels) if pos != index],
                alpha=alpha,
                neutral_bound=neutral_bound,
                equivalence_bound=equivalence_bound,
                include_lodo=False,
            )
            omitted.append({"omitted": label, "pooled": summary["pooled"]})
        estimates = [item["pooled"] for item in omitted]
        lodo = {
            "estimates": omitted,
            "minimum": float(min(estimates)),
            "maximum": float(max(estimates)),
            "max_absolute_change": float(max(abs(value - pooled) for value in estimates)),
            "all_same_sign": bool(
                all(value > 0 for value in estimates)
                or all(value < 0 for value in estimates)
            ),
        }

    return {
        "k": k,
        "datasets": study_labels,
        "effects": y.tolist(),
        "standard_errors": se.tolist(),
        "pooled": pooled,
        "pooled_se": pooled_se,
        "ci_low": float(ci_low),
        "ci_high": float(ci_high),
        "p": pooled_p,
        "q": None,
        "inference_df": inference_df,
        "tau2": tau2,
        "tau": math.sqrt(tau2),
        "heterogeneity_Q": q_statistic if k > 1 else None,
        "heterogeneity_Q_df": q_df if k > 1 else None,
        "heterogeneity_Q_p": q_p,
        "I2": i2 if k > 1 else None,
        "prediction_low": prediction_low,
        "prediction_high": prediction_high,
        "prediction_excludes_zero": bool(
            prediction_low is not None
            and (prediction_low > 0 or prediction_high < 0)
        ),
        "median": float(np.median(y)),
        "q25": float(np.quantile(y, 0.25)),
        "q75": float(np.quantile(y, 0.75)),
        "minimum": float(np.min(y)),
        "maximum": float(np.max(y)),
        "n_positive": n_positive,
        "n_negative": n_negative,
        "n_neutral": n_neutral,
        "dominant_direction": "positive" if dominant_positive else "negative",
        "sign_consistency": sign_consistency,
        "sign_consistency_ci_low": None if math.isnan(sign_low) else sign_low,
        "sign_consistency_ci_high": None if math.isnan(sign_high) else sign_high,
        "weighted_sign_consistency": weighted_consistency,
        "equivalence": equivalence,
        "leave_one_dataset_out": lodo,
        "warnings": warnings,
    }


def json_safe(value: Any) -> Any:
    """Recursively convert NumPy values and non-finite floats for strict JSON."""

    if isinstance(value, Mapping):
        return {str(key): json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, np.ndarray)):
        return [json_safe(item) for item in value]
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        value = float(value)
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value
