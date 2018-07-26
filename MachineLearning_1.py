import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import sklearn
import os
oecd_file_path = os.getcwd() + '/Datasets/datasets/lifesat/oecd_bli_2015.csv'
gdp_file_path = os.getcwd() + '/Datasets/datasets/lifesat/gdp_per_capita.csv'

print(oecd_file_path)
# load the data
oecd_bli = pd.read_csv(oecd_file_path, thousands=',')
gdp_per_capita = pd.read_csv(gdp_file_path, thousands=',', delimiter='\t', encoding='latin1', na_values="n/a")

#prep the data
# whast = oecd_bli["INEQUALITY"] == "TOT"
# print(whast)
print(oecd_bli.shape)
print(oecd_bli["INEQUALITY"].count())
print(len(oecd_bli.index))
print(oecd_bli.index)

# oecd
oecd_bli = oecd_bli[oecd_bli["INEQUALITY"] == "TOT"]
# the following won't work if there are duplicate "column" for a given index
oecd_bli = oecd_bli.pivot(index="Country", columns="Indicator", values="Value") # uses Country as the new index, uses Indicator for the columns, and Value for their values
# print(oecd_bli.head(2))
# print(oecd_bli["Life satisfaction"].head())


# gdp
gdp_per_capita.rename(columns={"2015": "GDP per capita"}, inplace=True)  # changes the column name "2015" to GDP_per_capita
gdp_per_capita.set_index("Country", inplace=True)
print(len(gdp_per_capita.index))

# mm = gdp_per_capita.index
# print(mm[1:4])
full_country_stats = pd.merge(left=oecd_bli, right=gdp_per_capita, left_index=True, right_index=True)
full_country_stats.sort_values(by="GDP per capita", inplace="True")
print('printing full country stats')
# print(full_country_stats.head(2))
print(len(full_country_stats.index))

print(full_country_stats[["GDP per capita", 'Life satisfaction']].loc["United States"]) # for index = United States, print these 2 columns
print(full_country_stats[["GDP per capita", 'Life satisfaction']].loc["Turkey"])

# do some sampling and plotting
remove_indices = [0, 1, 6, 8, 33, 34, 35]
keep_indices = list(set(range(36)) - set(remove_indices))

sample_data = full_country_stats[["GDP per capita", 'Life satisfaction']].iloc[keep_indices]
missing_data = full_country_stats[["GDP per capita", 'Life satisfaction']].iloc[remove_indices]

sample_data.plot(kind='scatter', x="GDP per capita", y='Life satisfaction', figsize=(5,3))
plt.axis([0, 60000, 0, 10])
position_text = {
    "Hungary": (5000, 1),
    "Korea": (18000, 1.7),
    "France": (29000, 2.4),
    "Australia": (40000, 3.0),
    "United States": (52000, 3.8),
    "Turkey": (9437, 9)
}
for country, pos_text in position_text.items():
    pos_data_x, pos_data_y = sample_data.loc[country]
    country = "U.S." if country == "United States" else country
    plt.annotate(country, xy=(pos_data_x, pos_data_y), xytext=pos_text,
            arrowprops=dict(facecolor='blue', width=0.5, shrink=0.1, headwidth=5))
    plt.plot(pos_data_x, pos_data_y, "ro")

plt.show()
print(sample_data.loc[list(position_text.keys())])