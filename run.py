if __name__ == '__main__':
    from Common.write_report_data import WriteReport
    from Conf.config import Config
    conf = Config()
    w_r = WriteReport(conf.template_path, conf.sheet_name)
    # 灰阶测试数据
    w_r.write_hj_data()
    # F光
    w_r.write_scenario_data(conf.f_data_path, conf.r_F_light)
    # cwf
    w_r.write_scenario_data(conf.cwf_data_path, conf.r_CWF_light)
    w_r.write_scenario_data(conf.d65_data_path, conf.r_D65_light)
    # w_r.write_scenario_data(conf.tl83_data_path, conf.r_TL83_light)
    w_r.write_scenario_data(conf.tl84_data_path, conf.r_TL84_light)
    # w_r.write_scenario_data(conf.mix_data_path, conf.r_mix_light)
