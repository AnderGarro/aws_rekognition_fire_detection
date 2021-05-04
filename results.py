#!/usr/bin/env python
import pandas as pd
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sn

df = pd.read_csv("./data/output.csv")
print(df.head())

cm = confusion_matrix(df.Real, df.Predicted, normalize= "true")
df_cm = pd.DataFrame(cm,index=["Not Fire","Fire"], columns=["Not Fire","Fire"])
plt.figure(figsize = (10,7))
sn.heatmap(df_cm, annot=True)
plt.savefig('./data/confusion_matrix.jpg')
plt.show()