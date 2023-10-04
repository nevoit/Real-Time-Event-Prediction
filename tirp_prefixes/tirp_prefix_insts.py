from core_comp.time_point_series import TimePointSeries
from tirp_prefixes.tirp_prefix import TIRPrefix


class TIRPPrefixInstances:
    """
    Instances of TIRP prefixes.
    """

    def __init__(self, tirp_prefix: TIRPrefix):
        """
        :param tirp_prefix: the TIRP prefix we consider

        """
        self._tirp_prefix = tirp_prefix
        self._instances: dict[str:TimePointSeries] = {}

    def add_instance(self, entity_id: int, inst_id: int, inst: TimePointSeries):
        """
        This function gets instance that represented by time point series
        and adds this instances to the list of instances
        """
        assert isinstance(inst, TimePointSeries), "Oh no! Wrong type input for this function!"
        self._instances[f'{entity_id}_{inst_id}'] = inst

    def get_instances(self) -> dict[str:TimePointSeries]:
        return self._instances

    def get_num_of_instances(self) -> int:
        return len(self._instances)

    def get_unique_num_of_instances(self) -> int:
        # Consider instances that occurred more than once in an entity only once
        unique_entities = {tps.get_entity_id() for tps in self._instances.values()}
        return len(unique_entities)
