from evaluate import evaluate
from mul_tirps import MulTIRPs
from sti_db import STIDB
from sti_series import STISeries
from tirp import TIRP


if __name__ == '__main__':
    sti_series_train = [STISeries(stis_list=[])]
    train_set = STIDB(sti_series_list=sti_series_train)

    sti_series_test = [STISeries(stis_list=[])]
    test_set = STIDB(sti_series_list=sti_series_test)

    tirps_list = [
        TIRP(stis=[], temp_rels=[])
    ]

    cont_pred_tim = MulTIRPs(pat_com_cls='XGBoost',
                             pat_com_reg='XGBoost',
                             agg_func='mean')
    cont_pred_tim.learn_model(train_set=train_set,
                              list_of_patterns=tirps_list)
    prob_res = cont_pred_tim.predict_prob(test_set=test_set)
    conf_mat = evaluate(prob_res)



