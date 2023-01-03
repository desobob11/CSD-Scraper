'''
    949eb6c5d3061308be1382734d5e6df61d56b15c16b7db0cf85a75bfdc0a34b0
'''
'''
    Above is a tag confirming that this scraper is written by me using the proper format.
    This means that it will make this file visible to the SQL Driver setup application
'''
import bs4.element
import numpy as np
import pandas as pd
import datetime as dt
import time as t
import selenium.webdriver as wd
import bs4 as bs
import requests
import warnings
import psycopg2 as pg
import sqlalchemy as sql
import pickle
# 
'''
    949eb6c5d3061308be1382734d5e6df61d56b15c16b7db0cf85a75bfdc0a34b0
'''

warnings.simplefilter("ignore")


config = None

file_name = __file__.split("\\")[-1]
parent_dir = __file__.removesuffix("\\scrapers\\%s" % file_name)
with open("%s\\pickles\\%s.pickle" % (parent_dir, file_name), "rb") as pkl:
    config = pickle.load(pkl)

engine = sql.create_engine(config[0])
schema = config[1][0]
table_name = config[1][1]




URL = "http://ets.aeso.ca/ets_web/ip/Market/Reports/CSDReportServlet"

now = dt.datetime.now()
version_stamp = dt.datetime.strftime(now, "%Y-%m-%d %H:%M:%S")
time_stamp = dt.datetime.strftime(now, "%Y-%m-%d %H:00:00")
hour_ending = now.hour + 1
last_update = None



FUEL_TYPES = {"GAS": None,
              "HYDRO": None,
              "ENERGY STORAGE": None,
              "SOLAR": None,
              "BIOMASS AND OTHER": None,
              "DUAL FUEL" : None,
              "COAL" : None}



source = requests.get(URL).text
soup = bs.BeautifulSoup(source, "html.parser")

tables = soup.find_all("table")
tds = soup.find_all("td")

for i in tds:
    if "Last Update" in i.text:
        str_update = i.text.replace("Last Update : ", "").strip()
        datetime_update = dt.datetime.strptime(str_update, "%b %d, %Y %H:%M")
        last_update = dt.datetime.strftime(datetime_update, "%Y-%m-%d %H:%M:%S")

                       


fuel_type_tables = [str(i) for i in tables if "SUMMARY" not in str(i) and "GENERATION"
                    not in str(i) and "INTERCHANGE" not in str(i)]

fuel_dict = {}
sub_dict = {}

for i in fuel_type_tables:
    string_table = i
    for j in FUEL_TYPES.keys():
        if j in string_table:
            FUEL_TYPES[j] = pd.read_html(string_table)[0]


sub_columns = ["ASSET", "MC", "TNG", "DCR", "FUEL_TYPE", "SUB_FUEL_TYPE"]



matrix = []

for i in FUEL_TYPES.keys():
    df = FUEL_TYPES[i]
    if i != "GAS" and not len(df) <= 1:
        mc = df[df.columns[1]].to_list()
        bool_mask = []
        for j in range(len(mc)):
            val = True
            try:
                check = int(mc[j])
            except ValueError:
                val = False

            bool_mask.append(val)


        df["check"] = bool_mask
        df["FUEL_TYPE"] = [i for j in range(len(df))]
        df["SUB_FUEL_TYPE"] = ["" for j in range(len(df))]


        df = df[df["check"]].drop("check", axis=1).to_numpy().tolist()



        for j in df:
            matrix.append(j)


df = FUEL_TYPES["GAS"]
df = df[df[df.columns[1]] != "MC"]


mc = df[df.columns[1]].to_list()
indices = []
for i in range(len(df)):
    try:
        check = int(mc[i])
    except ValueError:
        indices.append(i)


sub_gas_types = {}
for i in indices:
    sub_gas_types[i] = df.iloc[i, 0]


for i in range(0, len(indices)):
    if i == len(indices) - 1:
        sub_df = df[indices[i]:]
    else:
        sub_df = df[indices[i]:indices[i + 1]]

    mc = sub_df[sub_df.columns[1]].to_list()
    bool_mask = []
    for j in range(len(mc)):
        val = True
        try:
            check = int(mc[j])
        except ValueError:
            val = False

        bool_mask.append(val)

    sub_df["check"] = bool_mask
    sub_df["FUEL_TYPE"] = ["GAS" for j in range(len(sub_df))]
    sub_df["SUB_FUEL_TYPE"] = [sub_gas_types[indices[i]] for j in range(len(sub_df))]

    sub_df = sub_df[sub_df["check"]].drop("check", axis=1).to_numpy().tolist()



    for j in sub_df:
        matrix.append(j)

final_df = pd.DataFrame(matrix, columns=sub_columns)

asset_list = final_df["ASSET"].to_list()

asset_short_name = []
asset_long_name = []
net_to_grid = []
energy_storage = []


for i in asset_list:
    left_bracket = i.find("(")
    right_bracket = i.find(")")

    short_name = i[left_bracket + 1: right_bracket]
    long_name = i.split("(")[0].rstrip()

    asset_short_name.append(short_name)
    asset_long_name.append(long_name)
    if "*" in i:
        net_to_grid.append("yes")
    else:
        net_to_grid.append("")

    if "^" in i:
        energy_storage.append("yes")
    else:
        energy_storage.append("")


final_df.insert(0, "ASSET_SHORT_NAME", asset_short_name)
final_df.insert(0, "ASSET_LONG_NAME", asset_long_name)
final_df["NET_TO_GRID"] = net_to_grid
final_df["ENERGY_STORAGE_HYBRID"] = energy_storage
final_df = final_df.drop("ASSET", axis=1)

final_df.insert(0, "HE", [hour_ending for i in range(len(final_df))])
final_df.insert(0, "EFFECTIVE_TIME", [time_stamp for i in range(len(final_df))])
final_df["VERSION_TIME"] = [version_stamp for i in range(len(final_df))]
final_df["AESO_TIME"] = [last_update for i in range(len(final_df))]


conn = pg.connect(database="postgres", user="postgres",
            password="walterw123", host="localhost", port="5432")

#engine = sql.create_engine("postgresql://postgres:walterw123@localhost:5432/postgres")

#pd.DataFrame(final_df).to_sql(con=engine, schema="AESO", name="aeso_csd_t", index=False, if_exists="append")
pd.DataFrame(final_df).to_sql(con=engine, schema=schema, name=table_name, index=False, if_exists="append")