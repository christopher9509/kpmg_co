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
import matplotlib as mpl

st.set_page_config(page_title="비정형 ESG 통합 분석 플랫폼", page_icon=None, layout="wide", initial_sidebar_state="expanded", menu_items=None)

# 한글 깨짐 보정
mpl.rcParams['axes.unicode_minus'] = False


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
hide_dataframe_row_index = """
            <style>
            .row_heading.level0 {display:none}
            .blank {display:none}
            </style>
            """

# Inject CSS with Markdown
st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)

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
# font_name = font_manager.FontProperties(fname=font_manager.findfont('Malgun Gothic')).get_name()
# rc('font', family=font_name)
# plt.rcParams['font.family'] = 'Malgun Gothic'


##### Font Style & Color Style #####
c_style = ("text-align:left; padding: 0px; font-family: Noto Sans KR; font-size: 80%; line-height: 1.5")
t_style = ("text-align:center; padding: 0px; font-family: arial black; font-size: 160%")
b_style = ("text-align:center; padding: 0px; font-family: arial black; font-size: 110%; font-weight: 900;")
p_style = ("text-align:left; padding: 0px; font-family: Noto Sans KR; font-size: 100%; font-weight: 500; line-height: 1.5")
sub_style = ("text-align:center; padding: 0px; font-family: arial black; font-size: 110%; font-weight: 900; line-height: 1.5")
cols = ['#58C558', '#E9C544', '#475EAA']
col_vs = ['#BAEBBA', '#F3E5B1', '#B3BEE0']
col_show = ['#58C558', '#475EAA', '#E9C544']
col_ia = '#ECE6E0'
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
        st.write(f"<h5 style='{sub_style}'><br><strong>분야별 ESG 키워드 리스트</strong><br></h5>", unsafe_allow_html = True)
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
        st.write(f"<h5 style='{sub_style}'><br><strong>ESG 키워드 리스트</strong><br><br></h5>", unsafe_allow_html = True)
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
        st.write(f"<h5 style='{t_style}'><br><br>ESG 뉴스 분석<br><br></h5>", unsafe_allow_html = True)
        c61, c62 = st.columns([1,1])
        st.write(f"<h5 style='{t_style}'><br><br>{vs_com} ESG 뉴스 목록<br><br></h5>", unsafe_allow_html = True)
        c381, c382, ___, c383, c384, c385= st.columns([1,1,0.3,0.4,0.4,0.4])
        n_s_date = c381.date_input('조회 시작 날짜를 선택하세요.', datetime.date(2022,8,20), min_value = datetime.date(2021,12,31), max_value = datetime.date(2023,1,13))
        n_e_date = c382.date_input('조회 종료 날짜를 선택하세요.', datetime.date(2022,12,20), min_value = n_s_date, max_value = datetime.date(2023,1,13))
        st.write(f"<h5 style='{c_style}'>{n_s_date} - {n_e_date} 기간에 작성된 뉴스를 조회합니다.<br><br></h5>", unsafe_allow_html = True)
        sent = st.selectbox('긍/부정을 선택하세요.', sents)
        n_vs_tab_e, n_vs_tab_s, n_vs_tab_g = st.tabs(["&nbsp;&nbsp;&nbsp;E&nbsp;&nbsp;&nbsp;", "&nbsp;&nbsp;&nbsp;S&nbsp;&nbsp;&nbsp;", "&nbsp;&nbsp;&nbsp;G&nbsp;&nbsp;&nbsp;"])
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
news = pd.read_csv(path2+ "final_test_hyundai_home_shopping_analysis.csv")
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
n_show_e = n_show[n_show['pre_label']==1][['date', 'abstract', 'sent_range']].copy()
n_show_e = n_show_e.sort_values('date', ascending = False).reset_index(drop = True)
n_show_s = n_show[n_show['pre_label']==2][['date', 'abstract', 'sent_range']].copy()
n_show_s = n_show_s.sort_values('date', ascending = False).reset_index(drop = True)
n_show_g = n_show[n_show['pre_label']==3][['date', 'abstract', 'sent_range']].copy()
n_show_g = n_show_g.sort_values('date', ascending = False).reset_index(drop = True)
# 뉴스 유사 키워드 데이터
n_sim_list = os.listdir(path2 + 'news_similarity_output/final_test_hyun_analysis.csv')
n_sim = {}
for s in n_sim_list:
    globals()[f'n_{esg_idx[s]}_sim_vocab'] = np.load(path2 + 'news_similarity_output/final_test_hyun_analysis.csv/'+s+'/vocabs.npy')
    globals()[f'n_{esg_idx[s]}_sim_vec'] = np.load(path2 + 'news_similarity_output/final_test_hyun_analysis.csv/'+s+'/word_vectors.npy')
    n_sim[esg_idx[s]] = [globals()[f'n_{esg_idx[s]}_sim_vocab'], globals()[f'n_{esg_idx[s]}_sim_vec']]

