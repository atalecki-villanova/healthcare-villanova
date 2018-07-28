import time
import pickle
import numpy as np
import pandas as pd


from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression

import connect

conn = connect.MySqlConnect('localhost', 'root', 'root', 'sampledb')

#data = pd.read_csv('data.csv', index_col=False)
data = pd.read_sql("SELECT * FROM UW_Data", conn)
print(data.head(5))

Y = data['diagnosis'].values
X = data.drop('diagnosis', axis=1).values

# Below shows SVC is better than Logistics model; DO NOT NEED FOR PRODUCTION!
num_folds = 10
kfold = KFold(n_splits=num_folds, random_state=123)
start = time.time()
cv_results = cross_val_score(LogisticRegression(), X, Y, cv=kfold, scoring='accuracy')
end = time.time()
print("Logistics regression accuracy: %f, run time: %f)" % (cv_results.mean(), end - start))

start = time.time()
scaler = StandardScaler().fit(X)
X_scaled = scaler.transform(X)
cv_results = cross_val_score(SVC(C=2.0, kernel="rbf"), X_scaled, Y, cv=kfold, scoring='accuracy')
end = time.time()
print("SVC accuracy: %f, run time: %f)" % (cv_results.mean(), end - start))

# THIS IS WHAT IS NEEDED FOR PRODUCTION TO ESTIMATE THE MODEL
scaler = StandardScaler().fit(X)
X_scaled = scaler.transform(X)
model = SVC(C=2.0, kernel='rbf', probability=True)
model.fit(X_scaled, Y)

pickled_model = pickle.dumps(model)


# THIS IS WHAT IS NEEDED FOR PREDICTION
restored_model = pickle.loads(pickled_model)
X_test_scaled = scaler.transform(X[10, :].reshape(1, -1))
predictions = restored_model.predict(X_test_scaled)
probability = restored_model.predict_proba(X_test_scaled)

print("Predicted: {}, with probability: {}, actual: {}".format(
    predictions[0], probability[0], Y[10]))

connect.MySQLInsertModel(conn, pickled_model, cv_results.mean(), "sampledb.UW_Data", len(data.index))
