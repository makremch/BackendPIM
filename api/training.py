import pandas as pd
from pandas import Series
np = pd.np
import pickle
from sklearn.linear_model import LogisticRegression


data = pd.read_csv("./epilepcy.csv",sep=";")
x,y=data[data.columns[:-1]],data["cas"]
clf = LogisticRegression(random_state=0, solver='lbfgs',multi_class='multinomial').fit(x, y)
filename = 'model.sav'
pickle.dump(clf, open(filename, 'wb'))