"""Predicting fuel consumption: single-feature polynomial regression and a
multi-feature linear baseline for comparison."""
from types import SimpleNamespace

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures


def polynomial_regression_comparison(df, degrees=(1, 2, 3), feature='weight_lbs',
                                      target='miles_per_gallon', test_size=0.2, random_state=42):
    """Fits a polynomial regression of `target` on `feature` for each degree
    and compares them on held-out R² and RMSE.
    """
    X = df[[feature]].values
    y = df[target].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    results = []
    fits = {}

    for degree in degrees:
        poly = PolynomialFeatures(degree=degree)
        X_train_poly = poly.fit_transform(X_train)
        X_test_poly = poly.transform(X_test)

        model = LinearRegression()
        model.fit(X_train_poly, y_train)
        y_pred_test = model.predict(X_test_poly)

        r2 = r2_score(y_test, y_pred_test)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))

        results.append({'Degree': degree, 'R^2 Test': r2, 'RMSE': rmse})
        fits[degree] = (poly, model)

    return SimpleNamespace(
        X=X, y=y,
        X_train=X_train, X_test=X_test, y_train=y_train, y_test=y_test,
        results_df=pd.DataFrame(results),
        fits=fits,
    )


def multiple_regression(df, features, target='miles_per_gallon', test_size=0.2, random_state=42):
    """Linear regression on several features at once, as a comparison point
    against the single-feature polynomial fits."""
    X = df[features].values
    y = df[target].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    return SimpleNamespace(
        model=model,
        r2=r2_score(y_test, y_pred),
        rmse=np.sqrt(mean_squared_error(y_test, y_pred)),
    )
