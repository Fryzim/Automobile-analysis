"""All plotting functions used in the analysis notebook."""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from .data import QUANTITATIVE_VARS

plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


def plot_distributions(df, variables=QUANTITATIVE_VARS):
    """Histogram per variable, with mean/median markers."""
    fig, axes = plt.subplots(3, 3, figsize=(16, 12))
    fig.suptitle('Variable Distributions', fontsize=16, fontweight='bold')

    for idx, var in enumerate(variables):
        row, col = idx // 3, idx % 3
        ax = axes[row, col]
        ax.hist(df[var], bins=30, alpha=0.7, edgecolor='black', color='steelblue')
        mean_val = df[var].mean()
        median_val = df[var].median()
        ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_val:.1f}')
        ax.axvline(median_val, color='green', linestyle='--', linewidth=2, label=f'Median: {median_val:.1f}')
        ax.set_xlabel(var.replace('_', ' ').title())
        ax.set_ylabel('Frequency')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

    for idx in range(len(variables), 9):
        fig.delaxes(axes[idx // 3, idx % 3])
    plt.tight_layout()
    plt.show()


def plot_origin_comparison(df, variables=('miles_per_gallon', 'horsepower', 'weight_lbs',
                                           'acceleration', 'displacement', 'cylinders')):
    """Bar chart of each variable's average, grouped by origin country."""
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    fig.suptitle('Average Characteristics by Origin', fontsize=16, fontweight='bold')

    for idx, var in enumerate(variables):
        row, col = idx // 3, idx % 3
        ax = axes[row, col]

        means = df.groupby('origin_name')[var].mean()
        means.plot(kind='bar', ax=ax, color=['red', 'blue', 'green'], alpha=0.7, edgecolor='black')
        ax.set_title(var.replace('_', ' ').title(), fontweight='bold')
        ax.set_xlabel('Origin')
        ax.set_ylabel('Average')
        ax.grid(True, alpha=0.3, axis='y')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

    plt.tight_layout()
    plt.show()


def plot_correlation_heatmap(df, variables=QUANTITATIVE_VARS):
    """Correlation matrix heatmap, and MPG's correlation with every other variable."""
    plt.figure(figsize=(10, 8))
    correlation_matrix = df[variables].corr()
    sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm',
                center=0, square=True, linewidths=1)
    plt.title('Correlation Matrix', fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.show()

    mpg_corr = correlation_matrix['miles_per_gallon'].drop('miles_per_gallon').sort_values()
    print("Correlations with MPG:")
    for var, corr in mpg_corr.items():
        print(f"{var:20s}: {corr:+.3f}")


def plot_pairplot(df, key_vars=('miles_per_gallon', 'weight_lbs', 'horsepower', 'displacement')):
    sns.pairplot(df[list(key_vars) + ['origin_name']], hue='origin_name',
                 diag_kind='kde', plot_kws={'alpha': 0.6, 's': 30}, height=2.5)
    plt.suptitle('Relations Between Key Variables', y=1.02, fontsize=14, fontweight='bold')
    plt.show()


def plot_cafe_analysis(df, threshold=24):
    """Three panels: compliance rate by origin, compliance over time, and
    where the threshold sits in the MPG distribution."""
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    cafe_origin = pd.crosstab(df['origin_name'], df['meets_cafe'], normalize='index') * 100
    cafe_origin.plot(kind='bar', ax=axes[0], color=['#ff6b6b', '#51cf66'])
    axes[0].set_title('Compliance by Origin', fontweight='bold')
    axes[0].set_ylabel('Percentage (%)')
    axes[0].legend(['< 24', '>= 24'])
    axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=45)

    cafe_year = df.groupby('model_year')['meets_cafe'].mean() * 100
    axes[1].plot(cafe_year.index + 1900, cafe_year.values, marker='o', linewidth=2.5, markersize=8)
    axes[1].axhline(50, color='red', linestyle='--', linewidth=2, label='50%')
    axes[1].set_title('Temporal Evolution', fontweight='bold')
    axes[1].set_xlabel('Year')
    axes[1].set_ylabel('% >= 24 mpg')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    axes[2].hist(df['miles_per_gallon'], bins=40, alpha=0.7, edgecolor='black')
    axes[2].axvline(threshold, color='red', linestyle='--', linewidth=3, label='CAFE Threshold')
    axes[2].set_title('MPG Distribution', fontweight='bold')
    axes[2].set_xlabel('MPG')
    axes[2].legend()

    plt.tight_layout()
    plt.show()


def plot_pca_scree(pca_result):
    """Per-component variance and cumulative variance, with the 90% line."""
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))

    explained_var = pca_result.explained_var
    cumulative_var = pca_result.cumulative_var

    axes[0].bar(range(1, len(explained_var) + 1), explained_var * 100, alpha=0.7, edgecolor='black')
    axes[0].set_xlabel('Component')
    axes[0].set_ylabel('Variance (%)')
    axes[0].set_title('Scree Plot', fontweight='bold')
    axes[0].grid(True, alpha=0.3, axis='y')

    axes[1].plot(range(1, len(cumulative_var) + 1), cumulative_var * 100, marker='o', linewidth=2.5)
    axes[1].axhline(90, color='red', linestyle='--', linewidth=2, label='90%')
    axes[1].set_xlabel('Number of Components')
    axes[1].set_ylabel('Cumulative Variance (%)')
    axes[1].set_title('Cumulative Variance', fontweight='bold')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


