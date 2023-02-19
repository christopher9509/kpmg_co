# 삼정KPMG Ideaton 2023

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
- Period : 2022년 공시, 세부 일자는 기업마다 상이
- From : 기업공시채널 https://kind.krx.co.kr/

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

(4) ESG corpus 구축 모델
- 사용 모델 : Soynlp 명사추출기 (https://github.com/lovit/soynlp) + tf-idf
- Input : E/S/G별 지속가능보고서 요약본 추출 텍스트 (기업 통합)
- Output : E/S/G 공시 텍스트에서 추출된 명사 중 tf-idf가 높은 명사 순으로 정렬

(5) 공시 데이터 사업 요약 모델
- 사용 모델 : t5 based pretrained model (https://huggingface.co/eenzeenee/t5-base-korean-summarization)
- Input : KeyBert로 뽑힌 클러스터의 키워드 + 클러스터 내 공시 텍스트 전체
- Output : 공시 텍스트 클러스터별 요약문

## Evaluation
- Metric: Accuracy, F1 score
