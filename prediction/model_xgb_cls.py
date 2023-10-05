from sklearn.ensemble import GradientBoostingClassifier
from xgboost import XGBClassifier

from prediction.model_const_cls import ConstCls


class XGBCls:
    def __init__(self):
        self._cls = GradientBoostingClassifier()
        self.const_val = None

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
            single_class = unique_values[0]
            self.const_val = ConstCls(cons_val=single_class)
        else:
            self._cls.fit(X, y)

    def predict_proba(self, inst):
        # This function returns the probability for observing the event of interest
        if self.const_val is not None:
            return self.const_val.predict_proba()
        else:
            return self._cls.predict_proba(inst)[:, 1][0]
