import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import font_manager, rc
import numpy as np
import os
import base64
import re
import datetime
from dateutil.rrule import rrule, DAILY
from PIL import Image
from sklearn.decomposition import PCA

st.set_page_config(page_title="비정형 ESG 통합 분석 플랫폼", page_icon=None, layout="wide", initial_sidebar_state="expanded", menu_items=None)

# with open('style.css') as f:
#     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

coms = ['신세계', 'GS리테일', '롯데하이마트']
comp = {'신세계': 'sinsegae', 'GS리테일':'GSretail', '롯데하이마트':'Lottehi', '현대홈쇼핑':'hyundai_home_shopping' }
esg = ['E', 'S', 'G']
esg_sp = ['E (Environment)', 'S (Social)', 'G (Governance)']
esg_idx = {'e':0,'s':1,'g':2}
sents = ('전체', '긍정', '중립', '부정')
dis = {'신세계': '2022.06.29', 'GS리테일':'2022.07.04', '롯데하이마트':'2022.06.24', '현대홈쇼핑':'2022.11.08' }

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

def plot_2d_graph(vocabs, xs, ys, col):
    plt.figure(figsize=(8 ,6))
    plt.scatter(xs, ys, marker = 'o', c=col)
    for i, v in enumerate(vocabs):
        plt.annotate(v, xy=(xs[i], ys[i]))

# 한글폰트 세팅
font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)


##### Font Style & Color Style #####
c_style = ("text-align:left; padding: 0px; font-family: Noto Sans KR; font-size: 80%; line-height: 1.5")
t_style = ("text-align:center; padding: 0px; font-family: arial black; font-size: 160%")
b_style = ("text-align:center; padding: 0px; font-family: arial black; font-size: 110%; font-weight: 900;")
p_style = ("text-align:left; padding: 0px; font-family: Noto Sans KR; font-size: 100%; font-weight: 500; line-height: 1.5")
sub_style = ("text-align:center; padding: 0px; font-family: arial black; font-size: 110%; font-weight: 900; line-height: 1.5")
cols = ['#58C558', '#E9C544', '#475EAA']
col_vs = ['#BAEBBA', '#F3E5B1', '#B3BEE0']
#####

##### Logo #####
_, cl, _ = st.columns([0.5, 1, 0.5])
logo = Image.open('./dataset/logo'+'.png')
cl.image(logo)
st.write(' ')
#####
##### Sidebar #####

with st.sidebar:
    _, c00, _ = st.columns([1,1,1])
    _, c01 = st.columns([0.6,2])
    com_logo = Image.open('./dataset/logo_현대홈쇼핑'+'.png')
    c00.image(com_logo)
    menu = c01.radio('', ('자사 분석', '산업군 분석'), label_visibility='collapsed')
#####

##### Layout #####
if menu == '자사 분석':
    ##### 자사분석 #####
    tab1, tab2 = st.tabs(["공시 분석", "뉴스 분석"])
    # 공시분석
    with tab1:
        st.write(f"<h5 style='{c_style}'>2021 지속가능경영보고서, {dis[com]} 기준</h5>", unsafe_allow_html = True)
        st.write(f"<h5 style='{t_style}'><br>{com} ESG 사업 요약</h5>", unsafe_allow_html = True)
        o_tab_e, o_tab_s, o_tab_g = st.tabs(["&nbsp;&nbsp;&nbsp;E&nbsp;&nbsp;&nbsp;", "&nbsp;&nbsp;&nbsp;S&nbsp;&nbsp;&nbsp;", "&nbsp;&nbsp;&nbsp;G&nbsp;&nbsp;&nbsp;"])
        st.write(f"<h5 style='{t_style}'><br><br>지속가능경영보고서, 지배구조보고서<br><br></h5>", unsafe_allow_html = True)
        c11, c12 = st.columns([1.5,1])
        st.write(f"<h5 style='{t_style}'><br><br>ESG 공시 키워드 분석<br><br></h5>", unsafe_allow_html = True)
        c13, c14 = st.columns([1,1])
    # 뉴스분석
    with tab2:
        c21, c22 = st.columns([1,1])
        s_date = c21.date_input('분석 시작 날짜를 선택하세요.', datetime.date(2022,7,13), min_value = datetime.date(2021,12,31), max_value = datetime.date(2023,1,13))
        e_date = c22.date_input('분석 종료 날짜를 선택하세요.', datetime.date(2023,1,13), min_value = s_date, max_value = datetime.date(2023,1,13))
        st.write(f"<h5 style='{c_style}'>{s_date} - {e_date} 기간에 작성된 뉴스를 기반으로 분석을 진행합니다.</h5>", unsafe_allow_html = True)
        st.write(f"<h5 style='{t_style}'><br><br>{com} ESG 뉴스 키워드 분석<br><br></h5>", unsafe_allow_html = True)
        c23, _, c24 = st.columns([1,0.1,1])
        st.write(f"<h5 style='{sub_style}'><strong>분야별 ESG 키워드 리스트</strong><br></h5>", unsafe_allow_html = True)
        c251, c252, c253 = st.columns([1,1,1])
        st.write(f"<h5 style='{t_style}'><br><br>{com} ESG 뉴스 분석<br><br></h5>", unsafe_allow_html = True)
        c26, __, c27 = st.columns([1,0.05,1])
        st.write(f"<h5 style='{t_style}'><br><br>{com} ESG 뉴스 목록<br><br></h5>", unsafe_allow_html = True)
        c281, c282, ___, c283, c284, c285= st.columns([1,1,0.3,0.4,0.4,0.4])
        n_s_date = c281.date_input('조회 시작 날짜를 선택하세요.', datetime.date(2022,8,20), min_value = datetime.date(2021,12,31), max_value = datetime.date(2023,1,13))
        n_e_date = c282.date_input('조회 종료 날짜를 선택하세요.', datetime.date(2022,12,20), min_value = n_s_date, max_value = datetime.date(2023,1,13))
        st.write(f"<h5 style='{c_style}'>{n_s_date} - {n_e_date} 기간에 작성된 뉴스를 조회합니다.<br><br></h5>", unsafe_allow_html = True)
        sent = st.selectbox('긍/부정을 선택하세요.', sents)
        n_tab_e, n_tab_s, n_tab_g = st.tabs(["&nbsp;&nbsp;&nbsp;E&nbsp;&nbsp;&nbsp;", "&nbsp;&nbsp;&nbsp;S&nbsp;&nbsp;&nbsp;", "&nbsp;&nbsp;&nbsp;G&nbsp;&nbsp;&nbsp;"])
