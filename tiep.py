class Tiep:
    """
    This class represents the time interval endpoint that comprised of time, type, symbol id, and the symbol instance id
    """
    def __init__(self, time: int, tiep_type: str, sym_id: int, sym_inst_id: int):
        self.time: int = time
        self.tiep_type: str = tiep_type
        self.sym_id: int = sym_id
        self.sym_inst_id: int = sym_inst_id  # each instance of this tiep should get different id
        self._check_input_validity()

    def get_time(self) -> int:
        return self.time

    def get_tiep_type(self) -> str:
        return self.tiep_type

    def get_symbol_id(self) -> int:
        return self.sym_id

    def get_symbol_instance_id(self) -> int:
        return self.sym_inst_id

    def is_start_type(self) -> bool:
        return self.tiep_type == '+'

    def is_end_type(self) -> bool:
        return self.tiep_type == '-'

    def _check_input_validity(self):
        # This function check the validity of the input and assert in case of wrong input
        if not self.time >= 0:
            assert "The provided time should be greater than zero!"
        elif self.tiep_type not in {'+', '-'}:
            assert "The provided type should be '+' or '-'!"
        elif not self.sym_id >= 0:
            assert "The symbol id should be greater than zero!"
        elif not self.sym_inst_id >= 0:
            assert "The symbol instance id should be greater than zero!"
