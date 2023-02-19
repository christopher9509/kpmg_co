# 삼정KPMG Ideaton 2023
<img src="https://github.com/christopher9509/kpmg_co/blob/main/image/main.png" alt="drawing" width="900"/>

- 프로토타입 시연 링크 : https://yun-jeongchoi-kpmg-co-main-prototype-93qkl3.streamlit.app/


## Main
- 참여자 : 이수민, 김영진, 최윤정, 이금진

## Project
- Title: 비정형 ESG 통합 분석 플랫폼
- Category: Classification, News data, NLP, data analysis
- Tool Used: python, pandas, sklearn, pytorch, streamlit, pigma

## Data
- target companies = (1) 신세계 (2) 현대홈쇼핑 (3) 롯데하이마트 (4) GS리테일 (5) LG생활건강
- target domain = 도매 및 소매업

(1) News data
- Period :  20.01.01 ~ 23.01.15
- train/val : 20.01.01 ~ 21.12.31 / 22.01.01 ~ 23.01. 15
- Samples : Total # 156,449개 기사
- From : naver news crawling

(2) ESG report(지속가능경영보고서 요약본)
- Period : (22년도 공시) 2022.06.24. 06.29, 07.04, 08.11, 11.08  
- From : 한국거래소 ESG 포털
- Companies : 총 5개 기업에 대한 공시
- 처리 방법 : (1) Adobe의 data extractor solution을 활용하여 pdf 내 그림 및 테이블, 텍스트를 추출, (2) 저장된 json 파일에서 key 값인 'Text'에 대해 길이 10 이상의 문장을 뽑아서 전처리 하는 알고리즘 개발, (3) KeyBERT를 통해 문장들에 대해 대표 ESG Keyword 도출 및 ESG corpus 구축

## Model

(1) ESG 분류 모델
- 사용 모델 : KoBERT(https://huggingface.co/skt/kobert-base-v1)
- Label 4개(None/E/S/G)에 대해 Fine-tuning 진행
- Input : News title + Contents
- Output : 4가지 label에 대한 확률값

(2) ESG 감성분석 모델
- 사용 모델 : KoBERT(https://huggingface.co/skt/kobert-base-v1)
- Label 2개(Positive/Negative)에 대해 Fine-tuning 진행
- Input : News title + Contents
- Output : 긍정/부정 2가지 label에 대한 확률값 + Sentiment score

(3) 키워드 추출 모델
- 사용 모델 및 방법론 : KeyBERT + Two-step clustering
- 첫 번째 클러스터링 : 중복 기사들에 대해 제거하기 위한 클러스터링(cosine distance 기반)
- 두 번째 클러스터링 : 유사한 기사들 간 군집화(최적 K-cluster를 도출하기 위해 실루엣 계수 사용)
- KeyBERT : 각 클러스터를 대표하는 키워드 및 상위 키워드 중 ESG corpus 내 키워드가 있을 경우 corpus 키워드를 뽑음
- Output : modeling_keyword, corpus_keyword

(4) Word2Vec 기반 키워드 임베딩
- 사용 모델 : Word2Vec
- 공시 키워드 워드 임베딩 : ESG corpus에 있는 단어들을 기반으로, 공시 데이터에서 추출된 문장마다 매핑, 문장과 키워드를 Word2Vec model에 input으로 하여 매핑된 keyword들의 embedding space 상 분포 벡터 도출
- 뉴스 키워드 워드 임베딩 : 뉴스 별 cluster에 있는 corpus keyword를 기반, 해당 키워드의 뉴스와 키워드를 Word2Vec model에 input으로 하여 매핑된 keyword들의 embedding space 상 분포 벡터 도출
- 시각화 : matplotlib scatter plot

(5) ESG corpus 구축 모델
- 사용 모델 : Soynlp 명사추출기 (https://github.com/lovit/soynlp) + tf-idf
- Input : E/S/G별 지속가능보고서 요약본 추출 텍스트 (기업 통합)
- Output : E/S/G 공시 텍스트에서 추출된 명사 중 tf-idf가 높은 명사 순으로 정렬

(6) 공시 데이터 사업 요약 모델
- 사용 모델 : t5 based pretrained model (https://huggingface.co/eenzeenee/t5-base-korean-summarization)
- Input : KeyBert로 뽑힌 클러스터의 키워드 + 클러스터 내 공시 텍스트 전체
- Output : 공시 텍스트 클러스터별 요약문

## Framework
<img src="https://github.com/christopher9509/kpmg_co/blob/main/image/framework.png" alt="drawing" width="900"/>
