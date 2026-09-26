"""Principal Component Analysis on the quantitative variables."""
from types import SimpleNamespace

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from .data import QUANTITATIVE_VARS


def run_pca(df, variables=QUANTITATIVE_VARS):
    """Standardizes `variables`, fits a full PCA (for the scree/cumulative
    variance plots) and a 2-component PCA (for the 2D projection).

    Returns a namespace with everything the plotting functions need:
    X_scaled, explained_var, cumulative_var, n_90 (components for 90%
    variance), pca_2d, X_pca_2d, components_df (loadings).
    """
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[variables])

    pca_full = PCA()
    pca_full.fit(X_scaled)
    explained_var = pca_full.explained_variance_ratio_
    cumulative_var = np.cumsum(explained_var)
    n_90 = int(np.argmax(cumulative_var >= 0.90) + 1)

    pca_2d = PCA(n_components=2)
    X_pca_2d = pca_2d.fit_transform(X_scaled)
    components_df = pd.DataFrame(pca_2d.components_.T, columns=['PC1', 'PC2'], index=variables)

    return SimpleNamespace(
        X_scaled=X_scaled,
        explained_var=explained_var,
        cumulative_var=cumulative_var,
        n_90=n_90,
        pca_2d=pca_2d,
        X_pca_2d=X_pca_2d,
        components_df=components_df,
    )
