class ConstCls:
    """
    In cases there are one unique value in the labels list
    it could be occur for example when the patterns found only in entities with the event of interest
    """
    def __init__(self, cons_val: int):
        self.const_val = cons_val

    def predict_proba(self):
        return self.const_val
