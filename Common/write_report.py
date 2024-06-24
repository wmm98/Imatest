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
        red_font = Font(color="FF0000")

        # 写入灰阶动态范围
        dynamic_range_cell = sheet['E22']
        dynamic_range = hj_test_data[conf.hj_dynamic_range]
        dynamic_range_cell.value = dynamic_range
        if dynamic_range <= 5.5:
            dynamic_range_cell.font = red_font

        # 写入对比度
        contrast_cell = sheet['E23']
        contrast = hj_test_data[conf.hj_contrast]
        contrast_cell.value = str(contrast * 100) + "%"
        if contrast <= 0.75:
            contrast_cell.font = red_font

        # 写入可读灰阶数


        # 保存文件
        wb.save(self.file_path)
        # 关闭工作簿
        wb.close()


if __name__ == '__main__':
    report = ReportWrite(conf.template_path, conf.sheet_name)
    report.get_report_sheet()
