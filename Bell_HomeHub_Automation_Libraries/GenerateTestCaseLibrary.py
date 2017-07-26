#  ECIN Networks
#  Copyright 2017     Robot Framework Foundation

def CreateTestCommand(var_test_name_in, var_test_type_in, var_load_mode_in, var_direction_in, var_band_selection_in, var_channel_in, var_frameSize_in, var_loads_in, var_expectConn_in, var_source_in, var_destination_in, var_duration_in, var_mcs_in, var_ss_in, var_bw_in, var_gi_in, var_eth_dut_in, var_w_dut_in, var_w_grouptype_in, var_savepcaps_in, var_throughput_multiplier_in):
	
	global global_test_name_in, global_test_type_in, global_load_mode_in, global_direction_in, global_band_selection_in, global_channel_in, global_frameSize_in, global_loads_in, global_expectConn_in, global_source_in, global_destination_in, global_duration_in, global_mcs_in, global_ss_in, global_bw_in, global_gi_in, global_eth_dut_in, global_w_dut_in, global_w_grouptype_in, global_savepcaps_in, global_throughput_multiplier_in, Directory
	
	global_test_name_in = var_test_name_in
	global_test_type_in = var_test_type_in
	global_load_mode_in = var_load_mode_in 
	global_direction_in = str(var_direction_in) 
	global_band_selection_in = str(var_band_selection_in )
	global_channel_in = var_channel_in
	global_frameSize_in = var_frameSize_in 
	global_loads_in = var_loads_in
	global_expectConn_in = str(var_expectConn_in)
	global_source_in = var_source_in
	global_destination_in = var_destination_in 
	global_duration_in = var_duration_in 
	global_mcs_in = var_mcs_in 
	global_ss_in = str(var_ss_in)
	global_bw_in = str(var_bw_in )
	global_gi_in = var_gi_in 
	global_eth_dut_in = var_eth_dut_in 
	global_w_dut_in = var_w_dut_in 
	global_w_grouptype_in = var_w_grouptype_in 
	global_savepcaps_in = var_savepcaps_in 
	global_throughput_multiplier_in = var_throughput_multiplier_in
	if var_test_type_in !="TP":
		global_throughput_multiplier_in = None

	print "Execution starts for GenerateTestCase Library"

