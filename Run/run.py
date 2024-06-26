if __name__ == '__main__':
    import shutil
    import os
    import yaml
    from Common.write_report_data import WriteReport
    from Conf.config import Config
    conf = Config()

    # 复制模板
    if os.path.exists(conf.template_path):
        os.remove(conf.template_path)
    shutil.copy(conf.origin_template_path, conf.report_template_base_path)
    if not os.path.exists(conf.template_path):
        shutil.copy(conf.origin_template_path, conf.report_template_base_path)

    yaml_file_path = os.path.join(conf.project_path, "Conf", "test_data.yaml")
    # 加载 YAML 文件
    with open(yaml_file_path, 'r', encoding="utf-8") as file:
        data = yaml.safe_load(file)
    # data["CameraData"]["pixels"]
    # data["CameraData"]["project_name"]
    # data["CameraData"]["camera_product"]
    # data["CameraData"]["is_f_test"] = "true"
    # data["CameraData"]["is_d65_test"] = "true"
    # data["CameraData"]["is_tl84_test"] = "true"
    # data["CameraData"]["is_tl83_test"] = "true"
    # data["CameraData"]["is_cwf_test"] = "true"
    # data["CameraData"]["is_hj_test"] = "true"
    # data["CameraData"]["is_mix_test"] = "true"
    #
    w_r = WriteReport(conf.template_path, conf.sheet_name)
    # 灰阶测试数据
    if data["CameraData"]["is_hj_test"]:
        w_r.write_hj_data()
    # F
    if data["CameraData"]["is_f_test"]:
        w_r.write_scenario_data(conf.f_data_path, conf.r_F_light)
    # cwf
    if data["CameraData"]["is_cwf_test"]:
        w_r.write_scenario_data(conf.cwf_data_path, conf.r_CWF_light)
    if data["CameraData"]["is_d65_test"]:
        w_r.write_scenario_data(conf.d65_data_path, conf.r_D65_light)
    if data["CameraData"]["is_tl83_test"]:
        w_r.write_scenario_data(conf.tl83_data_path, conf.r_TL83_light)
    if data["CameraData"]["is_tl84_test"]:
        w_r.write_scenario_data(conf.tl84_data_path, conf.r_TL84_light)
    if data["CameraData"]["is_mix_test"]:
        w_r.write_scenario_data(conf.mix_data_path, conf.r_mix_light)

    file_name = "招投标规格参数确认-%s-%s-%d万摄像头-指标测试报告.csv" % (data["CameraData"]["camera_product"],
                                                       data["CameraData"]["project_name"], int(data["CameraData"]["pixels"]))
    if os.path.exists(file_name):
        os.remove(file_name)

    shutil.move(conf.template_path, os.path.join(conf.project_path, file_name))
