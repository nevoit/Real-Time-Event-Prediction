import numpy as np
import pandas as pd

from core_comp.tirp import TIRP
from tirp_prefixes.tirp_prefix_insts import TIRPPrefixInstances


class TIRPCompletionInstances:
    def __init__(self, tirp):
        self.tirp: TIRP = tirp
        self._tirp_prefixes_instances_w_event = {}
        self._tirp_prefixes_instances_wo_event = {}
        self.event_occr_time = None
        self.feature_matrices = {}
        self.support = {}

    def add_tirp_prefix_w_event(self, tirp_prefix_id: int, tirp_prefix_insts: TIRPPrefixInstances):
        self._add_tirp_prefix(tirp_prefix_id, tirp_prefix_insts, w_event=True)

    def add_tirp_prefix_wo_event(self, tirp_prefix_id: int, tirp_prefix_insts: TIRPPrefixInstances):
        self._add_tirp_prefix(tirp_prefix_id, tirp_prefix_insts, w_event=False)

    def _add_tirp_prefix(self, tirp_prefix_id: int, tirp_prefix_insts: TIRPPrefixInstances, w_event: bool):
        if w_event:
            dict_ref = self._tirp_prefixes_instances_w_event
        else:
            dict_ref = self._tirp_prefixes_instances_wo_event

        dict_ref[tirp_prefix_id] = tirp_prefix_insts

    def _generate_feature_matrix(self, tirp_prefix_id):
        # This function generates the feature matrix for a specific TIRP-prefix by its index
        feature_dict = {i: [] for i in range(tirp_prefix_id)}
        feature_dict['index'] = []
        feature_dict['class'] = []
        feature_dict['tte'] = []

        inst_w_dict: dict = self._tirp_prefixes_instances_w_event[tirp_prefix_id].get_instances()
        for s_id, s_val in inst_w_dict.items():
            occr_time = self.event_occr_time[s_val.get_entity_id()]
            self._add_inst_to_dict(inst_index=s_id, inst=s_val, feature_dict=feature_dict,
                                   class_val=1, occur_time=occr_time)

        inst_wo_dict: dict = self._tirp_prefixes_instances_wo_event[tirp_prefix_id].get_instances()
        for s_id, s_val in inst_wo_dict.items():
            occr_time = -1
            self._add_inst_to_dict(inst_index=s_id, inst=s_val, feature_dict=feature_dict,
                                   class_val=0, occur_time=occr_time)

        df_feature_matrix = pd.DataFrame.from_dict(feature_dict)
        df_feature_matrix = df_feature_matrix.set_index('index')
        self.feature_matrices[tirp_prefix_id] = df_feature_matrix

    def _add_inst_to_dict(self, inst_index, inst, feature_dict, class_val, occur_time):
        # This function adds the instance into the provided dictionary
        dur_list = inst.get_durations_between_all_tieps()
        prev_dur = dur_list[:-1]

        i = len(dur_list) - 1
        d = dur_list[-1]
        inst_end_time = inst.get_last_time_point_time()
        tte_first = occur_time - inst_end_time + d
        for j in range(1, d + 1):
            feature_dict['index'].append(f'{inst_index}_{j}')

            if len(prev_dur) > 0:  # previous durations also should be added
                for k, k_dur in enumerate(prev_dur):
                    feature_dict[k].append(k_dur)

            feature_dict[i].append(j)  # add the current duration

            for q in range(i + 1, len(dur_list)):  # next duration should be zero
                feature_dict[q].append(0)

            feature_dict['class'].append(class_val)
            if occur_time == -1:  # for entities without event
                feature_dict['tte'].append(np.nan)
            else:  # for entities with the event
                feature_dict['tte'].append(tte_first - j + 1)

    def compute_prob(self):
        num_of_prefixes = len(self._tirp_prefixes_instances_w_event)
        sup_q = len(self._tirp_prefixes_instances_w_event[num_of_prefixes - 1].get_instances())
        for i in range(num_of_prefixes):
            sup_i = len(self._tirp_prefixes_instances_w_event[i].get_instances()) \
                    + len(self._tirp_prefixes_instances_wo_event[i].get_instances())
            self.support[i] = sup_q / sup_i

    def generate_feature_matrices(self, event_occr_time):
        # This function returns feature matrix for each TIRP prefix
        self.event_occr_time = event_occr_time
        for i in range(1, self.tirp.get_tieps_num() - 1):
            # The first feature matrix is not relevant as it contains not duration
            self._generate_feature_matrix(tirp_prefix_id=i)

    def get_feature_matrices(self):
        return self.feature_matrices

    def get_prefixes_support(self):
        return self.support
