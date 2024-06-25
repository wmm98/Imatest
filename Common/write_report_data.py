from openpyxl import load_workbook
from openpyxl.styles import Font
from Conf.config import Config
from Common.interface import Interface

conf = Config()


class WriteReport(Interface):
    def __init__(self, file_path, sheet_name):
        self.file_path = file_path
        self.sheet_name = sheet_name
        self.red_font = Font(color="FF0000")

    def write_contrast_data(self, position, value):
        wb = load_workbook(self.file_path)
        sheet = wb[self.sheet_name]
        pos = position[conf.r_hj_relate_pos]
        contrast_cell = sheet.cell(row=pos[0], column=pos[1])
        contrast_cell.value = value[conf.hj_contrast]
        wb.save(self.file_path)
        wb.close()

    def write_readable_hj_data(self, position, value):
        wb = load_workbook(self.file_path)
        sheet = wb[self.sheet_name]
        pos = position[conf.r_hj_relate_pos]
        contrast_cell = sheet.cell(row=pos[0], column=pos[1])
        contrast_cell.value = value[conf.hj_readable]
        wb.save(self.file_path)
        wb.close()

    def write_dynamic_range_data(self, position, value):
        wb = load_workbook(self.file_path)
        sheet = wb[self.sheet_name]
        # 写入灰阶动态范围
        pos = position[conf.r_hj_relate_pos]
        dynamic_range_cell = sheet.cell(row=pos[0], column=pos[1])
        dynamic_range_cell.value = value[conf.hj_dynamic_range]
        # if dynamic_range <= 5.5:
        #     dynamic_range_cell.font = red_font
        wb.save(self.file_path)
        wb.close()

    def write_snr_data(self, position, value):
        wb = load_workbook(self.file_path)
        sheet = wb[self.sheet_name]

        r_cell = sheet.cell(row=position[conf.R][0], column=position[conf.R][1])
        r_cell.value = "R：%s" % str(value[conf.R])
        g_cell = sheet.cell(row=position[conf.G][0], column=position[conf.G][1])
        g_cell.value = "G：%s" % str(value[conf.G])
        b_cell = sheet.cell(row=position[conf.B][0], column=position[conf.B][1])
        b_cell.value = "B：%s" % str(value[conf.B])
        y_cell = sheet.cell(row=position[conf.Y][0], column=position[conf.Y][1])
        y_cell.value = "Y：%s" % str(value[conf.Y])

        wb.save(self.file_path)
        wb.close()

    def write_white_balance_data(self, position, value):
        wb = load_workbook(self.file_path)
        sheet = wb[self.sheet_name]

        nineteen_cell = sheet.cell(row=position[conf.nineteen][0], column=position[conf.nineteen][1])
        nineteen_cell.value = "%s block： %s" % (conf.nineteen, str(value[conf.nineteen]))
        twenty_cell = sheet.cell(row=position[conf.twenty][0], column=position[conf.twenty][1])
        twenty_cell.value = "%s block： %s" % (conf.twenty, str(value[conf.twenty]))
        twenty_one_cell = sheet.cell(row=position[conf.twenty_one][0], column=position[conf.twenty_one][1])
        twenty_one_cell.value = "%s block： %s" % (conf.twenty_one, str(value[conf.twenty_one]))
        twenty_two_cell = sheet.cell(row=position[conf.twenty_two][0], column=position[conf.twenty_two][1])
        twenty_two_cell.value = "%s block： %s" % (conf.twenty_two, str(value[conf.twenty_two]))
        twenty_three_cell = sheet.cell(row=position[conf.twenty_three][0], column=position[conf.twenty_three][1])
        twenty_three_cell.value = "%s block： %s" % (conf.twenty_three, str(value[conf.twenty_three]))
        twenty_four_cell = sheet.cell(row=position[conf.twenty_four][0], column=position[conf.twenty_four][1])
        twenty_four_cell.value = "%s block： %s" % (conf.twenty_four, str(value[conf.twenty_four]))
        wb.save(self.file_path)
        wb.close()

    def write_rgby_noise_data(self, position, value):
        wb = load_workbook(self.file_path)
        sheet = wb[self.sheet_name]

        r_cell = sheet.cell(row=position[conf.R][0], column=position[conf.R][1])
        r_cell.value = "R：%s%%" % str(value[conf.R])
        g_cell = sheet.cell(row=position[conf.G][0], column=position[conf.G][1])
        g_cell.value = "G：%s%%" % str(value[conf.G])
        b_cell = sheet.cell(row=position[conf.B][0], column=position[conf.B][1])
        b_cell.value = "B：%s%%" % str(value[conf.B])
        y_cell = sheet.cell(row=position[conf.Y][0], column=position[conf.Y][1])
        y_cell.value = "Y：%s%%" % str(value[conf.Y])

        wb.save(self.file_path)
        wb.close()

    def write_color_accuracy_data(self, position, value):
        wb = load_workbook(self.file_path)
        sheet = wb[self.sheet_name]

        e1_cell = sheet.cell(row=position[conf.E1][0], column=position[conf.E1][1])
        e1_cell.value = "△E1：%s%%" % str(value[conf.E1])
        c1_cell = sheet.cell(row=position[conf.C1][0], column=position[conf.C1][1])
        c1_cell.value = "△C1：%s%%" % str(value[conf.C1])
        c2_cell = sheet.cell(row=position[conf.C2][0], column=position[conf.C2][1])
        c2_cell.value = "△C2：%s%%" % str(value[conf.C2])
        sat_cell = sheet.cell(row=position[conf.Sat][0], column=position[conf.Sat][1])
        sat_cell.value = "Sat：%s%%" % str(value[conf.Sat])

        wb.save(self.file_path)
        wb.close()


