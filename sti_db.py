class STIDB:
    def __init__(self, sti_series_list: list):
        self.sti_series_list: list = sti_series_list
        self._check_input_validity()

    def _check_input_validity(self):
        # This function check the validity of the input and assert in case of wrong input
        if not len(self.sti_series_list) >= 0:
            assert "The STI series list should be greater than zero!"

