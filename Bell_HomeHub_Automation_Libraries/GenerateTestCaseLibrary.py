#########################################################################################################################################
# Description : GenerateTestCaseLibrary contains a library that will validate the generate Test Parameters set by user in Robot Framework.
# Developer   : Govinda Revanwar
# Date        : -
# Modified By : Kiran Mandal
#########################################################################################################################################
"""
*GenerateTestCaseLibrary*  contains a library that will validate the generate Test Parameters set by user in Robot Framework.
"""


import os
import time
import datetime
import Logger
import TestParameterValidationLibrary
from robot.api.deco import keyword

ROBOT_LIBRARY_SCOPE = 'GLOBAL'
ROBOT_LIBRARY_VERSION = '0.0.1'
Directory = None
ConfigFilePath = "userconfig.txt"
global_execMode_in = None



class GenerateTestCaseLibrary:
    
    @keyword('Library Command')
    def comment(*message):
        pass
        
    #Initialization of Logger File
    

    def SetUserConfig(self):
        """
            Function Name        : SetUserConfig
            Function Description : This function will read the configuration parameter from userconfig.txt file and use in exeuction .
            Inputs   : 
                
            Outputs  : 
                Configures the parameter from userconfig.txt
                
        """ 
            
        global var_ssid_in, var_pw_in, var_ap_in, var_apver_in, var_waversion, var_wahostname, var_wausername, var_wapassword, var_wasshkey, var_debug_level_in
        try:
            configFile = open(ConfigFilePath, 'r')
            content = configFile.read()
            lines = content.split("\n")
        except IOError as e:
            err = "Input/Output error: %s" % ( str(e) )
            raise MyException(err)
        #print len(lines)
        for eachline in lines:
            #print eachline
            str = eachline
            try:
                #print str.find("var_ssid_in}")
                if (str.find("var_ssid_in}")>0):
                    start = str.index("}")
                    end = str.index("#")
                    substr = str[start+1:end]
                    substr = substr.replace(" ","")
                    substr.strip()
                    var_ssid_in = substr
                #   print var_ssid_in
                elif (str.find("var_pw_in}")>0):
                    start = str.index("}")
                    end = str.index("#")
                    substr = str[start+1:end]
                    substr = substr.replace(" ","")
                    substr.strip()
                    var_pw_in = substr
                #   print var_pw_in
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
            except ValueError as e:
                err = "Value Error is %s" % ( str(e) )
                raise MyException(err)
                            
        #print "*****SUC*****value of ssid is %s" % var_ssid_in

    
                
    def SetExecutionMode(self,var_execMode_in):
        """
            Function Name        : SetExecutionMode
            Function Description : If the Execution mode is Auto It creates a directory with time stamp.
            Inputs   : 
                var_execMode_in  : Auto or Manual.
            Outputs  : 
                Configures the parameter from userconfig.txt
                
        """ 
            
        global global_execMode_in, Directory
        global_execMode_in = var_execMode_in
        #print Directory
        
            
        '''if global_execMode_in == "Manual" or global_execMode_in == "manual":
            print "*****ExecM***** execution mode set to manual"
            global_execMode_in = "Manual"
            Directory = "../Bell_Homehub_Automation_TestCommand/TC_Manual"+"/"
            if not os.path.exists(Directory):
                os.makedirs(Directory)  
        '''
        if global_execMode_in == "Auto":
            #print "*****ExecM***** execution mode set to Auto"
            Logger.messageLog("Execution mode has been set to AUTOMATIC by user.")
            global_execMode_in = "Auto"
                    
            if not Directory:
                #print "*****ExecM***** As Directory is not created Previously Creating new"
                Logger.messageLog("Initiating directory creation to store test command files.")
                ts = time.time()
                st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d-%H%M%S')
                Directory = "../Bell_Homehub_Automation_TestCommand/TC_"+st+"/"
                #print "Created New Directory : "+Directory
                try:    
                    if not os.path.exists(Directory):
                        os.makedirs(Directory)
                        Logger.messageLog(Directory + "  directory created to store test command files.")
                except OSError, e:
                    if os.path.exists(Directory):
                        #print "Directory is beign created successfully" ,Directory
                        Logger.messageLog(Directory + "  directory is already present.")
                    else:  
                        raise Exception ("Error faced in creating directory to store Test Case command files.")

        else:
            #print "global_execMode_in is not set to AUTO"
            Logger.messageLog("Execution mode has been set to MANUAL by user.")



        
    def CreateTestCommand(self,var_test_name_in, var_test_type_in, var_load_mode_in, var_direction_in, var_band_selection_in, var_channel_in, var_frameSize_in, var_loads_in, var_expectConn_in, var_source_in, var_destination_in, var_duration_in, var_mcs_in, var_ss_in, var_bw_in, var_gi_in, var_eth_dut_in, var_w_dut_in, var_w_grouptype_in, var_throughput_multiplier_in, var_savepcaps_in):
        """
            Function Name        : CreateTestCommand
            Function Description : Validates the test parameter entered by the user.
            Inputs   : 
                global_test_name_in             -   Test Name which is pre-defined in Robot Framework.      
                global_test_type_in             -   Type of Test "TP" or "RR" or "Lat" or "MaxClient".                 
                global_load_mode_in             -   Auto or Manual.
                global_direction_in             -   Bi-Directional (1) or Uni-Directional (0) .
                global_band_selection_in        -   2.4G or 5G
                global_channel_in               -   The channel to be used  are 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 36, 40, 44, 48, 52, 56, 60, 64, 
                                                    100, 104, 108, 112, 166, 120, 124, 128, 132, 136, 140, 149, 153, 157, 161, 165.
                global_frameSize_in             -   User can Enter Frame size "1518, 1024, 512, 64"
                global_loads_in                 -   Frame size to be used
                global_expectConn_in            -   Expected Connection (102) ,Use only for MaxClient.
                global_source_in                -   "W_AC" or "W_N" or "W_G" or "ETH"
                global_destination_in           -   "W_AC" or "W_N" or "W_G" or "ETH"
                global_duration_in              -   Duration entered In seconds
                global_mcs_in                   -   MCS values can be '9' ,'8', '7', '6', '5', '4', '3', '2', '1', 'N', '31', '23', '15'.
                global_ss_in                    -   SS values can be 1 or 2 or 3 or 4
                global_bw_in                    -   Bandwidth can be 20 or 40 or 80
                global_gi_in                    -   Guard Interval can be "short" or "long".
                global_eth_dut_in               -   Ethernet port entered by the user.
                global_w_dut_in                 -   Wireless port entered by the user.
                global_w_grouptype_in           -   Wireless group type (802.11ac or 802.11bg or 802.11n or 802.3 or 802.11a or 802.11n5G )
                global_savepcaps_in             -   Enables wireshark trace capture in IxVeriwave via Wave Automation.("Yes" or "No")
                global_throughput_multiplier_in -   Throughput Multiplier (0.9) as default,Used only for TP Test cases.
                Directory                       -   Directory where the .bat file is present.
            Outputs  : 
                Validates the Global Parameters.
                
        """ 
        
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
        
        loggerTest = Logger.CreateLogFile(__name__)

        #Throughput value 0.9 by default unless entered explicitly by user
        if not var_throughput_multiplier_in:
            var_throughput_multiplier_in = "0.9"
            Logger.messageLog("Value for Throughput has been set to : %f" %var_throughput_multiplier_in )
        
        
        global_throughput_multiplier_in = var_throughput_multiplier_in
        if var_test_type_in !="TP":
            global_throughput_multiplier_in = None

        #print "Execution starts for GenerateTestCase Library"
        
        lInt_frameSize_arr = var_frameSize_in.split(" ")
        var_mcs_in = str(var_mcs_in)
        lStr_mcs = var_mcs_in.split(" " )
        WriteFile = True    #Initially Write to Command File set to True
        
        if "_" in var_destination_in:           #Truncate destination if _ is present
            dest = var_destination_in.split("_")
            var_dest_splited = dest[1]
        
        if not var_test_name_in:                #If Test Name is not defiened by user create atomatically
            
            list_mcs = global_mcs_in.split(" ")
            if (len(list_mcs) > 1):
                #print ("THERE ARE MORE THAN ONE MCS   %d"  %len(list_mcs))
                Logger.messageLog ("Multiple MCS values has been provided for command creation.")
                var_test_name_in = var_dest_splited+"-"+var_test_type_in+"-"+str(var_band_selection_in)+"G-"+str(var_bw_in)+"MHz-"+str(var_ss_in)+"ss-"+str(var_channel_in)+"c"+"-mcs"
                #print "****CTC**** Test name is null Automatically Created Test Name is: " + var_test_name_in
                global_test_name_in = var_test_name_in
            else:
                #print "NO MORE THAN ONE MCS  %d" %len(list_mcs)
                Logger.messageLog ("Single MCS value have been provided for command creation.")
                var_test_name_in = var_dest_splited+"-"+var_test_type_in+"-"+str(var_band_selection_in)+"G-"+str(var_bw_in)+"MHz-"+str(var_ss_in)+"ss-"+str(var_channel_in)+"c"+"-"+list_mcs[0]+"mcs"
                #print "****CTC**** Test name is null Automatically Created Test Name is: " + var_test_name_in
                Logger.messageLog ("Custom Test Case Name has not been provided by user.")
                Logger.messageLog ("Automatically generated Test Case Name is : " + var_test_name_in)
                global_test_name_in = var_test_name_in
            
        else:
            Logger.messageLog ("Test Case Name entered by user : " + var_test_name_in)  

        ## Check for the Test Parameter Validations..............
        Logger.messageLog("Initiating Validation of Test Parameters.")      
        tpv = TestParameterValidationLibrary.testParameterValidation()
        isParametersValid = tpv.parameterValidation(global_test_name_in, global_test_type_in, global_load_mode_in, global_direction_in, 
                            global_band_selection_in, global_channel_in, global_frameSize_in, global_loads_in, global_expectConn_in, global_source_in, 
                            global_destination_in, global_duration_in, global_mcs_in, global_ss_in, global_bw_in, global_gi_in, global_eth_dut_in, 
                            global_w_dut_in, global_w_grouptype_in, global_savepcaps_in, global_throughput_multiplier_in, Directory)
        #print "*****CTC***** Parameter Validations are done all parameters valid = %r " %isParametersValid
        Logger.messageLog("Validation of Test Parameters completed successfully.")
        
        ## Incase of Test Parameter Validation not successful, Test Command file creation will be aborted.
        if(isParametersValid == False):
            raise AssertionError("!!!!!CTC!!!!! Test Parameter Validation Failed.")

        ## Check for the Test Parameter Dependency Validation
        Logger.messageLog("Initiating Dependency Validation of Test Parameters.")
        isDepedencyCheckSuccess = tpv.parameterDependencyValidation(global_test_type_in, global_source_in, global_destination_in, global_band_selection_in, 
                                    global_channel_in, global_bw_in, global_mcs_in)
        #print "*****CTC***** Parameter Dependency Validations: All Dependency check succeed = %r " %isDepedencyCheckSuccess
        Logger.messageLog("Validation of Test Dependency Parameters completed successfully.")

        #If parameter dependency validation failed then creating TestCommand file will gets aborted.
        if(isDepedencyCheckSuccess == False):
            raise AssertionError("!!!!!CTC!!!!! Test Parameter Dependancy Validation Failed")
        
        CommandFileName = Directory+var_test_name_in+".bat"
        #print "*****CTC***** Command File Name is : " +CommandFileName
        Logger.messageLog("Creating Test Command file : " + CommandFileName)
        
        if(isParametersValid == True):
        
            if(isDepedencyCheckSuccess == True):
                if(WriteFile == True):
                    Logger.messageLog("Initiating writing of data for .bat file creation.")
                    self.writeTestCommandToFile(CommandFileName)
                    Logger.messageLog("Created Test Command .bat file for : " + CommandFileName)
                    if(var_test_type_in == "TP"):
                        Logger.messageLog("Saving test case details for TP Test case in text TP_Values.txt file.")
                        self.SaveTPValue()
                        Logger.messageLog("Completed saving test case details in TP_Values.txt file.")
                    
                else:
                    #print "*****CTC**** Write to File flag is False"
                    Logger.errorLog("Test Command Write to File Flag found FALSE.")
                    raise AssertionError("Write to File flag is False")
                    
            else:
                #print "*****CTC**** Test Dependancy Validation Failed"
                Logger.errorLog("Test Parameter Dependancy Validation has FAILED.")
                raise AssertionError("Test Dependancy Validation Failed")
        else:
            #print "*****CTC**** Test Parameter Validation Failed"
            Logger.errorLog("Test Parameter Validation has FAILED.")
            raise AssertionError("Test Parameter Validation Failed")
        
        #print "*****CTC**** Command File Name: " + CommandFileName
        Logger.messageLog("Command File Created : " + CommandFileName)
        
    def writeTestCommandToFile(self,FileName):
        """
            Function Name        : writeTestCommandToFile
            Function Description : writes the test command to a (.bat) file.
            Inputs   : 
                FileName         : File name(.bat file)
            Outputs  : 
                creates a (.bat file)
                
        """ 

        global global_test_name_in, global_test_type_in, global_load_mode_in, global_direction_in, global_band_selection_in, global_channel_in, global_frameSize_in, global_loads_in, global_expectConn_in, global_source_in, global_destination_in, global_duration_in, global_mcs_in, global_ss_in, global_bw_in, global_gi_in, global_eth_dut_in, global_w_dut_in, global_w_grouptype_in, global_savepcaps_in, global_throughput_multiplier_in
        try:
            CreateCommandFile = open(FileName, "w+")
            Logger.messageLog ("Opening " + FileName + "  for writing data for test command creation.")
        except IOError as e:
            err = "Input/Output error: %s" % ( str(e) )
            Logger.errorLog ("Cannot open " + FileName + " to write data for Test Command creation.")
            raise MyException(err)
        
        #print "*****WTC***** Direction is : " + str(global_direction_in)
        
        try:
            if(global_direction_in == "0" or global_test_type_in == "RR" or global_test_type_in == "MaxClient" ):
                #print "*****CTC***** Writing to uni Directional file."
                Logger.messageLog ("Creating UNI-DIRECTIONAL Test Command File.")
                
                CreateCommandFile.write("::"+global_test_name_in)
                CreateCommandFile.write("\n")
                CreateCommandFile.write("tclsh ..\\..\\bin\\vw_auto.tcl -f "+global_test_type_in+".tcl ^")
                CreateCommandFile.write("\n")
                CreateCommandFile.write("--var ssid "+"\""+var_ssid_in+"\" ^")
                CreateCommandFile.write("\n")
                CreateCommandFile.write("--var pw "+"\""+var_pw_in+"\" ^")
                CreateCommandFile.write("\n")
                CreateCommandFile.write("--var save \"C:\\WifiResults\\"+var_ap_in+"\\"+var_apver_in+"\\"+var_ssid_in+"\\"+global_test_type_in+"\\DS\" ^")
                if(global_test_name_in == "MaxClient"):
                    CreateCommandFile.write("--pause 60 ^")
                    CreateCommandFile.write("\n")
                    
                CreateCommandFile.write("\n")
                CreateCommandFile.write("--var ap \""+var_ap_in+ "\" ^")
                CreateCommandFile.write("\n")
                CreateCommandFile.write("--var apver \""+var_apver_in+"\" ^")
                CreateCommandFile.write("\n")
                CreateCommandFile.write("--var channel \""+str(global_channel_in)+"\" ^")
                CreateCommandFile.write("\n")
                CreateCommandFile.write("--var frameSize \""+global_frameSize_in+"\" ^")
                CreateCommandFile.write("\n")
                CreateCommandFile.write("--var loads \""+global_loads_in+"\" ^")
                CreateCommandFile.write("\n")       
                CreateCommandFile.write("--var expectConn \""+str(global_expectConn_in)+"\" ^")
                CreateCommandFile.write("\n")       
                       
                CreateCommandFile.write("--var source \""+global_source_in+"\" ^")
                CreateCommandFile.write("\n")       
                CreateCommandFile.write("--var destination \""+global_destination_in+"\" ^")
                CreateCommandFile.write("\n")       
                CreateCommandFile.write("--var duration \""+str(global_duration_in)+"\" ^")
                CreateCommandFile.write("\n")
                CreateCommandFile.write("--var mcs \""+global_mcs_in+"\" ^")
                CreateCommandFile.write("\n")
                CreateCommandFile.write("--var ss \""+str(global_ss_in)+"\" ^")
                CreateCommandFile.write("\n")
                CreateCommandFile.write("--var bw \""+str(global_bw_in)+"\" ^")
                CreateCommandFile.write("\n")
                CreateCommandFile.write("--var gi \""+global_gi_in+"\" ^")
                CreateCommandFile.write("\n")
                CreateCommandFile.write("--var eth_dut \""+global_eth_dut_in+"\" ^")
                CreateCommandFile.write("\n")
                CreateCommandFile.write("--var w_dut \""+global_w_dut_in+"\" ^")
                CreateCommandFile.write("\n")
                CreateCommandFile.write("--var w_grouptype \""+global_w_grouptype_in+"\" ^")
                CreateCommandFile.write("\n")
                #print"*****WTC***** Save PCAP value is :%s" %global_savepcaps_in
                if(global_savepcaps_in=="Yes" or global_savepcaps_in=="YES"):
                    CreateCommandFile.write("--savepcaps ^")
                    CreateCommandFile.write("\n")
                if not var_debug_level_in:
                    CreateCommandFile.write("--debug 5")
                    CreateCommandFile.write("\n")
                else:
                    CreateCommandFile.write("--debug "+var_debug_level_in)
                    CreateCommandFile.write("\n")
                CreateCommandFile.write("::")
                
            if(global_direction_in == "1" and global_test_type_in != "RR" and global_test_type_in != "MaxClient"):
                #print "*****CTC***** Writing to Bi Directional file."
                Logger.messageLog ("Creating BI-DIRECTIONAL Test Command File.")
                CreateCommandFile.write("::"+global_test_name_in)
                CreateCommandFile.write("\n")
                CreateCommandFile.write("tclsh ..\\..\\bin\\vw_auto.tcl -f "+global_test_type_in+".tcl ^")
                CreateCommandFile.write("\n")
                CreateCommandFile.write("--var ssid "+"\""+var_ssid_in+"\" ^")
                CreateCommandFile.write("\n")
                CreateCommandFile.write("--var pw "+"\""+var_pw_in+"\" ^")
                CreateCommandFile.write("\n")
                CreateCommandFile.write("--var save \"C:\\WifiResults\\"+var_ap_in+"\\"+var_apver_in+"\\"+var_ssid_in+"\\"+global_test_type_in+"\\DS\" ^")
                if(global_test_name_in == "MaxClient"):
                    CreateCommandFile.write("--pause 60 ^")
                    CreateCommandFile.write("\n")
                    
                CreateCommandFile.write("\n")
                CreateCommandFile.write("--var ap \""+var_ap_in+ "\" ^")
                CreateCommandFile.write("\n")
                CreateCommandFile.write("--var apver \""+var_apver_in+"\" ^")
                CreateCommandFile.write("\n")
                CreateCommandFile.write("--var channel \""+str(global_channel_in)+"\" ^")
                CreateCommandFile.write("\n")
                CreateCommandFile.write("--var frameSize \""+global_frameSize_in+"\" ^")
                CreateCommandFile.write("\n")
                CreateCommandFile.write("--var loads \""+global_loads_in+"\" ^")
                CreateCommandFile.write("\n")
                CreateCommandFile.write("--var expectConn \""+str(global_expectConn_in)+"\" ^")
                CreateCommandFile.write("\n")       
                CreateCommandFile.write("--var source \""+global_destination_in+"\" ^")
                CreateCommandFile.write("\n")       
                CreateCommandFile.write("--var destination \""+global_source_in+"\" ^")
                CreateCommandFile.write("\n")       
                CreateCommandFile.write("--var duration \""+str(global_duration_in)+"\" ^")
                CreateCommandFile.write("\n")
                CreateCommandFile.write("--var mcs \""+global_mcs_in+"\" ^")
                CreateCommandFile.write("\n")
                CreateCommandFile.write("--var ss \""+str(global_ss_in)+"\" ^")
                CreateCommandFile.write("\n")
                CreateCommandFile.write("--var bw \""+str(global_bw_in)+"\" ^")
                CreateCommandFile.write("\n")
                CreateCommandFile.write("--var gi \""+global_gi_in+"\" ^")
                CreateCommandFile.write("\n")
                CreateCommandFile.write("--var eth_dut \""+global_eth_dut_in+"\" ^")
                CreateCommandFile.write("\n")
                CreateCommandFile.write("--var w_dut \""+global_w_dut_in+"\" ^")
                CreateCommandFile.write("\n")
                CreateCommandFile.write("--var w_grouptype \""+global_w_grouptype_in+"\" ^")
                CreateCommandFile.write("\n")
                if(global_savepcaps_in=="Yes" or global_savepcaps_in=="YES" ):
                    CreateCommandFile.write("--savepcaps ^")
                    CreateCommandFile.write("\n")
                if not var_debug_level_in:
                    CreateCommandFile.write("--debug 5")
                    CreateCommandFile.write("\n")
                else:
                    CreateCommandFile.write("--debug "+var_debug_level_in)
                    CreateCommandFile.write("\n")
                CreateCommandFile.write("::")
                CreateCommandFile.write("\n")
                CreateCommandFile.write("::"+global_test_name_in)
                CreateCommandFile.write("\n")
                CreateCommandFile.write("tclsh ..\\..\\bin\\vw_auto.tcl -f "+global_test_type_in+".tcl ^")
                CreateCommandFile.write("\n")
                CreateCommandFile.write("--var ssid "+"\""+var_ssid_in+"\" ^")
                CreateCommandFile.write("\n")
                CreateCommandFile.write("--var pw "+"\""+var_pw_in+"\" ^")
                CreateCommandFile.write("\n")
                CreateCommandFile.write("--var save \"C:\\WifiResults\\"+var_ap_in+"\\"+var_apver_in+"\\"+var_ssid_in+"\\"+global_test_type_in+"\\US\" ^")
                CreateCommandFile.write("\n")
                if(global_test_name_in == "MaxClient"):
                    CreateCommandFile.write("--pause 60 ^")
                    CreateCommandFile.write("\n")
                
                CreateCommandFile.write("--var ap \""+var_ap_in+ "\" ^")
                CreateCommandFile.write("\n")
                CreateCommandFile.write("--var apver \""+var_apver_in+"\" ^")
                CreateCommandFile.write("\n")
                CreateCommandFile.write("--var channel \""+str(global_channel_in)+"\" ^")
                CreateCommandFile.write("\n")
                CreateCommandFile.write("--var frameSize \""+global_frameSize_in+"\" ^")
                CreateCommandFile.write("\n")
                CreateCommandFile.write("--var loads \""+global_loads_in+"\" ^")
                CreateCommandFile.write("\n")
                CreateCommandFile.write("--var expectConn \""+str(global_expectConn_in)+"\" ^")
                CreateCommandFile.write("\n")       
                CreateCommandFile.write("--var source \""+global_source_in+"\" ^")
                CreateCommandFile.write("\n")       
                CreateCommandFile.write("--var destination \""+global_destination_in+"\" ^")
                CreateCommandFile.write("\n")       
                CreateCommandFile.write("--var duration \""+str(global_duration_in)+"\" ^")
                CreateCommandFile.write("\n")
                CreateCommandFile.write("--var mcs \""+global_mcs_in+"\" ^")
                CreateCommandFile.write("\n")
                CreateCommandFile.write("--var ss \""+str(global_ss_in)+"\" ^")
                CreateCommandFile.write("\n")
                CreateCommandFile.write("--var bw \""+str(global_bw_in)+"\" ^")
                CreateCommandFile.write("\n")
                CreateCommandFile.write("--var gi \""+global_gi_in+"\" ^")
                CreateCommandFile.write("\n")
                CreateCommandFile.write("--var eth_dut \""+global_eth_dut_in+"\" ^")
                CreateCommandFile.write("\n")
                CreateCommandFile.write("--var w_dut \""+global_w_dut_in+"\" ^")
                CreateCommandFile.write("\n")
                CreateCommandFile.write("--var w_grouptype \""+global_w_grouptype_in+"\" ^")
                CreateCommandFile.write("\n")
                if(global_savepcaps_in=="Yes" or global_savepcaps_in=="YES"):
                    CreateCommandFile.write("--savepcaps ^")
                    CreateCommandFile.write("\n")
                if not var_debug_level_in:
                    CreateCommandFile.write("--debug 5")
                    CreateCommandFile.write("\n")
                else:
                    CreateCommandFile.write("--debug "+var_debug_level_in)
                    CreateCommandFile.write("\n")
                CreateCommandFile.write("::")
        except ValueError as e:
            err = "Value Error is %s" % ( str(e) )
            Logger.errorLog ("Raising Value Error while writing of Test Command File.")
            raise MyException(err)

    def SaveTPValue(self):
        #ts = time.time()
        #st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d')
        try:
            #saveTP = open(Directory+"TPValues_"+st+".txt","a")
            Logger.messageLog ("Opening TPValues.txt to write details for TP test case.")
            saveTP = open(Directory+"TPValues.txt","a")
        except IOError as e:
            err = "Input/Output error: %s" % ( str(e) )
            Logger.errorLog ("Raising I/O Error while writing details to TPValues.txt. Please check whether it is present or not.")
            raise MyException(err)
        
        try:
            if(global_direction_in == "1"):
                saveTP.write(global_test_name_in+ " " + "DS "+ global_throughput_multiplier_in)
                saveTP.write("\n")
                saveTP.write(global_test_name_in+ " " + "US "+ global_throughput_multiplier_in)
                saveTP.write("\n")
            else:
                saveTP.write(global_test_name_in+ " " + "DS "+ global_throughput_multiplier_in)
                saveTP.write("\n")
            saveTP.close()
            Logger.messageLog ("Closing TPValues.txt after writing details for TP test case.")
        except ValueError as e:
            errMsg = "Value Error : %s " %(str(e) )
            Logger.errorLog ("Raising Value Error while writing of details to TPValues.txt File.")
            raise MyException(err)