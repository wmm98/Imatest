from openpyxl import load_workbook
from openpyxl.styles import Font
from Conf.config import Config
conf = Config()


class ReportWrite:
    def __init__(self, file_path, sheet_name):
        self.file_path = file_path
        self.sheet_name = sheet_name

    def write_hj_data(self, hj_test_data):
        wb = load_workbook(self.file_path)
        sheet = wb[self.sheet_name]

        print(sheet)
        red_font = Font(color="FF0000")

        # 写入灰阶动态范围
        dynamic_range_cell = sheet['E57']
        dynamic_range = hj_test_data[conf.hj_dynamic_range]
        dynamic_range_cell.value = dynamic_range
        if dynamic_range <= 5.5:
            dynamic_range_cell.font = red_font

        print(dynamic_range_cell.value)

        # 写入对比度
        contrast_cell = sheet['E58']
        contrast = hj_test_data[conf.hj_contrast]
        contrast_cell.value = str(contrast * 100) + "%"
        if contrast <= 0.75:
            contrast_cell.font = red_font

        # 写入可读灰阶数
        readable_cell = sheet['E59']
        readable = hj_test_data[conf.hj_readable]
        readable_cell.value = readable
        if contrast < 19:
            readable_cell.font = red_font

        # 保存#并且关闭工作簿
        wb.save(self.file_path)
        wb.close()




if __name__ == '__main__':
    from Common.color_data_filter import CSVTestData
    csv = CSVTestData(conf.hj_data_path)
    hj_data = csv.get_hj_relate_data(csv.read_csv_to_matrix())
    print(hj_data)
    report = ReportWrite(conf.template_path, conf.sheet_name)
    report.write_hj_data(hj_data)
