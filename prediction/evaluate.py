import numpy as np

from prediction.pred_at_time import PredAtTime

from sklearn.metrics import auc


class Evaluate:
    def __init__(self, actual_labels, actual_event_time, pred_over_time):
        self._actual_labels = actual_labels
        self._actual_event_time = actual_event_time
        self._pred_over_time = pred_over_time

    def make_decisions(self, theta, tau):
        entities_decisions = {}
        for entity_id, entity_pred in self._pred_over_time.items():
            decision = False
            decision_time = 0

            exceeded_time = 0
            for t in sorted(entity_pred, key=lambda key: int(key)):
                decision_time = t
                pred_at_time = entity_pred[t]
                p = pred_at_time.get_pred_prob()
                if p > theta:
                    exceeded_time += 1
                    if exceeded_time == tau:
                        decision = True
                        break
                else:
                    exceeded_time = 0

            entities_decisions[entity_id] = PredAtTime(curr_time=decision_time,
                                                       pred_prob=entity_pred[decision_time].get_pred_prob(),
                                                       est_tte=entity_pred[decision_time].get_est_tte(),
                                                       decision=decision)
        return entities_decisions

    def compute_confusion_matrix(self, entities_decisions, w):
        """
        This function returns the confusion matrix
        :param entities_decisions: the decision for each entity
        :param w: the window size
        :return: True Positive (TP), or False Positive (FP),
        which could be False Ture Positive (FTP ) or False False Positive (FFP).
        TP is the case when the event actually occurred within the time window [est_tte−w, est_tte+w].
        FTP is the case when the event actually was not occurred within the time window.
        FFP is the case when the event has not occurred within the time window.
        """
        tp, fp, tn, fn, ftp, ffp = 0, 0, 0, 0, 0, 0
        for entity_id, pred_at_time in entities_decisions.items():
            dec = pred_at_time.get_decision()
            actual_dec = self._actual_labels[entity_id]

            curr_time = pred_at_time.get_curr_time()
            tte_est = pred_at_time.get_est_tte()
            actual_time = self._actual_event_time[entity_id]

            if dec:
                if actual_dec and (curr_time + tte_est - w) <= actual_time <= (curr_time + tte_est + w):
                    tp += 1
                else:
                    fp += 1
                    if actual_dec:
                        ftp += 1
                    else:
                        ffp += 1
            else:
                if actual_dec:
                    fn += 1
                else:
                    tn += 1
        return tp, fp, tn, fn, ftp, ffp

    @staticmethod
    def compute_tpr_fpr_precision(fn, fp, tn, tp):
        # This function returns the TPR (or recall), FPR and precision
        tpr = 0 if tp == 0 and fn == 0 else tp / (tp + fn)
        fpr = 0 if fp == 0 and tn == 0 else fp / (fp + tn)

        recall = tpr
        precision = 0 if tp == 0 and fp == 0 else tp / (tp + fp)

        return tpr, fpr, precision, recall

    @staticmethod
    def compute_auc_roc(fpr_list, tpr_list):
        # For monotonic increasing FPR
        fpr_list, tpr_list = zip(*sorted(zip(fpr_list, tpr_list), reverse=True))
        return auc(x=fpr_list, y=tpr_list)

    @staticmethod
    def compute_auc_prc(recall_list, precision_list):
        # For monotonic increasing recall
        recall_list, precision_list = zip(*sorted(zip(recall_list, precision_list), reverse=True))

        return auc(x=recall_list, y=precision_list)

    @staticmethod
    def evaluate_per_w_tau(eval_model, tau, w):
        tpr_list, fpr_list, recall_list, precision_list = [], [], [], []

        for theta in np.arange(-0.1, 1.1, 0.1).round(decimals=2):
            decisions = eval_model.make_decisions(theta=theta, tau=tau)
            tp, fp, tn, fn, ftp, ffp = eval_model.compute_confusion_matrix(entities_decisions=decisions, w=w)
            tpr, fpr, precision, recall = eval_model.compute_tpr_fpr_precision(fn=fn, fp=fp, tn=tn, tp=tp)
            tpr_list.append(tpr)
            fpr_list.append(fpr)
            recall_list.append(recall)
            precision_list.append(precision)

        auc_roc = eval_model.compute_auc_roc(fpr_list=fpr_list, tpr_list=tpr_list)
        auc_prc = eval_model.compute_auc_prc(recall_list=recall_list, precision_list=precision_list)
        return auc_roc, auc_prc
