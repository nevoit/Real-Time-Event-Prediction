import const
from sti_db import STIDB
from sti_series import STISeries
from tiep import Tiep
from time_point_series import TimePointSeries
from tirp import TIRP
from tirp_based_model import TIRPBasedModel, SCPM, XGBoost
from tirp_comp_insts import TIRPCompletionInstances
from tirp_prefix import TIRPPrefix
from tirp_prefix_detection import TIRPPrefixDetection
from tirp_prefix_insts import TIRPPrefixInstances


class TIRPCompletion:
    def __init__(self, tirp: TIRP, sti_train_set: STIDB):
        self.tirp: TIRP = tirp
        self.event_occr_time = {}

        # get the tiep order and ignore the ending tiep of the event of interest.
        # the assumption is the event ot interest ending tiep is always the last tiep
        self._tiep_order: list[list[Tiep]] = tirp.get_sorted_tieps()[:-1]
        self._tiep_prefixes: list[TIRPPrefix] = self._get_tirp_prefixes()
        self._tirp_prefixes_instances = TIRPCompletionInstances(tirp=self.tirp)
        self._detect_tirp_prefixes(sti_train_set)

        self._tirp_prefixes_instances.compute_prob()
        self._tirp_prefixes_instances.generate_feature_matrices(event_occr_time=self.event_occr_time)

        # Create feature matrix for each TIRP prefix
        self.feature_matrices = self._tirp_prefixes_instances.get_feature_matrices()

        self.X = {}
        self.y_class = {}
        self.X_tte = {}
        self.y_tte = {}
        for i in range(1, len(self.feature_matrices) + 1):
            df_i = self.feature_matrices[i]
            self.X[i] = df_i.drop(columns=['class', 'tte'])
            self.y_class[i] = df_i['class']
            self.y_tte[i] = df_i[~df_i['tte'].isnull()]['tte']
            self.X_tte[i] = df_i[~df_i['tte'].isnull()].drop(columns=['class', 'tte'])

        self.prefixes_support = self._tirp_prefixes_instances.get_prefixes_support()

    def _get_tirp_prefixes(self) -> list[TIRPPrefix]:
        # This function returns a list of TIRP prefixes
        tiep_prefixes = []
        for i in range(len(self._tiep_order)):
            tiep_prefixes.append(TIRPPrefix(tieps=self._tiep_order[:i + 1]))
        return tiep_prefixes

    def _detect_tirp_prefixes(self, sti_train_set: STIDB):
        # This function returns all detected instances per TIRP Prefix
        train_set_with_event: list[STISeries] = [s for s in sti_train_set.get_sti_series() if
                                                 s.is_symbol_in_series(const.EVENT_INDEX)]
        for sti_series in train_set_with_event:
            self.event_occr_time[sti_series.get_series_id()] = sti_series.get_last_sti_start_time()

        train_set_without_event: list[STISeries] = [s for s in sti_train_set.sti_series_list if
                                                    not s.is_symbol_in_series(const.EVENT_INDEX)]

        for i, tirp_prefix in enumerate(self._tiep_prefixes):
            inst_w_event = self._detect_tirp_prefix_for_db(tirp_prefix=tirp_prefix, db=train_set_with_event)
            self._tirp_prefixes_instances.add_tirp_prefix_w_event(tirp_prefix_id=i,
                                                                  tirp_prefix_insts=inst_w_event)

            inst_wo_event = self._detect_tirp_prefix_for_db(tirp_prefix=tirp_prefix, db=train_set_without_event)
            self._tirp_prefixes_instances.add_tirp_prefix_wo_event(tirp_prefix_id=i,
                                                                   tirp_prefix_insts=inst_wo_event)

    def _detect_tirp_prefix_for_db(self, tirp_prefix: TIRPPrefix, db: list[STISeries]):
        tirp_prefix_instances: TIRPPrefixInstances = TIRPPrefixInstances(tirp_prefix)
        for sti_series in db:
            sti_series_id = sti_series.get_series_id()
            time_point_series: TimePointSeries = sti_series.get_time_points()
            tirp_pfx_detect = TIRPPrefixDetection(tirp_prefix=tirp_prefix)
            tirp_pfx_insts: list[TimePointSeries] = tirp_pfx_detect.detect(time_point_series=time_point_series)
            for inst in tirp_pfx_insts:
                tirp_prefix_instances.add_instance(inst_id=sti_series_id, inst=inst)
        return tirp_prefix_instances

    def learn_occ_prob_model(self, cls_model: str):
        if cls_model == 'SCPM':
            SCPM(prefixes_support=self.prefixes_support)
        elif cls_model == 'XGBoost':
            XGBoost()

    def learn_occ_time_model(self):
        pass
