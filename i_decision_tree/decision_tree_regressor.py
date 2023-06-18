from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class Node:
    """Decision tree node."""
    feature: int = None
    threshold: float = None
    n_samples: int = None
    value: int = None
    mse: float = None
    left: Node = None
    right: Node = None


@dataclass
class DecisionTreeRegressor:
    """Decision tree regressor."""
    max_depth: int
    min_samples_split: int = 2

    def fit(self, X: np.ndarray, y: np.ndarray) -> DecisionTreeRegressor:
        """Build a decision tree regressor from the training set (X, y)."""
        self.n_features_ = X.shape[1]
        self.tree_ = self._split_node(X, y)
        return self

    def _mse(self, y: np.ndarray) -> float:
        """Compute the mse criterion for a given set of target values."""
        return np.mean((y - y.mean()) ** 2)

    def _weighted_mse(self, y_left: np.ndarray, y_right: np.ndarray) -> float:
        """Compute the weithed mse criterion for a two given sets of target values"""
        sum_lr = self._mse(y_left) * y_left.shape[0] + self._mse(y_right) * y_right.shape[0]
        cnt_lr = y_left.shape[0] + y_right.shape[0]
        return sum_lr / cnt_lr

    def _split(self, X: np.ndarray, y: np.ndarray, feature: int) -> float:
        """Find the best split for a node (one feature)"""

        x_vec_unique = np.unique(X[:, feature])
        x_vec = X[:, feature]
        best_mse = self._mse(y)
        best_threshold = x_vec_unique[0]

        for thr in x_vec_unique[1:]:
            x_left, x_right = x_vec[x_vec <= thr], x_vec[x_vec > thr]
            y_left, y_right = y[x_vec <= thr], y[x_vec > thr]

            if y_left.shape[0] == 0 or y_right.shape[0] == 0:
                continue

            cur_mse = self._weighted_mse(y_left, y_right)
            if best_mse > cur_mse:
                best_threshold = thr
                best_mse = cur_mse

        return best_threshold, best_mse

    def _best_split(self, X: np.ndarray, y: np.ndarray) -> tuple[int, float]:
        """Find the best split for a node."""
        num_features = X.shape[1]
        best_idx = 0
        best_thr, best_mse = self._split(X, y, 0)

        for i in range(1, num_features):
            cur_threshold, cur_mse = self._split(X, y, i)
            if best_mse > cur_mse:
                best_mse = cur_mse
                best_idx = i
                best_thr = cur_threshold

        return best_idx, best_thr

    def _split_node(self, X: np.ndarray, y: np.ndarray, depth: int = 0) -> Node:
        """Split a node and return the resulting left and right child nodes."""

        n_sm = y.shape[0]

        node = Node(n_samples=n_sm,
                    mse=self._mse(y),
                    value=round(np.mean(y)))

        if depth < self.max_depth and n_sm >= self.min_samples_split:

            node.feature, node.threshold = self._best_split(X, y)
            left_mask = X[:, node.feature] <= node.threshold
            right_mask = X[:, node.feature] > node.threshold
            node.left = self._split_node(X[left_mask], y[left_mask], depth + 1)
            node.right = self._split_node(X[right_mask], y[right_mask], depth + 1)

        return node

    def as_json(self) -> str:
        """Return the decision tree as a JSON string."""

        dict_tree = dict()

        if self.tree_.feature is not None:
            dict_tree["feature"] = self.tree_.feature
        if self.tree_.threshold is not None:
            dict_tree["threshold"] = round(self.tree_.threshold, 2)
        dict_tree["n_samples"] = self.tree_.n_samples
        dict_tree["mse"] = round(self.tree_.mse, 2)
        dict_tree["left"] = self._as_json(self.tree_.left)
        dict_tree["right"] = self._as_json(self.tree_.right)

        return str(dict_tree).replace("'", '"')

    def _as_json(self, node: Node) -> dict:
        """Return the decision tree as a JSON string. Execute recursively."""

        dict_tree = dict()

        if node.feature is not None:
            dict_tree["feature"] = node.feature
        if node.threshold is not None:
            dict_tree["threshold"] = round(node.threshold, 2)
        dict_tree["n_samples"] = node.n_samples
        dict_tree["mse"] = round(node.mse, 2)

        if node.left is not None:
            dict_tree["left"] = self._as_json(node.left)
        else:
            dict_tree["value"] = node.value

        if node.right is not None:
            dict_tree["right"] = self._as_json(node.right)
        else:
            dict_tree["value"] = node.value

        return dict_tree

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict regression target for X.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            The input samples.

        Returns
        -------
        y : array of shape (n_samples,)
            The predicted values.
        """

        res = np.array([self._predict_one_sample(i) for i in X])

        return res

    def _predict_one_sample(self, features: np.ndarray) -> int:
        """Predict the target value of a single sample."""

        tree = self.tree_

        while tree.right:
            if features[tree.feature] > tree.threshold:
                tree = tree.right
            else:
                tree = tree.left

        return tree.value