if __name__ == '__main__':
    from Common.color_data_filter import CSVTestData
    from Common.get_report_position import GetReportPosition

    w_r = WriteReport(conf.template_path, conf.sheet_name)
    report_position = GetReportPosition(conf.template_path, conf.sheet_name)

    # 灰阶测试
    # csv = CSVTestData(conf.hj_data_path)
    # hj_data = csv.get_hj_relate_data(csv.read_csv_to_matrix())
    # print(hj_data)
    #
    #
    # dr_key_pos = report_position.find_scenario_position_by_keyword(conf.r_dynamic_range)
    # print(dr_key_pos)
    # dr_pos = report_position.get_hj_relate_position(dr_key_pos)
    # print(dr_pos)
    # w_r.write_dynamic_range_data(dr_pos, hj_data)
    #
    # contrast_key_pos = report_position.find_scenario_position_by_keyword(conf.r_contrast_test)
    # print(contrast_key_pos)
    # contrast_pos = report_position.get_hj_relate_position(contrast_key_pos)
    # print(contrast_pos)
    # w_r.write_contrast_data(contrast_pos, hj_data)
    #
    # readable_key_pos = report_position.find_scenario_position_by_keyword(conf.r_readable_hj_num)
    # print(readable_key_pos)
    # readable_pos = report_position.get_hj_relate_position(readable_key_pos)
    # print(readable_pos)
    # w_r.write_readable_hj_data(readable_pos, hj_data)

    # color check
    csv = CSVTestData(conf.f_data_path)
    data = csv.read_csv_to_matrix()
    # snr
    f_key_position = report_position.find_scenario_position_by_keyword(conf.r_F_light)
    snr_data = csv.get_snr_data(data)
    snr_position = report_position.get_snr_position(f_key_position)
    w_r.write_snr_data(snr_position, snr_data)
    # 白平衡
    white_balance_data = csv.get_white_balance_err_data(data)
    white_balance_position = report_position.get_white_balance_position(f_key_position)
    w_r.write_white_balance_data(white_balance_position, white_balance_data)
    # 噪点测试
    noise_data = csv.get_rgby_noise_data(data)
    noise_position = report_position.get_rgby_noise_position(f_key_position)
    w_r.write_rgby_noise_data(noise_position, noise_data)
    # 颜色偏差 / 饱和度测试
    saturation_data = csv.get_color_accuracy_data(data)
    saturation_position = report_position.get_color_accuracy_position(f_key_position)
    w_r.write_color_accuracy_data(saturation_position, saturation_data)




