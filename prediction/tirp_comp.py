import gc

import pandas as pd

import const
from core_comp.sti_db import STIDB
from core_comp.sti_series import STISeries
from core_comp.tiep import Tiep
from core_comp.time_point_series import TimePointSeries
from core_comp.tirp import TIRP
from prediction.tirp_based_model import TIRPBasedModel
from prediction.model_scpm_cls import SCPMCls
from prediction.model_xgb_cls import XGBCls
from prediction.model_gamma_reg import GammaReg
from prediction.tirp_comp_insts import TIRPCompletionInstances
from tirp_prefixes.tirp_prefix import TIRPrefix
from tirp_prefixes.tirp_prefix_detection import TIRPrefixDetection
from tirp_prefixes.tirp_prefix_insts import TIRPPrefixInstances


class TIRPCompletion:
    def __init__(self, tirp: TIRP, sti_train_set: STIDB):
        self.tirp: TIRP = tirp
        self.event_occr_time = {}

        # get the tiep order and ignore the ending tiep of the event of interest.
        # the assumption is the event ot interest ending tiep is always the last tiep
        self._tiep_order: list[list[Tiep]] = tirp.get_sorted_tieps()[:-1]
        self._tiep_prefixes: list[TIRPrefix] = self._get_tirp_prefixes()
        self._tirp_prefixes_instances = TIRPCompletionInstances(tirp=self.tirp)
        self._detect_tirp_prefixes(sti_train_set)

        self._tirp_prefixes_instances.compute_prob()
        self._tirp_prefixes_instances.generate_feature_matrices(event_occur_time=self.event_occr_time)

        # Create feature matrix for each TIRP prefix
        self.feature_matrices = self._tirp_prefixes_instances.get_feature_matrices()
        self.prefixes_support = self._tirp_prefixes_instances.get_prefixes_support()

        self.tirp_based_model = TIRPBasedModel(feature_matrices=self.feature_matrices, pref_sup=self.prefixes_support)
        self.prob_model = {}
        self.time_model = {}

    def _get_tirp_prefixes(self) -> list[TIRPrefix]:
        # This function returns a list of TIRP prefixes
        tiep_prefixes = []
        for i in range(len(self._tiep_order)):
            tiep_prefixes.append(TIRPrefix(tieps=self._tiep_order[:i + 1]))
        return tiep_prefixes

    def get_tirp_prefixes(self) -> list[TIRPrefix]:
        return self._tiep_prefixes

    def get_tirp(self) -> TIRP:
        return self.tirp

    def _detect_tirp_prefixes(self, sti_train_set: STIDB):
        # This function returns all detected instances per TIRP Prefix
        train_set_with_event: list[STISeries] = [s for s in sti_train_set.get_sti_series() if
                                                 s.is_symbol_in_series(const.EVENT_INDEX)]
        for sti_series in train_set_with_event:
            self.event_occr_time[sti_series.get_series_id()] = sti_series.get_last_sti_end_time()

        train_set_without_event: list[STISeries] = [s for s in sti_train_set._sti_series_list if
                                                    not s.is_symbol_in_series(const.EVENT_INDEX)]

        for i, tirp_prefix in enumerate(self._tiep_prefixes):
            inst_w_event = self._detect_tirp_prefix_for_db(tirp_prefix=tirp_prefix, db=train_set_with_event)
            self._tirp_prefixes_instances.add_tirp_prefix_w_event(tirp_prefix_id=i,
                                                                  tirp_prefix_insts=inst_w_event)

            inst_wo_event = self._detect_tirp_prefix_for_db(tirp_prefix=tirp_prefix, db=train_set_without_event)
            self._tirp_prefixes_instances.add_tirp_prefix_wo_event(tirp_prefix_id=i,
                                                                   tirp_prefix_insts=inst_wo_event)

    def _detect_tirp_prefix_for_db(self, tirp_prefix: TIRPrefix, db: list[STISeries]):
        tirp_prefix_instances: TIRPPrefixInstances = TIRPPrefixInstances(tirp_prefix)
        for sti_series in db:
            sti_series_id = sti_series.get_series_id()
            time_point_series: TimePointSeries = sti_series.get_time_points()
            tirp_pfx_detect = TIRPrefixDetection(tirp_prefix=tirp_prefix)
            tirp_pfx_insts: list[TimePointSeries] = tirp_pfx_detect.detect(sti_series_id=sti_series_id,
                                                                           time_point_series=time_point_series)
            for inst_j, inst in enumerate(tirp_pfx_insts):
                tirp_prefix_instances.add_instance(entity_id=sti_series_id, inst_id=inst_j, inst=inst)
        return tirp_prefix_instances

    def learn_occ_prob_model(self, cls_name: str):
        self.prob_model[cls_name] = {}
        for i in range(0, len(self.feature_matrices) + 1):
            cls = None
            if cls_name == const.MOD_CLS_SCPM_NAME:
                prob = self.tirp_based_model.get_pref_sup(prefix_index=i)
                cls = SCPMCls(prob=prob)
            elif i > 0:
                X, y = self.tirp_based_model.get_df_for_classification(prefix_index=i)
                if cls_name == const.MOD_CLS_XGB_NAME:
                    cls = XGBCls()
                    cls.fit(X=X, y=y)
            self.prob_model[cls_name][i] = cls

    def learn_occ_time_model(self, cls_name: str):
        self.time_model[cls_name] = {}
        for i in range(1, len(self.feature_matrices) + 1):
            cls = None
            X_tte, y_tte = self.tirp_based_model.get_df_for_regression(prefix_index=i)
            if cls_name == const.MOD_REG_GAM_GLM_NAME:
                cls = GammaReg()
                cls.fit(X=X_tte, y=y_tte)
            self.time_model[cls_name][i] = cls

    def _create_df_row_for_inst(self, prefix_index, inst, current_time):
        dur_list = inst.get_durations_between_all_tieps()
        # adds the gap between the last time point and current time
        dur_list.append(current_time - inst.get_last_time_point_time())
        feature_dict = {i: [dur_list[i - 1]] for i in range(prefix_index + 1)}
        return pd.DataFrame.from_dict(feature_dict)

    def predict_proba(self, cls_name, prefix_index, inst, current_time):
        inst_row = self._create_df_row_for_inst(prefix_index, inst, current_time)
        if 0 in inst_row[0].to_numpy():  # TODO: REMOVE IT! IT'S ONLY FOR DEBUG
            print("WRONG LOGIC!")
        if cls_name == const.MOD_CLS_SCPM_NAME:
            cls = self.prob_model[cls_name][prefix_index]
        else:
            cls = self.prob_model[cls_name][prefix_index + 1]
        return cls.predict_proba(inst_row)

    def predict_time(self, reg_name, prefix_index, inst, current_time):
        inst_row = self._create_df_row_for_inst(prefix_index, inst, current_time)
        if 0 in inst_row[0].to_numpy():  # TODO: REMOVE IT! IT'S ONLY FOR DEBUG
            print("WRONG LOGIC!")
        reg = self.time_model[reg_name][prefix_index + 1]
        return reg.predict_time(inst_row)

    def post_training_deletion(self):
        # Remove unnecessary training artifacts that could consume a lot of memory.
        # Thanks to @LiorTkach for his suggestion to add that.
        self.feature_matrices = None
        self._tirp_prefixes_instances = None

        gc.collect()
