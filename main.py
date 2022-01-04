import pandas as pd

from script.cummulative import *
from script.daily import *

from os.path import dirname, join
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs
from bokeh.io import show, output_file

output_file("tubes.html")

df = pd.read_csv(
    join(dirname(__file__), "data", "imp_line_covid.csv"), index_col=0
).dropna()

df["Date"] = pd.to_datetime(df["Date"], format="%Y/%m/%d")

tab1 = daily(df)
tab2 = cummulative(df)

tab = Tabs(tabs=[tab1, tab2])

curdoc().add_root(tab)
curdoc().title = "World Corona Cases"

show(curdoc)
