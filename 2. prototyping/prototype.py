import streamlit as st
import pandas as pd
import numpy as np
import os
import base64
import re
import time
from PIL import Image
from annotated_text import annotated_text

st.set_page_config(page_title="서비스명", page_icon=None, layout="wide", initial_sidebar_state="expanded", menu_items=None)

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

coms = []
def select_coms(com):
    coms.append(com)

def reset_coms():
    coms = []

com = '현대홈쇼핑'

# 해당 디렉토리가 없으면 디렉토리를 만들어주는 함수
def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return

# 디렉토리에 파일을 저장하는 함수
def save_uploaded_file(path, file):
    make_dir(path)
    filename = re.sub(r'[,()* ]', '_', file.name)
    with open(os.path.join(path, filename), 'wb') as f:
        f.write(file.getbuffer())
    return filename

success = False

def success_alarm(c, suc, mes):
    with c:
        if suc == True:
            st.success(mes)

c1, c2, c3 = st.columns([2,1,0.2])
c1 = st.empty()
# with c2: ---> 산업군 분석으로 이동
#     com = st.selectbox("Select company", ['현대홈쇼핑', 'LG생활건강', '롯데하이마트', 'GS리테일', '신세계'])
# with c3:
#     image = Image.open(com+'.jpg')
#     st.image(image)

##### Font Style #####
c_style = ("text-align:left; padding: 0px; font-family: arial black; font-size: 70%")
t_style = ("text-align:center; padding: 0px; font-family: arial black; font-size: 160%")
b_style = ("text-align:center; padding: 0px; font-family: arial black; font-size: 110%; font-weight: 900;")
p_style = ("text-align:left; padding: 0px; font-family: Noto Sans KR; font-size: 100%; font-weight: 500; line-height: 1.5")
#####

##### Sidebar #####
with st.sidebar:
    st.text('서비스명')
    st.radio('뷰티인사이드', ('자사 분석', '산업군 분석'))
#####

##### Layout #####
tab1, tab2 = st.tabs(["공시분석", "뉴스분석"])
with tab1:
    st.write(f"<h5 style='{c_style}'>2021 지속가능경영보고서, 2022.07.04 기준</h5>", unsafe_allow_html = True)
    st.write(f"<h5 style='{t_style}'><br>현대홈쇼핑 ESG 사업 요약</h5>", unsafe_allow_html = True)
    tab_e, tab_s, tab_g = tab1.tabs(["&nbsp;&nbsp;&nbsp;E&nbsp;&nbsp;&nbsp;", "&nbsp;&nbsp;&nbsp;S&nbsp;&nbsp;&nbsp;", "&nbsp;&nbsp;&nbsp;G&nbsp;&nbsp;&nbsp;"])
    st.write(f"<h5 style='{t_style}'><br><br>지속가능경영보고서, 지배구조보고서<br><br></h5>", unsafe_allow_html = True)
    c1, c2 = st.columns([1.5,1])
    st.write(f"<h5 style='{t_style}'><br><br>ESG 키워드<br></h5>", unsafe_allow_html = True)
    c3, c4 = st.columns([1,1])
#####

##### Directory error handling #####
path = '../1. preprocessing/1-2. ESG report/'
make_dir(path)
make_dir(path+'output/')
make_dir(path+'esg_report/')
make_dir(path+'esg_report/'+com+'/')
#####


