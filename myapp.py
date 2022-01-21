import pandas as pd
import numpy as np
from datetime import date

# Bokeh libraries
from bokeh.io import show, save, output_file, output_notebook
from bokeh.plotting import figure, reset_output, curdoc
from bokeh.models import ColumnDataSource, Legend
from bokeh.models.widgets import Tabs, Panel
from bokeh.models import HoverTool
from bokeh.models.widgets import DateRangeSlider
from bokeh.layouts import column, row, layout

df_currency1 = pd.read_csv("./data/currency.csv", parse_dates = ["Date"], usecols=['Date', 'Euro', 'U.S. Dollar'])
df_currency2 = pd.read_csv("./data/currency.csv", parse_dates = ["Date"], usecols=['Date', 'Indonesian Rupiah', 'U.S. Dollar'])
df_currency3 = pd.read_csv("./data/currency.csv", parse_dates = ["Date"], usecols=['Date', 'Japanese Yen', 'U.S. Dollar'])

df_currency2.rename(columns={'Indonesian Rupiah':'Rupiah'}, inplace=True)
df_currency3.rename(columns={'Japanese Yen':'Yen'}, inplace=True)

df_currency1['Date'] = pd.to_datetime(df_currency1['Date'])
df_currency2['Date'] = pd.to_datetime(df_currency2['Date'])
df_currency3['Date'] = pd.to_datetime(df_currency3['Date'])

start_date = '01-01-2017'
end_date = '05-01-2018'

mask = (df_currency1['Date'] > start_date) & (df_currency1['Date'] <= end_date)

df1 = df_currency1.loc[mask]
df1.reset_index(drop=True, inplace=True)

df2 = df_currency2.loc[mask]
df2.reset_index(drop=True, inplace=True)

df3 = df_currency3.loc[mask]
df3.reset_index(drop=True, inplace=True)

dfn_1 = df1.dropna()
dfn_2 = df2.dropna()
dfn_3 = df3.dropna()

cds_euro = ColumnDataSource(dfn_1)
cds_rupiah = ColumnDataSource(dfn_2)
cds_yen = ColumnDataSource(dfn_3)

"""# Fitur 1"""

# Membuat Figure untuk menampilkan data Euro
fig_euro = figure(
    x_axis_type='datetime',
    x_axis_label='Date',
    y_axis_label='Euro',
    title='Nilai Mata Uang Euro Kurs U.S Dollar',
    toolbar_location='below',
    plot_height=600,
    plot_width=800
)

# Untuk menampilkan line plot Euro
a = fig_euro.line(
    x='Date',
    y='Euro',
    source=cds_euro,
    color='blue',
    legend_label='Euro'
)

# Bokeh Library
tooltips = [('Euro','@Euro')]

# Menambahkan HoverTool untuk membuat fig
fig_euro.add_tools(HoverTool(tooltips=tooltips, mode='vline'))

# Euro Date Slider
euro_date_slider = DateRangeSlider(value=(min(df['Date']), max(df['Date'])),
                                    start=min(df['Date']), end=max(df['Date']))

euro_date_slider.js_link("value", fig_euro.x_range, "start", attr_selector=0)
euro_date_slider.js_link("value", fig_euro.x_range, "end", attr_selector=1)

# Membuat Figure untuk menampilkan data Euro
fig_rupiah = figure(
    x_axis_type='datetime',
    x_axis_label='Date',
    y_axis_label='Rupiah',
    title='Nilai Mata Uang Rupiah Kurs U.S Dollar',
    toolbar_location='below',
    plot_height=600,
    plot_width=800
)

# Untuk menampilkan line plot Euro
a = fig_rupiah.line(
    x='Date',
    y='Rupiah',
    source=cds_rupiah,
    color='red',
    legend_label='Indonesian Rupiah'
)

# Bokeh Library
tooltips = [('Rupiah','@Rupiah')]

# Menambahkan HoverTool untuk membuat fig
fig_rupiah.add_tools(HoverTool(
    tooltips=tooltips,
    mode='vline'
))

# Rupiah Date Slider
rupiah_date_slider = DateRangeSlider(value=(min(df['Date']), max(df['Date'])),
                                    start=min(df['Date']), end=max(df['Date']))

rupiah_date_slider.js_link("value", fig_rupiah.x_range, "start", attr_selector=0)
rupiah_date_slider.js_link("value", fig_rupiah.x_range, "end", attr_selector=1)

# Membuat Figure untuk menampilkan data Yen
fig_yen = figure(
    x_axis_type='datetime',
    x_axis_label='Date',
    y_axis_label='Yen',
    title='Nilai Mata Uang Yen Kurs U.S Dollar',
    toolbar_location='below',
    plot_height=600,
    plot_width=800
)

# Untuk menampilkan line plot Yen
a = fig_yen.line(
    x='Date',
    y='Yen',
    source=cds_yen,
    color='green',
    legend_label='Japanese Yen'
)

# Bokeh Library
tooltips = [('Yen','@Yen')]

# Menambahkan HoverTool untuk membuat fig
fig_yen.add_tools(HoverTool(
    tooltips=tooltips,
    mode='vline'
))

# Yen Date Slider
yen_date_slider = DateRangeSlider(value=(min(df['Date']), max(df['Date'])),
                                    start=min(df['Date']), end=max(df['Date']))

yen_date_slider.js_link("value", fig_yen.x_range, "start", attr_selector=0)
yen_date_slider.js_link("value", fig_yen.x_range, "end", attr_selector=1)

euro_tools = column(euro_date_slider)
rupiah_tools = column(rupiah_date_slider)
yen_tools = column(yen_date_slider)

euro_layout = row([fig_euro, euro_tools])
rupiah_layout = row([fig_rupiah, rupiah_tools])
yen_layout = row([fig_yen, yen_tools])

# Membuat tiga panel yaitu Euro,Rupiah,Yen
euro_tab = Panel(child=euro_layout, title='Euro')
rupiah_tab = Panel(child=rupiah_layout, title='Rupiah')
yen_tab = Panel(child=yen_layout, title='Yen')

tabs = Tabs(tabs=[euro_tab, rupiah_tab, yen_tab])

curdoc().add_root(tabs)
# output_file('myapp.html')
# show(tabs)