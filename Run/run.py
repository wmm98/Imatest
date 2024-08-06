if __name__ == '__main__':
    import shutil
    import os
    import yaml
    from Conf.config import Config
    from Common.write_report_data import WriteReport

    conf = Config()
    yaml_file_path = os.path.join(conf.project_path, "Conf", "test_data.yaml")
    # 加载 YAML 文件
    with open(yaml_file_path, 'r', encoding="utf-8") as file:
        data = yaml.safe_load(file)

    # 复制模板
    # 如果是精品
    template_path = ""  # 定义复制后的模板名称
    tmp_path = ""
    if data["CameraData"]["standard"]:
        template_path = os.path.join(conf.report_template_base_path, conf.template_quality_name)
        origin_path_path = conf.origin_template_quality_path
        if os.path.exists(template_path):
            os.remove(template_path)
        shutil.copy(conf.origin_template_quality_path, conf.report_template_base_path)
    else:
        template_path = os.path.join(conf.report_template_base_path, conf.template_standard_name)
        origin_path_path = conf.origin_template_standard_path
        if os.path.exists(template_path):
            os.remove(template_path)
        shutil.copy(conf.origin_template_standard_path, conf.report_template_base_path)

    w_r = WriteReport(template_path, template_path, conf.sheet_name)
    w_r.is_quality = data["CameraData"]["standard"]

    w_r.write_project_name({"project_name": data["CameraData"]["project_name"], "pixels": data["CameraData"]["pixels"],
                            "camera_product": data["CameraData"]["camera_product"]})
    # F
    if data["CameraData"]["is_f_test"]:
        w_r.write_scenario_data(conf.f_data_path, conf.r_F_light)
        # 处理问题汇总
        if len(w_r.F_light_description) != 0:
            w_r.F_light_description.insert(0, "A光")
            w_r.questions_summary.append(w_r.F_light_description)
    # cwf
    if data["CameraData"]["is_cwf_test"]:
        w_r.write_scenario_data(conf.cwf_data_path, conf.r_CWF_light)
        if len(w_r.CWF_light_description) != 0:
            w_r.CWF_light_description.insert(0, "CWF光")
            w_r.questions_summary.append(w_r.CWF_light_description)

    if data["CameraData"]["is_d65_test"]:
        w_r.write_scenario_data(conf.d65_data_path, conf.r_D65_light)
        if len(w_r.D65_light_description) != 0:
            w_r.D65_light_description.insert(0, "D65光")
            w_r.questions_summary.append(w_r.D65_light_description)

    if data["CameraData"]["is_tl84_test"]:
        w_r.write_scenario_data(conf.tl84_data_path, conf.r_TL84_light)
        if len(w_r.TL84_light_description) != 0:
            w_r.TL84_light_description.insert(0, "TL84光")
            w_r.questions_summary.append(w_r.TL84_light_description)

    # 灰阶测试数据
    if data["CameraData"]["is_hj_test"]:
        w_r.write_hj_data()
        if len(w_r.HJ_light_description) != 0:
            w_r.questions_summary.append(w_r.HJ_light_description)

    # 解像力数据,测试一室需要写解像力，二室不用
    if data["CameraData"]["is_team_one"]:
        team = 1
    else:
        team = 2
    jxl_data = {"team": team, "pixels": data["CameraData"]["pixels"]}
    if data["CameraData"]["is_jxl_test"]:
        w_r.write_jxl_data(jxl_data)
        if len(w_r.JXL_light_description) != 0:
            w_r.JXL_light_description.insert(0, "解析力")
            w_r.questions_summary.append(w_r.JXL_light_description)

    # 写入问题汇总
    w_r.write_questions_summary_data()

    shutil.move(template_path, os.path.join(conf.project_path, data["CameraData"]["report_file_name"]))
