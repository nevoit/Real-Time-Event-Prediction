class SCPMCls:
    """
    The class implements SCPM
    """
    def __init__(self, prob):
        self.prob = prob

    def predict_proba(self, inst_row):
        # This function returns the probability for observing the event of interest
        return self.prob
