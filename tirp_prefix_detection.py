from tiep_series import TiepSeries
from tirp_prefix import TIRPPrefix


class TIRPPrefixDetection:
    def __init__(self, tirp_prefix: TIRPPrefix):
        self.tirp_prefix: TIRPPrefix = tirp_prefix

    def detect(self, tiep_series: TiepSeries):
        print()