from sklearn.linear_model import GammaRegressor
from xgboost import XGBClassifier


class TIRPBasedModel:
    def __init__(self, feature_matrices, pref_sup):
        self._feature_matrices = feature_matrices
        self._pref_sup = pref_sup

        self._X = {}
        self._y_class = {}
        self._X_tte = {}
        self._y_tte = {}

        self._prepare_for_learning()  # TODO: shuffle X to be random

    def _prepare_for_learning(self):
        for i in range(1, len(self._feature_matrices) + 1):
            df_i = self._feature_matrices[i]
            self._X[i] = df_i.drop(columns=['class', 'tte'])
            self._y_class[i] = df_i['class']
            self._y_tte[i] = df_i[~df_i['tte'].isnull()]['tte']
            self._X_tte[i] = df_i[~df_i['tte'].isnull()].drop(columns=['class', 'tte'])

    def get_pref_sup(self, prefix_index):
        return self._pref_sup[prefix_index]

    def get_df_for_classification(self, prefix_index):
        return self._X[prefix_index], self._y_class[prefix_index]

    def get_df_for_regression(self, prefix_index):
        return self._X_tte[prefix_index], self._y_tte[prefix_index]


class SCPM:
    def __init__(self, prob):
        self.prob = prob

    def predict_proba(self, inst_row):
        # This function returns the probability for observing the event of interest
        return self.prob


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


class GLM:
    def __init__(self):
        self._reg = GammaRegressor()

    def fit(self, X, y):
        self._reg.fit(X, y)

    def predict_time(self, inst):
        return self._reg.predict(inst)[0]
