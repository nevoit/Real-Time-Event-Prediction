from time_point_series import TimePointSeries
from tirp_prefix import TIRPPrefix


class TIRPPrefixInstances:
    """
    Instances of TIRP prefixes.
    """

    def __init__(self, tirp_prefix: TIRPPrefix):
        """
        :param tirp_prefix: the TIRP prefix we consider

        """
        self.tirp_prefix = tirp_prefix
        self.instances = {}

    def add_instance(self, inst_id: int, inst: TimePointSeries):
        """
        This function gets instance that represented by time point series
        and adds this instances to the list of instances
        """
        if inst_id not in self.instances.keys():
            self.instances[inst_id] = []
        self.instances[inst_id].append(inst)

    def get_instances(self):
        return self.instances
