"""Maximum-likelihood intrinsic dimension calculation."""


def mle_intrinsic_dimension(embeddings, **kwargs):
    """Run scikit-dimension's MLE estimator on prepared embeddings."""
    try:
        from skdim.id import MLE
    except ImportError as exc:
        raise ImportError("install scikit-dimension to calculate MLE intrinsic dimension") from exc
    return float(MLE(**kwargs).fit_transform(embeddings))
