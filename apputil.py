import pandas as pd
import numpy as np


class GroupEstimate(object):
    def __init__(self, estimate):

        # Validate type of estimate
        if estimate not in ["mean","median"]:
            raise ValueError("estimate should be either 'mean' or 'median'")
        self.estimate = estimate
        self.group_estimates = None
        self.group_features = None
       
    def fit(self, X, y):

        # Validate type of input
        if not isinstance(X, pd.DataFrame):
            raise TypeError("X must be a dataframe")

        if len(X) != len(y):
            raise ValueError("X and y must have same legnth")

        # Check missing values in y
        if pd.isnull(y).any() :
            raise ValueError("y has missing values")
        
        # Combine X and y as one dataframe
        df = X.copy()
        df["y"] = y

        # Group by columns in X
        grouped = df.groupby(list(X.columns))["y"]

        # Calculate required estimate
        if self.estimate == "mean":
            result = grouped.mean()

        else:
            result = grouped.median()

        # Store results
        self.group_estimates = result.reset_index().rename(columns={"y": self.estimate})
        self.group_features = list(X.columns)

        return self
        

    def predict(self, X_):
        # check if model is fitted
        if self.group_estimates is None:
            raise ValueError("Model not fitted yet, call fit()")

        # Convert to dataframe, if needed
        X_ = pd.DataFrame(X_ , columns = self.group_features)

        # Check columns match
        if list(X_.columns) != self.group_features:
            raise ValueError("Input columns must match those used during fitting.")

        # Merge new data with group_estimates
        merged = X_.merge(self.group_estimates, on=self.group_features, how="left")

        # Count missing groups
        missing_count = merged[self.estimate].isna().sum()

        if missing_count > 0:
            print(f"{missing_count} observation(s) have unseen group combinations; returning NaN for them.")

        return merged[self.estimate].to_numpy()
    
