if __name__ == '__main__':
    import shutil
    import os
    import yaml
    from Conf.config import Config
    from Common.write_report_data import WriteReport

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

    w_r = WriteReport(conf.template_path, conf.sheet_name)
    w_r.camera_pixels = data["CameraData"]["pixels"]

    w_r.write_project_name({"project_name": data["CameraData"]["project_name"], "pixels": data["CameraData"]["pixels"],
                            "camera_product": data["CameraData"]["camera_product"]})
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

    shutil.move(conf.template_path, os.path.join(conf.project_path, data["CameraData"]["report_file_name"]))