else:
    ##### 산업군 분석 #####
    vs_com = st.selectbox('비교할 기업을 선택하세요.', coms, key = 'sel_1')
    tab3, tab4 = st.tabs(["공시 분석", "뉴스 분석"])
    # 공시 분석
    with tab3:
        ____, c31 = st.columns([3,2])
        st.write(f"<h5 style='{t_style}'><br><br>ESG 공시 키워드<br><br></h5>", unsafe_allow_html = True)
        c32, _, c33 = st.columns([1,0.1,1])
        st.write(f"<h5 style='{sub_style}'><br><strong>ESG 키워드 리스트</strong><br></h5>", unsafe_allow_html = True)
        c341, c342, c343 = st.columns([1,1,1])
        st.write(f"<h5 style='{t_style}'><br><br>지속가능경영보고서, 지배구조보고서<br><br></h5>", unsafe_allow_html = True)
        c35 = st.container()

    with tab4:
        c42, c43 = st.columns([1,1])
        s_date = c42.date_input('분석 시작 날짜를 선택하세요.', datetime.date(2022,7,13), min_value = datetime.date(2021,12,31), max_value = datetime.date(2023,1,13))
        e_date = c43.date_input('분석 종료 날짜를 선택하세요.', datetime.date(2023,1,13), min_value = s_date, max_value = datetime.date(2023,1,13))
        st.write(f"<h5 style='{c_style}'>{s_date} - {e_date} 기간에 작성된 뉴스를 기반으로 분석을 진행합니다.</h5>", unsafe_allow_html = True)
        st.write(f"<h5 style='{t_style}'><br><br>ESG 뉴스 키워드 분석<br><br></h5>", unsafe_allow_html = True)
        c44, _, c45 = st.columns([1,0.1,1])
        st.write(f"<h5 style='{sub_style}'><br><br><strong>ESG TOP 키워드 리스트</strong><br></h5>", unsafe_allow_html = True)
        c50 = st.expander('&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;E')
        c51 = st.expander('&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;S')
        c52 = st.expander('&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;G')
        c381, c382, ___, c383, c384, c385= st.columns([1,1,0.3,0.4,0.4,0.4])
        n_s_date = c381.date_input('조회 시작 날짜를 선택하세요.', datetime.date(2022,8,20), min_value = datetime.date(2021,12,31), max_value = datetime.date(2023,1,13))
        n_e_date = c382.date_input('조회 종료 날짜를 선택하세요.', datetime.date(2022,12,20), min_value = n_s_date, max_value = datetime.date(2023,1,13))
        st.write(f"<h5 style='{c_style}'>{n_s_date} - {n_e_date} 기간에 작성된 뉴스를 조회합니다.<br><br></h5>", unsafe_allow_html = True)
        sent = st.selectbox('긍/부정을 선택하세요.', sents)
#####

##### Directory error handling #####
path = './1. preprocessing/'
make_dir(path)
make_dir(path+'1-2. ESG report/output/')
make_dir(path+'1-2. ESG report/esg_report/')
make_dir(path+'1-2. ESG report/esg_report/'+com+'/')
make_dir(path+"2-1. analysis dataset/")
path2 = './dataset/'
make_dir(path2)
#####


