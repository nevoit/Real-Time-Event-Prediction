import const
from sti import STI
from sti_db import STIDB
from sti_series import STISeries
from tiep import Tiep
import pandas as pd
import ast

from tirp import TIRP


def read_patterns_file(file_path) -> list[TIRP]:
    """
    This function read the patterns file and creates list of TIRP objects
    :param file_path: path of the file
    :return: list of TIRP objects
    """
    tirp_list = []
    pat_df = pd.read_csv(file_path)
    for index, row in pat_df.iterrows():
        sti_list = ast.literal_eval(row[const.PAT_STIS_COL_NAME])
        rel_list = ast.literal_eval(row[const.PAT_TEMP_RELS_COL_NAME])
        vs = row[const.PAT_TEMP_VS_COL_NAME]
        hs = row[const.PAT_TEMP_HS_COL_NAME]
        if len(sti_list) <= 1 or sti_list[-1] != const.EVENT_INDEX:
            # relevant only if the pattern ends with the event of interest
            continue
        else:
            tirp = TIRP(stis=sti_list, temp_rels=rel_list, vs=vs, hs=hs)
            for i in range(len(sti_list)-1):
                rel_with_event = tirp.get_temp_rel_by_sti_ids(i, len(sti_list) - 1)
                if rel_with_event not in {const.TEMP_REL_BEFORE, const.TEMP_REL_MEETS}:
                    print('Temporal relations with the event of interest must be before or meets')
                    continue
            tirp_list.append(tirp)
    return tirp_list


def read_sti_file(file_path) -> STIDB:
    """
    This function reads the STIs data and creates relevant objects.
    :param file_path: path of the file
    :return: STIDB: list of STI series
    """
    sti_df = pd.read_csv(file_path)
    sti_df = sti_df.sort_values(by=[const.STI_DATA_SERIES_ID_COL_NAME,
                                    const.STI_DATA_START_TIME_COL_NAME,
                                    const.STI_DATA_END_TIME_COL_NAME,
                                    const.STI_DATA_SYM_ID_COL_NAME])

    series_list = []
    for series_id in sti_df[const.STI_DATA_SERIES_ID_COL_NAME].unique():
        # iterates over the series id in the dataframe
        stis_list = []
        symbol_inst_id = {}

        series_df = sti_df[sti_df[const.STI_DATA_SERIES_ID_COL_NAME] == series_id]
        for index, row in series_df.iterrows():
            # iterates over the rows in the dataframe
            symbol_id = int(row[const.STI_DATA_SYM_ID_COL_NAME])
            var_id = int(row[const.STI_DATA_VAR_ID_COL_NAME])
            start_time = int(row[const.STI_DATA_START_TIME_COL_NAME])
            end_time = int(row[const.STI_DATA_END_TIME_COL_NAME])

            if symbol_id not in symbol_inst_id:
                symbol_inst_id[symbol_id] = 1
            else:
                symbol_inst_id[symbol_id] += 1

            start_tiep = Tiep(time=start_time, tiep_type=const.START_TIEP,
                              sym_id=symbol_id, sym_inst_id=symbol_inst_id[symbol_id], var_id=var_id)
            end_tiep = Tiep(time=end_time, tiep_type=const.END_TIEP,
                            sym_id=symbol_id, sym_inst_id=symbol_inst_id[symbol_id], var_id=var_id)
            sti = STI(start_tiep=start_tiep, end_tiep=end_tiep)
            stis_list.append(sti)

        # create STI series and append to a list
        sti_series = STISeries(series_id=series_id, stis_list=stis_list)
        series_list.append(sti_series)

    return STIDB(sti_series_list=series_list)
