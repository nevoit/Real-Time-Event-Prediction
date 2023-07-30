import functools

import const
from tiep import Tiep


class TIRP:
    """
    Time intervals-related pattern (TIRP).
    """

    def __init__(self, stis: list[int], temp_rels: list[str], vs: float, hs: float):
        """
        :param stis: a list that represents all the STIs of the pattern in lexicography order
        :param temp_rels: a list that represents the temporal relations of the pattern
        :param vs: vertical support
        :param hs: horizontal support

        A one dimensional array that represents a two-diminutions array of the half matrix presented in Robert's paper:
            B   C   D
        A   o   <   <                 ---------A---------              --------C--------    --------D------
        B   X   <   <                       ------------B-----------
        C   X   X   <

        Note: The char 'X' represents empty since we do not need the reverse relation between symbols.

        The indices of the one-sized array are based on the order below:
            B   C   D
        A   0   1   3
        B   X   2   4
        C   X   X   5
                                                            0    1    2    3    4    5
                                                           (AB) (AC) (AD) (BC) (BD) (CD)
        In this case, the relations list looks like this: ['o', 'b', 'b', 'b', 'b', 'b']
        """
        self.stis: list[int] = stis
        self.temp_rels: list[str] = temp_rels
        self.vs: float = vs
        self.hs: float = hs

        self.tiep_comparison: dict = {1: [], 0: [], -1: []}
        self.sorted_tieps: list[list[Tiep]] = self._get_tiep_order()

        self._check_input_validity()

    def get_stis(self) -> list[int]:
        return self.stis

    def get_rels(self) -> list[str]:
        return self.temp_rels

    def get_sorted_tieps(self) -> list[list[Tiep]]:
        # Get the sorted tieps
        return self.sorted_tieps

    def get_tirp_size(self) -> int:
        return len(self.stis)

    def get_vs(self) -> float:
        return self.vs

    def get_hs(self) -> float:
        return self.hs

    def get_tieps_num(self) -> int:
        return len(self.sorted_tieps)

    def get_temp_rel_by_sti_ids(self, early_sti_id: int, later_sti_id: int) -> str:
        """
        This function gets two different STI indexes and returns the temporal relation between them.
        For example, here is an example of a TIRP with STIs [A, B, C, D]

        Visual representation:

        ---A----
           ---B----
           ---C----   ----D-----

        Its half matrix representation:

            B   C   D
        A   o   o   b
        B       e   b
        C           b

        The temporal relations list will be
        [o(between A, B), o(between A, C), e(between B, C), b(between A, D), b(between B, D), b(between C, D)]

        fst_sti_id = 0 and snd_sti_id = 1 will return the temporal relation between A and B: 'o'
        fst_sti_id = 0 and snd_sti_id = 2 will return the temporal relation between A and C: 'o'
        fst_sti_id = 0 and snd_sti_id = 3 will return the temporal relation between A and D: 'b'
        fst_sti_id = 2 and snd_sti_id = 3 will return the temporal relation between C and D: 'b'

        :param early_sti_id: the index of the earlier STI
        :param later_sti_id: the index of the later STI
        :return: the temporal relation between them
        """
        if not 0 <= early_sti_id < len(self.stis):
            raise Exception('Wrong index of the earlier STI')
        elif not 0 <= later_sti_id < len(self.stis):
            raise Exception('Wrong index of the later STI')
        elif early_sti_id >= later_sti_id:
            raise Exception('The STI later index mush be greater than the STI earlier index')
        else:
            column_starting_index = 0
            for i in range(0, later_sti_id):
                column_starting_index += i
            relation_index = column_starting_index + early_sti_id
            return self.temp_rels[relation_index]

    def get_tieps_str(self) -> str:
        tiep_str = ''
        for i, tps in enumerate(self.sorted_tieps):
            if len(tps) > 1:
                tiep_str += '('
            for tp in tps:
                tiep_str += f'{tp._tiep_type}{tp._sym_id}'
            if len(tps) > 1:
                tiep_str += ')'
            if i != len(self.sorted_tieps) - 1:
                tiep_str += const.REL_TIEP
        return tiep_str

    def _get_tiep_order(self) -> list[list[Tiep]]:
        """
        This function gets returns all the tieps of this pattern.
        For example, see this pattern and below the tiep.
        ---------------A---------------
                    ---------------B------------
                                       ----C----
        (A+)       (B+)               (A-C+)   (B-C-)

        As you can see in this example, the tieps with the same timestamp merged together.
        In this case, the function returns the list: [['A+'], ['B+'], ['A-', 'C+'], ['B-', 'C-']]

        :param symbols_list: a list of relations, in this format = ['A', 'B', 'C', 'D']
        :return: a list of all the tieps of the given pattern,
        in this format : [['A+'], ['B+'], ['A-', 'C+'], ['B-', 'C-']]
        """
        tieps_list: list = []
        tiep_index = 0
        for sym_i, sym_id in enumerate(self.stis):
            # adding the starting tiep
            starting_tiep = Tiep(time=-1, tiep_type=const.START_TIEP, sym_id=sym_id, sym_inst_id=sym_i,
                                 var_id=-1, tiep_inst_id=tiep_index, dummy=True)
            tieps_list.append(starting_tiep)
            tiep_index += 1

            # adding the ending tiep
            ending_tiep = Tiep(time=-1, tiep_type=const.END_TIEP, sym_id=sym_id, sym_inst_id=sym_i,
                               var_id=-1, tiep_inst_id=tiep_index, dummy=True)
            tieps_list.append(ending_tiep)
            tiep_index += 1

        # This code sorts the tieps by the temporal relations of their STIs
        cmp = functools.cmp_to_key(self._sort_tieps_by_stis_temp_rels)
        tieps_list.sort(key=cmp)

        # Co-occurrence tieps should be merged to a specific time point
        o_occur_tieps = self._merge_overlaps_lists()
        sorted_tieps = self._merge_co_occur_tieps(o_occur_tieps=o_occur_tieps,
                                                  tieps=tieps_list)
        return sorted_tieps

    def _merge_co_occur_tieps(self, o_occur_tieps, tieps):
        """
        This function takes all the co-occurrence tieps and merges them
        :param o_occur_tieps: list of groups of co-occurrence endpoints
        :param tieps: list of all the tieps
        :return: a list of merged tieps
        """
        final_tieps = []
        i = 0
        while i < len(tieps):
            tp: Tiep = tieps[i]
            if any(tp.get_tiep_instance_id() in sublist for sublist in o_occur_tieps):
                # if there is more than one tiep at a specific time point
                list_of_values = []
                rel_list = self.in_list(o_occur_tieps, tp.get_tiep_instance_id())
                len_list = len(rel_list)
                for j in range(i, i + len_list):
                    list_of_values.append(tieps[j])
                final_tieps.append(list_of_values)
                i += len_list
            else:
                # if there is only only one tiep at a specific time point
                final_tieps.append([tp])
                i += 1
        return final_tieps

    @staticmethod
    def in_list(list_of_lists, item):
        """
        This function gets a list of lists and returns whether or not the item is in this list of lists
        :param list_of_lists: for example [[...],[....],....., [...]]
        :param item: the item we want to find
        :return: the first list that contains this item
        """
        for list_ in list_of_lists:
            if item in list_:
                return list_

    def _update_tiep_comparison(self, earlier_tiep_index: int, later_tiep_index: int, comparison_result: int):
        """
        This function updates the tiep comparison dictionary
        :param earlier_tiep_index: the earlier tiep index
        :param later_tiep_index: the later tiep index
        :param comparison_result: nothing
        :return:
        """
        self.tiep_comparison[comparison_result].append([earlier_tiep_index, later_tiep_index])

    def _sort_tieps_by_stis_temp_rels(self, earlier_tiep: Tiep, later_tiep: Tiep):
        """
        This function gets two tieps and sorts them using their temporal relation
        :param earlier_tiep: earlier tiep
        :param later_tiep: later tiep
        :return:
        """
        # earlier tiep values
        earlier_tiep_index = earlier_tiep.get_tiep_instance_id()
        earlier_sti_index = earlier_tiep.get_symbol_instance_id()
        earlier_tiep_type = earlier_tiep.get_tiep_type()

        # later tiep values
        later_tiep_index = later_tiep.get_tiep_instance_id()
        later_sti_index = later_tiep.get_symbol_instance_id()
        later_tiep_type = later_tiep.get_tiep_type()

        result = None
        if earlier_sti_index > later_sti_index:
            # a lexicographical order for the symbols of the tiep,
            # if it not the case, we will return the opposite value
            return self._sort_tieps_by_stis_temp_rels(later_tiep, earlier_tiep) * -1
        elif earlier_sti_index == later_sti_index:  # if it is the same symbol (e.g. A+ or A-)
            if earlier_tiep_type == later_tiep_type:  # if it is the same tiep (e.g., A+ and A+)
                raise Exception('A tiep with the same symbol could not be occur at the same time')
            elif earlier_tiep_type == const.START_TIEP and later_tiep_type == const.END_TIEP:
                result = -1  # if the earlier is + and the second is later is - (e.g., A+ and A-)
            elif earlier_tiep_type == const.END_TIEP and later_tiep_type == const.START_TIEP:
                result = 1  # if the earlier is - and the second is later is + (e.g., A- and A+)
        else:  # different symbol indexes (e.g., A and a different A)
            temp_rel = self.get_temp_rel_by_sti_ids(early_sti_id=earlier_sti_index,
                                                    later_sti_id=later_sti_index)
            result = self._get_tiep_rep(earlier_tiep_type=earlier_tiep_type,
                                        temp_rel=temp_rel,
                                        later_tiep_type=later_tiep_type)
        self._update_tiep_comparison(earlier_tiep_index, later_tiep_index, result)
        return result

    def _get_tiep_rep(self, earlier_tiep_type: str, temp_rel: str, later_tiep_type: str):
        """
        This function returns the tiep order of two tieps based on the relation between them.

        For example:
        (1) A- is at the same time as B+ when the relation is meets
        (2) A- occurs earlier than B+ when the relation is before

        In general, the idea of this function is based on the tiep representation:
        A starts B      |   As=Bs<Ae<Be
        A contains B    |   As<Bs<Be<Ae
        A finished-by B |   As<Bs<Ae=Be
        A overlaps B    |   As<Bs<Ae<Be
        A meets B       |   As<Ae=Bs<Be
        A before B      |   As<Ae<Bs<Be
        A equals B      |   As=Bs<Ae=Be

        :param earlier_tiep_type: the first tiep type
        :param temp_rel: the temporal relation between them
        :param later_tiep_type: the second tiep type
        :return:
        """
        if earlier_tiep_type == const.START_TIEP and later_tiep_type == const.START_TIEP:
            # For example: A+, B+
            if temp_rel in {const.TEMP_REL_STARTS, const.TEMP_REL_EQUALS}:
                return 0
            elif temp_rel in {const.TEMP_REL_CONTAINS, const.TEMP_REL_FINISHED_BY, const.TEMP_REL_OVERLAPS,
                              const.TEMP_REL_MEETS, const.TEMP_REL_BEFORE}:
                return -1
        elif earlier_tiep_type == const.START_TIEP and later_tiep_type == const.END_TIEP:
            # For example: A+, B-. It's always the same answer (A+ < B-).
            return -1
        elif earlier_tiep_type == const.END_TIEP and later_tiep_type == const.START_TIEP:
            # For example A-, B+
            if temp_rel in {const.TEMP_REL_MEETS}:
                return 0
            elif temp_rel in {const.TEMP_REL_BEFORE}:
                return -1
            elif temp_rel in {const.TEMP_REL_STARTS, const.TEMP_REL_OVERLAPS, const.TEMP_REL_FINISHED_BY,
                              const.TEMP_REL_CONTAINS, const.TEMP_REL_EQUALS}:
                return 1
        elif earlier_tiep_type == const.END_TIEP and later_tiep_type == const.END_TIEP:
            # For example A-, B-
            if temp_rel in {const.TEMP_REL_FINISHED_BY, const.TEMP_REL_EQUALS}:
                return 0
            elif temp_rel in {const.TEMP_REL_STARTS, const.TEMP_REL_OVERLAPS, const.TEMP_REL_MEETS,
                              const.TEMP_REL_BEFORE}:
                return -1
            elif temp_rel in {const.TEMP_REL_CONTAINS}:
                return 1
        raise Exception('There is a problem with the tiep representation')

    def _merge_overlaps_lists(self) -> list:
        """
        This function takes all lists of lists and merges overlaps lists
        For example: [[1,2], [2,3], [1,3], [5,6]] --> [[1,2,3], [5,6]]
        :return: a list of co-occurred tieps
        """
        co_occur_tieps = self.tiep_comparison[0].copy()
        is_changed = True
        while is_changed:
            is_changed = self._merge_pair(co_occur_tieps=co_occur_tieps)
        return co_occur_tieps

    @staticmethod
    def _merge_pair(co_occur_tieps):
        """
        This function takes all the co-occurrence tieps and merges only one pair, then remove one occurrence
        :param co_occur_tieps:  co-occurrence endpoints
        :return: True if the list changed
        """
        for i in range(len(co_occur_tieps) - 1):
            for j in range(i + 1, len(co_occur_tieps)):
                first_set = set(co_occur_tieps[i])
                second_set = set(co_occur_tieps[j])
                if first_set.intersection(second_set):
                    co_occur_tieps[i] = co_occur_tieps[i] + list(second_set.difference(first_set))
                    del co_occur_tieps[j]
                    return True
        return False

    def _check_input_validity(self):
        # This function checks the validity of the input and assert in case of wrong input
        if not len(self.stis) >= 0:
            assert "The STIs list should be greater than zero!"
        if not len(self.temp_rels) >= 0:
            assert "The temporal relation list should be greater than zero!"
        if not 0 < self.vs <= 1:
            assert "The vertical support should be between zero and one"
        if not self.hs >= 1:
            assert "The horizontal support should be greater than one"
        if not (len(self.stis) ** 2 - len(self.stis) / 2) == len(self.temp_rels):
            assert "The temporal relation list should exactly equal to (|STIs|^2-|STIs|) / 2!"
