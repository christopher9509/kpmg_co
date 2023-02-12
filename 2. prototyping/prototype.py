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

tab1, tab2 = st.tabs(["공시분석", "뉴스분석"])

with st.sidebar:
    st.text('서비스명')
    st.radio('뷰티인사이드', ('자사 분석', '산업군 분석'))


tab1.write('2021 지속가능경영보고서, 2022.07.04 기준')
# tab1.markdown("<center><h3><code>현대홈쇼핑</code> ESG 사업 요약</h3></center>", True)
tab1.markdown(f"<center><h3>현대홈쇼핑 ESG 사업 요약</h3></center>", True)

tab_e, tab_s, tab_g = tab1.tabs(["&nbsp;&nbsp;&nbsp;E&nbsp;&nbsp;&nbsp;", "&nbsp;&nbsp;&nbsp;S&nbsp;&nbsp;&nbsp;", "&nbsp;&nbsp;&nbsp;G&nbsp;&nbsp;&nbsp;"])

path = '../1. preprocessing/1-2. ESG report/'
make_dir(path)
make_dir(path+'output/')
make_dir(path+'esg_report/')

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
        c1.markdown(f"<center><h5><code>{e_df.iloc[0,0]}</code></h5></center>", True)
        c1.write(e_df.iloc[0,1])
        c2.markdown(f"<center><h5>{e_df.iloc[1,0]}</h5></center>", True)
        # c2.write(e_df.iloc[1,0])
        c2.write(e_df.iloc[1,1])
        c3.markdown(f"<center><h5>{e_df.iloc[2,0]}</h5></center>", True)
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
    # s_df.reset_index(inplace=True, drop=True)
    # if s_df.empty:
    #     tab1.tab_s.write('S와 관련된 활동 키워드가 없습니다.')
    # else:
    #     c1, c2, c3, c4, c5 = st.columns([1,1,1,1,0.4])
    #     s_df = df[df['label']=='s']
    #     c1.text_area(s_df.iloc[0,0], value=s_df.iloc[0,1])
    #     # c1.write(s_df.iloc[0,0])
    #     # c1.write(s_df.iloc[0,1])
    #     # c1.metric(s_df.iloc[0,0], s_df.iloc[0,1], delta=None, delta_color="normal", help=None, label_visibility="visible")
    #     c2.metric(s_df.iloc[1,0], s_df.iloc[1,1], delta=None, delta_color="normal", help=None, label_visibility="visible")
    #     c3.metric(s_df.iloc[2,0], s_df.iloc[2,1], delta=None, delta_color="normal", help=None, label_visibility="visible")
    #     c4.metric(s_df.iloc[3,0], s_df.iloc[3,1], delta=None, delta_color="normal", help=None, label_visibility="visible")
    #     c5.button("더보기",key='s_more')

with tab_g:
    g_df = df[df['label']=='g']
    g_df.reset_index(inplace=True, drop=True)
    # if g_df.empty:
    #     tab1.tab_g.write('G와 관련된 활동 키워드가 없습니다.')
    # else:
    #     c1, c2, c3, c4, c5 = st.columns([1,1,1,1,0.4])
    #     c1.text_area(g_df.iloc[0,0], value=g_df.iloc[0,1])
    #     # c1.write(g_df.iloc[0,0])
    #     # c1.write(g_df.iloc[0,1])
    #     # c1.metric(g_df.iloc[0,0], g_df.iloc[0,1], delta=None, delta_color="normal", help=None, label_visibility="visible")
    #     c2.metric(g_df.iloc[1,0], g_df.iloc[1,1], delta=None, delta_color="normal", help=None, label_visibility="visible")
    #     c3.metric(g_df.iloc[2,0], g_df.iloc[2,1], delta=None, delta_color="normal", help=None, label_visibility="visible")
    #     c4.metric(g_df.iloc[3,0], g_df.iloc[3,1], delta=None, delta_color="normal", help=None, label_visibility="visible")
    #     c5.button("더보기",key='g_more')

c6, c7 = tab1.columns([1.5,1])
file_list = [f for f in os.listdir(path+'esg_report/') if f.startswith('hyundae')]
        
with c6:
    st.subheader('파일 리스트')
    # st.markdown(f'<h4>바로가기</h4>', True)
    url = "https://kind.krx.co.kr/common/disclsviewer.do?method=search&acptno=20221108000292&docno=&viewerhost=&viewerport="
    st.markdown(f'KRX 공시 <a href="https://kind.krx.co.kr/common/disclsviewer.do?method=search&acptno=20221108000292&docno=&viewerhost=&viewerport=" target="_blank"><button>바로가기</button></a>', unsafe_allow_html=True)
    
    for file in file_list:
        if file is not None:
            with open(path+'esg_report/'+file, "rb") as f:
                encoded_pdf = base64.b64encode(f.read()).decode("utf-8")
            with st.expander(file.replace(".pdf","")):
                st.write('2021 지속가능경영보고서 요약본, 2022.07.04 기준')
                st.markdown(f'{file} <a href="data:application/pdf;base64,{encoded_pdf}" download={file}><button>다운로드</button></a>', unsafe_allow_html=True)

    # selected_file = st.selectbox("Select a file:", file_list)
    # if selected_file is not None:
    #     st.write('2021 지속가능경영보고서 요약본')
    #     with open(path+'esg_report/'+selected_file, "rb") as f:
    #         encoded_pdf = base64.b64encode(f.read()).decode("utf-8")
    #     st.markdown(f'{selected_file} <a href="data:application/pdf;base64,{encoded_pdf}" download={selected_file}><button>다운로드</button></a>', unsafe_allow_html=True)
    #     with st.expander("세부 정보 보기"):
    #         st.write('2021 지속가능경영보고서 요약본, 2022.07.04 기준')
    #         with open(path+'esg_report/'+selected_file, "rb") as f:
    #             encoded_pdf = base64.b64encode(f.read()).decode("utf-8")
    #         if st.button("Download PDF"):
    #             st.markdown(f'<a href="data:application/pdf;base64,{encoded_pdf}" download={selected_file}<button>Download {selected_file}</button></a>', unsafe_allow_html=True)
        # encoded_pdf
            # st.download_button('파일 다운로드', selected_file)

with c7:
    st.subheader('파일 추가 업로드')
    uploaded_files = st.file_uploader('추가 파일을 업로드하세요.', accept_multiple_files = True)
    for up in uploaded_files:
        if up is not None:
            filename = save_uploaded_file(path+'esg_report/', up)
            with c6:
                with st.expander(filename):
                    with open(path+'esg_report/'+filename, "rb") as f:
                        encoded_pdf = base64.b64encode(f.read()).decode("utf-8")   
                    st.markdown(f'{filename } <a href="data:application/pdf;base64,{encoded_pdf}" download="{encoded_pdf}"><button>다운로드</button></a>', True)
            # st.balloons()
            suc = st.success('파일을 성공적으로 업로드했습니다.')

# 기존 데이터는 새로 올리는 파일과 구분될 수 있도록 파일명 변경
# 링크 리스트 파일로 작성
# 산업군때 구현할 select 그거를 명시적으로 드러내지는 않아도 com으로 기업명 설정하기 (com = hyndae)
# 파일명 수정 요청