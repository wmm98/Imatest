import csv
from Conf.config import Config
from Common.interface import Interface
import numpy as np
import pandas as pd

conf = Config


class CSVTestData(Interface):
    def __init__(self, file_path):
        self.file_path = file_path

    def read_csv_to_matrix(self):
        data = pd.read_csv(self.file_path, sep="\t", encoding="GBK")
        title = [k.strip() for k in data.columns.tolist()[0].split(",")]
        data = np.array(data)
        clear_data = []
        for i in data:
            line = [j.strip() for j in i[0].split(",")]
            clear_data.append(line)
        clear_data.insert(0, title)
        return clear_data

    def get_white_balance_err_data(self, data):
        # 取最后一排色卡的的六个数据,19-14
        row_num = 0
        for row in data:
            row_num += 1
            if self.remove_space(conf.wb_err_s) in [self.remove_space(i) for i in row]:
                break
        # 取后面六行的最后六个数据
        balance_err_array = data[row_num: row_num + 6]
        # 按顺序返回19-24的数据['0.166', '0.104', '0.098', '0.129', '0.192', '0.405']
        return [line[-1] for line in balance_err_array]

    def get_rgby_noise_data(self, data):
        row_num = 0
        for row in data:
            line = [self.remove_space(i) for i in row]
            row_num += 1
            if self.remove_space(conf.r_noise) in line or self.remove_space(conf.g_noise) in line\
                    or self.remove_space(conf.b_noise) in line or self.remove_space(conf.y_noise) in line:
                break
        # 取后面六行的最后六个数据
        balance_err_array = data[row_num + 19: row_num + 23]
        # 按顺序返回19-24的数据['0.166', '0.104', '0.098', '0.129', '0.192', '0.405']
        return [line[-1] for line in balance_err_array]



if __name__ == '__main__':
    cvs_data = CSVTestData(conf.f_data_path)
    data = cvs_data.read_csv_to_matrix()
    # print(data)
    print(cvs_data.get_white_balance_err_data(data))
    print(cvs_data.get_rgby_noise_data(data))