##### Data Loading #####
# d : 공시 데이터셋
d = pd.read_csv(path2 + 'disclosure_hyundai_home_shopping.csv', encoding = 'cp949')
d_e = d[d['label']=='e']
d_s = d[d['label']=='s']
d_s = d_s.reset_index(drop=True)
d_g = d[d['label']=='g']
d_g = d_g.reset_index(drop=True)
d_sim_list = os.listdir(path2 + 'disclosure_output/disclosure_hyundai_home_shopping.csv')
d_sim = {}
for s in d_sim_list:
    globals()[f'd_{esg_idx[s]}_sim_vocab'] = np.load(path2 + 'disclosure_output/disclosure_hyundai_home_shopping.csv/'+s+'/vocabs.npy')
    globals()[f'd_{esg_idx[s]}_sim_vec'] = np.load(path2 + 'disclosure_output/disclosure_hyundai_home_shopping.csv/'+s+'/word_vectors.npy')
    d_sim[esg_idx[s]] = [globals()[f'd_{esg_idx[s]}_sim_vocab'], globals()[f'd_{esg_idx[s]}_sim_vec']]

try:
    # d_vs : 경쟁사 공시 데이터셋
    d_vs = pd.read_csv(path2 + f'disclosure_{comp[vs_com]}.csv', encoding = 'cp949')
    d_vs_e = d_vs[d_vs['label']=='e']
    d_vs_s = d_vs[d_vs['label']=='s']
    d_vs_s = d_vs_s.reset_index(drop=True)
    d_vs_g = d_vs[d_vs['label']=='g']
    d_vs_g = d_vs_g.reset_index(drop=True)

    # d_vs_sim : 경쟁사 공시 키워드 유사도 데이터
    d_vs_sim_list = os.listdir(path2 + f'disclosure_output/disclosure_{comp[vs_com]}.csv')
    d_vs_sim = {}
    for s in d_vs_sim_list:
        globals()[f'd_{esg_idx[s]}_vs_sim_vocab'] = np.load(path2 + f'disclosure_output/disclosure_{comp[vs_com]}.csv/'+s+'/vocabs.npy')
        globals()[f'd_{esg_idx[s]}_vs_sim_vec'] = np.load(path2 + f'disclosure_output/disclosure_{comp[vs_com]}.csv/'+s+'/word_vectors.npy')
        d_vs_sim[esg_idx[s]] = [globals()[f'd_{esg_idx[s]}_vs_sim_vocab'], globals()[f'd_{esg_idx[s]}_vs_sim_vec']]
except:
    pass

# d_tot : 산업군 전체 공시 데이터셋
d_tot = pd.read_csv(path2 + f'disclosure_total.csv', encoding = 'cp949')

# news : ESG 뉴스 데이터셋
news = pd.read_csv(path2+ "test_hyundai_home_shopping_analysis.csv", encoding = 'cp949')
news = news.loc[news['pre_label']>0]
news['date'] = pd.to_datetime(news['date']).dt.date
news['re_sent'] = news['sentiment'].apply(lambda x: 1 if x == 1 else -1)
news['re_sent_score'] = news['re_sent']*news['score']
# n : 분석기간 내 ESG 뉴스 데이터셋
n = news.loc[(news['date'] >= s_date) & (news['date'] <= e_date)]
n_e = n.loc[n['pre_label'] == 1]
n_s = n.loc[n['pre_label'] == 2]
n_g = n.loc[n['pre_label'] == 3]
# n_show : 조회기간 내 ESG 뉴스 데이터셋
n_show = news.loc[(news['date'] >= n_s_date) & (news['date'] <= n_e_date)]
n_show_e = n_show[n_show['pre_label']==1][['date', 'text', 'sent_range']].copy()
n_show_e = n_show_e.sort_values('date', ascending = False).reset_index(drop = True)
n_show_s = n_show[n_show['pre_label']==2][['date', 'text', 'sent_range']].copy()
n_show_s = n_show_s.sort_values('date', ascending = False).reset_index(drop = True)
n_show_g = n_show[n_show['pre_label']==3][['date', 'text', 'sent_range']].copy()
n_show_g = n_show_g.sort_values('date', ascending = False).reset_index(drop = True)

# 산업군 데이터셋
news_tot = pd.read_csv(path2 + f'test_sinsegae_analysis.csv', encoding = 'cp949')
news_tot['date'] = pd.to_datetime(news_tot['date']).dt.date
n_tot = news_tot.loc[(news_tot['date'] >= s_date) & (news_tot['date'] <= e_date)].copy()

n_show_tot = news_tot.loc[(news_tot['date'] >= n_s_date) & (news_tot['date'] <= n_e_date)].copy()

