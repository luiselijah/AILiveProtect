import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# Sample data
data = {'amount': [100, 200, 150, 120],
        'location': [1, 2, 1, 3],
        'transaction_type': [1, 0, 1, 0],
        'fraud': [0, 1, 0, 1]}

df = pd.DataFrame(data)

# Features and labels
X = df[['amount', 'location', 'transaction_type']]
y = df['fraud']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

# Model
model = LogisticRegression()
model.fit(X_train, y_train)

# Prediction
predictions = model.predict(X_test)
print("Predictions: ", predictions)
