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


if __name__ == '__main__':
    from Common.color_data_filter import CSVTestData
    from Common.get_report_position import GetReportPosition
    csv = CSVTestData(conf.hj_data_path)
    hj_data = csv.get_hj_relate_data(csv.read_csv_to_matrix())

    report_position = GetReportPosition(conf.template_path, conf.sheet_name)
    dr_key_pos = report_position.find_scenario_position_by_keyword(conf.r_dynamic_range)
    print(dr_key_pos)
    dr_pos = report_position.get_hj_relate_position(dr_key_pos)
    print(dr_pos)

    # scenario = report_position.find_scenario_position_by_keyword(conf.r_dynamic_range)
    # print(scenario)
    # print(report_position.get_hj_relate_position(scenario))

    w_r = WriteReport(conf.template_path, conf.sheet_name)
    w_r.write_dynamic_range_data(dr_pos, hj_data)