try:
    # vs_news : 경쟁사ESG 뉴스 데이터셋
    vs_news = pd.read_csv(path2+ f"test_{comp[vs_com]}_analysis.csv", encoding = 'cp949')
    vs_news = vs_news.loc[vs_news['pre_label']>0]
    vs_news['date'] = pd.to_datetime(vs_news['date']).dt.date
    vs_news['re_sent'] = vs_news['sentiment'].apply(lambda x: 1 if x == 1 else -1)
    vs_news['re_sent_score'] = vs_news['re_sent']*vs_news['score']
    # n : 분석기간 내 ESG 뉴스 데이터셋
    n_vs = vs_news.loc[(vs_news['date'] >= s_date) & (vs_news['date'] <= e_date)]
    n_vs_e = n_vs.loc[n_vs['pre_label'] == 1]
    n_vs_s = n_vs.loc[n_vs['pre_label'] == 2]
    n_vs_g = n_vs.loc[n_vs['pre_label'] == 3]
    # n_show : 조회기간 내 ESG 뉴스 데이터셋
    n_vs_show = vs_news.loc[(vs_news['date'] >= n_s_date) & (vs_news['date'] <= n_e_date)]
    n_vs_show_e = n_vs_show[n_vs_show['pre_label']==1][['date', 'text', 'sent_range']].copy()
    n_vs_show_e = n_vs_show_e.sort_values('date', ascending = False).reset_index(drop = True)
    n_vs_show_s = n_vs_show[n_vs_show['pre_label']==2][['date', 'text', 'sent_range']].copy()
    n_vs_show_s = n_vs_show_s.sort_values('date', ascending = False).reset_index(drop = True)
    n_vs_show_g = n_vs_show[n_vs_show['pre_label']==3][['date', 'text', 'sent_range']].copy()
    n_vs_show_g = n_vs_show_g.sort_values('date', ascending = False).reset_index(drop = True)
    #####
except:
    pass

