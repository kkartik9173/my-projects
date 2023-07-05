from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import pandas as pd

df = pd.read_csv("data.csv")

# Assuming df is your DataFrame

# Shift the 'Signal' column to align with the features at the previous time step
df['Shifted_Signal'] = df['Signal'].shift(-1)

# Drop the last row, which will have a NaN 'Shifted_Signal'
df = df.dropna()

# Encode 'Shifted_Signal' to numerical values
le = LabelEncoder()
df['Encoded_Signal'] = le.fit_transform(df['Shifted_Signal'])

# Define features and target
X = df[['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits', 'RSI']]
y = df['Encoded_Signal']

# Split the data into train and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Logistic Regression model
clf = LogisticRegression(max_iter=1000)
clf.fit(X_train, y_train)

# Predict on the validation set
y_pred = clf.predict(X_val)

from joblib import dump

# Save model
dump(clf, 'clf.joblib')

# Save label encoder
dump(le, 'le.joblib')

# Print classification metrics
print(classification_report(y_val, y_pred, target_names=le.classes_))
