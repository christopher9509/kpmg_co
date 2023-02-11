import streamlit as st
import pandas as pd
import numpy as np
import os
import base64
from annotated_text import annotated_text

st.set_page_config(page_title="서비스명", page_icon=None, layout="wide", initial_sidebar_state="expanded", menu_items=None)

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


tab1, tab2 = st.tabs(["공시분석", "뉴스분석"])

with st.sidebar:
    st.text('서비스명')
    st.radio('뷰티인사이드', ('자사 분석', '산업군 분석'))

tab1.write('2021 지속가능경영보고서, 2022.07.04 기준')

tab_e, tab_s, tab_g = tab1.tabs(["&nbsp;&nbsp;&nbsp;E&nbsp;&nbsp;&nbsp;", "&nbsp;&nbsp;&nbsp;S&nbsp;&nbsp;&nbsp;", "&nbsp;&nbsp;&nbsp;G&nbsp;&nbsp;&nbsp;"])

path = '../1. preprocessing/1-2. ESG report/'
dir = path + 'output/summarized_hyundaehomeshopping_2023.csv'
df = pd.read_csv(dir)

with tab_e:
    e_df = df[df['label']=='e']
    if e_df.empty:
        tab1.tab_s.write('E와 관련된 활동 키워드가 없습니다.')
    else:
        c1, c2, c3 = st.columns([1,1,1])
        # with c1.expander(e_df.iloc[0,0]):
        #     st.write(e_df.iloc[0,1])
        # with c2.expander(e_df.iloc[1,0]):
        #     st.write(e_df.iloc[1,1])
        # with c3.expander(e_df.iloc[2,0]):
        #     st.write(e_df.iloc[2,1])
        # with c1.expander(e_df.iloc[3,0]):
        #     st.write(e_df.iloc[3,1])
        # with c2.expander(e_df.iloc[4,0]):
        #     st.write(e_df.iloc[4,1])
        # with c3.expander(e_df.iloc[5,0]):
        #     st.write(e_df.iloc[5,1])
        c1.write(e_df.iloc[0,0])
        c1.write(e_df.iloc[0,1])
        c2.write(e_df.iloc[1,0])
        c2.write(e_df.iloc[1,1])
        c3.write(e_df.iloc[2,0]) 
        c3.write(e_df.iloc[2,1])
        c4,c5,c6 = st.columns([1,1,1])
        c4.write(e_df.iloc[3,0])
        c4.write(e_df.iloc[3,1])
        c5.write(e_df.iloc[4,0])
        c5.write(e_df.iloc[4,1])
        c6.write(e_df.iloc[5,0]) 
        c6.write(e_df.iloc[5,1])
    with st.expander("더보기"):
        left = len(e_df)-6
        for i in range(left//3+1):
            globals()[f"c_{i+2}0"], globals()[f"c_{i+2}1"], globals()[f"c_{i+2}2"] = st.columns([1,1,1])
        for i, item in e_df.iterrows():
            if i<6:
                continue
            else:
                globals()[f"c_{i//3}{i%3}"].write(e_df.iloc[i,0])
                globals()[f"c_{i//3}{i%3}"].write(e_df.iloc[i,1])
        # c1, c2, c3= st.columns([1,1,1])
        # # c1.text_area(e_df.iloc[0,0], value=e_df.iloc[0,1])
        # c1.write(e_df.iloc[0,0])
        # c1.write(e_df.iloc[0,1])
        # # c1.metric(e_df.iloc[0,0], e_df.iloc[0,1], delta=None, delta_color="normal", help=None, label_visibility="visible")
        # c2.write(e_df.iloc[1,0])
        # c2.write(e_df.iloc[1,1])
        # c3.write(e_df.iloc[2,0]) 
        # c3.write(e_df.iloc[2,1])

with tab_s:
    s_df = df[df['label']=='s']
    s_df.reset_index(inplace=True, drop=True)
    if s_df.empty:
        tab1.tab_s.write('S와 관련된 활동 키워드가 없습니다.')
    else:
        c1, c2, c3, c4, c5 = st.columns([1,1,1,1,0.4])
        s_df = df[df['label']=='s']
        c1.text_area(s_df.iloc[0,0], value=s_df.iloc[0,1])
        # c1.write(s_df.iloc[0,0])
        # c1.write(s_df.iloc[0,1])
        # c1.metric(s_df.iloc[0,0], s_df.iloc[0,1], delta=None, delta_color="normal", help=None, label_visibility="visible")
        c2.metric(s_df.iloc[1,0], s_df.iloc[1,1], delta=None, delta_color="normal", help=None, label_visibility="visible")
        c3.metric(s_df.iloc[2,0], s_df.iloc[2,1], delta=None, delta_color="normal", help=None, label_visibility="visible")
        c4.metric(s_df.iloc[3,0], s_df.iloc[3,1], delta=None, delta_color="normal", help=None, label_visibility="visible")
        c5.button("더보기",key='s_more')

with tab_g:
    g_df = df[df['label']=='g']
    g_df.reset_index(inplace=True, drop=True)
    if g_df.empty:
        tab1.tab_g.write('G와 관련된 활동 키워드가 없습니다.')
    else:
        c1, c2, c3, c4, c5 = st.columns([1,1,1,1,0.4])
        c1.text_area(g_df.iloc[0,0], value=g_df.iloc[0,1])
        # c1.write(g_df.iloc[0,0])
        # c1.write(g_df.iloc[0,1])
        # c1.metric(g_df.iloc[0,0], g_df.iloc[0,1], delta=None, delta_color="normal", help=None, label_visibility="visible")
        c2.metric(g_df.iloc[1,0], g_df.iloc[1,1], delta=None, delta_color="normal", help=None, label_visibility="visible")
        c3.metric(g_df.iloc[2,0], g_df.iloc[2,1], delta=None, delta_color="normal", help=None, label_visibility="visible")
        c4.metric(g_df.iloc[3,0], g_df.iloc[3,1], delta=None, delta_color="normal", help=None, label_visibility="visible")
        c5.button("더보기",key='g_more')

c6, c7 = tab1.columns([2,1])
with c6:
    st.subheader('파일 리스트')
    url = "https://kind.krx.co.kr/common/disclsviewer.do?method=search&acptno=20221108000292&docno=&viewerhost=&viewerport="
    if st.button('KRX ESG 공시 링크'):
        st.markdown("[KRX ESG 공시 링크](%s)" % url)
    file_list = [f for f in os.listdir(path+'esg_report/') if f.startswith('hyundae')]
    selected_file = st.selectbox("Select a file:", file_list)
    
    if selected_file is not None:
        st.write('2021 지속가능경영보고서 요약본')
        with open(path+'esg_report/'+selected_file, "rb") as f:
            encoded_pdf = base64.b64encode(f.read()).decode("utf-8")
        st.markdown(f'<a href="data:application/pdf;base64,{encoded_pdf}" download={selected_file}>Download {selected_file}</a>', unsafe_allow_html=True)
        with st.expander("세부 정보 보기"):
            st.write('2021 지속가능경영보고서 요약본, 2022.07.04 기준')
            with open(path+'esg_report/'+selected_file, "rb") as f:
                encoded_pdf = base64.b64encode(f.read()).decode("utf-8")
            if st.button("Download PDF"):
                st.markdown(f'<a href="data:application/pdf;base64,{encoded_pdf}" download={selected_file}>Download {selected_file}</a>', unsafe_allow_html=True)
        # encoded_pdf
            # st.download_button('파일 다운로드', selected_file)

with c7:
    st.subheader('파일 추가 업로드')
    uploaded_file = st.file_uploader('')