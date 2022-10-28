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

st.set_page_config(
    page_title="Real-Time Data Science Dashboard",
    page_icon="✅",
    layout="wide",
)

# dashboard title
st.title("Real-Time / Live Data Science Dashboard")

with st.sidebar:
    with st.echo():
        st.write("This code will be printed to the sidebar.")

    with st.spinner("Loading..."):
        time.sleep(5)
    st.success("Done!")

# creating a single-element container
placeholder = st.empty()

count = 1


req = requests.get('http://128.199.136.204:1880/temp_all');
req= req.json()

le = len(req)
ids = req[le-1]["id"]


# near real-time / live feed simulation
while True:

    r = requests.get('http://128.199.136.204:1880/temp?id='+str(ids))
    r = r.json()

    req.append(r[0])

    if any(elem is not None for elem in req):

        ids += 1

        df = pd.DataFrame.from_dict(req)
        df = df[['timestamp','value', 'id']]

        df.timestamp = pd.to_datetime(df.timestamp)
        df.set_index(df.timestamp,inplace=True)

        dfFreezer = pd.pivot_table(df, values='value', index=df.index)
        dfFreezer.columns = ['°C']

        # st.dataframe(df)

        with placeholder.container():
        
            # st.dataframe(data)

            row2_1, row2_2, row2_3 = st.columns((4, 2, 2))


            with row2_1:
                with st.expander("Freezer Temperation (°C)", True):

                    st.line_chart(dfFreezer, height=226)


                with st.expander("Product IN (basket/min)", True):
                    chart_data = pd.DataFrame(
                    np.random.randn(20, 1),
                    columns=['a'])

                    st.area_chart(chart_data, height=226)

            with row2_2:
                
                with st.container():
                    with st.expander("Product Count", True):
                        # st.header("")
                        # st.markdown("<h2 style='text-align: center; color: grey;'>Product Count</h2>", unsafe_allow_html=True)
                        st.markdown("<h1 style='text-align: center; color: grey;'>"+str(count)+"</h1>", unsafe_allow_html=True)
                        st.markdown("<h3 style='text-align: center; color: grey;'>pcs</h3>", unsafe_allow_html=True)
                        st.header("\n")



                with st.container():
                    with st.expander("Runtime (hr)", True):
                        st.markdown("<h2 style='text-align: center;'>17.7</h2>", unsafe_allow_html=True)
                        my_bar = st.progress(0)
                        my_bar.progress(70)
                        st.header("\n")


                with st.container():
                    with st.expander("Net Runtime (hr)", True):
                        st.markdown("<h2 style='text-align: center;'>15.7</h2>", unsafe_allow_html=True)
                        my_bar = st.progress(0)
                        my_bar.progress(60)
                        st.header("\n")

            with row2_3:
                with st.container():
                    with st.expander("OEE", True):
                        q = 100
                        p = 60
                        a = 70

                        st.markdown("<h3 style='text-align: center; color: grey;'>Overall OEE : 60%</h3>", unsafe_allow_html=True)
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

                        fig.update_layout(annotations=[dict(text="Q  : "+str(q)+"%", x=0.5, y=0.1, font_size=15, showarrow=False),
                                                       dict(text="P : "+str(p)+"%", x=0.5, y=0.5, font_size=15, showarrow=False),
                                                       dict(text="A : "+str(a)+"%", x=0.5, y=0.9, font_size=15, showarrow=False),
                                                      ])
                        fig.update_layout(showlegend=False)
                        fig.update_layout(margin=dict(l=0,r=0,b=0,t=0))
                        fig.update_layout(font_family="'Roboto', sans-serif")


                        st.plotly_chart(fig, use_container_width=True)

    count += 1
    time.sleep(60)
