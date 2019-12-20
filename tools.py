import statsmodels.tsa.stattools as ts
import os, re
import pandas as pd

'''
合约代码对照表 -> 字典
'''
keywords = ['小麦', '棉花', '白糖', '棉纱', '苹果', '红枣', '籼稻', '玉米', '大豆', '菜籽油', '豆油', '棕榈油', '鸡蛋', '粳米']
df_detail = pd.read_csv("./SecurityCheck.csv")
security_dce =  df_detail["品种"].drop_duplicates().tolist()
SecurityDic_dce = {} # construct a dictionary for the security
for sec in keywords:
    if sec in security_dce:
        SecurityDic_dce[sec] = df_detail[df_detail["品种"]==sec]["合约代码"].tolist()

def withoutUnitRoot(l): # input a list, output true if there is no unit root
    result = ts.adfuller(l)
    adfResult = float(result[0])
    pVal = float(result[1])
    first, fifth, tenth = float(result[4]['1%']), float(result[4]['5%']), float(result[4]['10%'])
    if pVal < 0.0001:
        return "Strongly Stable", result
    elif adfResult < first and adfResult < fifth and adfResult < tenth:
        return "Strongly Stable", result
    elif adfResult > first and adfResult < fifth and adfResult < tenth:
        return "Weakly Stable", result
    else:
        return "Not Stable", result

def find_by_pat(filelist, ptns): # find the file according to the pattern
    res = []
    for f in filelist:
        if type(ptns) == list:
            for ptn in ptns:
                if len(ptn.findall(f)) != 0:
                    res.append(f)
                    break
        else:
            if len(ptns.findall(f)) != 0:
                res.append(f)  
    return res

def readData(filename): # enter a price file name, return a dataframe of the data

    def findSec(a, security_dce): # find the security name according to the code
        for key in security_dce:
            if a in security_dce[key]:
                return key

    df = (pd.read_csv("{}".format(filename), names=["SecurityID","DateTime","PreClosePx","PreLastPx","OpenPx","HighPx","LowPx","ClosePx","LastPx","up1","up2","xxx1","xxx2","xxx3"]))[1:]
    df["SecurityID"] = df["SecurityID"].map(lambda x: findSec(str(x), SecurityDic_dce))
    df = df.dropna(axis=0, how='any')
    df = df.iloc[:, [0,1,8]] # pick the column with the last_price
    date = {}
    for _, row in df.iterrows():
        DateTime, LastPx = row["DateTime"], float(row["LastPx"])
        if DateTime in date.keys(): # add all the transection with the same security name
            date[DateTime] += LastPx
        else:
            date[DateTime] = LastPx
    data = {
        "date": list(date.keys()),
        "LastPx": [date[key] for key in date.keys()]
    }
    return pd.DataFrame(data)