# 산업군 데이터셋
news_tot = pd.read_csv(path2 + f'final_merge.csv')
news_tot['date'] = pd.to_datetime(news_tot['date']).dt.date
news_tot['re_sent'] = news_tot['sentiment'].apply(lambda x: 1 if x == 1 else -1)
news_tot['re_sent_score'] = news_tot['re_sent']*news_tot['score']
n_tot = news_tot.loc[(news_tot['date'] >= s_date) & (news_tot['date'] <= e_date)].copy()

n_show_tot = news_tot.loc[(news_tot['date'] >= n_s_date) & (news_tot['date'] <= n_e_date)].copy()

try:
    # vs_news : 경쟁사ESG 뉴스 데이터셋
    vs_news = pd.read_csv(path2+ f"final_test_{comp[vs_com]}_analysis.csv")
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
    n_vs_show_e = n_vs_show[n_vs_show['pre_label']==1][['date', 'abstract', 'sent_range']].copy()
    n_vs_show_e = n_vs_show_e.sort_values('date', ascending = False).reset_index(drop = True)
    n_vs_show_s = n_vs_show[n_vs_show['pre_label']==2][['date', 'abstract', 'sent_range']].copy()
    n_vs_show_s = n_vs_show_s.sort_values('date', ascending = False).reset_index(drop = True)
    n_vs_show_g = n_vs_show[n_vs_show['pre_label']==3][['date', 'abstract', 'sent_range']].copy()
    n_vs_show_g = n_vs_show_g.sort_values('date', ascending = False).reset_index(drop = True)

    # n_vs_sim : 경쟁사 키워드 유사도 데이터
    n_vs_sim_list = os.listdir(path2 + f'news_similarity_output/final_test_{comp[vs_com]}_analysis.csv')
    n_vs_sim = {}
    for s in n_sim_list:
        globals()[f'n_vs_{esg_idx[s]}_sim_vocab'] = np.load(path2 + f'news_similarity_output/final_test_{comp[vs_com]}_analysis.csv/'+s+'/vocabs.npy')
        globals()[f'n_vs_{esg_idx[s]}_sim_vec'] = np.load(path2 + f'news_similarity_output/final_test_{comp[vs_com]}_analysis.csv/'+s+'/word_vectors.npy')
        n_vs_sim[esg_idx[s]] = [globals()[f'n_vs_{esg_idx[s]}_sim_vocab'], globals()[f'n_vs_{esg_idx[s]}_sim_vec']]
    #####
except:
    pass


