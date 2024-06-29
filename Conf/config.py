import os


class Config:
    project_path = os.getcwd()

    hj_name = "HJ.csv"
    f_name = "F.csv"
    cwf_name = "CWF.csv"
    d65_name = "D65.csv"
    tl83_name = "TL83.csv"
    tl84_name = "TL84.csv"
    mix_name = "Mix.csv"
    # template_name = ""
    template_quality_name = "Template_Quality.xlsx"
    template_standard_name = "Template_Standard.xlsx"
    sheet_name = "指标数据"

    hj_data_path = os.path.join(project_path, "TestData", "HJ", hj_name)
    f_data_path = os.path.join(project_path, "TestData", "F", f_name)
    cwf_data_path = os.path.join(project_path, "TestData", "CWF", cwf_name)
    d65_data_path = os.path.join(project_path, "TestData", "D65", d65_name)
    tl83_data_path = os.path.join(project_path, "TestData", "TL83", tl83_name)
    tl84_data_path = os.path.join(project_path, "TestData", "TL84", tl84_name)
    mix_data_path = os.path.join(project_path, "TestData", "Mix", mix_name)
    report_template_base_path = os.path.join(project_path, "ReportTemplate")
    # template_path = os.path.join(report_template_base_path, template_name)
    origin_template_quality_path = os.path.join(report_template_base_path, "Template", template_quality_name)
    origin_template_standard_path = os.path.join(report_template_base_path, "Template", template_standard_name)

    # 色彩专业名词
    wb_err_s = "WB ERR S(HSV)"
    y_noise = "Y-noise%"
    r_noise = "R-noise%"
    g_noise = "R-noise%"
    b_noise = "B-noise%"
    snr_bw = "SNR_BW"

    # 色彩偏差关键字
    Sat_key = "Mean camera chroma %"
    C1_key = "Mean  Delta-C sat corr"
    C2_key = "Mean  Delta-C uncorr"
    E1_key = "Mean  Delta-E*ab uncorr"

    # 列, 报告RGBY坐标位置的key,测试数据返回字典的key
    R = "R"
    G = "G"
    B = "B"
    Y = "Y"

    nineteen = "19"
    twenty = "20"
    twenty_one = "21"
    twenty_two = "22"
    twenty_three = "23"
    twenty_four = "24"

    # 提取返回的测试数据key， 报告坐标的key
    C1 = "C1"
    C2 = "C2"
    E1 = "E1"
    Sat = "Sat"

    dynamic_range_key = "Total"
    hj_relate_key = "Pixel/255"

    # 提取返回的测试数据key， 报告坐标的key
    hj_dynamic_range = "dynamic_range"
    hj_contrast = "contrast"
    hj_readable = "readable"
    r_hj_relate_pos = "hj_relate"

    # 报告相关关键字
    r_mix_light = "混光"
    r_D65_light = "6500K"
    r_TL84_light = "4000K"
    r_F_light = "2700K"
    r_CWF_light = "4150K"
    r_TL83_light = "3000K"

    r_contrast_test = "对比度"
    r_readable_hj_num = "可读灰阶数"
    r_dynamic_range = "Dynamic Range"

    r_test_project = "测试项目"
    r_camera_p_last_key = "闪光均匀性(暗边)"
    r_camera_standard = "判定标准（标准）"
    r_camera_most_standard = "判定标准（精品）"