##### Data Loading #####
dir = path + 'output/summarized_hyundaehomeshopping_2023.csv'
# o_sum : 공시 사업요약
o_sum = pd.read_csv(dir)
e_o_sum = o_sum[o_sum['label']=='e']
s_o_sum = o_sum[o_sum['label']=='s']
s_o_sum = s_o_sum.reset_index(drop=True)
g_o_sum = o_sum[o_sum['label']=='g']
g_o_sum = g_o_sum.reset_index(drop=True)
# o_files : 공시 파일 리스트 (로컬 저장된)
o_files = [f for f in os.listdir(path+'esg_report/'+com+'/') if f.startswith('_기존_')]
##### Tab1_공시분석 #####
with tab_e:
    if e_o_sum.empty:
        st.write(f"<h5 style='{p_style}'><br>'E와 관련된 활동 키워드가 없습니다.'<br><br></h5>", unsafe_allow_html = True)
    else:
        ce0, ce1, ce2 = st.columns([1,1,1])
        ce3, ce4, ce5 = st.columns([1,1,1])
        for i in range(6):
            if len(e_o_sum)>i:
                globals()[f'ce{i}'].write(f"<h5 style='{b_style}'><strong>{e_o_sum.iloc[i,0]}</strong></h5>", unsafe_allow_html = True)
                globals()[f'ce{i}'].write(f"<h5 style='{p_style}'><br>{e_o_sum.iloc[i,1]}<br><br></h5>", unsafe_allow_html = True)
    with st.expander("더보기"):
        left = len(e_o_sum)-6
        for i in range(left//3+1):
            globals()[f"ce_{i+2}0"], globals()[f"ce_{i+2}1"], globals()[f"ce_{i+2}2"] = st.columns([1,1,1])
        for i, item in e_o_sum.iterrows():
            if i<6:
                continue
            else:
                globals()[f'ce_{i//3}{i%3}'].write(f"<h5 style='{b_style}'><strong>{e_o_sum.iloc[i,0]}</strong></h5>", unsafe_allow_html = True)
                globals()[f'ce_{i//3}{i%3}'].write(f"<h5 style='{p_style}'><br>{e_o_sum.iloc[i,1]}<br><br></h5>", unsafe_allow_html = True)

with tab_s:
    if s_o_sum.empty:
        st.write(f"<h5 style='{p_style}'><br>'E와 관련된 활동 키워드가 없습니다.'<br><br></h5>", unsafe_allow_html = True)
    else:
        cs0, cs1, cs2 = st.columns([1,1,1])
        cs3, cs4, cs5 = st.columns([1,1,1])
        for i in range(6):
            if len(s_o_sum)>i:
                globals()[f'cs{i}'].write(f"<h5 style='{b_style}'><strong>{s_o_sum.iloc[i,0]}</strong></h5>", unsafe_allow_html = True)
                globals()[f'cs{i}'].write(f"<h5 style='{p_style}'><br>{s_o_sum.iloc[i,1]}<br><br></h5>", unsafe_allow_html = True)
    with st.expander("더보기"):
        left = len(s_o_sum)-6
        for i in range((left//3)+1):
            globals()[f"cs_{i+2}0"], globals()[f"cs_{i+2}1"], globals()[f"cs_{i+2}2"] = st.columns([1,1,1])
        for i, item in s_o_sum.iterrows():
            if i<6:
                continue
            else:
                globals()[f'cs_{i//3}{i%3}'].write(f"<h5 style='{b_style}'><strong>{s_o_sum.iloc[i,0]}</strong></h5>", unsafe_allow_html = True)
                globals()[f'cs_{i//3}{i%3}'].write(f"<h5 style='{p_style}'><br>{s_o_sum.iloc[i,1]}<br><br></h5>", unsafe_allow_html = True)

with tab_g:
    if g_o_sum.empty:
        st.write(f"<h5 style='{p_style}'><br>'E와 관련된 활동 키워드가 없습니다.'<br><br></h5>", unsafe_allow_html = True)
    else:
        cg0, cg1, cg2 = st.columns([1,1,1])
        cg3, cg4, cg5 = st.columns([1,1,1])
        for i in range(6):
            if len(g_o_sum)>i:
                globals()[f'cg{i}'].write(f"<h5 style='{b_style}'><strong>{g_o_sum.iloc[i,0]}</strong></h5>", unsafe_allow_html = True)
                globals()[f'cg{i}'].write(f"<h5 style='{p_style}'><br>{g_o_sum.iloc[i,1]}<br><br></h5>", unsafe_allow_html = True)
    with st.expander("더보기"):
        left = len(g_o_sum)-6
        for i in range(left//3+1):
            globals()[f"cg_{i+2}0"], globals()[f"cg_{i+2}1"], globals()[f"cg_{i+2}2"] = st.columns([1,1,1])
        for i, item in g_o_sum.iterrows():
            if i<6:
                continue
            else:
                globals()[f'cg_{i//3}{i%3}'].write(f"<h5 style='{b_style}'><strong>{g_o_sum.iloc[i,0]}</strong></h5>", unsafe_allow_html = True)
                globals()[f'cg_{i//3}{i%3}'].write(f"<h5 style='{p_style}'><br>{g_o_sum.iloc[i,1]}<br><br></h5>", unsafe_allow_html = True)
    

      
with c1:
    urls_df = pd.read_csv(path+'esg_report/report_url.csv', encoding = 'cp949')
    com_urls = urls_df[urls_df['com']==com]
    for _, u in com_urls.iterrows():
        url = u['url']
        text = u['text']
        st.markdown(f'{text} <a href=url target="_blank"><button>바로가기</button></a>', unsafe_allow_html=True)
    
    ###### 기존 로컬에 저장해둔  공시 파일 올리는 코드... 이지만 
    # for file in o_files:
    #     if file is not None:
    #         with open(path+'esg_report/'+com+'/'+file, "rb") as f:
    #             encoded_pdf = base64.b64encode(f.read()).decode("utf-8")
    #         name = file.replace('_기존_','')
    #         st.markdown(f'{name}  <a href="data:application/pdf;base64,{encoded_pdf}" download={encoded_pdf}><button>다운로드</button></a>', unsafe_allow_html=True)

with c2:
    uploaded_files = st.file_uploader('추가 파일을 업로드하세요.', accept_multiple_files = True)
    for up in uploaded_files:
        if up is not None:
            filename = save_uploaded_file(path+'esg_report/', up)
            with c1:
                with open(path+'esg_report/'+com+'/'+filename, "rb") as f:
                    encoded_pdf = base64.b64encode(f.read()).decode("utf-8")   
                st.markdown(f'{filename } <a href="data:application/pdf;base64,{encoded_pdf}" download="{encoded_pdf}"><button>다운로드</button></a>', True)
            # st.balloons()
            suc = st.success('파일을 성공적으로 업로드했습니다.')

# esg 키워드 파이차트
# with c3:

# 공시 esg 키워드 보여주는 표
# with c4:


