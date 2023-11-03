from flask import Flask, render_template
import pandas as pd


app = Flask(__name__)
df2 = pd.read_csv("Data/stations.csv")


@app.route("/")
def home_page():
    cities = df2[["sr_no", "Location_Name"]].to_html(index=False)
    return render_template("home.html", data=cities)


@app.route("/api/v1/<station>/<date>")
def dately(station, date):
    df = pd.read_csv(f"Data/{station}.csv")
    tmp = df.loc[df["time"] == date]["tavg"].squeeze()
    if tmp:
        return {"City": station, "Date": date, "Data": tmp}
    else:
        return {"City": station, "Date": date,
                "Data": "data not available"}


@app.route("/api/v1/<station>")
def stationly(station):
    df = pd.read_csv(f"Data/{station}.csv")
    station_data = df.to_dict(orient="records")
    return station_data


@app.route("/api/v1/<station>/<year>/yearly")
def yearly(station, year):
    df = pd.read_csv(f"Data/{station}.csv")
    df["time"] = df["time"].astype(str)
    yearly_data = (df.loc[df["time"].str.endswith(str(year))]
                   .to_dict(orient="records"))
    return yearly_data


if __name__ == "__main__":
    app.run(debug=True)
