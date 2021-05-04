#!/usr/bin/env python
from app import AWS
import os
import pandas as pd
import numpy as np

aws = AWS()

photos_fire     = os.listdir("./data/FireImages")
photos_not_fire = os.listdir("./data/NotFireImages")
photos_fire_full = ["./data/FireImages/"+s for s in photos_fire]
photos_not_fire_full = ["./data/NotFireImages/"+s for s in photos_not_fire]

personFoundFire, personConfidenceFire, fireFoundFire, fireConfidenceFire, errorFire = aws.__rekogMulti__(photos_fire_full)
personFoundNotF, personConfidenceNotF, fireFoundNotF, fireConfidenceNotF, errorNotF = aws.__rekogMulti__(photos_not_fire_full)

data = np.array([fireFoundFire+fireFoundNotF,
                 list(np.ones(len(fireFoundFire))) + list(np.zeros(len(fireFoundNotF))),
                 errorFire + errorNotF])

df = pd.DataFrame(data=data.T, index=photos_fire+photos_not_fire, columns=["Predicted", "Real", "Error"])
df["Predicted"] = df["Predicted"].astype("int")
df["Real"] = df["Real"].astype("int")
df["Error"] = df["Error"].astype("int")
df.to_csv("./data/output.csv")