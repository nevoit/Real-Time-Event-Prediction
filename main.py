from evaluate import evaluate
from mul_tirps import MulTIRPs
import read_files
from os import path

from tirp_comp import TIRPCompletion

if __name__ == '__main__':
    # Input folders and files names
    input_folder = 'input'
    sti_data_folder = 'STI data'
    sti_train_file_name = 'sti_train.csv'
    sti_test_file_name = 'sti_test.csv'
    patterns_file_name = 'patterns.csv'
    raw_data_folder = 'Raw data'
    raw_train_file_name = 'raw_train.csv'
    raw_y_train_file_name = 'train_class.csv'
    raw_test_file_name = 'raw_test.csv'
    raw_y_test_file_name = 'test_class.csv'

    # STI data paths
    sti_train_path = path.join(input_folder, sti_data_folder, sti_train_file_name)
    sti_test_path = path.join(input_folder, sti_data_folder, sti_test_file_name)
    patterns_path = path.join(input_folder, sti_data_folder, patterns_file_name)

    # Raw data paths
    raw_train_path = path.join(input_folder, raw_data_folder, raw_train_file_name)
    raw_y_train_path = path.join(input_folder, raw_data_folder, raw_train_file_name)
    raw_test_path = path.join(input_folder, raw_data_folder, raw_y_train_file_name)
    raw_y_test_path = path.join(input_folder, raw_data_folder, raw_y_test_file_name)

    train_set = read_files.read_sti_file(sti_train_path)
    test_set = read_files.read_sti_file(sti_test_path)

    tirps_list = read_files.read_patterns_file(patterns_path)

    for tirp in tirps_list:
        tirp_comp = TIRPCompletion(tirp=tirp, sti_train_set=train_set)
        tirp_comp.learn_model(pat_com_cls='XGBoost', pat_com_reg='XGBoost')

    cont_pred_tim = MulTIRPs(pat_com_cls='XGBoost',
                             pat_com_reg='XGBoost',
                             agg_func='mean')
    cont_pred_tim.learn_model(train_set=train_set,
                              list_of_patterns=tirps_list)
    prob_res = cont_pred_tim.predict_prob(test_set=test_set)
    conf_mat = evaluate(prob_res)
