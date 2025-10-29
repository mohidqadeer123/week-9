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

        # Validate type of input
        if not isinstance(X, pd.Dataframe):
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
        

    def predict(self, X):
        return None