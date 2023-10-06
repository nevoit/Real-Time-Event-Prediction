import warnings
import numpy as np
import pandas as pd
import scipy.stats as ss
from scipy.stats._continuous_distns import _distn_names  # ***Note*** can caused problem if removed

from prediction.model_const_cls import ConstCls


class FCPMCls:
    """
    The Fully Continuous Prediction Model (FCPM) considers the distributions of the durations between the TIRP-prefixes’
    consecutive tieps, in addition to the TIRP-prefixes’ number of occurrences in the DB.
    The FCPM uses these distributions to estimate the TIRP’s completion given the durations between the tieps
    in the TIRP-prefix ptc of Q observed at any time point tc .
    """

    def __init__(self, db_entities_num: int, params: dict):
        self._db_entities_num = db_entities_num
        # Assumption: fit() gets X with index with the format 'entityID_instanceID_Timestamp'
        self._x_train_index_order = ['entityID', 'instanceID', 'Timestamp']

        self._epsilon = params['epsilon']
        self._uncertainty_prob = params['uncertainty_prob']
        self._sample_to_gen = params['sample_to_gen']
        self._distributions = params['distributions']
        self._default_dist = params['default_dist']
        self._default_dist_param = params['default_dist_param']

        self._dur_w = None
        self._dist_pdf_w = {}
        self._dist_cdf_w = {}
        self._pr_ptc_stc = None  # Pr(ptc, stc)

        self._dur_wo = None
        self._dist_pdf_wo = {}
        self._dist_cdf_wo = {}
        self._pr_ptc_not_stc = None  # Pr(ptc, NOT stc)

        self._di_len = -1
        self._const_val = None

    def fit(self, X, y):
        """
        This function learns a model
        :param X: the dataframe train
        :param y: the labels
        :return:
        """
        unique_values = y.unique()
        if len(unique_values) == 1:  # for cases of a single class
            single_class = unique_values[0]
            self._const_val = ConstCls(cons_val=single_class)
        else:
            self._extract_durations(X=X, y=y)
            self._assign_cdf_pdf(durs=self._dur_w, pdfs=self._dist_pdf_w, cdfs=self._dist_cdf_w)  # with event
            self._assign_cdf_pdf(durs=self._dur_wo, pdfs=self._dist_pdf_wo, cdfs=self._dist_cdf_wo)  # without event
            self._di_len = max(self._dur_w.keys())  # number of duration components

    def _assign_cdf_pdf(self, durs: dict, pdfs: dict, cdfs: dict):
        # This function assigns the pdf and cdf to the relevant dictionaries
        for i, durations in durs.items():
            pdf, cdf = self._get_pdf_cdf(durations)
            pdfs[i] = pdf
            cdfs[i] = cdf

    def _extract_durations(self, X, y):
        # This function creates the durations histograms for learning the relevant distributions later
        X_end, y_end = self._get_end_durations(X, y)

        self._dur_w, self._pr_ptc_stc = self._create_dur(rel_class=1, X_end=X_end, y_dur=y_end)
        self._dur_wo, self._pr_ptc_not_stc = self._create_dur(rel_class=0, X_end=X_end, y_dur=y_end)

    def _create_dur(self, rel_class, X_end, y_dur):
        # This function creates the duration dictionary and prior probability for each duration component
        y_indices = y_dur.loc[lambda x: x == rel_class]
        X_end_dur = X_end.loc[y_indices.index]
        durs = {i: X_end_dur[i].to_numpy() for i in range(X_end_dur.shape[1])}
        prior_prob = len(y_indices) / self._db_entities_num
        return durs, prior_prob

    def _get_end_durations(self, X, y):
        # Only the final duration of a prefix is interesting in this model
        # Thus, we want to take only the last timestamp for each instance and to learn the relevant durations
        rows_details = pd.DataFrame(X.index.str.split('_').tolist(), columns=self._x_train_index_order)
        rows_details[self._x_train_index_order] = rows_details[self._x_train_index_order].apply(pd.to_numeric)
        max_time_per_ent_inst = rows_details.groupby(self._x_train_index_order[:2],
                                                     as_index=False)[self._x_train_index_order[-1]].max()
        max_time_indices = pd.merge(rows_details, max_time_per_ent_inst, on=self._x_train_index_order,
                                    how="outer", indicator=True).query('_merge=="both"').index  # only both rows
        return X.iloc[max_time_indices], y.iloc[max_time_indices]

    def _get_pdf_cdf(self, durations):
        # This function computes the PDF and CDF given the duration
        # Based on this comment: https://stackoverflow.com/a/37616966/14076446
        best_dist, best_fit_params = self._compute_best_dist(durations=durations)
        pdf, cdf = self._create_pdf_cdf(dist=best_dist, params=best_fit_params)
        return pdf, cdf

    def _create_pdf_cdf(self, dist, params):
        # This function generates PDF and CDF given the best distribution and parameters
        # Separate parts of parameters
        arg = params[:-2]
        loc = params[-2]
        scale = params[-1]

        # Get sane start and end points of distribution
        start = dist.ppf(0.01, *arg, loc=loc, scale=scale) if arg else dist.ppf(0.01, loc=loc, scale=scale)
        end = dist.ppf(0.99, *arg, loc=loc, scale=scale) if arg else dist.ppf(0.99, loc=loc, scale=scale)

        # Build PDF and turn into pandas Series
        x = np.linspace(start, end, self._sample_to_gen)
        y = dist.pdf(x, loc=loc, scale=scale, *arg)
        pdf = pd.Series(data=y, index=x)  # a matrix of x and y, where x is the indices and y are the values
        if np.isinf(pdf).any():
            pdf[np.isinf(pdf)] = 0
        cdf = pdf.cumsum() / pdf.sum()

        return pdf, cdf

    def _compute_best_dist(self, durations: list):
        # This function find the best distribution and returns its best parameters
        data = pd.Series(durations)
        num_of_bins = len(np.histogram_bin_edges(a=data, bins='fd'))
        best_fit_name, best_fit_params = self._best_fit_distribution(data=data, bins=num_of_bins)
        best_dist = getattr(ss, best_fit_name)
        return best_dist, best_fit_params

    def _best_fit_distribution(self, data, bins):
        # Model data by finding best fit distribution to data
        # Get histogram of original data
        y, x = np.histogram(data, bins=bins, density=True)
        x = (x + np.roll(x, -1))[:-1] / 2.0

        # Best holders
        best_distribution = self._default_dist
        best_params = self._default_dist_param
        best_sse = np.inf

        # Estimate distribution parameters from data
        for distribution in self._distributions:
            try:  # Try to fit the distribution
                with warnings.catch_warnings():
                    warnings.filterwarnings('ignore')  # Ignore warnings from data that can't be fit

                    params = distribution.fit(data)  # fit dist to data
                    arg = params[:-2]  # Separate parts of parameters
                    loc = params[-2]
                    scale = params[-1]

                    # Calculate fitted PDF and error with fit in distribution
                    pdf = distribution.pdf(x, loc=loc, scale=scale, *arg)
                    sse = np.sum(np.power(y - pdf, 2.0))

                    # identify if this distribution is better
                    if best_sse > sse > 0:
                        best_distribution = distribution
                        best_params = params
                        best_sse = sse
            except Exception:
                pass
        return best_distribution.name, best_params

    def predict_proba(self, inst):
        # This function returns the probability for observing the event of interest
        if self._const_val is not None:
            return self._const_val.predict_proba()
        else:
            psi = self._compute_psi(inst=inst, prior_prob=self._pr_ptc_stc, cdf=self._dist_cdf_w)
            not_psi = self._compute_psi(inst=inst, prior_prob=self._pr_ptc_not_stc, cdf=self._dist_cdf_wo)
            return psi / (psi + not_psi) if (psi + not_psi) != 0 else self._uncertainty_prob  # Law of total probability

    def _compute_psi(self, inst, prior_prob, cdf):
        # This function gets computes the psi\not psi probability per instance
        pi_prob = 1
        for j in range(self._di_len + 1):
            dur = int(inst.values[0][j])
            if j == self._di_len:  # censoring - not a completed duration component
                pi_prob *= self._censoring_prob(cdf=cdf[j], duration=dur)
            else:  # a completed duration component
                pi_prob *= self._calc_dist_prob(cdf=cdf[j], duration=dur)
        return prior_prob * pi_prob

    def _calc_dist_prob(self, cdf, duration):
        # This function gets the relevant cdf and the duration
        # and returns the probability for this duration in the distribution
        cdf_max = max(cdf.index.values)
        cdf_min = min(cdf.index.values)

        # in case the duration is outside of the distribution
        if duration < cdf_min and cdf_min - duration < self._epsilon:
            return self._calc_dist_prob(cdf, duration + self._epsilon)
        elif duration > cdf_max and duration - cdf_max < self._epsilon:
            return self._calc_dist_prob(cdf, duration - self._epsilon)
        elif duration < cdf_min or duration > cdf_max:  # in case the duration is outside of the distribution
            # print("Check it out! the duration is outside of the distribution")
            return self._uncertainty_prob

        top = min(cdf.index.values, key=lambda x: abs(x - (duration + self._epsilon)))
        closest_num_max = min(top, cdf_max)  # in case its after the distribution's maximum value

        bottom = min(cdf.index.values, key=lambda x: abs(x - (duration - self._epsilon)))
        closest_num_min = max(bottom, cdf_min)  # in case its before the distribution's minimum value

        prob = cdf[closest_num_max] - cdf[closest_num_min]

        # in case of scenarios that durations are the same
        if not isinstance(prob, (np.floating, float)):
            print("Check it out! the durations are the same!")
            return 1

        return prob

    @staticmethod
    def _censoring_prob(cdf, duration):
        # For the duration of the last and unfinished element of ptc(i.e., dg),
        # the probability of it belonging to a narrow interval and the exact duration is not yet known.
        opp_cdf = 1 - cdf

        bottom = min(opp_cdf.index.values, key=lambda x: abs(x - duration))
        prob = opp_cdf[bottom]

        return prob
