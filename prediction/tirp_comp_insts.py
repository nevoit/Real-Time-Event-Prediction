import numpy as np
import pandas as pd

from core_comp.tirp import TIRP
from tirp_prefixes.tirp_prefix_insts import TIRPPrefixInstances


class TIRPCompletionInstances:
    def __init__(self, tirp):
        self.tirp: TIRP = tirp
        self._tirp_prefixes_instances_w_event = {}
        self._tirp_prefixes_instances_wo_event = {}
        self.event_occur_time = None
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
            occr_time = self.event_occur_time[s_val.get_entity_id()]
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
        """
        The function computes the probabilities for each prefix of the pattern,
        considering instances that occurred more than once in an entity only once.

        ***Note***
            Instances that occurred more than once in an entity must be considered only once, otherwise,
            this can cause problems (especially when the temporal relation "before" is involved)
            and in some cases lead to values greater than one, which is not a probability.

        ***For example***
            Consider the following database with three entities (E1, E2, E3) and the current pattern Q={A<B, A<y, B<y}:

            (E1) (A+)---A-----(A-)    (B+)-----B------(B-)   (B+)-----B------(B-)           y+
            (E2) (A+)---A-----(A-)        (B+)-----B------(B-)   (B+)-----B------(B-)       y+
            (E3) (A+)---A-----(A-)        (B+)-----B------(B-)   (B+)-----B------(B-)

            Let's represent Q as a sequence of time interval endpoints: A+<A-<B+<B-<y+

            * Counting the number of instances for the earliest prefix A+ in DB results in 3 instances.
            * Counting the number instances of the prefix A+<A-<B+ in DB results in 6 instances (2 per entity).
            * Counting the number instances of Q=A+<A-<B+<B-<y+ in DB results in 4 instances (2 per E1 and E2).

            To compute the probability P(Q|tc) for the completion of a pattern at current time tc,
            the number of instances of Q is divided by the number of instances of the current prefix.

        ***Problems***
            (1) Given prefix A+ is observed the probability of seeing Q is greater than one 4/3 > 1, which is incorrect.
            (2) The probabilities for pattern completion should increase as more of the pattern is revealed.
                However, in the example given, the probability decreases from 4/3 (given A+) to 4/6 (given A+<A-<B+).

        ***Solution***
            Consider instances that occurred more than once in an entity only once.

            Let's try to compute the probabilities again:

            * Counting the number of instances for the earliest prefix A+ in DB results in 3 instances.
            * Counting the number instances of the prefix A+<A-<B+ in DB results in 3 instances (1 per entity).
            * Counting the number instances of Q=A+<A-<B+<B-<y+ in DB results in 2 instances (1 per E1 and E2).

            Solved!

        ***Things to consider in the future***
            * The number of instances per entity could help to predict the event of interest y,
            but the above method solution ignores this.

        ***Thanks to @TaliMalenboim for debugging this function
        """
        num_of_prefixes = len(self._tirp_prefixes_instances_w_event)
        # Pattern Q: Consider instances that occurred more than once in an entity only once
        sup_q = self._tirp_prefixes_instances_w_event[num_of_prefixes - 1].get_unique_num_of_instances()
        for i in range(num_of_prefixes):
            # i-th Q-Prefix: Consider instances that occurred more than once in an entity only once
            sup_i = self._tirp_prefixes_instances_w_event[i].get_unique_num_of_instances() \
                    + self._tirp_prefixes_instances_wo_event[i].get_unique_num_of_instances()
            self.support[i] = sup_q / sup_i

    def generate_feature_matrices(self, event_occur_time):
        # This function returns feature matrix for each pattern prefix
        self.event_occur_time = event_occur_time
        for i in range(1, self.tirp.get_tieps_num() - 1):
            # The first feature matrix is not relevant as it contains not duration
            self._generate_feature_matrix(tirp_prefix_id=i)

    def get_feature_matrices(self):
        return self.feature_matrices

    def get_prefixes_support(self):
        return self.support
