import pandas as pd
import math, os, re, sys
from tools import *

if __name__ == "__main__":
    rootdir = sys.argv[1] # get the rootdir
    dirs = sorted(os.listdir(rootdir)) # two part, first index, second price
    index_dir, price_dir = dirs[0], dirs[1]
    
    '''
    Here for the index data processing
    '''
    print("start index processing...")
    
    files = sorted(os.listdir("{}{}/".format(rootdir, index_dir)))
    files = [x for x in files if len(re.compile("log-diff").findall(x)) == 0]
    for file in files:
        path = "{}{}/{}".format(rootdir, index_dir, file)
        print(path)
        df_tmp = pd.read_csv(path, usecols=[1,2,3])
        df_index = df_tmp[df_tmp["type"]=="all"][["date","index"]].iloc[3:] # combine mobile and pc together
        df_index["date"] = df_index["date"].map(lambda x: x.replace("-",""))
        
        # log-diff transformation
        DRR, flag = [], 0
        palm= df_index.iloc[0,1]
        for _,row in df_index.iterrows():

            if flag == 0:
                flag += 1
                continue

            daily = {}
            if float(row["index"]) == 0:
                tmp = 0.0001
            else:
                tmp = float(row["index"])
            if float(palm) == 0:
                tmp2 = 0.0001
            else:
                tmp2 = float(palm)
            palm_drr = math.log(tmp*1.0/tmp2)

            daily["date"] = row["date"]
            daily["index"] = palm_drr

            DRR.append(daily)

            palm = tmp

        df_drr = pd.DataFrame(DRR)
        
        '''uncomment the following to save the raw files'''
#         df_drr = df_drr.set_index(["date"])
#         df_drr.to_csv("{}{}/log-diff-{}".format(rootdir, index_dir, file))
    
    print("done.\n")
        
    '''
    Here for the price data processing
    '''
    print("start price processing...")
    
    files = sorted(os.listdir("{}{}/".format(rootdir, price_dir)))
    files = [x for x in files if len(re.compile("数据表").findall(x)) == 0]
    first = "{}{}/{}".format(rootdir, price_dir, files[0]) # get 2010 price for starters
    
    # start concating
    df = readData(first)
    for file in files[1:]:
        path = "{}{}/{}".format(rootdir, price_dir, file)
        print(path)
        df1 = df
        df2 = readData(path)
        df = pd.concat([df1, df2])
            
    # log-diff
    # here palm is the sign of price
    DRR, flag = [], 0
    palm= df.iloc[0,1]
    for _,row in df.iterrows():

        if flag == 0:
            flag += 1
            continue

        daily = {}
        palm_drr = math.log(float(row["LastPx"])*1.0/float(palm))

        daily["date"] = row["date"]
        daily["{}结算价".format(rootdir.replace("/",""))] = palm_drr

        DRR.append(daily)

        palm = float(row["LastPx"])


    df_drr = pd.DataFrame(DRR)
    
    '''uncomment the following to save the raw file'''
#     df_drr2 = df_drr.set_index(["date"], inplace=False)
#     df_drr2.to_csv("{}{}/{}结算价对数差分数据表.csv".format(rootdir, price_dir, rootdir.replace("/","")))
    
    '''uncomment the following to save the raw file'''
#     df2 = df.set_index(["date"], inplace=False)
#     df2.to_csv("{}{}/{}结算价数据表.csv".format(rootdir, price_dir, rootdir.replace("/","")))

    print("done.\n")
    
    '''
    Here for merge price and index
    '''
    print("start merging price and index")
    
    files = sorted(os.listdir("{}{}/".format(rootdir, index_dir)))
    pattern = re.compile("log-diff")
    for f in find_by_pat(files, pattern):
        path = "{}{}/{}".format(rootdir, index_dir, f)
        df2 = pd.read_csv(path)
        df_drr['date']=df_drr['date'].astype(int)
        df_cross = pd.merge(df2, df_drr, on="date")
        df_cross = df_cross.set_index(["date"])
        df_cross.to_csv("{}{}结算价和{}index的比对.csv".format(rootdir, rootdir.replace("/",""), f[9:-4]))
    
    print("all done.")