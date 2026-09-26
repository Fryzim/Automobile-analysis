# Automobile Dataset Analysis

Analyse exploratoire et modélisation statistique d'un jeu de données de véhicules (consommation, puissance, poids, origine), avec un focus sur la conformité aux normes CAFE (24 mpg) et la prédiction de la consommation par régression.

## Démarche

1. **Nettoyage et statistiques descriptives** : variables quantitatives, répartition par origine géographique.
2. **Visualisations exploratoires** : distributions, comparaisons par origine, matrice de corrélations, pairplot.
3. **Analyse CAFE** : quels véhicules respectent le seuil de 24 mpg, et quelles caractéristiques les distinguent des autres.
4. **ACP** : standardisation, variance expliquée, projection 2D et contribution des variables, pour identifier les axes structurants du dataset.
5. **Régression polynomiale** : prédiction de la consommation, comparaison de plusieurs degrés de polynôme sur R² et erreur quadratique.

## Contenu du dépôt

```
src/
  data.py             chargement + nettoyage (dropna, origine, seuil CAFE)
  pca_analysis.py      standardisation + ACP (variance expliquée, projection 2D, contributions)
  regression.py        régression polynomiale (weight -> mpg) et régression multiple
  visualize.py          toutes les fonctions de graphique utilisées dans le notebook
automobile.ipynb     notebook d'analyse : charge les données, appelle src/, affiche les résultats
report_analysis.pdf  rapport détaillant la méthodologie et les résultats
```

**Remarque :** le fichier `automobiles.csv` n'est pas versionné dans ce dépôt — le notebook s'attend à le trouver à la racine pour tourner de bout en bout.

## Stack

Python — `pandas`, `numpy`, `scikit-learn` (PCA, régression), `matplotlib`, `seaborn`
