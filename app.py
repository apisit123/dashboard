import time  # to simulate a real time data, time loop

import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import streamlit as st  # 🎈 data web app development

import pydeck as pdk
import streamlit as st
import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import pytz
from datetime import datetime, timezone, timedelta

import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

st.set_page_config(
    page_title="Real-Time Data Science Dashboard",
    page_icon="✅",
    layout="wide",
)

# dashboard title
st.title("Real-Time / Live Data Science Dashboard")

# with st.sidebar:
#     with st.echo():
#         st.write("This code will be printed to the sidebar.")

#     with st.spinner("Loading..."):
#         time.sleep(5)
#     st.success("Done!")

# creating a single-element container
placeholder = st.empty()

count = 1


req = requests.get('http://128.199.136.204:1880/temp_all');
req= req.json()

ts = pd.DataFrame.from_dict(req)
filter_timestamp = ts[['timestamp']].iloc[0]

# st.write(filter_timestamp[0])
req2 = requests.get('http://128.199.136.204:1880/product_count?ts='+ filter_timestamp[0]) 
req2 = req2.json()

le = len(req)
ids = req[le-1]["id"]

le2 = len(req2)
ids2 = req2[le2-1]["id"]

tz = timezone(timedelta(hours = 7))
# near real-time / live feed simulation
threshold = 5


while True:

    r = requests.get('http://128.199.136.204:1880/temp?id='+str(ids))
    r = r.json()

    r2 = requests.get('http://128.199.136.204:1880/product_count_id?id='+str(ids2))
    r2 = r2.json()


    if len(r) > 0 and len(r2) > 0:

        if r[0] is not None:
            req.append(r[0])

        if r2[0] is not None:
            req2.append(r2[0])
        ids += 1
        ids2 += 1

        df = pd.DataFrame.from_dict(req)
        df = df[['timestamp','value', 'id']]

        df.timestamp = pd.to_datetime(df.timestamp)

        df2 = pd.DataFrame.from_dict(req2)
        df2 = df2[['id', 'timestamp', 'product_count_fg']]

        df2.timestamp = pd.to_datetime(df2.timestamp)

        df3 = pd.merge_asof(df, df2, on='timestamp')
        df3 = df3.fillna(0)


        df3.set_index(df3.timestamp,inplace=True)

        t1 = df3.timestamp[0].tz_convert(None)
        dfFreezer = pd.pivot_table(df, values='value', index=df3.index)
        dfFreezer.columns = ['°C']

        dfCnt = pd.pivot_table(df3, values='product_count_fg', index=df3.index)
        dfCnt.columns = ['bk/min']

        xx = int(df3['product_count_fg'].sum())
        rt = df3[df3.value < -20].count()
        runtime = rt[0]/60

        nrt = df3[df3.product_count_fg > 0].count()
        net_runtime = nrt[0]/60

        t2 = datetime.now()


        all_time = rt[0] / ((t2-t1).total_seconds() // 60.0)
        # st.write(all_time)

        a = (net_runtime / runtime) * 100
        p = ((xx / net_runtime) / 715) * 100
        q = 100

        all_oee = (a * p * q ) / 10000
        with placeholder.container():
        
            # st.dataframe(data)

            row2_1, row2_2, row2_3 = st.columns((4, 2, 2))

            with row2_1:
                with st.expander("Freezer Temperation (°C)", True):

                    st.line_chart(dfFreezer, height=226)


                with st.expander("Product IN (basket/min)", True):
                    st.line_chart(dfCnt, height=226)

            with row2_2:
                
                with st.container():
                    with st.expander("Product Count", True):
                        # st.header("")
                        # st.markdown("<h2 style='text-align: center; color: grey;'>Product Count</h2>", unsafe_allow_html=True)
                        st.markdown("<h1 style='text-align: center; color: grey;'>"+str(xx)+"</h1>", unsafe_allow_html=True)
                        st.markdown("<h3 style='text-align: center; color: grey;'>pcs</h3>", unsafe_allow_html=True)



                with st.container():
                    with st.expander("Runtime (hr)", True):
                        st.markdown("<h2 style='text-align: center;'>"+str("{:.1f}".format(runtime))+"</h2>", unsafe_allow_html=True)
                        my_bar = st.progress(0)
                        my_bar.progress(70)
                        st.header("\n")
                with st.container():
                    with st.expander("Net Runtime (hr)", True):
                        st.markdown("<h2 style='text-align: center;'>"+str("{:.1f}".format(net_runtime))+"</h2>", unsafe_allow_html=True)
                        my_bar = st.progress(0)
                        my_bar.progress(60)
                        st.header("\n")

            with row2_3:
                with st.container():
                    with st.expander("OEE", True):

                        st.markdown("<h3 style='text-align: center; color: grey;'>Overall OEE : "+str("{:.1f}".format(all_oee))+"%</h3>", unsafe_allow_html=True)
                        st.header("\n")

                        fig = make_subplots (rows=3,cols=1,
                                     specs=[[{"type": "pie"}], [{"type": "pie"}], [{"type": "pie"}]])


                        fig.add_trace(go.Pie(labels=['',''],
                                              values=[a,100-a],
                                              hole=0.7,
                                              textinfo='none',
                                              marker_colors=['rgb(113,209,145)','rgb(240,240,240)'],
                                              ),row=1, col=1)

                        fig.add_trace(go.Pie(labels=['',''],
                                              values=[p,100-p],
                                              hole=0.7,
                                              textinfo='none',
                                              marker_colors=['rgb(113,209,145)','rgb(240,240,240)'],
                                              ),row=2, col=1)

                        fig.add_trace(go.Pie(labels=['',''],
                                              values=[q,100-q],
                                              hole=0.7,
                                              textinfo='none',
                                              marker_colors=['rgb(113,209,145)','rgb(240,240,240)'],
                                              ),row=3, col=1)

                        fig.update_layout(annotations=[dict(text="Q  : "+str("{:.1f}".format(q))+"%", x=0.5, y=0.1, font_size=15, showarrow=False),
                                                       dict(text="P : "+str("{:.1f}".format(p))+"%", x=0.5, y=0.5, font_size=15, showarrow=False),
                                                       dict(text="A : "+str("{:.1f}".format(a))+"%", x=0.5, y=0.9, font_size=15, showarrow=False),
                                                      ])
                        fig.update_layout(showlegend=False)
                        fig.update_layout(margin=dict(l=0,r=0,b=0,t=0))
                        fig.update_layout(font_family="'Roboto', sans-serif")
                        st.plotly_chart(fig, use_container_width=True)

    count += 1
    time.sleep(30)
