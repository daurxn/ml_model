from __future__ import annotations

from typing import List

import numpy as np
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


class ModelService:
    def __init__(self, random_state: int = 42) -> None:
        data = load_iris()
        X, y = data.data, data.target
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=random_state, stratify=y
        )
        self.model = RandomForestClassifier(n_estimators=200, random_state=random_state)
        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)
        self._accuracy = float(accuracy_score(y_test, y_pred))
        self.target_names = data.target_names.tolist()

    @property
    def accuracy(self) -> float:
        return self._accuracy

    def predict(self, features: List[float]) -> dict:
        x = np.array(features, dtype=float).reshape(1, -1)
        pred = int(self.model.predict(x)[0])
        label = self.target_names[pred]
        return {"class_index": pred, "class_label": label}
