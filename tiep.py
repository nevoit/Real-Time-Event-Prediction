import const


class Tiep:
    """
    This class represents the time interval endpoint that comprised of time, type, symbol id, and the symbol instance id
    """

    def __init__(self, time: int, tiep_type: str, sym_id: int, sym_inst_id: int, var_id: int,
                 tiep_inst_id: int = -1, dummy: bool = False):
        """
        :param time: the time of occurrence
        :param tiep_type: starting or ending endpoint
        :param sym_id: the symbol id
        :param sym_inst_id: the occurrence index of the same tiep in the series
        :param var_id: the variable id
        :param dummy: whether this object represents a dummy tiep (True) or real instances (False).
        """
        self.time: int = time
        self.tiep_type: str = tiep_type
        self.sym_id: int = sym_id
        self.var_id: int = var_id
        self.sym_inst_id: int = sym_inst_id  # each instance of this tiep should get the STI id
        self.tiep_inst_id: int = tiep_inst_id  # each instance of this tiep should get different id
        self.pair_tiep = None
        self.dummy: bool = dummy
        self._check_input_validity()

    def add_pair_tiep(self, tiep):
        self.pair_tiep: Tiep = tiep

    def get_pair_tiep(self):
        return self.pair_tiep

    def get_time(self) -> int:
        return self.time

    def get_tiep_type(self) -> str:
        return self.tiep_type

    def get_symbol_id(self) -> int:
        return self.sym_id

    def get_var_id(self) -> int:
        return self.var_id

    def get_symbol_instance_id(self) -> int:
        return self.sym_inst_id

    def get_tiep_instance_id(self) -> int:
        return self.tiep_inst_id

    def is_start_type(self) -> bool:
        return self.tiep_type == const.START_TIEP

    def is_end_type(self) -> bool:
        return self.tiep_type == const.END_TIEP

    def is_same_tiep(self, tp):
        if self.tiep_type == tp.get_tiep_type() and self.sym_id == tp.get_symbol_id():
            return True
        else:
            return False

    def is_same_tiep_instance(self, tp):
        if self.tiep_type == tp.get_tiep_type() and self.sym_id == tp.get_symbol_id() \
                and self.sym_inst_id == tp.get_symbol_instance_id() and self.var_id == tp.get_var_id():
            return True
        else:
            return False

    def _check_input_validity(self):
        # This function check the validity of the input and assert in case of wrong input
        if not self.dummy and not self.time >= 0:
            assert "The provided time should be greater than zero!"
        elif self.tiep_type not in {const.START_TIEP, const.END_TIEP}:
            assert "The provided type should be '+' or '-'!"
        elif not self.sym_id >= 0:
            assert "The symbol id should be greater than zero!"
        elif not self.dummy and not self.var_id >= 0:
            assert "The variable id should be greater than zero!"
        elif not self.sym_inst_id >= 0:
            assert "The symbol instance id should be greater than zero!"
