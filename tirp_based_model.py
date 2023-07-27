class TIRPBasedModel:
    def __init__(self):
        pass


class TIRPPrefixBasedModel:
    def __init__(self):
        pass


class SCPM(TIRPPrefixBasedModel):
    def __init__(self, prefixes_support: dict):
        self.prefixes_support = prefixes_support

    def predict_proba(self):
        pass


class CPML(TIRPPrefixBasedModel):
    def __init__(self):
        pass


class XGBoost(CPML):
    def __init__(self):
        pass
