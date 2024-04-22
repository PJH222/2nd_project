import pandas as pd
import numpy as np
import os

# 파일들이 있는 폴더명으로 폴더내 파일 목록 확인
path = "Crawler/output/어떤_병원"
# PATH1 = path.replace("\\","/")
# print(PATH1)
folders = os.listdir(path)
dfs = pd.DataFrame()

for i in range(len(folders)):
    concat_output = 'Crawler/output/어떤_병원/' + folders[i]
    df = pd.read_csv(concat_output, encoding = 'utf-8')
    print()
    print(len(folders) - i,"개 남았습니다.")
    # print(df.shape)
    dfs = pd.concat([dfs, df])

print(dfs)

dfs.to_csv("Crawler/output/concat_어떤_병원.csv")
# print(dfs)
    
