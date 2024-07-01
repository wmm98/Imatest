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
        result = [line[-1] for line in balance_err_array]
        return {conf.nineteen: float(result[0]), conf.twenty: float(result[1]), conf.twenty_one: float(result[2]),
                conf.twenty_two: float(result[3]), conf.twenty_three: float(result[4]),
                conf.twenty_four: float(result[5])}

    def get_rgby_noise_data(self, data):
        row_num = 0
        for row in data:
            line = [self.remove_space(i) for i in row]
            row_num += 1
            if self.remove_space(conf.r_noise) in line or self.remove_space(conf.g_noise) in line \
                    or self.remove_space(conf.b_noise) in line or self.remove_space(conf.y_noise) in line:
                break
        # 取后面六行的最后六个数据
        balance_err_array = np.array(data[row_num + 19: row_num + 23])[:, 2:6]
        Y = [float(y) for y in balance_err_array[:, 0].tolist()]
        R = [float(r) for r in balance_err_array[:, 1].tolist()]
        G = [float(g) for g in balance_err_array[:, 2].tolist()]
        B = [float(b) for b in balance_err_array[:, 3].tolist()]

        # 转为float列表
        # err_array = balance_err_array.tolist()
        # float_err_array = [[float(j) for j in i] for i in err_array]
        # 返回平均数，即为RGBY,取小数点后两位 "{:.2f}".format()
        # RGBY = [float("{:.2f}".format((sum(e_a) / len(e_a)))) for e_a in float_err_array]
        return {conf.R: float("{:.2f}".format((sum(R) / len(R)))), conf.G: float("{:.2f}".format((sum(G) / len(G)))),
                conf.B: float("{:.2f}".format((sum(B) / len(B)))), conf.Y: float("{:.2f}".format((sum(Y) / len(Y))))}

    def get_snr_data(self, data):
        for row in data:
            line = [self.remove_space(i) for i in row]
            if self.remove_space(conf.snr_bw) in line[0]:
                return {conf.R: float(line[1]), conf.G: float(line[2]), conf.B: float(line[3]), conf.Y: float(line[4])}

    def get_color_accuracy_data(self, data):
        accuracy_data = {}
        flag = 0
        for row in data:
            line = [self.remove_space(i) for i in row]
            if self.remove_space(conf.C1_key) in line:
                flag += 1
                accuracy_data[conf.C1] = float(line[1])
                continue
            if self.remove_space(conf.C2_key) in line:
                flag += 1
                accuracy_data[conf.C2] = float(line[1])
                continue
            if self.remove_space(conf.E1_key) in line:
                flag += 1
                accuracy_data[conf.E1] = float(line[1])
                continue
            if self.remove_space(conf.Sat_key) in line:
                flag += 1
                accuracy_data[conf.Sat] = float(line[1])
                continue
            if flag == 4:
                break
        return accuracy_data

    def get_HJ_contrast_and_readable_data(self, data):
        row_num = 0
        # start row
        for row in data:
            row_num += 1
            if self.remove_space(conf.hj_relate_key) in [self.remove_space(i) for i in row]:
                break
        # end row
        end_row_num = row_num
        for end_row in data[row_num:]:

            flag = 0
            for elem in end_row:
                if elem.isdigit() or (elem.replace('.', '', 1).isdigit()) or (
                        elem.startswith('-') and elem[1:].replace('.', '', 1).isdigit()):
                    flag += 1
            if flag == len(end_row):
                end_row_num += 1
            else:
                break
        # 取第二列数据
        relate_data = np.array(data[row_num: end_row_num])[:, 1]
        zone_data = [float(i) for i in relate_data.tolist()]

        # 前后相减， 获取可读灰阶数
        zone_length = len(zone_data)
        readable_relate = [float("{:.1f}".format(zone_data[r] - zone_data[r + 1])) if r < (zone_length - 1) else float(
            "{:.1f}".format(zone_data[-1])) for r in range(zone_length)][:-1]
        readable_num = len([i for i in readable_relate if i >= 8])

        # 获取对比度
        contrast = float("{:.4f}".format(((zone_data[0] - zone_data[-1]) / 255)))
        return {conf.hj_readable: readable_num, conf.hj_contrast: contrast}

    def get_hj_dynamic_range_data(self, data):
        for row in data:
            if self.remove_space(conf.dynamic_range_key) in [self.remove_space(i) for i in row]:
                return float(row[2])

    def get_hj_relate_data(self, t_data):
        contrast_readable = self.get_HJ_contrast_and_readable_data(t_data)
        return {conf.hj_dynamic_range: self.get_hj_dynamic_range_data(t_data),
                conf.hj_readable: contrast_readable[conf.hj_readable],
                conf.hj_contrast: contrast_readable[conf.hj_contrast]}


if __name__ == '__main__':
    cvs_data = CSVTestData(conf.f_data_path)
    data = cvs_data.read_csv_to_matrix()
    # print(data)
    print(cvs_data.get_white_balance_err_data(data))
    print(cvs_data.get_rgby_noise_data(data))
    print(cvs_data.get_snr_data(data))
    print(cvs_data.get_color_accuracy_data())
    print("***************************")
    cvs_data = CSVTestData(conf.hj_data_path)
    data = cvs_data.read_csv_to_matrix()
    hj_relate_data = cvs_data.get_hj_relate_data(data)
    print(hj_relate_data)
