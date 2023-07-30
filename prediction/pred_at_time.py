class PredAtTime:
    def __init__(self, curr_time, pred_prob, est_tte, decision=None):
        self._curr_time = curr_time
        self._pred_prob = pred_prob
        self._est_tte = est_tte

        self._decision = decision

    def get_curr_time(self):
        return self._curr_time

    def get_pred_prob(self):
        return self._pred_prob

    def get_est_tte(self):
        return self._est_tte

    def get_decision(self):
        return self._decision
