import pandas as pd


def GroupEstimate(object):
    def __init__(self, estimate):

        # Validate type of estimate
        if estimate not in ["mean","median"]:
            raise ValueError("estimate should be either 'mean' or 'median'")
        self.estimate = estimate
        self.group_estimates = None
        self.group_features = None
       
    def fit(self, X, y):
        return None

    def predict(self, X):
        return None