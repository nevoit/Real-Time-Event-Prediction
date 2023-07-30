from mul_tirps import MulTIRPs
from pred_at_time import PredAtTime
from core_comp.sti_series import STISeries
from core_comp.time_point_series import TimePointSeries
from core_comp.tirp import TIRP
from tirp_prefixes.tirp_prefix_entity_insts_at_time import TIRPrefixEntityInstsAtTime
from tirp_prefixes.tirp_prefix_insts import TIRPPrefixInstances


class ContSimulator:
    def __init__(self, tirp_comp_list: list, entity: STISeries):
        self.tirp_comp_list: list = tirp_comp_list
        self.entity: STISeries = entity
        self.entity_id = self.entity.get_series_id()
        self.entity_timestamps: list = self.entity.get_start_to_end_time_timestamp_list()
        self.det_insts = {}
        self.prob_time = {}
        self.agg_pred = {}
        self._detect_tirp_prefixes_in_entity()

    def _detect_tirp_prefixes_in_entity(self):
        # This loop iterates over the entity's relevant symbolic time intervals in their tiep representation
        for tc in self.entity_timestamps:
            time_point_series: TimePointSeries = self.entity.get_time_points_at(until_time=tc)
            self.det_insts[tc] = {}
            for tirp_comp in self.tirp_comp_list:
                tirp: TIRP = tirp_comp.get_tirp()
                tirp_prefixes = tirp_comp.get_tirp_prefixes()
                self.det_insts[tc][tirp.get_tieps_str()] = {}
                for i, tirp_prefix in enumerate(tirp_prefixes):
                    det_insts = TIRPrefixEntityInstsAtTime(entity_id=self.entity_id,
                                                           prefix_index=i,
                                                           tirp_prefix=tirp_prefix,
                                                           time_point_series=time_point_series)
                    self.det_insts[tc][tirp.get_tieps_str()][i] = det_insts

    def predict_proba_plus_time(self, prob_cls_name, time_cls_model):
        # This loop iterates over the entity's detected TIRP prefixes' instances and
        # compute the probabilities ant time to occurrence for each one of them
        for tc in self.entity_timestamps:
            self.prob_time[tc] = {}
            for tirp_comp in self.tirp_comp_list:
                tirp: TIRP = tirp_comp.get_tirp()
                tirp_prefixes = tirp_comp.get_tirp_prefixes()
                self.prob_time[tc][tirp.get_tieps_str()] = {}
                for i, tirp_prefix in enumerate(tirp_prefixes):
                    insts: TIRPPrefixInstances = self.det_insts[tc][tirp.get_tieps_str()][i]
                    self.prob_time[tc][tirp.get_tieps_str()][i] = []
                    if insts.get_num_of_instances() > 0:
                        for _, inst in insts.get_instances().items():
                            pred_prob = tirp_comp.predict_proba(cls_name=prob_cls_name, prefix_index=i, inst=inst,
                                                                current_time=tc)
                            est_tte = tirp_comp.predict_time(reg_name=time_cls_model, prefix_index=i, inst=inst,
                                                             current_time=tc)
                            pred_at_time = PredAtTime(curr_time=tc, pred_prob=pred_prob, est_tte=est_tte)
                            self.prob_time[tc][tirp.get_tieps_str()][i].append(pred_at_time)

    def agg_prob_plus_time(self, agg_func: str):
        # This function aggregates the probabilities and estimated times for each timestamp
        for tc in self.entity_timestamps:
            pred_prob_time_per_tc = self.prob_time[tc]
            mul_tirps = MulTIRPs(current_time=tc, pred_prob_time_per_tc=pred_prob_time_per_tc, agg_func=agg_func)
            self.agg_pred[tc] = mul_tirps.agg_values()

    def get_agg_pred(self):
        return self.agg_pred

    def plot_prediction(self):
        import seaborn as sns
        import pandas as pd
        import matplotlib.pyplot as plt

        df = pd.DataFrame({'Time': list(self.agg_pred.keys()),
                           'Predicted Probability': [v.get_pred_prob() for v in self.agg_pred.values()],
                           'Estimated Time': [t.get_est_tte() for t in self.agg_pred.values()]})

        sns.lineplot(x='Time', y='Predicted Probability',
                     color='r', data=df)
        plt.show()

        sns.lineplot(x='Time', y='Estimated Time',
                     color='g', data=df, )
        plt.show()

        plt.clf()
