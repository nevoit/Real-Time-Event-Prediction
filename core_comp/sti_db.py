class STIDB:
    """
    This class represents STI data contain entities, that each entity is comprised of STI series
    """

    def __init__(self, sti_series_list: list):
        self._sti_series_list: list = sti_series_list
        self._check_input_validity()

    def get_sti_series(self):
        return self._sti_series_list

    def _check_input_validity(self):
        # This function check the validity of the input and assert in case of wrong input
        if not len(self._sti_series_list) >= 0:
            assert "The STI series list should be greater than zero!"

