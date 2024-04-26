import pandas as pd
import numpy as np
import os
# C:\Users\asd\2nd_project\Crawler\output\어떤_병원
# 파일들이 있는 폴더명으로 폴더내 파일 목록 확인
for j in ["어느_병원"]:
    path = f"C:/Users/asd/2nd_project/Crawler/output/{j}"
    # PATH1 = path.replace("\\","/")
    # print(PATH1)
    folders = os.listdir(path)
    dfs = pd.DataFrame()

    for i in range(len(folders)):
        concat_output = f'C:/Users/asd/2nd_project/Crawler/output/{j}/' + folders[i]
        df = pd.read_csv(concat_output, encoding = 'utf-8')
        print()
        print(len(folders) - i,"개 남았습니다.")
        # print(df.shape)
        dfs = pd.concat([dfs, df])

    print(dfs)

    dfs.to_csv(f"C:/Users/asd/2nd_project/Crawler/output/concat_{j}.csv")
    # print(dfs)
    
