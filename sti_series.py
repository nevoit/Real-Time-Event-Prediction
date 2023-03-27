class STISeries:
    def __init__(self, stis_list: list):
        self.stis_list: list = stis_list
        self._check_input_validity()

    def _check_input_validity(self):
        # This function check the validity of the input and assert in case of wrong input
        if not len(self.stis_list) >= 0:
            assert "The STIs list should be greater than zero!"