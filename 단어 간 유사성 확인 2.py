# from konlpy.tag import Mecab
# from tqdm import tqdm
# import google
# import google.colab
import re
import pickle
import csv
import pandas as pd
import numpy as np

# from google.colab import drive
# drive.mount("/content/drive")
# from google.colab import drive

# drive.mount('/content/drive/')

# 병명증상정보.csv : "병명/증상 정보 data"를 csv로 변환한 파일
# df = pd.read_csv("/content/drive/MyDrive/멀티캠퍼스_DS_DE_33/2nd_pjt/병명증상정보.csv", encoding='cp949')
df = pd.read_csv("병명증상정보.csv", encoding='cp949')

# n-gram 어휘 벡터 생성
def getNgramWord(N,txt):
    txt = txt.split()
    ngrams = [txt[i:i+N] for i in range(len(txt)-N+1)]
    return ngrams

import konlpy
from konlpy.tag import Kkma, Komoran, Hannanum, Okt
from konlpy.utils import pprint
from konlpy.tag import Mecab

okt = Okt()

columns = []

for i in df['증상']:

  # 단어를 몇 개까지 이어 붙일지 결정
  for j in range(2,4):

    for k in range(len(getNgramWord(j,i))):
      # 정상 출력되는지 확인용
      # print(getNgramWord(j,i)[k], hannanum.nouns(str(getNgramWord(j,i)[k][-1])))

      change_word = okt.nouns(str(getNgramWord(j,i)[k][-1]))

      tmp2 = getNgramWord(j,i)[k][:j - 1] + change_word

      if tmp2 != "":
        columns.append(' '.join(tmp2))
        
dff = pd.DataFrame(data = None, columns=columns, index = columns)

print(dff)