##### 자사분석 - 공시분석 #####
try:
    with o_tab_e:
        if d_e.empty:
            st.write(f"<h5 style='{p_style}'><br>E와 관련된 활동 키워드가 없습니다.<br><br></h5>", unsafe_allow_html = True)
        else:
            ce0, ce1, ce2 = st.columns([1,1,1])
            ce3, ce4, ce5 = st.columns([1,1,1])
            for i in range(6):
                if len(d_e)>i:
                    globals()[f'ce{i}'].write(f"<h5 style='{b_style}'><strong>{d_e.iloc[i,0]}</strong></h5>", unsafe_allow_html = True)
                    globals()[f'ce{i}'].write(f"<h5 style='{p_style}'><br>{d_e.iloc[i,1]}<br><br></h5>", unsafe_allow_html = True)
        with st.expander("더보기"):
            left = len(d_e)-6
            for i in range(left//3+1):
                globals()[f"ce_{i+2}0"], globals()[f"ce_{i+2}1"], globals()[f"ce_{i+2}2"] = st.columns([1,1,1])
            for i, item in d_e.iterrows():
                if i<6:
                    continue
                else:
                    globals()[f'ce_{i//3}{i%3}'].write(f"<h5 style='{b_style}'><strong>{d_e.iloc[i,0]}</strong></h5>", unsafe_allow_html = True)
                    globals()[f'ce_{i//3}{i%3}'].write(f"<h5 style='{p_style}'><br>{d_e.iloc[i,1]}<br><br></h5>", unsafe_allow_html = True)

    with o_tab_s:
        if d_s.empty:
            st.write(f"<h5 style='{p_style}'><br>S와 관련된 활동 키워드가 없습니다.<br><br></h5>", unsafe_allow_html = True)
        else:
            cs0, cs1, cs2 = st.columns([1,1,1])
            cs3, cs4, cs5 = st.columns([1,1,1])
            for i in range(6):
                if len(d_s)>i:
                    globals()[f'cs{i}'].write(f"<h5 style='{b_style}'><strong>{d_s.iloc[i,0]}</strong></h5>", unsafe_allow_html = True)
                    globals()[f'cs{i}'].write(f"<h5 style='{p_style}'><br>{d_s.iloc[i,1]}<br><br></h5>", unsafe_allow_html = True)
        with st.expander("더보기"):
            left = len(d_s)-6
            for i in range((left//3)+1):
                globals()[f"cs_{i+2}0"], globals()[f"cs_{i+2}1"], globals()[f"cs_{i+2}2"] = st.columns([1,1,1])
            for i, item in d_s.iterrows():
                if i<6:
                    continue
                else:
                    globals()[f'cs_{i//3}{i%3}'].write(f"<h5 style='{b_style}'><strong>{d_s.iloc[i,0]}</strong></h5>", unsafe_allow_html = True)
                    globals()[f'cs_{i//3}{i%3}'].write(f"<h5 style='{p_style}'><br>{d_s.iloc[i,1]}<br><br></h5>", unsafe_allow_html = True)

    with o_tab_g:
        if d_g.empty:
            st.write(f"<h5 style='{p_style}'><br>G와 관련된 활동 키워드가 없습니다.<br><br></h5>", unsafe_allow_html = True)
        else:
            cg0, cg1, cg2 = st.columns([1,1,1])
            cg3, cg4, cg5 = st.columns([1,1,1])
            for i in range(6):
                if len(d_g)>i:
                    globals()[f'cg{i}'].write(f"<h5 style='{b_style}'><strong>{d_g.iloc[i,0]}</strong></h5>", unsafe_allow_html = True)
                    globals()[f'cg{i}'].write(f"<h5 style='{p_style}'><br>{d_g.iloc[i,1]}<br><br></h5>", unsafe_allow_html = True)
        with st.expander("더보기"):
            left = len(d_g)-6
            for i in range(left//3+1):
                globals()[f"cg_{i+2}0"], globals()[f"cg_{i+2}1"], globals()[f"cg_{i+2}2"] = st.columns([1,1,1])
            for i, item in d_g.iterrows():
                if i<6:
                    continue
                else:
                    globals()[f'cg_{i//3}{i%3}'].write(f"<h5 style='{b_style}'><strong>{d_g.iloc[i,0]}</strong></h5>", unsafe_allow_html = True)
                    globals()[f'cg_{i//3}{i%3}'].write(f"<h5 style='{p_style}'><br>{d_g.iloc[i,1]}<br><br></h5>", unsafe_allow_html = True)
        

        
    with c11:
        urls_df = pd.read_csv(path2+'report_url.csv', encoding = 'cp949')
        com_urls = urls_df[urls_df['com']==com]
        for _, u in com_urls.iterrows():
            url = u['url']
            text = u['text']
            st.write(f'{text} <a href="{url}" target="_blank"><button>바로가기</button></a>', unsafe_allow_html=True)

        
        ###### 기존 로컬에 저장해둔  공시 파일 올리는 코드... 이지만 용량 문제로 올리는것은 배제
        # for file in o_files:
        #     if file is not None:
        #         with open(path+'esg_report/'+com+'/'+file, "rb") as f:
        #             encoded_pdf = base64.b64encode(f.read()).decode("utf-8")
        #         name = file.replace('_기존_','')
        #         st.markdown(f'{name}  <a href="data:application/pdf;base64,{encoded_pdf}" download={encoded_pdf}><button>다운로드</button></a>', unsafe_allow_html=True)

    with c12:
        uploaded_files = st.file_uploader('추가 파일을 업로드하세요.', accept_multiple_files = True)
        for up in uploaded_files:
            if up is not None:
                filename = save_uploaded_file(path+'1-2. ESG report/esg_report/', up)
                with c11:
                    with open(path+'1-2. ESG report/esg_report/'+com+'/'+filename, "rb") as f:
                        encoded_pdf = base64.b64encode(f.read()).decode("utf-8")   
                    st.markdown(f'{filename } <a href="data:application/pdf;base64,{encoded_pdf}" download="{encoded_pdf}"><button>다운로드</button></a>', True)
                # st.balloons()
                suc = st.success('파일을 성공적으로 업로드했습니다.')

    # esg 키워드 파이차트
    with c13:
        st.write(f"<h5 style='{sub_style}'><strong>ESG 공시 키워드 분포도</strong></h5>", unsafe_allow_html = True)
        x = np.arange(3)
        d_keys = [d_e['keyword'].nunique(), d_s['keyword'].nunique(), d_g['keyword'].nunique()]
        leg = [i + ': '+str(j)+'가지' for i, j in zip(esg, d_keys)]
        leg.append('전체: '+str(sum(d_keys))+'가지')
        idx = [i for i, x in enumerate(d_keys) if x == max(d_keys)]
        d_key_max = [x for j, x in enumerate(esg_sp) if j in idx]
        d_key_max = ', '.join(d_key_max)
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.pie(d_keys, labels = esg, radius = 0.5, colors = cols, autopct='%.1f%%', textprops = {'size':5})

        st.pyplot(fig)
        leg = "   ".join(leg)
        st.write(f"<center>{leg}</center><br>", unsafe_allow_html = True)
        st.write(f"<h5 style='{p_style}'>{com} 2021 지속가능경영보고서, {dis[com]} 기준 <br><strong>{d_key_max}</strong> 관련 키워드가 가장 많이 추출되었습니다.<br><br></h5>", unsafe_allow_html = True)

    # 공시 esg 키워드 보여주는 표
    with c14:

        st.write(f"<h5 style='{sub_style}'><strong>ESG 공시 키워드 리스트</strong></h5>", unsafe_allow_html = True)
        c141, c142, c143 = st.columns([1,1,1])
        ds = [d_e, d_s, d_g]
        for c, i in zip([c141, c142, c143], range(3)):
            c.write(f"<h5 style='{sub_style}'><strong>{esg[i]}</strong></h5>", unsafe_allow_html = True)
            c.dataframe(ds[i].loc[:,'keyword'])

    ##### 자사분석 - 뉴스분석 #####
    with c23:
        x = np.arange(3)
        n_keys = [n_e['modeling_keyword'].nunique(), n_s['modeling_keyword'].nunique(), n_g['modeling_keyword'].nunique()]
        leg = [i + ': '+str(j)+'가지' for i, j in zip(esg, n_keys)]
        leg.append('전체: '+str(sum(n_keys))+'가지')
        idx = [i for i, x in enumerate(n_keys) if x == max(n_keys)]
        n_key_max = [x for j, x in enumerate(esg_sp) if j in idx]
        n_key_max = ', '.join(n_key_max)
        fig, ax = plt.subplots()
        ax.bar(x, n_keys, color = cols)
        plt.xticks(x, esg, fontsize = 15)
        plt.yticks(range(max(n_keys)+1))
        st.write(f"<h5 style='{sub_style}'><strong>ESG 키워드 분포도</strong></h5>", unsafe_allow_html = True)
        st.pyplot(fig)
        leg = "   ".join(leg)
        st.write(f"<center>{leg}</center><br>", unsafe_allow_html = True)
        st.write(f"<h5 style='{p_style}'>{s_date} - {e_date} 동안 {com} 뉴스에서 <br><strong>{n_key_max}</strong> 관련 키워드가 가장 많이 추출되었습니다.<br><br></h5>", unsafe_allow_html = True)

    with c24:
        st.write(f"<h5 style='{sub_style}'><strong>기간별 ESG 키워드 그래프</h5>", unsafe_allow_html = True)
        dates = list(rrule(DAILY, dtstart=s_date, until=e_date))
        n_key_per_date = pd.DataFrame({"date": dates})
        n_key_per_date = n_key_per_date.set_index("date")
        n_key_per_date["n_e"] = n_e.groupby("date")["modeling_keyword"].nunique().reindex(dates, fill_value=0)
        n_key_per_date["n_s"] = n_s.groupby("date")["modeling_keyword"].nunique().reindex(dates, fill_value=0)
        n_key_per_date["n_g"] = n_g.groupby("date")["modeling_keyword"].nunique().reindex(dates, fill_value=0)

        fig, ax = plt.subplots()
        ax.plot(dates, n_key_per_date["n_e"], label = 'E', color = cols[0])
        ax.plot(dates, n_key_per_date["n_s"], label = 'S', color = cols[1])
        ax.plot(dates, n_key_per_date["n_g"], label = 'G', color = cols[2])
        plt.xticks(fontsize=10, rotation = 45)
        # plt.xticks(fontsize=7)
        plt.ylabel('count')
        plt.legend()
        st.pyplot(fig)
        st.write('차트 설명 추가')
        # st.write(f"<h5 style='{p_style}'>{s_date} - {e_date} 동안 {com} 뉴스에서 <br><strong>{n_key_max}</strong> 관련 키워드가 가장 많이 추출되었습니다.<br><br></h5>", unsafe_allow_html = True)

    with c251:
        st.write(f"<h5 style='{sub_style}'><br>E<br><br></h5>", unsafe_allow_html = True)
        n_e_dup = n_e['modeling_keyword'].value_counts().to_dict()
        n_e_k = n_e.copy()
        n_e_k['dup_key_cnt'] = n_e_k['modeling_keyword'].map(n_e_dup)
        n_e_k = n_e_k.drop_duplicates('modeling_keyword').sort_values('dup_key_cnt', ascending = False).reset_index(drop = True)
        if n_e_k.empty:
            st.write(f"<h5 style='{p_style}'><br>해당 기간에 <strong>E</strong>와 관련된 뉴스 키워드가 없습니다.<br><br></h5>", unsafe_allow_html = True)
        else:
            st.write(n_e_k[['modeling_keyword', 'corpus_keyword']])

    with c252:
        st.write(f"<h5 style='{sub_style}'><br>S<br><br></h5>", unsafe_allow_html = True)
        n_s_dup = n_s['modeling_keyword'].value_counts().to_dict()
        n_s_k = n_s.copy()
        n_s_k['dup_key_cnt'] = n_s_k['modeling_keyword'].map(n_s_dup)
        n_s_k = n_s_k.drop_duplicates('modeling_keyword').sort_values('dup_key_cnt', ascending = False).reset_index(drop = True)
        if n_s_k.empty:
            st.write(f"<h5 style='{p_style}'><br>해당 기간에 <strong>S</strong>와 관련된 뉴스 키워드가 없습니다.<br><br></h5>", unsafe_allow_html = True)
        else:
            st.write(n_s_k[['modeling_keyword', 'corpus_keyword']])

    with c253:
        st.write(f"<h5 style='{sub_style}'><br>G<br><br></h5>", unsafe_allow_html = True)
        n_g_dup = n_g['modeling_keyword'].value_counts().to_dict()
        n_g_k = n_g.copy()
        n_g_k['dup_key_cnt'] = n_g_k['modeling_keyword'].map(n_g_dup)
        n_g_k = n_g_k.drop_duplicates('modeling_keyword').sort_values('dup_key_cnt', ascending = False).reset_index(drop = True)
        if n_g_k.empty:
            st.write(f"<h5 style='{p_style}'>해당 기간에 <strong>G</strong>와 관련된 뉴스 키워드가 없습니다.<br><br></h5>", unsafe_allow_html = True)
        else:
            st.write(n_g_k[['modeling_keyword', 'corpus_keyword']])

    with c26:
        st.write(f"<h5 style='{sub_style}'><strong>ESG 뉴스 비율</h5>", unsafe_allow_html = True)
        n_cnt = [len(n_e), len(n_s), len(n_g)]
        leg = [i + ': '+str(j)+'개' for i, j in zip(esg, n_cnt)]
        leg.append('전체: '+str(sum(n_cnt))+'개')
        try:
            n_cnt = [i/len(n)*100 for i in n_cnt]
        except:
            n_cnt = [0, 0, 0]
        idx = [i for i, x in enumerate(n_cnt) if x == max(n_cnt)]
        n_max = [x for j, x in enumerate(esg_sp) if j in idx]
        n_max = ', '.join(n_max)
        fig, ax = plt.subplots()
        ax.pie(n_cnt, labels = esg, colors = cols, radius = 1, autopct='%.1f%%', textprops = {'size':10})
        st.pyplot(fig)
        leg = "   ".join(leg)
        st.write(f"<center>{leg}</center><br>", unsafe_allow_html = True)
        st.write(f"<h5 style='{p_style}'>{s_date} - {e_date} 동안 {com}은 <br><strong>{n_max}</strong> 관련 활동을 가장 활발히 했습니다.<br><br></h5>", unsafe_allow_html = True)

    with c27:
        st.write(f"<h5 style='{sub_style}'><br><br><strong>시계열 ESG 뉴스 감성분석 그래프</strong><br></h5>", unsafe_allow_html = True)
        fig, ax = plt.subplots()
        n_sent_per_date = pd.DataFrame({"date": dates}).set_index("date")
        n_sent_per_date["n_e"] = n_e.groupby("date")["re_sent_score"].mean().reindex(dates, fill_value=0)
        n_sent_per_date["n_s"] = n_s.groupby("date")["re_sent_score"].mean().reindex(dates, fill_value=0)
        n_sent_per_date["n_g"] = n_g.groupby("date")["re_sent_score"].mean().reindex(dates, fill_value=0)
        # ax.plot(dates, n_sent_per_date["n_e"], label = 'E', color = cols[0])
        # ax.plot(dates, n_sent_per_date["n_s"], label = 'S', color = cols[1])
        # ax.plot(dates, n_sent_per_date["n_g"], label = 'G', color = cols[2])
        ax.plot(dates, n.groupby("date")["re_sent_score"].mean().reindex(dates, fill_value=0), color = "#FF7A00")
        plt.xticks(fontsize=10, rotation = 45)
        plt.ylim(-5,5)
        plt.hlines(0, dates[0], dates[-1], color='black', linestyle='solid', linewidth=1)
        # plt.xticks(fontsize=7)
        plt.ylabel('sentiment score')
        # plt.legend()
        st.pyplot(fig)
        with st.expander("감성분석 산정 기준"):
            st.write("kobert를 esg 긍/부정 감성 분류 task로 fine-tuning한 모델을 사용하여 도출한 해당 날짜의 뉴스에 대한 감성점수입니다.\n\n강한/보통/약한/중립 긍부정 나누는 기준은 다음과 같습니다:\n- sentiment score를 분위수 4개로 나누어서 4개의 그룹으로 나눔\n- 구체적으로 (1) 0.5 이하 : 중립, (2) 0.5 초과 1.5 이하 : 약한, (3) 1.5 초과 2.5 이하 : 보통, (4) 2.5 초과 : 강한 으로 판단\n- label이 1일 경우, 긍정, label이 0일 경우 부정으로 판단함")

    c283.metric('Environment', "  "+str(len(n_show_e))+"  ")
    c284.metric('Social', "  "+str(len(n_show_s))+"  ")
    c285.metric('Governance', "  "+str(len(n_show_g))+"  ")

    n_tabs = [(n_tab_e, n_show_e), (n_tab_s, n_show_s), (n_tab_g, n_show_g)]
    for n_tab in n_tabs:
        with n_tab[0]:
            if n_tab[1].empty:
                st.write(f"<h5 style='{p_style}'>해당 기간에 조회된 뉴스가 없습니다.<br><br></h5>", unsafe_allow_html = True)
            elif sent == '전체':
                st.write(n_tab[1])
            else:
                tmp = n_tab[1][n_tab[1]['sent_range'].str.contains(sent)].copy().reset_index(drop = True)
                if tmp.empty:
                    st.write(f"<h5 style='{p_style}'>해당 기간에 조회된 {sent} 뉴스가 없습니다.<br><br></h5>", unsafe_allow_html = True)
                else:
                    st.write(tmp)
except:
    pass


with c31:
    st.write(f"<h5 style='{c_style}'>{com}: 2021 지속가능경영보고서, {dis[com]} 기준</h5>", unsafe_allow_html = True)
    st.write(f"<h5 style='{c_style}'>{vs_com}: 2021 지속가능경영보고서, {dis[vs_com]} 기준</h5>", unsafe_allow_html = True)

with c32:
    st.write(f"<h5 style='{sub_style}'><br><strong>ESG 공시 키워드 분포</strong><br></h5>", unsafe_allow_html = True)
    e_key = [len(d_e), len(d_tot[d_tot['label']=='e']), len(d_vs_e)]
    s_key = [len(d_s), len(d_tot[d_tot['label']=='s']), len(d_vs_s)]
    g_key = [len(d_g), len(d_tot[d_tot['label']=='g']), len(d_vs_g)]
    name = ['Hyundai\nHome shopping'.upper(), 'IA\n(Industrial Average)', comp[vs_com].upper()]
    fig, ax = plt.subplots()
    plt.bar(name, e_key, color = cols[0]) 
    plt.bar(name, s_key, bottom=e_key, color = cols[1])
    plt.bar(name, g_key, bottom=np.array(s_key)+np.array(e_key), color = cols[2])
    plt.legend(esg)
    st.pyplot(fig)

with c33:
    st.write(f"<h5 style='{sub_style}'><br><strong>ESG 유사 키워드 분포</strong><br></h5>", unsafe_allow_html = True)
    fig, ax = plt.subplots()
    for k, v in d_sim.items():
        vocabs = v[0]
        word_vectors_list = v[1]
        pca = PCA(n_components=2)
        xys = pca.fit_transform(word_vectors_list)
        xs = xys[:,0]
        ys = xys[:,1]
        ax.scatter(xs, ys, marker = 'o', c=cols[k], label = f'{comp[com]}'.replace('_',' ').upper()+', ' +esg[k])
        for i, v in enumerate(vocabs):
            ax.annotate(v, xy=(xs[i], ys[i]))
    for k, v in d_vs_sim.items():
        vocabs = v[0]
        word_vectors_list = v[1]
        pca = PCA(n_components=2)
        xys = pca.fit_transform(word_vectors_list)
        xs = xys[:,0]
        ys = xys[:,1]
        ax.scatter(xs, ys, marker = 'o', c=col_vs[k], label = f'{comp[vs_com]}'.upper()+', ' +esg[k])
        for i, v in enumerate(vocabs):
            ax.annotate(v, xy=(xs[i], ys[i]))
    plt.xlim(-0.06,0.06)
    plt.ylim(-0.06,0.06)
    plt.legend(loc='lower left')
    st.pyplot(fig)

with c35:
    st.write(f"<h5 style='{c_style}'>{vs_com}의 공시 링크입니다.<br><br></h5>", unsafe_allow_html = True)
    urls_df = pd.read_csv(path2+'report_url.csv', encoding = 'cp949')
    com_urls = urls_df[urls_df['com']==vs_com]
    for _, u in com_urls.iterrows():
        url = u['url']
        text = u['text']
        st.write(f'{text} <a href="{url}" target="_blank"><button>바로가기</button></a>', unsafe_allow_html=True)

with c44:
    st.write(f"<h5 style='{sub_style}'><strong>ESG 뉴스 키워드 분포<br></h5>", unsafe_allow_html = True)
    bar_width = 0.35
    n_e_key = [n_e['modeling_keyword'].nunique(), n_tot[n_tot['pre_label']==1]['modeling_keyword'].nunique(), n_vs_e['modeling_keyword'].nunique()]
    n_s_key = [n_s['modeling_keyword'].nunique(), n_tot[n_tot['pre_label']==2]['modeling_keyword'].nunique(), n_vs_s['modeling_keyword'].nunique()]
    n_g_key = [n_g['modeling_keyword'].nunique(), n_tot[n_tot['pre_label']==3]['modeling_keyword'].nunique(), n_vs_g['modeling_keyword'].nunique()]
    name = ['Hyundai\nHome shopping'.upper(), 'IA\n(Industrial Average)', comp[vs_com].upper()]
    fig, ax = plt.subplots()
    ax.bar([0,1,2], n_e_key, color=cols[0], width=0.2, align='center', label=esg[0])
    ax.bar([0.2,1.2,2.2], n_s_key, color=cols[1], width=0.2, align='center', label=esg[1])
    ax.bar([0.4,1.4,2.4], n_g_key, color=cols[2], width=0.2, align='center', label=esg[2])
    ax.set_xticks([0.1, 1.1, 2.1])
    ax.set_xticklabels(name)
    plt.legend()
    st.pyplot(fig)

with c45:
    st.write(f"<h5 style='{sub_style}'><strong>ESG 유사 키워드 분포<br></h5>", unsafe_allow_html = True)

for c in [c50, c51, c52]:
    with c:
        st.write('키워드')
#####