def plot_pca_projection(df, pca_result):
    """2D PCA projection, colored once by MPG and once by origin."""
    pca_2d = pca_result.pca_2d
    X_pca_2d = pca_result.X_pca_2d

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    scatter1 = axes[0].scatter(X_pca_2d[:, 0], X_pca_2d[:, 1], c=df['miles_per_gallon'],
                                cmap='viridis', alpha=0.6, edgecolor='black', s=50)
    axes[0].set_xlabel(f'PC1 ({pca_2d.explained_variance_ratio_[0] * 100:.1f}%)')
    axes[0].set_ylabel(f'PC2 ({pca_2d.explained_variance_ratio_[1] * 100:.1f}%)')
    axes[0].set_title('PCA by MPG', fontweight='bold')
    axes[0].grid(True, alpha=0.3)
    plt.colorbar(scatter1, ax=axes[0], label='MPG')

    colors = {'USA': 'red', 'Europe': 'blue', 'Japan': 'green'}
    for origin, color in colors.items():
        mask = (df['origin_name'] == origin).values
        axes[1].scatter(X_pca_2d[mask, 0], X_pca_2d[mask, 1],
                         label=origin, alpha=0.6, edgecolor='black', s=50, c=color)
    axes[1].set_xlabel(f'PC1 ({pca_2d.explained_variance_ratio_[0] * 100:.1f}%)')
    axes[1].set_ylabel(f'PC2 ({pca_2d.explained_variance_ratio_[1] * 100:.1f}%)')
    axes[1].set_title('PCA by Origin', fontweight='bold')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


def plot_pca_contributions(pca_result):
    """Which original variables load most on PC1 and PC2."""
    components_df = pca_result.components_df
    print("Contributions:")
    print(components_df.round(3))

    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    for i, pc in enumerate(['PC1', 'PC2']):
        components_df[pc].plot(kind='barh', ax=axes[i], color='steelblue', edgecolor='black')
        axes[i].set_title(f'Contributions to {pc}', fontweight='bold')
        axes[i].axvline(0, color='black', linewidth=0.8)
        axes[i].grid(True, alpha=0.3, axis='x')
    plt.tight_layout()
    plt.show()


def plot_regression_curves(reg_result):
    """Test-set scatter plus fitted curve, one panel per polynomial degree."""
    fig, axes = plt.subplots(1, len(reg_result.fits), figsize=(6 * len(reg_result.fits), 5))
    if len(reg_result.fits) == 1:
        axes = [axes]

    X, X_test, y_test = reg_result.X, reg_result.X_test, reg_result.y_test

    for idx, degree in enumerate(sorted(reg_result.fits)):
        ax = axes[idx]
        poly, model = reg_result.fits[degree]

        X_test_poly = poly.transform(X_test)
        y_pred_test = model.predict(X_test_poly)

        X_range = np.linspace(X.min(), X.max(), 200).reshape(-1, 1)
        y_range_pred = model.predict(poly.transform(X_range))

        r2 = reg_result.results_df.set_index('Degree').loc[degree, 'R^2 Test']

        ax.scatter(X_test, y_test, alpha=0.5, s=30, edgecolor='black')
        ax.plot(X_range, y_range_pred, 'r-', linewidth=2)
        ax.set_xlabel('Weight (lbs)')
        ax.set_ylabel('MPG')
        ax.set_title(f'Degree {degree} (R^2={r2:.3f})', fontweight='bold')
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()
