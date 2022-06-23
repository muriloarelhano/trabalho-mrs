import numpy as np
import pandas as pd
import multiprocessing as mp

from gitter.utils import timeit 

@timeit
def parallelize(dataframe, func, workes_num = mp.cpu_count() -1):
    pool = mp.Pool()
    dataframe_splited = np.array_split(dataframe, workes_num)
    dataframe_return = pd.concat(pool.map(func, dataframe_splited), ignore_index=True)
    pool.close()
    pool.join()
    return dataframe_return