##### 자사분석 - 공시분석 #####
try:
    for j, t in zip(range(3),[o_tab_e, o_tab_s, o_tab_g]):
        with t:
            if globals()[f'd_{esg[j].lower()}'].empty:
                st.write(f"<h5 style='{p_style}'><br>{esg[j]}와 관련된 활동 키워드가 없습니다.<br><br></h5>", unsafe_allow_html = True)
            else:
                globals()[f'c{esg[j].lower()}0'], globals()[f'c{esg[j].lower()}1'], globals()[f'c{esg[j].lower()}2'] = st.columns([1,1,1])
                globals()[f'c{esg[j].lower()}3'], globals()[f'c{esg[j].lower()}4'], globals()[f'c{esg[j].lower()}5'] = st.columns([1,1,1])
                for i in range(6):
                    if len(globals()[f'd_{esg[j].lower()}'])>i:
                        globals()[f'c{esg[j].lower()}{i}'].write(f"<h5 style='{b_style}'><strong>{globals()[f'd_{esg[j].lower()}'].iloc[i,0]}</strong></h5>", unsafe_allow_html = True)
                        globals()[f'c{esg[j].lower()}{i}'].write(f"<h5 style='{p_style}'><br>{globals()[f'd_{esg[j].lower()}'].iloc[i,1]}<br><br></h5>", unsafe_allow_html = True)
            with st.expander("더보기"):
                left = len(globals()[f'd_{esg[j].lower()}'])-6
                for i in range(left//3+1):
                    globals()[f"c{esg[j].lower()}_{i+2}0"], globals()[f"c{esg[j].lower()}_{i+2}1"], globals()[f"c{esg[j].lower()}_{i+2}2"] = st.columns([1,1,1])
                for i, item in globals()[f'd_{esg[j].lower()}'].iterrows():
                    if i<6:
                        continue
                    else:
                        globals()[f'c{esg[j].lower()}_{i//3}{i%3}'].write(f"<h5 style='{b_style}'><strong>{globals()[f'd_{esg[j].lower()}'].iloc[i,0]}</strong></h5>", unsafe_allow_html = True)
                        globals()[f'c{esg[j].lower()}_{i//3}{i%3}'].write(f"<h5 style='{p_style}'><br>{globals()[f'd_{esg[j].lower()}'].iloc[i,1]}<br><br></h5>", unsafe_allow_html = True)
        
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
        ax.pie(d_keys, labels = [esg[i]+': '+str(d_keys[i])+'가지' for i in range(3)], colors = cols, autopct='%.1f%%', textprops = {'size':6})
        st.pyplot(fig)
        # leg = "   ".join(leg)
        # st.write(f"<center>{leg}</center><br>", unsafe_allow_html = True)
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
        n_keys = [n_e['model_keyword'].nunique(), n_s['model_keyword'].nunique(), n_g['model_keyword'].nunique()]
        idx = [i for i, x in enumerate(n_keys) if x == max(n_keys)]
        n_key_max = [x for j, x in enumerate(esg_sp) if j in idx]
        n_key_max = ', '.join(n_key_max)
        fig, ax = plt.subplots()
        for i in range(3):
            ax.bar(esg[i], n_keys[i], color = cols[i])
        plt.xticks(x, esg, fontsize = 15)
        plt.yticks(range(0,max(n_keys)+1,5))
        st.write(f"<h5 style='{sub_style}'><strong>ESG 키워드 분포도</strong></h5>", unsafe_allow_html = True)
        for i, v in enumerate(x):
            plt.text(v, n_keys[i], str(n_keys[i]),
                fontsize=9,
                color="black",
                horizontalalignment='center',
                verticalalignment='bottom')
        ax.legend([esg[i]+': '+f'{(n_keys[i]/sum(n_keys)):.2f}'+'%' for i in range(3)])
        st.pyplot(fig)
        st.write(f"<h5 style='{p_style}'>{s_date} - {e_date} 동안 {com} 뉴스에서 <br><strong>{n_key_max}</strong> 관련 키워드가 가장 많이 추출되었습니다.<br><br></h5>", unsafe_allow_html = True)

    with c24:
        st.write(f"<h5 style='{sub_style}'><strong>기간별 ESG 키워드 그래프</h5>", unsafe_allow_html = True)
        dates = list(rrule(DAILY, dtstart=s_date, until=e_date))
        n_key_per_date = pd.DataFrame({"date": dates})
        n_key_per_date = n_key_per_date.set_index("date")
        n_key_per_date["n_e"] = n_e.groupby("date")["model_keyword"].nunique().reindex(dates, fill_value=0)
        n_key_per_date["n_s"] = n_s.groupby("date")["model_keyword"].nunique().reindex(dates, fill_value=0)
        n_key_per_date["n_g"] = n_g.groupby("date")["model_keyword"].nunique().reindex(dates, fill_value=0)
        e_max= max(n_key_per_date["n_e"].copy())
        s_max = max(n_key_per_date["n_s"].copy())
        g_max = max(n_key_per_date["n_g"].copy())
        idx = [i for i, x in enumerate([e_max,s_max,g_max]) if x == max([e_max,s_max,g_max])]
        n_key_per_date_max = [x for j, x in enumerate(esg_sp) if j in idx]
        n_key_per_date_max = ', '.join(n_key_per_date_max)
        fig, ax = plt.subplots()
        ax.plot(dates, n_key_per_date["n_e"], label = 'E', color = cols[0])
        ax.plot(dates, n_key_per_date["n_s"], label = 'S', color = cols[1])
        ax.plot(dates, n_key_per_date["n_g"], label = 'G', color = cols[2])
        plt.xticks(fontsize=10, rotation = 45)
        plt.ylabel('count')
        plt.legend()
        st.pyplot(fig)
        st.write(f"<h5 style='{p_style}'>{s_date} - {e_date} 동안 하루 기준 <strong>{n_key_per_date_max}</strong> 관련 키워드가 최대 <strong>{max([e_max,s_max,g_max])}</strong>개로 가장 많이 추출되었습니다.<br><br></h5>", unsafe_allow_html = True)
    
    for i, c in zip(range(3),[c251, c252, c253]):
        with c:
            st.write(f"<h5 style='{sub_style}'><br>{esg[i]}<br><br></h5>", unsafe_allow_html = True)
            globals()[f'n_{esg[i].lower()}_dup'] = globals()[f'n_{esg[i].lower()}']['model_keyword'].value_counts().to_dict()
            globals()[f'n_{esg[i].lower()}_k'] = globals()[f'n_{esg[i].lower()}'].copy()
            globals()[f'n_{esg[i].lower()}_k']['dup_key_cnt'] = globals()[f'n_{esg[i].lower()}_k']['model_keyword'].map(globals()[f'n_{esg[i].lower()}_dup'])
            globals()[f'n_{esg[i].lower()}_k'] = globals()[f'n_{esg[i].lower()}_k'].drop_duplicates('model_keyword').sort_values('dup_key_cnt', ascending = False).reset_index(drop = True)
            if globals()[f'n_{esg[i].lower()}_k'].empty:
                st.write(f"<h5 style='{p_style}'><br>해당 기간에 <strong>{esg[i]}</strong>와 관련된 뉴스 키워드가 없습니다.<br><br></h5>", unsafe_allow_html = True)
            else:
                st.write(globals()[f'n_{esg[i].lower()}_k'][['model_keyword', 'corpus_keyword']])
    
    with c26:
        st.write(f"<h5 style='{sub_style}'><strong>ESG 뉴스 비율</h5>", unsafe_allow_html = True)
        n_cnt = [len(n_e), len(n_s), len(n_g)]
        try:
            n_cnt = [i/len(n)*100 for i in n_cnt]
        except:
            n_cnt = [0, 0, 0]
        idx = [i for i, x in enumerate(n_cnt) if x == max(n_cnt)]
        n_max = [x for j, x in enumerate(esg_sp) if j in idx]
        n_max = ', '.join(n_max)
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.pie(n_cnt, labels = [esg[i]+': '+f'{(n_cnt[i]*len(n)/100):.0f}'+'개' for i in range(3)], colors = cols, autopct='%.1f%%', textprops = {'size':6})
        st.pyplot(fig)
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
            st.write("kobert를 esg 긍/부정 감성 분류 task로 fine-tuning한 모델을 사용하여 도출한 해당 날짜의 뉴스에 대한 감성점수입니다.\n\n강한/보통/약한 긍·부정 및 중립을 나누는 기준:\n- label이 1일 경우, 긍정, label이 0일 경우 부정으로 분류\n- sentiment score를 분위수 4개로 나누어서 4개의 그룹으로 분류\n  - (1) 0.5 이하 : 중립, (2) 0.5 초과 1.5 이하 : 약한, (3) 1.5 초과 2.5 이하 : 보통, (4) 2.5 초과 : 강한 으로 분류")

    c283.metric('Environment', "  "+str(len(n_show_e))+"  ")
    c284.metric('Social', "  "+str(len(n_show_s))+"  ")
    c285.metric('Governance', "  "+str(len(n_show_g))+"  ")

    n_tabs = [(n_tab_e, n_show_e), (n_tab_s, n_show_s), (n_tab_g, n_show_g)]
    for n_tab in n_tabs:
        with n_tab[0]:
            if sent == '전체':
                tmp = n_tab[1]
            else:
                tmp = n_tab[1][n_tab[1]['sent_range'].str.contains(sent)].copy().reset_index(drop = True)
            if tmp.empty:
                st.write(f"<h5 style='{p_style}'>해당 기간에 조회된 {sent} 뉴스가 없습니다.<br><br></h5>", unsafe_allow_html = True)
            else:
                st.write(tmp)
except:
    pass

try:
    with c31:
        st.write(f"<h5 style='{c_style}'>{com}: 2021 지속가능경영보고서, {dis[com]} 기준</h5>", unsafe_allow_html = True)
        st.write(f"<h5 style='{c_style}'>{vs_com}: 2021 지속가능경영보고서, {dis[vs_com]} 기준</h5>", unsafe_allow_html = True)

    with c32:
        st.write(f"<h5 style='{sub_style}'><br><strong>ESG 공시 키워드 분포</strong><br></h5>", unsafe_allow_html = True)
        e_key = [len(d_e), len(d_tot[d_tot['label']=='e'])/4, len(d_vs_e)]
        s_key = [len(d_s), len(d_tot[d_tot['label']=='s'])/4, len(d_vs_s)]
        g_key = [len(d_g), len(d_tot[d_tot['label']=='g'])/4, len(d_vs_g)]
        name = ['Hyundai\nHome shopping'.upper(), 'IA\n(Industrial Average)', comp[vs_com].upper()]
        x = name + name + name
        y = e_key + [x+y for x,y in zip(e_key, s_key)] + [x+y for x,y in zip([x+y for x,y in zip(e_key, s_key)], g_key)]
        actual_y = e_key+s_key+g_key
        fig, ax = plt.subplots()
        plt.bar(name, e_key, color = cols[0]) 
        plt.bar(name, s_key, bottom=e_key, color = cols[1])
        plt.bar(name, g_key, bottom=np.array(s_key)+np.array(e_key), color = cols[2])
        plt.legend(esg)
        for i, v in enumerate(x):
            plt.text(v, y[i], str(actual_y[i]),
                fontsize=9,
                color="black",
                horizontalalignment='center',
                verticalalignment='bottom')
        st.pyplot(fig)
        e_t = e_key[0]-e_key[1]
        s_t = s_key[0]-s_key[1]
        g_t = g_key[0]-g_key[1]
        e_txt = f'{abs(e_t)}개 적고' if e_t<0 else ('동일하고' if e_t==0 else f'{abs(e_t)}개 많고')
        s_txt = f'{abs(s_t)}개 적으며' if s_t<0 else ('동일하며' if s_t==0 else f'{abs(s_t)}개 많으며')
        g_txt = f'{abs(g_t)}개 적습니다' if g_t<0 else ('동일합니다' if g_t==0 else f'{abs(g_t)}개 많습니다')

        st.write(f"{com}은 산업평균 대비<br><strong>E(Environment)</strong> 키워드 가짓수가 {e_txt}, <br><strong>S(Social)</strong> 키워드 가짓수가 {s_txt}, <br><strong>G(Governance)</strong> 키워드 가짓수가 {g_txt}.<br></h5>", unsafe_allow_html = True)
        


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
        plt.legend(loc='lower left', fontsize=8)
        st.pyplot(fig)

    for c, i in zip([c341, c342, c343], [com, vs_com, '전체']):
        with c:
            st.write(f"<h5 style='{p_style}'><center><strong>{i} TOP 키워드</strong></center><br></h5>", unsafe_allow_html = True)
            if i == '전체':
                top_keywords = d_tot.groupby('label')['keyword'].unique().apply(lambda x: pd.Series(x).drop_duplicates().head(3))
                st.dataframe(pd.DataFrame(top_keywords.to_dict()).transpose()[['e','s','g']].fillna('-'))
            elif i == com:
                top_keywords = d.groupby('label')['keyword'].unique().apply(lambda x: pd.Series(x).drop_duplicates().head(3))
                st.dataframe(pd.DataFrame(top_keywords.to_dict()).transpose()[['e','s','g']].fillna('-'))
            else:
                top_keywords = d_vs.groupby('label')['keyword'].unique().apply(lambda x: pd.Series(x).drop_duplicates().head(3))
                st.dataframe(pd.DataFrame(top_keywords.to_dict()).transpose()[['e','s','g']].fillna('-'))


    with c35:
        st.write(f"<h5 style='{c_style}'>{vs_com}의 공시 링크입니다.<br><br></h5>", unsafe_allow_html = True)
        urls_df = pd.read_csv(path2+'report_url.csv', encoding = 'cp949')
        com_urls = urls_df[urls_df['com']==vs_com]
        for _, u in com_urls.iterrows():
            url = u['url']
            text = u['text']
            st.write(f'{text} <a href="{url}" target="_blank"><button>바로가기</button></a>', unsafe_allow_html=True)

    #####산업군분석 - 뉴스분석
    with c44:
        st.write(f"<h5 style='{sub_style}'><strong>ESG 뉴스 키워드 분포<br></h5>", unsafe_allow_html = True)
        fig, ax = plt.subplots()
        x = [0,1,2,0.2,1.2,2.2,0.4,1.4,2.4]
        y = [n_e['model_keyword'].nunique(),n_s['model_keyword'].nunique(),n_g['model_keyword'].nunique(),n_tot[n_tot['pre_label']==1]['model_keyword'].nunique()/4, n_tot[n_tot['pre_label']==2]['model_keyword'].nunique()/4, n_tot[n_tot['pre_label']==3]['model_keyword'].nunique()/4,n_vs_e['model_keyword'].nunique(), n_vs_s['model_keyword'].nunique(),n_vs_g['model_keyword'].nunique()]
        ax.bar(0, n_e['model_keyword'].nunique(), color = cols[0], width=0.2, align='center', label='Hyundai Home shopping'.upper()+', '+esg[0])
        ax.bar(1, n_s['model_keyword'].nunique(), color = cols[1], width=0.2, align='center', label='Hyundai Home shopping'.upper()+', '+esg[1])
        ax.bar(2, n_g['model_keyword'].nunique(), color = cols[2], width=0.2, align='center', label='Hyundai Home shopping'.upper()+', '+esg[2])
        ax.bar([0.2,1.2,2.2], [n_tot[n_tot['pre_label']==1]['model_keyword'].nunique()/4, n_tot[n_tot['pre_label']==2]['model_keyword'].nunique()/4, n_tot[n_tot['pre_label']==3]['model_keyword'].nunique()/4], color = col_ia, width=0.2, align='center', label='IA (Industrial Average)')
        ax.bar(0.4, n_vs_e['model_keyword'].nunique(), color = col_vs[0], width=0.2, align='center', label=comp[vs_com].upper()+', '+esg[0])
        ax.bar(1.4, n_vs_s['model_keyword'].nunique(), color = col_vs[1], width=0.2, align='center', label=comp[vs_com].upper()+', '+esg[1])
        ax.bar(2.4, n_vs_g['model_keyword'].nunique(), color = col_vs[2], width=0.2, align='center', label=comp[vs_com].upper()+', '+esg[2])
        ax.set_xticks([0.2, 1.2, 2.2])
        ax.set_xticklabels(esg)
        for i, v in enumerate(x):
            plt.text(v, y[i], str(y[i]),
                fontsize=9,
                color="black",
                horizontalalignment='center',
                verticalalignment='bottom')
        plt.legend(fontsize = 9)
        st.pyplot(fig)
        e_t = n_e['model_keyword'].nunique()-(n_tot[n_tot['pre_label']==1]['model_keyword'].nunique()/4)
        s_t = n_s['model_keyword'].nunique()-(n_tot[n_tot['pre_label']==2]['model_keyword'].nunique()/4)
        g_t = n_g['model_keyword'].nunique()-(n_tot[n_tot['pre_label']==3]['model_keyword'].nunique()/4)
        e_txt = f'{abs(e_t)}개 적고' if e_t<0 else ('동일하고' if e_t==0 else f'{abs(e_t)}개 많고')
        s_txt = f'{abs(s_t)}개 적으며' if s_t<0 else ('동일하며' if s_t==0 else f'{abs(s_t)}개 많으며')
        g_txt = f'{abs(g_t)}개 적습니다' if g_t<0 else ('동일합니다' if g_t==0 else f'{abs(g_t)}개 많습니다')

        st.write(f"{com}은 산업평균 대비<br><strong>E(Environment)</strong> 키워드 가짓수가 {e_txt}, <br><strong>S(Social)</strong> 키워드 가짓수가 {s_txt}, <br><strong>G(Governance)</strong> 키워드 가짓수가 {g_txt}.<br></h5>", unsafe_allow_html = True)
        # st.write(f"<h5 style='{c_style}'>각 기업의 ESG별 뉴스 키워드 가짓수 분포와 산업 평균 키워드 가짓수를 나타낸 차트입니다.<br></h5>", unsafe_allow_html = True)

    with c45:
        st.write(f"<h5 style='{sub_style}'><strong>ESG 유사 키워드 분포<br></h5>", unsafe_allow_html = True)
        fig, ax = plt.subplots()
        for k, v in n_sim.items():
            vocabs = v[0]
            word_vectors_list = v[1]
            pca = PCA(n_components=2)
            xys = pca.fit_transform(word_vectors_list)
            xs = xys[:,0]
            ys = xys[:,1]
            ax.scatter(xs, ys, marker = 'o', c=cols[k], label = f'{comp[com]}'.replace('_',' ').upper()+', ' +esg[k])
            for i, v in enumerate(vocabs):
                ax.annotate(v, xy=(xs[i], ys[i]))
        for k, v in n_vs_sim.items():
            vocabs = v[0]
            word_vectors_list = v[1]
            pca = PCA(n_components=2)
            xys = pca.fit_transform(word_vectors_list)
            xs = xys[:,0]
            ys = xys[:,1]
            ax.scatter(xs, ys, marker = 'o', c=col_vs[k], label = f'{comp[vs_com]}'.upper()+', ' +esg[k])
            for i, v in enumerate(vocabs):
                ax.annotate(v, xy=(xs[i], ys[i]))
        plt.xlim(-0.2,0.4)
        plt.ylim(-0.1,0.15)
        plt.legend(loc='upper right', fontsize = 8)
        st.pyplot(fig)


    keyword_show = [com, vs_com, '전체']
    for c, i in zip([c50, c51, c52], range(3)):
        with c:
            globals()[f'{c}{i}0'], globals()[f'{c}{i}1'], globals()[f'{c}{i}2'] = st.columns([1,1,1])
            for c_, i_ in zip([globals()[f'{c}{i}0'], globals()[f'{c}{i}1'], globals()[f'{c}{i}2']], range(3)):
                with c_:
                    st.write(f"<h5 style='{p_style}'><center><strong>{keyword_show[i_]} TOP 키워드</strong></center><br></h5>", unsafe_allow_html = True)
                    if i_ == 2:
                        n_dup = n_tot['model_keyword'].value_counts().to_dict()
                        n_tmp = n_tot[n_tot['pre_label'] == (i+1)].copy()
                        n_tmp['dup_key_cnt'] = n_tmp['model_keyword'].map(n_dup)
                        n_tmp = n_tmp.drop_duplicates('model_keyword').sort_values('dup_key_cnt', ascending = False).reset_index(drop = True)
                        n_tmp = n_tmp[['model_keyword', 'corpus_keyword']].head(3)
                        if n_tmp.empty:
                            st.write(f"<h5 style='{c_style}'><center>해당 기간에 <strong>{keyword_show[i_]}</strong>의 <strong>{esg[i]}</strong> 키워드가<br>존재하지 않습니다.</center><br></h5>", unsafe_allow_html = True)
                        else:
                            st.write(n_tmp[['model_keyword', 'corpus_keyword']].head(3))
                    elif i_ == 0:
                        n_dup = n['model_keyword'].value_counts().to_dict()
                        n_tmp = n[n['pre_label'] == (i+1)].copy()
                        n_tmp['dup_key_cnt'] = n_tmp['model_keyword'].map(n_dup)
                        n_tmp = n_tmp.drop_duplicates('model_keyword').sort_values('dup_key_cnt', ascending = False).reset_index(drop = True)
                        n_tmp = n_tmp[['model_keyword', 'corpus_keyword']].head(3)
                        if n_tmp.empty:
                            st.write(f"<h5 style='{c_style}'><center>해당 기간에 <strong>{keyword_show[i_]}</strong>의 <strong>{esg[i]}</strong> 키워드가<br>존재하지 않습니다.</center><br></h5>", unsafe_allow_html = True)
                        else:
                            st.write(n_tmp[['model_keyword', 'corpus_keyword']].head(3))
                    else:
                        n_dup = n_vs['model_keyword'].value_counts().to_dict()
                        n_tmp = n_vs[n_vs['pre_label'] == (i+1)].copy()
                        n_tmp['dup_key_cnt'] = n_tmp['model_keyword'].map(n_dup)
                        n_tmp = n_tmp.drop_duplicates('model_keyword').sort_values('dup_key_cnt', ascending = False).reset_index(drop = True)
                        n_tmp = n_tmp[['model_keyword', 'corpus_keyword']].head(3)
                        if n_tmp.empty:
                            st.write(f"<h5 style='{c_style}'><center>해당 기간에 <strong>{keyword_show[i_]}</strong>의 <strong>{esg[i]}</strong> 키워드가<br>존재하지 않습니다.</center><br></h5>", unsafe_allow_html = True)
                        else:
                            st.write(n_tmp[['model_keyword', 'corpus_keyword']].head(3))

    with c61:
        st.write(f"<h5 style='{sub_style}'><strong>ESG 뉴스 비율<br></h5>", unsafe_allow_html = True)
        e_news = [len(n_e), len(n_tot[n_tot['pre_label']==1]), len(n_vs_e)]
        e_news_p = e_news.copy()
        s_news = [len(n_s), len(n_tot[n_tot['pre_label']== 2]), len(n_vs_s)]
        s_news_p = s_news.copy()
        g_news = [len(n_g), len(n_tot[n_tot['pre_label']==3]), len(n_vs_g)]
        g_news_p = g_news.copy()
        for i in range(3):
            for p in [e_news_p, s_news_p, g_news_p]:
                try:
                    p[i] = p[i]/(e_news[i]+s_news[i]+g_news[i])*100
                except:
                    p[i] = 0

        name = ['Hyundai\nHome shopping'.upper(), 'IA\n(Industrial Average)', comp[vs_com].upper()]
        x = name + name + name
        y = e_news_p + [x+y for x,y in zip(e_news_p, s_news_p)] + [x+y for x,y in zip([x+y for x,y in zip(e_news_p, s_news_p)], g_news_p)]

        actual_y = e_news_p + s_news_p + g_news_p
        fig, ax = plt.subplots()
        plt.bar(name, e_news_p, color = cols[0]) 
        plt.bar(name, s_news_p, bottom=e_news_p, color = cols[1])
        plt.bar(name, g_news_p, bottom=np.array(s_news_p)+np.array(e_news_p), color = cols[2])
        plt.legend(esg)
        plt.ylabel('%')
        for i, v in enumerate(x):
            if actual_y[i]==0:
                continue
            plt.text(v, y[i], f'{actual_y[i]:.1f}'+'%',
                    fontsize=9,
                    color="black",
                    horizontalalignment='center',
                    verticalalignment='bottom')
        st.pyplot(fig)
        st.write(f"<h5 style='{c_style}'>각 기업별 ESG 뉴스 개수와 E,S,G 뉴스가 각각 차지하는 비율을 막대그래프 형식으로 나타낸 차트입니다.<br>자사({com})의 ESG 뉴스 비율을 선택한 기업({vs_com}), 그리고 산업평균과 함께 비교 분석함으로써 상대적 ESG 활동을 파악할 수 있습니다.<br></h5>", unsafe_allow_html = True)

    with c62:
        st.write(f"<h5 style='{sub_style}'><strong>시계열 ESG 뉴스 감성분석 그래프<br></h5>", unsafe_allow_html = True)
        dates = list(rrule(DAILY, dtstart=s_date, until=e_date))
        fig, ax = plt.subplots()
        n_sent_per_date = pd.DataFrame({"date": dates}).set_index("date")
        ax.plot(dates, n.groupby("date")["re_sent_score"].mean().reindex(dates, fill_value=0), color = col_show[0], label = 'Hyundai Home Shopping')
        n_tot_sent_per_date = pd.DataFrame({"date": dates}).set_index("date")
        ax.plot(dates, n_tot.groupby("date")["re_sent_score"].mean().reindex(dates, fill_value=0), color = col_show[1], label = 'IA (Industrial Average)')
        n_vs_sent_per_date = pd.DataFrame({"date": dates}).set_index("date")
        ax.plot(dates, n_vs.groupby("date")["re_sent_score"].mean().reindex(dates, fill_value=0), color = col_show[2], label = comp[vs_com].upper())
        plt.xticks(fontsize=10, rotation = 45)
        plt.ylim(-5,5)
        plt.hlines(0, dates[0], dates[-1], color='black', linestyle='solid', linewidth=1)
        plt.ylabel('sentiment score')
        plt.legend()
        st.pyplot(fig)
        with st.expander("감성분석 산정 기준"):
            st.write("kobert를 esg 긍/부정 감성 분류 task로 fine-tuning한 모델을 사용하여 도출한 해당 날짜의 뉴스에 대한 감성점수입니다.\n\n강한/보통/약한 긍·부정 및 중립을 나누는 기준:\n- label이 1일 경우, 긍정, label이 0일 경우 부정으로 분류\n- sentiment score를 분위수 4개로 나누어서 4개의 그룹으로 분류\n  - (1) 0.5 이하 : 중립, (2) 0.5 초과 1.5 이하 : 약한, (3) 1.5 초과 2.5 이하 : 보통, (4) 2.5 초과 : 강한 으로 분류")

    c383.metric('Environment', "  "+str(len(n_vs_show_e))+"  ")
    c384.metric('Social', "  "+str(len(n_vs_show_s))+"  ")
    c385.metric('Governance', "  "+str(len(n_vs_show_g))+"  ")

    n_vs_tabs = [(n_vs_tab_e, n_vs_show_e), (n_vs_tab_s, n_vs_show_s), (n_vs_tab_g, n_vs_show_g)]
    for n_vs_tab in n_vs_tabs:
        with n_vs_tab[0]:
            if sent == '전체':
                tmp = n_vs_tab[1]
            else:
                tmp = n_vs_tab[1][n_vs_tab[1]['sent_range'].str.contains(sent)].copy().reset_index(drop = True)
            if tmp.empty:
                st.write(f"<h5 style='{p_style}'>해당 기간에 조회된 {sent} 뉴스가 없습니다.<br><br></h5>", unsafe_allow_html = True)
            else:
                st.write(tmp)
except:
    pass
#####
