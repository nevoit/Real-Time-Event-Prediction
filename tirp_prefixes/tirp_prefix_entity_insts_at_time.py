from core_comp.time_point_series import TimePointSeries
from tirp_prefix_detection import TIRPPrefixDetection
from tirp_prefix_insts import TIRPPrefixInstances


class TIRPrefixEntityInstsAtTime:
    def __init__(self, entity_id, prefix_index, tirp_prefix, time_point_series):
        self._entity_id = entity_id
        self._prefix_index = prefix_index
        self._tirp_prefix = tirp_prefix
        self._time_point_series = time_point_series
        self._tirp_prefix_instances: TIRPPrefixInstances = TIRPPrefixInstances(self._tirp_prefix)
        self._detect_instances()

    def _detect_instances(self):
        tirp_pfx_detect = TIRPPrefixDetection(tirp_prefix=self._tirp_prefix)
        tirp_pfx_insts: list[TimePointSeries] = tirp_pfx_detect.detect(sti_series_id=self._entity_id,
                                                                       time_point_series=self._time_point_series)
        for inst_j, inst in enumerate(tirp_pfx_insts):
            self._tirp_prefix_instances.add_instance(entity_id=self._entity_id, inst_id=inst_j, inst=inst)

    def get_num_of_instances(self) -> int:
        return self._tirp_prefix_instances.get_num_of_instances()

    def get_instances(self) -> TIRPPrefixInstances:
        return self._tirp_prefix_instances.get_instances()

