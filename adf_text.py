import pandas as pd
import os, re, sys
from tools import *

if __name__ == "__main__":
    rootdir = sys.argv[1] # get the rootdir
    files_ = sorted(os.listdir(rootdir))
    files = find_by_pat(files_, re.compile("log-diff"))
    # files
    adfResult = []
    for f in files:
        tmp = {}
        testlist = pd.read_csv(rootdir+f).iloc[:, 1].to_list()
    #     print(testlist)
        tmp["filename"], tmp["Stable?"], tmp["ADFTest result"], tmp["pValue"], tmp["1%"], tmp["5%"], tmp["10%"] = f[:-4],\
            withoutUnitRoot(testlist)[0], withoutUnitRoot(testlist)[1][0],withoutUnitRoot(testlist)[1][1],\
            withoutUnitRoot(testlist)[1][4]["1%"], withoutUnitRoot(testlist)[1][4]["5%"], withoutUnitRoot(testlist)[1][4]["10%"]
        adfResult.append(tmp)

    df1 = pd.DataFrame(adfResult).set_index(["filename"])
    df1.to_csv("./ADFTestResults/{}.csv".format(rootdir.replace("/","")))