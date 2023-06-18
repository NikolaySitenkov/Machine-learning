import numpy as np
import pandas as pd

from sklearn.tree import DecisionTreeRegressor


class GradientBoostingRegressor:
    def __init__(
        self,
        n_estimators=100,
        learning_rate=0.1,
        max_depth=3,
        min_samples_split=2,
        loss="mse",
        verbose=False,
        subsample_size=0.5,
        replace=False
    ):
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.loss = loss
        if loss == "mse":
            self.loss = self._mse
        self.verbose = verbose
        self.subsample_size = subsample_size
        self.replace = replace
        self.base_pred_ = 0
        self.trees_ = []

    def _mse(self, y_true, y_pred):
        """Calculating the mse"""

        loss = np.mean((y_pred - y_true) ** 2) ** 0.5
        grad = y_pred - y_true

        return loss, grad

    def _subsample(self, X, y):
        """Select a subsample"""

        idxs = np.arange(y.shape[0])
        s_size = int(y.shape[0] * self.subsample_size)
        s_idxs = np.random.choice(idxs, s_size, replace=self.replace)

        sub_X = X[s_idxs, :]
        sub_y = y[s_idxs]

        return sub_X, sub_y

    def fit(self, X, y):
        """
        Fit the model to the data.

        Args:
            X: array-like of shape (n_samples, n_features)
            y: array-like of shape (n_samples,)

        Returns:
            GradientBoostingRegressor: The fitted model.
        """

        self.base_pred_ = np.mean(y)
        s_size = int(y.shape[0] * self.subsample_size)
        preds = np.ones(y.shape[0]) * self.base_pred_
        sub_preds = np.ones(s_size) * self.base_pred_

        for i in range(self.n_estimators):

            loss, grad = self.loss(y, preds)

            if self.verbose:
                print(f"{i}: {loss}")

            regressor = DecisionTreeRegressor(random_state=0,
                                              max_depth=self.max_depth,
                                              min_samples_split=self.min_samples_split)

            sub_X, sub_grad = self._subsample(X, -grad)
            regressor.fit(sub_X, sub_grad)
            self.trees_.append(regressor)

            residuals = regressor.predict(X)

            preds += self.learning_rate * residuals

    def predict(self, X):
        """Predict the target of new data.

        Args:
            X: array-like of shape (n_samples, n_features)

        Returns:
            y: array-like of shape (n_samples,)
            The predict values.

        """

        predictions = np.ones(X.shape[0]) * self.base_pred_
        for tree in self.trees_:
            predictions += self.learning_rate * tree.predict(X)

        return predictions
