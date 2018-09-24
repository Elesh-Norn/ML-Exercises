import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sklearn.linear_model

# Importing datas

oecd_bli = pd.read_csv("ocde_bli_2017.csv", thousands=',')
gdp_per_capita = pd.read_csv("WEO_Data.xls", thousands=',',
                             delimiter='\t', encoding='latin1', na_values="n/a")

# Preparing datas (taken from https://github.com/ageron/handson-ml/issues/33#issuecomment-357722126)

def prepare_country_stats(oecd_bli, gdp_per_capita):
    oecd_bli = oecd_bli[oecd_bli["INEQUALITY"]=="TOT"]
    oecd_bli = oecd_bli.pivot(index="Country", columns="Indicator", values="Value")
    gdp_per_capita.rename(columns={"2015": "GDP per capita"}, inplace=True)
    gdp_per_capita.set_index("Country", inplace=True)
    full_country_stats = pd.merge(left=oecd_bli, right=gdp_per_capita,
                                  left_index=True, right_index=True)
    full_country_stats.sort_values(by="GDP per capita", inplace=True)
    remove_indices = [0, 1, 6, 8, 33, 34, 35]
    keep_indices = list(set(range(36)) - set(remove_indices))
    return full_country_stats[["GDP per capita", 'Life satisfaction']].iloc[keep_indices]

country_stats = prepare_country_stats(oecd_bli, gdp_per_capita)
x = np.c_[country_stats["GDP per capita"]]
y = np.c_[country_stats["Life satisfaction"]]

country_stats.plot(kind='scatter', x="GDP per capita", y="Life satisfaction")
plt.show()

# Model choice
model = sklearn.linear_model.LinearRegression()

model.fit(x,y)
# Prediction for Chypre

X_new= [[22587]]
print(model.predict(X_new))