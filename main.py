import const
from prediction.count_simulator import ContSimulator
from prediction.evaluate import Evaluate
from input import read_files
from os import path

from prediction.tirp_comp import TIRPCompletion

if __name__ == '__main__':
    # STI data paths
    sti_train_path = path.join(const.INPUT_FOLDER, const.STI_DATA_FOLDER, const.STI_TRAIN_FILE_NAME)
    sti_test_path = path.join(const.INPUT_FOLDER, const.STI_DATA_FOLDER, const.STI_TEST_FILE_NAME)
    patterns_path = path.join(const.INPUT_FOLDER, const.STI_DATA_FOLDER, const.PATTERNS_FILE_NAME)

    # Raw data paths
    raw_train_path = path.join(const.INPUT_FOLDER, const.RAW_DATA_FOLDER, const.RAW_TRAIN_FILE_NAME)
    raw_y_train_path = path.join(const.INPUT_FOLDER, const.RAW_DATA_FOLDER, const.RAW_Y_TRAIN_FILE_NAME)
    raw_test_path = path.join(const.INPUT_FOLDER, const.RAW_DATA_FOLDER, const.RAW_TEST_FILE_NAME)
    raw_y_test_path = path.join(const.INPUT_FOLDER, const.RAW_DATA_FOLDER, const.RAW_Y_TEST_FILE_NAME)

    # Train & Test sets
    train_set = read_files.read_sti_file(sti_train_path)
    test_set = read_files.read_sti_file(sti_test_path)
    test_set_labels = {s.get_series_id(): s.is_symbol_in_series(const.EVENT_INDEX) for s in test_set.get_sti_series()}
    # This dictionary contains the actual time of the event of interest and set None for entities without the event
    test_set_times_with_event = {s.get_series_id(): s.get_last_sti_end_time() for s in test_set.get_sti_series() if
                                 s.is_symbol_in_series(const.EVENT_INDEX)}
    test_set_times_without_event = {s.get_series_id(): None for s in test_set.get_sti_series() if
                                    not s.is_symbol_in_series(const.EVENT_INDEX)}
    test_set_times = {**test_set_times_with_event, **test_set_times_without_event}

    tirps_list = read_files.read_patterns_file(patterns_path)

    # This block iterates over the TIRPs and for each pattern learns a completion model (probability and time to event)
    tirp_comp_models: list = []
    for tirp in tirps_list[:50]:
        tirp_comp = TIRPCompletion(tirp=tirp, sti_train_set=train_set)
        tirp_comp.learn_occ_prob_model(cls_name=const.MOD_CLS_SCPM_NAME)
        tirp_comp.learn_occ_prob_model(cls_name=const.MOD_CLS_XGB_NAME)
        tirp_comp.learn_occ_time_model(cls_name=const.MOD_REG_GAM_GLM_NAME)
        tirp_comp_models.append(tirp_comp)

    # This block iterates over the entities in the test data and predicts the probability and time of the event
    pred_over_time: dict = {}
    for entity in test_set.get_sti_series()[:100]:
        cont_sim = ContSimulator(tirp_comp_list=tirp_comp_models, entity=entity)
        cont_sim.predict_proba_plus_time(prob_cls_name=const.MOD_CLS_XGB_NAME,
                                         time_cls_model=const.MOD_REG_GAM_GLM_NAME)
        cont_sim.agg_prob_plus_time(agg_func=const.AGG_FUN_MEAN)
        pred_over_time[entity.get_series_id()] = cont_sim.get_agg_pred()
        cont_sim.plot_prediction()

    # Evaluates the learned model
    eval_model = Evaluate(actual_labels=test_set_labels,
                          actual_event_time=test_set_times,
                          pred_over_time=pred_over_time)
    auc_roc, auc_prc = eval_model.evaluate_per_w_tau(eval_model=eval_model, tau=0, w=5)
    print(f'AUC-ROC: {auc_roc}, AUPRC: {auc_prc}')
