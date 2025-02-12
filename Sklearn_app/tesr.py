# Import Libraries
from sklearn.datasets import load_digits
import pandas as pd

# Load Digits dataset
digits = load_digits()

# X Data
X = pd.DataFrame(digits.data)

# y Data
y = pd.Series(digits.target, name="target")
print([digits.images[:5]].shape)