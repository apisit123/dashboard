# -*- coding: utf-8 -*-
# Copyright 2018-2022 Streamlit Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""An example of showing geographic data."""

import altair as alt
import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st
import plotly.figure_factory as ff

import plotly.graph_objects as go
from plotly.subplots import make_subplots

import matplotlib.pyplot as plt

# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.set_page_config(layout="wide", page_title="NYC Ridesharing Demo", page_icon=":taxi:")


row2_1, row2_2, row2_3 = st.columns((4, 2, 2))

with row2_1:
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['a', 'b', 'c'])

    st.area_chart(chart_data)



    chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])

    st.area_chart(chart_data)

with row2_2:
    
    with st.container():
        with st.expander("Product Count", True):
            # st.header("")
            # st.markdown("<h2 style='text-align: center; color: grey;'>Product Count</h2>", unsafe_allow_html=True)
            st.markdown("<h1 style='text-align: center; color: grey;'>8,000</h1>", unsafe_allow_html=True)
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

            st.markdown("<h3 style='text-align: center; color: grey;'>Overall OEE : 10%</h3>", unsafe_allow_html=True)
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


            st.plotly_chart(fig, use_container_width=True)
            
