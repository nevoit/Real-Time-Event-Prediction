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
