import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

g = 9.8
rho = 1000

def check_interval():
    interval_lake_df = pd.DataFrame({"Date Time, GMT-07:00":
                                         pd.date_range(start="05/30/23 10:00:00", end="08/07/23 18:00:00", freq="30T")})
    interval_air_df = pd.DataFrame({"Date Time, GMT-07:00":
                                        pd.date_range(start="05/30/23 10:00:00", end="08/30/23 10:30:00", freq="30T")})
    merge_lake = pd.merge(lake_df, interval_lake_df, on="Date Time, GMT-07:00", how='inner')

    merge_air = pd.merge(air_df, interval_air_df, on="Date Time, GMT-07:00", how='inner')
    lake_air_comp = pd.merge(lake_air_merge, lake_df, on="Date Time, GMT-07:00", how='inner')
    print(
        f'Is Lake pressure data consistence to 30 minutes interval: {merge_lake.shape[0] == interval_lake_df.shape[0]}')
    print(
        f'Is Air pressure data consistence to 30 minutes interval: {merge_air.shape[0] == interval_air_df.shape[0]}')
    print(
        f'If the inner merge of Lake and Air pressure data consistence to 30 minutes interval: {lake_air_comp.shape[0] == interval_lake_df.shape[0]}')

if __name__ == '__main__':
    lake_df = pd.read_csv("raw_data/20095431_LakeLevel.csv",
                          parse_dates=["Date Time, GMT-07:00"], date_format='%m/%d/%y %I:%M:%S  %p')
    air_df = pd.read_csv("raw_data/21248883_AirPressure.csv",
                         parse_dates=["Date Time, GMT-07:00"], date_format='%m/%d/%y %I:%M:%S  %p')

    lake_air_merge = pd.merge(lake_df, air_df, on="Date Time, GMT-07:00", how='inner')
    lake_air_merge = lake_air_merge.rename(columns={"Abs Pres, kPa (LGR S/N: 20095431, SEN S/N: 20095431)": "Lake+Air pressure (kpa)",
                                                    "Temp, °C (LGR S/N: 20095431, SEN S/N: 20095431)": "Lake Temp (°C)",
                                                    "Abs Pres, kPa (LGR S/N: 21248883, SEN S/N: 21248883)": "Air pressure (kpa)",
                                                    "Temp, °C (LGR S/N: 21248883, SEN S/N: 21248883)": "Air Temp (°C)"
                                                    })
    lake_air_merge["Lake pressure (kpa)"] = lake_air_merge["Lake+Air pressure (kpa)"] - lake_air_merge["Air pressure (kpa)"]
    lake_air_merge["Lake depth (m)"] = (lake_air_merge["Lake pressure (kpa)"] * 1000) / (g * rho)
    lake_air_merge.to_csv("Lake_air_pressure.csv", index=False)
