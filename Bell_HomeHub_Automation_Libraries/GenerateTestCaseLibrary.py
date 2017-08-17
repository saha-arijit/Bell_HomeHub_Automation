############################################################################################################################
# Description : GenerateTestCase contains a library that will validate and create the Test Command File.
# Developer   : Govinda Revanwar
# Date        : -
# Modified By : 
############################################################################################################################
"""
*GenerateTestCase*  contains a library that will validate and create Test Command File.
"""
import os
import time
import datetime
import TestParameterValidationLibrary
from robot.api.deco import keyword

@keyword('Library Command')
def comment(*message):
	pass

"""Global Parameter initilization
	ConfigFilePath			-			User Configuration which
	Execution Mode			-			Auto or Manual
	Directory 				-			Initially set to None
"""
Directory = None
ConfigFilePath = "userconfig.txt"
global_execMode_in = None

def SetUserConfig():
	"""
            Function Name        : SetUserConfig
            Function Description : This function will read the user configuration values from userconfig.txt file and use it for further execution.
            Inputs   : userconfig.txt file.
			Output	 : User Config parameters
					   var_ssid_in, var_pw_in, var_ap_in, var_apver_in, var_waversion, var_wahostname, var_wausername, var_wapassword, var_wasshkey	
    """    
	global var_ssid_in, var_pw_in, var_ap_in, var_apver_in, var_waversion, var_wahostname, var_wausername, var_wapassword, var_wasshkey, var_debug_level_in
	configFile = open(ConfigFilePath, 'r')
	content = configFile.read()
	lines = content.split("\n")
	#print len(lines)
	for eachline in lines:
		#print eachline
		str = eachline
		#print str.find("var_ssid_in}")
		if (str.find("var_ssid_in}")>0):
			start = str.index("}")
			end = str.index("#")
			substr = str[start+1:end]
			substr = substr.replace(" ","")
			substr.strip()
			var_ssid_in = substr
		#	print var_ssid_in
		elif (str.find("var_pw_in}")>0):
			start = str.index("}")
			end = str.index("#")
			substr = str[start+1:end]
			substr = substr.replace(" ","")
			substr.strip()
			var_pw_in = substr
		#	print var_pw_in
		elif (str.find("var_ap_in}")>0):
			start = str.index("}")
			end = str.index("#")
			substr = str[start+1:end]
			substr = substr.replace(" ","")
			substr.strip()
			var_ap_in = substr
		elif (str.find("var_apver_in}")>0):
			start = str.index("}")
			end = str.index("#")
			substr = str[start+1:end]
			substr = substr.replace(" ","")
			substr.strip()
			var_apver_in = substr
		elif (str.find("var_waversion}")>0):
			start = str.index("}")
			end = str.index("#")
			substr = str[start+1:end]
			substr = substr.replace(" ","")
			substr.strip()
			var_waversion = substr
		elif (str.find("var_wahostname}")>0):
			start = str.index("}")
			end = str.index("#")
			substr = str[start+1:end]
			substr = substr.replace(" ","")
			substr.strip()
			var_wahostname = substr
		elif (str.find("var_wausername}")>0):
			start = str.index("}")
			end = str.index("#")
			substr = str[start+1:end]
			substr = substr.replace(" ","")
			substr.strip()
			var_wausername =  substr
		elif (str.find("var_wapassword}")>0):
			start = str.index("}")
			end = str.index("#")
			substr = str[start+1:end]
			substr = substr.replace(" ","")
			substr.strip()
			var_wapassword = substr
		elif (str.find("var_wasshkey}")>0):
			start = str.index("}")
			end = str.index("#")
			substr = str[start+1:end]
			substr = substr.replace(" ","")
			substr.strip()
			var_wasshkey = substr
		elif (str.find("var_debug_level_in}")>0):
			start = str.index("}")
			end = str.index("#")
			substr = str[start+1:end]
			substr = substr.replace(" ","")
			substr.strip()
			var_debug_level_in = substr
	#print "*****SUC*****value of ssid is %s" % var_ssid_in

def SetExecutionMode(var_execMode_in):
	"""
            Function Name        : SetExecutionMode
            Function Description : This function will set the exeuction mode either Manual or Automation. Depends upon user input the location for saving command file will be decided.
            Inputs   : Execution Mode "Manual or Auto"
			Output	 : 
					Execution mode it set to Manual then the test command will be saved under //Bell HomeHub Automation/Bell_Homehub_Automation_TestCommand/TC_Manual
					Execution mode it set to Auto then the test command will be saved under //Bell HomeHub Automation/Bell_Homehub_Automation_TestCommand/TC_YYYYmmDD-MMHHSS
					   
			
    """
	global global_execMode_in, Directory
	global_execMode_in = var_execMode_in
	#print Directory
	
	if global_execMode_in == "Auto":
		print "*****ExecM***** execution mode set to Auto"
		global_execMode_in = "Auto"
		if not Directory:
			print "*****ExecM***** As Directory is not created Previously Creating new"
			ts = time.time()
			st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d-%H%M%S')
			Directory = "../Bell_Homehub_Automation_TestCommand/TC_"+st+"/"
			print "Created New Directory : "+Directory
			if not os.path.exists(Directory):
				os.makedirs(Directory)

