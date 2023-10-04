from sklearn.linear_model import GammaRegressor


class GammaReg:
    def __init__(self):
        self._reg = GammaRegressor()

    def fit(self, X, y):
        self._reg.fit(X, y)

    def predict_time(self, inst):
        return self._reg.predict(inst)[0]