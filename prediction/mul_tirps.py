from pred_at_time import PredAtTime


class MulTIRPs:
    def __init__(self, current_time: int, pred_prob_time_per_tc: dict, agg_func):
        self.current_time: int = current_time
        self._pred_prob_time_per_tc = pred_prob_time_per_tc
        self.agg_func: str = agg_func

        self._pred_prob: list = []
        self._est_tte: list = []
        self._weights: list = []

        self._create_prob_time_lists()

    def agg_values(self) -> PredAtTime:
        self._create_weights_list()
        # weighted average = \sum_{i=1}^n (w_i * x_i) / \sum_{i=1}^n (w_i)
        pred_prob = 0
        est_tte = 0
        if len(self._pred_prob) > 0 and len(self._est_tte):
            pred_prob = sum([p * w for p, w in zip(self._pred_prob, self._weights)]) / sum(self._weights)
            est_tte = sum([t * w for t, w in zip(self._est_tte, self._weights)]) / sum(self._weights)
        return PredAtTime(curr_time=self.current_time, pred_prob=pred_prob, est_tte=est_tte)

    def _create_prob_time_lists(self):
        for tirp_str, tirp in self._pred_prob_time_per_tc.items():
            for tirp_inedx, tirp_prefix in tirp.items():
                for inst in tirp_prefix:
                    self._pred_prob.append(inst.get_pred_prob())
                    self._est_tte.append(inst.get_est_tte())

    def _create_weights_list(self):
        for tirp_str, tirp in self._pred_prob_time_per_tc.items():
            for tirp_inedx, tirp_prefix in tirp.items():
                for inst in tirp_prefix:
                    self._weights.append(1)
