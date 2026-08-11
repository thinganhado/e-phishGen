"""Persistence Homology Dimension calculation for an embedding point cloud."""

import numpy as np
from scipy.spatial.distance import cdist


def _prim_tree(distance_matrix, alpha=1.0):
    infinity = np.max(distance_matrix) + 10
    distances = np.ones(distance_matrix.shape[0]) * infinity
    visited = np.zeros(distance_matrix.shape[0], dtype=bool)
    ancestor = -np.ones(distance_matrix.shape[0], dtype=int)
    vertex = 0
    total = 0.0
    for _ in range(distance_matrix.shape[0] - 1):
        visited[vertex] = True
        ancestor[distances > distance_matrix[vertex]] = vertex
        distances = np.minimum(distances, distance_matrix[vertex])
        distances[visited] = infinity
        vertex = np.argmin(distances)
        total += distance_matrix[vertex, ancestor[vertex]] ** alpha
    return total


def phd_intrinsic_dimension(embeddings, alpha=1.0, min_points=40, max_points=512, point_jump=40, reruns=3, samples_per_point=9, seed=None):
    """Estimate intrinsic dimension using the GPTID PHD procedure."""
    points = np.asarray(embeddings, dtype=float)
    if points.ndim != 2:
        raise ValueError("embeddings must have shape [N, D]")
    if points.shape[0] < max_points:
        max_points = points.shape[0]
    test_sizes = list(range(min_points, max_points, point_jump))
    if len(test_sizes) < 2:
        raise ValueError("at least two subsample sizes are required")
    rng = np.random.default_rng(seed)
    slopes = []
    for _ in range(reruns):
        lengths = []
        for size in test_sizes:
            repeat = samples_per_point if points.shape[0] > 2 * size else max(3, samples_per_point - 2)
            values = []
            for _ in range(repeat):
                indices = rng.choice(points.shape[0], size=size, replace=False)
                values.append(_prim_tree(cdist(points[indices], points[indices], metric="euclidean"), alpha))
            lengths.append(np.median(values))
        x, y = np.log(test_sizes), np.log(lengths)
        slopes.append((len(x) * (x * y).sum() - x.sum() * y.sum()) / (len(x) * (x ** 2).sum() - x.sum() ** 2))
    return float(1.0 / (1.0 - np.mean(slopes)))
