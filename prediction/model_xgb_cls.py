from xgboost import XGBClassifier


class XGBCls:
    def __init__(self):
        self._cls = XGBClassifier()
        self._always_one = False
        self._always_zero = False

    def fit(self, X, y):
        """
        This function learns a model
        :param X: the dataframe train
        :param y: the labels
        :return:
        """
        unique_values = y.unique()
        if len(unique_values) == 1:
            # in cases there are one unique value in the labels list
            # it could be occur for example when the patterns found only in entities with the event of interest
            if unique_values[0] == 1:
                self._always_one = True
            elif unique_values[0] == 0:
                self._always_zero = True
        else:
            self._cls.fit(X, y)

    def predict_proba(self, inst):
        # This function returns the probability for observing the event of interest
        if self._always_one:
            return 1
        elif self._always_zero:
            return 0
        else:
            return self._cls.predict_proba(inst)[:, 1][0]
