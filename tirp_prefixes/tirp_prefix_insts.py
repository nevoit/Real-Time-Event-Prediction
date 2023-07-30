from core_comp.time_point_series import TimePointSeries
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

    def add_instance(self, entity_id: int, inst_id: int, inst: TimePointSeries):
        """
        This function gets instance that represented by time point series
        and adds this instances to the list of instances
        """
        assert isinstance(inst, TimePointSeries), "Oh no! Wrong type input for this function!"
        self.instances[f'{entity_id}_{inst_id}'] = inst

    def get_instances(self):
        return self.instances

    def get_num_of_instances(self):
        return len(self.instances)
