import pandas as pd
import requests
import io
from os.path import join, dirname


URL = 'https://www.gstatic.com/covid19/mobility/2020_JP_Region_Mobility_Report.csv'

r = requests.get(URL)
df = pd.read_csv(io.BytesIO(r.content),sep=",")

df = df[df["sub_region_1"] == "Shiga"]

for d in df:
    print(df)

tocsvArr = [
    'date',
    'retail_and_recreation_percent_change_from_baseline',
    'grocery_and_pharmacy_percent_change_from_baseline',
    'parks_percent_change_from_baseline',
    'transit_stations_percent_change_from_baseline',
    'workplaces_percent_change_from_baseline',
    'residential_percent_change_from_baseline'
]

outputCsv = join(dirname(__file__), "datas/mobility.csv")

df.to_csv(outputCsv, columns=tocsvArr, index=False)