def CreateTestCommand(var_test_name_in, var_test_type_in, var_load_mode_in, var_direction_in, var_band_selection_in, var_channel_in, var_frameSize_in, var_loads_in, var_expectConn_in, var_source_in, var_destination_in, var_duration_in, var_mcs_in, var_ss_in, var_bw_in, var_gi_in, var_eth_dut_in, var_w_dut_in, var_w_grouptype_in, var_savepcaps_in, var_throughput_multiplier_in):
	"""
		Function Name        : CreateTestCommand
		Function Description : Validates the test parameter entered by the user On successful validation generates test command file.
		Inputs   : 
			var_test_name_in             - Test name Provided by user in RIDE or if not provided the Robot Automation will creates it own
			var_test_type_in             -   Type of Test "TP" or "RR" or "Lat" or "MaxClient".                 
			var_load_mode_in             -   Auto or Manual.
			var_direction_in             -   Bi-Directional (1) or Uni-Directional (0) .
			var_band_selection_in        -   2.4G or 5G
			var_channel_in               -   The channel to be used  are 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 36, 40, 44, 48, 52, 56, 60, 647, 
												100, 104, 108, 112, 166, 120, 124, 128, 132, 136, 140, 149, 153, 157, 161, 165.
			var_frameSize_in             -   User can Enter Frame size "1518, 1024, 512, 64"
			var_loads_in                 -   Frame size to be used
			var_expectConn_in            -   Expected Connection (102) ,Use only for MaxClient.
			var_source_in                -   "W_AC" or "W_N" or "W_G" or "ETH"
			var_destination_in           -   "W_AC" or "W_N" or "W_G" or "ETH"
			var_duration_in              -   Duration entered In seconds
			var_mcs_in                   -   MCS values can be '9' ,'8', '7', '6', '5', '4', '3', '2', '1', 'N', '31', '23', '15'.
			var_ss_in                    -   SS values can be 1 or 2 or 3 or 4
			var_bw_in                    -   Bandwidth can be 20 or 40 or 80
			var_gi_in                    -   Guard Interval can be "short" or "long".
			var_eth_dut_in               -   Ethernet port entered by the user.
			var_w_dut_in                 -   Wireless port entered by the user.
			var_w_grouptype_in           -   Wireless group type (802.11ac or 802.11bg or 802.11n or 802.3 or 802.11a or 802.11n5G )
			var_savepcaps_in             -   Enables wireshark trace capture in IxVeriwave via Wave Automation.("Yes" or "No")
			var_throughput_multiplier_in -   Throughput Multiplier (0.9),Used only for TP Test cases.
			Directory                       -   Directory where the .bat file is present.
		Outputs  : 
			On Successfully parameter validation generates test command file.

	"""
	global global_test_name_in, global_test_type_in, global_load_mode_in, global_direction_in, global_band_selection_in, global_channel_in, global_frameSize_in, global_loads_in, global_expectConn_in, global_source_in, global_destination_in, global_duration_in, global_mcs_in, global_ss_in, global_bw_in, global_gi_in, global_eth_dut_in, global_w_dut_in, global_w_grouptype_in, global_savepcaps_in, global_throughput_multiplier_in, Directory
	
	#Initially Write to Command File set to True
	writeToFile = True
	
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
	#If the test type rather than TP then setting the Throughput Multiplier is set to None
	if var_test_type_in !="TP":
		global_throughput_multiplier_in = None

	
	if "_" in var_destination_in:			#Truncate destination if _ is present
		dest = var_destination_in.split("_")
		var_dest_splited = dest[1]
	
	if not var_test_name_in:				#If Test Name is not defiened by user create atomatically
		var_test_name_in = var_dest_splited+"-"+var_test_type_in+"-"+str(var_band_selection_in)+"G-"+str(var_bw_in)+"MHz-"+str(var_ss_in)+"ss-"+str(var_channel_in)+"c"
		print "****CTC**** Test name is null Automatically Created Test Name is: " + var_test_name_in
		global_test_name_in = var_test_name_in
	else :
		print "*****CTC**** Test Name is : "+var_test_name_in
	
	#Created Object for Test PArameter Validation Library
	tpv = TestParameterValidationLibrary.testParameterValidation()
	isParametersValid = tpv.parameterValidation(global_test_name_in, global_test_type_in, global_load_mode_in, global_direction_in, global_band_selection_in, global_channel_in, global_frameSize_in, global_loads_in, global_expectConn_in, global_source_in, global_destination_in, global_duration_in, global_mcs_in, global_ss_in, global_bw_in, global_gi_in, global_eth_dut_in, global_w_dut_in, global_w_grouptype_in, global_savepcaps_in, global_throughput_multiplier_in, Directory)
	
	if(isParametersValid == True):
		print "*****CTC***** Parameter Validations are done all parameters are valid "
	else:
		print "!!!!!CTC!!!!! Test Parameter Validation Failed please check the logs for more details"
		writeToFile = False


	isDepedencyCheckSuccess = tpv.parameterDependencyValidation(global_test_type_in, global_source_in, global_destination_in, global_band_selection_in, global_channel_in, global_bw_in, global_mcs_in)
	
	if(isDepedencyCheckSuccess == True):
		print "*****CTC***** Parameter Dependancy check are done Successfully "
	else:
		print "!!!!!CTC!!!!! Parameter Dependancy Validation Failed please check the logs for more details"
		writeToFile = False
	