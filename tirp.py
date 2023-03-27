class TIRP:
    def __init__(self, stis: list, temp_rels: list):
        self.stis: list = stis
        self.temp_rels: list = temp_rels
        self._check_input_validity()

    def _check_input_validity(self):
        # This function check the validity of the input and assert in case of wrong input
        if not len(self.stis) >= 0:
            assert "The STIs list should be greater than zero!"
        if not len(self.temp_rels) >= 0:
            assert "The temporal relation list should be greater than zero!"
        if not (len(self.stis)**2 - len(self.stis) / 2) == len(self.temp_rels):
            assert "The temporal relation list should be exactly equals to (|STIs|^2-|STIs|) / 2!"
        