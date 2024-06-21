import os


class Config:
    project_path = os.path.dirname(os.getcwd())

    f_name = "F.csv"
    hj_name = "HJ.csv"
    template_name = "Template.xlsx"

    f_data_path = os.path.join(project_path, "TestData", "F", f_name)
    hj_data_path = os.path.join(project_path, "TestData", "HJ", hj_name)
    template_path = os.path.join(project_path, "ReportTemplate", template_name)

    # 色彩专业名词
    wb_err_s = "WB ERR S(HSV)"
    y_noise = "Y-noise%"
    r_noise = "R-noise%"
    g_noise = "R-noise%"
    b_noise = "B-noise%"


