import streamlit as st
import pandas as pd
import numpy as np
from annotated_text import annotated_text

st.set_page_config(page_title="서비스명", page_icon=None, layout="wide", initial_sidebar_state="expanded", menu_items=None)

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


tab1, tab2 = st.tabs(["공시분석", "뉴스분석"])

with st.sidebar:
    st.text('서비스명')
    st.radio('뷰티인사이드', ('자사 분석', '산업군 분석'))

tab1.write('2021 지속가능경영보고서, 2022.07.04 기준')

tab1.tab_e, tab1.tab_s, tab1.tab_s = st.tabs(["&nbsp;&nbsp;&nbsp;E&nbsp;&nbsp;&nbsp;", "&nbsp;&nbsp;&nbsp;S&nbsp;&nbsp;&nbsp;", "&nbsp;&nbsp;&nbsp;G&nbsp;&nbsp;&nbsp;"])

path = '../1. preprocessing/1-2. ESG report/output/hyundaehomeshopping_2023.csv'
df = pd.read_csv(path)


with tab1.tab_e:
    c1, c2, c3, c4, c5 = st.columns([1,1,1,1,1])
    e_df = df[df['label']=='e']
    c1.write(e_df.iloc[0,0])
    c1.write(e_df.iloc[0,1])
    # c1.metric(e_df.iloc[0,0], e_df.iloc[0,1], delta=None, delta_color="normal", help=None, label_visibility="visible")
    c2.metric(e_df.iloc[1,0], e_df.iloc[1,1], delta=None, delta_color="normal", help=None, label_visibility="visible")
    c3.metric(e_df.iloc[2,0], e_df.iloc[2,1], delta=None, delta_color="normal", help=None, label_visibility="visible")
    c4.metric(e_df.iloc[3,0], e_df.iloc[3,1], delta=None, delta_color="normal", help=None, label_visibility="visible")
    c5.metric(e_df.iloc[4,0], e_df.iloc[4,1], delta=None, delta_color="normal", help=None, label_visibility="visible")
    