############################################################################################################################
# Description : TestParameterValidation contains a library that will validate the Parameters set by user in Robot Framework.
# Developer   : Govinda Revanwar
# Date        : -
# Modified By : Kiran Mandal
############################################################################################################################
"""
*TestParameterValidation*  contains a library that will validate the Parameters set in Robot Framework.
"""
import sys
import os
from Logger import logMessage 
class testParameterValidation:

    def parameterValidation(self,global_test_name_in, global_test_type_in, global_load_mode_in, global_direction_in, global_band_selection_in, global_channel_in, global_frameSize_in, global_loads_in, global_expectConn_in, global_source_in, global_destination_in, global_duration_in, global_mcs_in, global_ss_in, global_bw_in, global_gi_in, global_eth_dut_in, global_w_dut_in, global_w_grouptype_in, global_savepcaps_in, global_throughput_multiplier_in, Directory):
        """
            Function Name        : parameterValidation
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
                global_throughput_multiplier_in -   Throughput Multiplier (0.9),Used only for TP Test cases.
                Directory                       -   Directory where the .bat file is present.
            Outputs  : 
                Validates the Global Parameters.
                
        """ 
        expectedChannel = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","36","40","44","48","52","56","60","64","100","104","108","112","166","120","124","128","132","136","140","149","153","157" ,"161","165"]
        expectFrameSize = ["1518","1024","512","64"]
        expectedMCS = ["31","30","29","28","27","26","25","24","23","22","21","20","19","18","17","16","15","14","13","12","11","10","9","8","7","6","5","4","3","2","1","N"]
        IsParamValid = True
        # validates global_test_type_in
        #print("Started validation of %s Test Case" %global_test_name_in)
        logMessage("Started validation of %s Test Case" %global_test_name_in)
        try:
            if (global_test_type_in.upper() == "TP" or global_test_type_in.upper() == "RR" or global_test_type_in.upper() == "LAT" or global_test_type_in.upper() == "MAXCLIENT"):
                print "Test Type  Parameter value is Valid"
                
            else:
                raise ValueError
        except ValueError:
            print "!!!!!TPV!!!!!Test Type  Parameter value is not Valid %s" %global_test_type_in
            IsParamValid = False
            
        
        # validates global_load_mode_in
        
        try:
            if (global_load_mode_in.upper() == "AUTO" or global_load_mode_in.upper() == "MANUAL"):
                print "Load Mode Parameter value is Valid"
                
            else:
                raise ValueError
        except ValueError:
            print "!!!!TPV!!!!!!Load Mode Parameter value is not Valid %s" %global_load_mode_in
            IsParamValid = False
            
            
        # validates global_direction_in 
        try:
            if (global_direction_in == "1" or global_direction_in == "0"):
                print "Direction Parameter value is Valid"
                
            else:
                raise ValueError
        except ValueError:
            print "!!!!!TPV!!!!!Direction Parameter value is not Valid %s" %global_direction_in
            IsParamValid = False
            
        
        # validates global_band_selection_in    
        try:
            if (global_band_selection_in == "5" or global_band_selection_in == "2.4"):
                print "Band Selection Parameter value is Valid"
                
            else:
                raise ValueError
        except ValueError:
            print "!!!!!TPV!!!!!Band Selection Parameter value is not Valid %s" %global_band_selection_in
            IsParamValid = False
            
            
        # validates global_channel_in
        
        
        try:
            if  (global_channel_in  in expectedChannel):
                print "Channel Parameter value is Valid"
                
            else:
                raise ValueError
        except ValueError:
            print "!!!!!TPV!!!!! Channel Parameter value is not Valid %s" %global_channel_in
            IsParamValid = False
            
        
                
        # validates global_frameSize_in
       
        global_frameSize_in=str(global_frameSize_in)
        frames=global_frameSize_in.split(" ")
    
        for frameSize in frames:
            result = -1
            try:
                result = expectFrameSize.index(frameSize)
                if(result>=0):
                    print "FrameSize Parameter value is Valid"
                    
                else:
                    raise ValueError
            except ValueError:
                IsParamValid = False
                print "!!!!!TPV!!!!! In FrameSize input %s parameter is not valid" %frameSize
                
  
        # validates global_expectConn_in
        try:
            if (global_test_type_in.upper() == "MAXCLIENT" and len(global_expectConn_in) > 0 and str(global_expectConn_in) == "102"):
                    print "Expected Connection Parameter value is Valid"
            elif (global_test_type_in.upper() == "TP" or global_test_type_in.upper() == "RR" or global_test_type_in.upper() == "LAT"):
                    pass
            else :
                raise ValueError
        except ValueError:  
            IsParamValid = False
            print "!!!!!TPV!!!!! Expected Connection`Parameter value is not Valid %s" %global_expectConn_in
            
        
        # validates global_load_mode_in
        # print "*****TPV***** Value of loads in is %s " %global_loads_in
        if global_load_mode_in.upper() == "MANUAL":
            try:
                if not global_loads_in:
                    print "!!!!!TPV!!!!! Load mode is specified as Manual but loads parameter is not specified by user"
                    IsParamValid = False
                    raise ValueError
                else:
                    print "value is entered"
                    
            except ValueError:
                print "value is not entered"
                
                
        
        if global_load_mode_in.upper() == "AUTO":
            
            try:
                if global_test_type_in =="LAT" or global_test_type_in =="RR":
                    print "*****TPV***** "+global_test_name_in
                    if(global_test_name_in.find("Lat")>0):
						temp_testname = global_test_name_in.replace("Lat", "TP")
                    if(global_test_name_in.find("lat")>0):
						temp_testname = global_test_name_in.replace("lat", "TP")
                    if(global_test_name_in.find("LAT")>0):
						temp_testname = global_test_name_in.replace("LAT", "TP")
                    if(global_test_name_in.find("RR")>0):
						temp_testname = global_test_name_in.replace("RR", "TP")
                    if(global_test_name_in.find("rr")>0):
						temp_testname = global_test_name_in.replace("rr", "TP")
					 
                    
                    
                    #print Directory
                    FileName = Directory + temp_testname+ ".bat"
                    print "****TPV***** Check for %s.bat command file created and executed previously" %temp_testname
                    if os.path.isfile(FileName):
                        with open(FileName) as openfileobject:
                                data=openfileobject.read().replace('\n', '')
                                #print data
                                ss_str = "--var ss \""+global_ss_in+"\""
                                print "*****TPV***** Check SS value %s present in TP file or not" %ss_str
                                if(data.find(ss_str)>0):
                                    print "*****TPV***** SS value present in TP file"
                                    
                                else:
                                    print "!!!!!TPV!!!!! SS value not present in TP file"
                                    IsParamValid = False
                                bw_str = "--var bw \""+global_bw_in+"\""
                                
                                print "*****TPV***** Check Bandwidth value %s present in TP file or not" %bw_str
                                if(data.find(bw_str)>0):
                                    print "*****TPV***** Bandwidth value present in TP file"
                                    
                                else:
                                    print "!!!!!TPV!!!!! Bandwidth value not present in TP file"
                                    IsParamValid = False
                                    
                                for index in range(len(frames)):
                                    #print index
                                    textToFind = str(frames[index])
                                    #print "*****TPV***** Checking frameSize %s present in TP file" %textToFind
                                    #print data.find(textToFind)
                                    if (data.find(textToFind)>0):
                                        
                                        print "Expected FrameSize %s is present in TP command File" %textToFind
                                        
                                    else:
                                        print "!!!!!TPV!!!!! Expected FrameSize %s is not present in TP command File" %textToFind                   
                                        IsParamValid = False
                    else:
                        print "File Expected %s.bat is not present under Folder path" % temp_testname
                        IsParamValid = False    
                else:
                    raise ValueError
            except ValueError:
                #print "global_test_type_in in not 'LAT' or 'RR'"
				pass
                #sys.exit(1)
        # validates global_source_in        
        try:
        
            if (global_source_in.upper() == "W_AC" or global_source_in.upper() == "W_N" or global_source_in.upper() == "W_G" or global_source_in.upper() == "ETH"):
                print "Source Parameter value is Valid"
                
            else:
                raise ValueError
        except ValueError:
            print "!!!!!TPV!!!!! Source Parameter value is not Valid %s" %global_source_in
            IsParamValid = False
            
        
        # validates global_destination_in       
        try:
        
            if (global_destination_in.upper() == "W_AC" or global_destination_in.upper() == "W_N" or global_destination_in.upper() == "W_G" or global_destination_in.upper() == "ETH"):
                print "Destination Parameter value is Valid"
                
            else:
                raise ValueError
        except ValueError:
            print "!!!!!TPV!!!!! Destination`Parameter value is not Valid %s" %global_destination_in
            IsParamValid = False
            
        
        # validates global_mcs_in
        
        global_mcs_in=str(global_mcs_in)
        Mcs = global_mcs_in.split(" ")
        
        for Mcs_Arg in Mcs:
            result = -1
            try:
                result = expectedMCS.index(Mcs_Arg)
                if(result>=0):
                    print "Channel Parameter value is Valid"
                else: 
                    raise ValueError
            except ValueError:
                print "!!!!!TPV!!!!!  MCS input %s parameter is not valid" %Mcs
                IsParamValid = False
                
        # validates global_ss_in    
        try:
            if (global_ss_in == "1" or global_ss_in == "2"  or global_ss_in == "3" or global_ss_in == "4"):
                print "SS Parameter value is Valid"
                
            else:
                raise ValueError
        except ValueError:
            print "!!!!!TPV!!!!! SS`Parameter value is not Valid %s" %global_ss_in
            IsParamValid = False
            
            
        # validates global_bw_in    
        try:
            if (global_bw_in == "20" or global_bw_in == "40" or global_bw_in == "80"):
                print "Channel Bandwidth Parameter value is Valid"
                
            else:
                raise ValueError
        except ValueError:
            print "!!!!TPV!!!!!! Channel Bandwidth`Parameter value is not Valid %s" %global_bw_in
            IsParamValid = False
            
            
        # validates global_gi_in
        try:
            if (global_gi_in.upper() == "SHORT" or global_gi_in.upper() =="LONG"):
                print "Guard Interval Parameter value is Valid"
                
            else:
                raise ValueError
        except ValueError:
            print "!!!!!TPV!!!!! Guard Interval`Parameter value is not Valid %s" %global_gi_in
            IsParamValid = False
            
            
        # validates global_gi_in
        try:
            if (global_savepcaps_in.upper() == "YES" or global_savepcaps_in.upper() == "NO"):
                print "pcap Parameter value is Valid"
                
            else:
                raise ValueError
        except ValueError:
            print "!!!!!TPV!!!!! Save Pcap Parameter value is not valid %s" %global_savepcaps_in
            IsParamValid = False
            
        
        return IsParamValid

    def parameterDependencyValidation(self,global_test_type_in, global_source_in, global_destination_in, global_band_selection_in, global_channel_in, global_bw_in, global_mcs_in):
        """
            Function Name        : parameterDependencyValidation
            Function Description : Validates the Dependency test parameters entered by the user.
            Inputs   : 
                global_test_type_in             -  Type of tests "TP,RR,LAT,MaxClient"         
                global_source_in                -   W_G,W_N,W_AC                   
                global_destination_in           -    W_G,W_N,W_AC
                global_band_selection_in        -    2.4G or 5G
                global_channel_in               -    channels entered by the user.
                global_bw_in                    -    20, 40, 80
                global_mcs_in                   -    Mcs value entered by the users.
            Outputs  : 
                Validates the Dependency Parameters.
                
        """
		
		
        global_mcs_in = str(global_mcs_in)
        IsParamValid = True
        mcs = global_mcs_in.split(" ")
        global_channel_in = str(global_channel_in)
        channel = global_channel_in.split(" ")
        
        expectedMCS_24Gz_WG_WG= ["16","13","11","9","7","5","3","1"]
        expectedMCS_24Gz_WN_WN = ["31","30","29","28","27","26","25","24","23","22","21","20","19","18","17","16","15","14","13","12","11","10","9","8","7","6","5","4","3","2","1"]
        expectedMCS_5Gz_WN_WN = ["31","30","29","28","27","26","25","24","23","22","21","20","19","18","17","16","15","14","13","12","11","10","9","8","7","6","5","4","3","2","1"]
        expectedMCS_5Gz_WAC_WAC = ["9","8","7","6","5","4","3","2","1"]
        
        expectedChannel_24Gz = ["1","2","3","4","5","6","7","8","9","10","11"]
        expectedChannel_5Gz = ["36","40","44","48","52","56","60","64","100","104","108","112","116","120","124","128","132","136","140","144","149","153","157","161","165"]
        
        # validates global_band_selection_in
        if global_band_selection_in == "2.4":
            
            if global_source_in.upper() =="W_G" or global_destination_in.upper() == "W_G":
                print "*****PDV***** Validating Dependency Band Selection is 2.4 and Source/Destination = W_G"
                
                global_mcs_in=str(global_mcs_in)
                mcs = global_mcs_in.split(" ")
               
                for eachMCS in mcs:
                    result = -1
                    try:
                        result = expectedMCS_24Gz_WG_WG.index(eachMCS)
                        if(result >= 0):
                            print ("*****PDV***** MCS  in desired range ")
                            
                        else:
                            raise ValueError
                    except ValueError:
                        print "!!!!!PDV!!!!! MCS Not in desired range " + eachMCS
                        IsParamValid = False
                
                #print channel
                
                for eachChannel in channel:
                    result = -1
                    try:
                        result = expectedChannel_24Gz.index(eachChannel)
                        if(result >= 0):
                            print ("*****PDV***** channel is in desired range ")
                            #
                        else:
                            raise ValueError
                    except ValueError:
                        print "!!!!!PDV!!!!! Channel not in desired range "+ eachChannel
                        IsParamValid = False                
                
                if global_bw_in == "20":
                    print "Bandwidth is in desired range "
                  #  
                else:
                    print "!!!!!PDV!!!!! Bandwidth not in desired range "+ global_bw_in
                    IsParamValid = False
                    
                    
            elif global_source_in.upper() =="W_N" or global_destination_in.upper() == "W_N":
                print "*****PDV***** Validating Dependency Band Selection is 2.4 and Source/Destination = W_N"
                   
                global_mcs_in=str(global_mcs_in)
                mcs = global_mcs_in.split(" ")
                
                for eachMCS in mcs:
                    result = -1
                    try:
                        result = expectedMCS_24Gz_WN_WN.index(eachMCS)
                        result = str(result)
                        if(result >= 0):
                            print ("*****PDV***** MCS  in desired range ")
                            
                        else:
                            raise ValueError
                    except ValueError:
                        print "!!!!!PDV!!!!! MCS "+eachMCS+" Not in desired range "
                        IsParamValid = False
                        
                #print channel
        
                for eachChannel in channel:
                    result = -1
                    try:
                        result = expectedChannel_24Gz.index(eachChannel)
                        if(result >= 0):
                            print ("*****PDV***** channel is in desired range ")
                            
                        else:
                            raise ValueError
                    except ValueError:
                        print "!!!!!PDV!!!!! Channel not in desired range "+ eachChannel
                        IsParamValid = False
                
                #print "*****PDV***** input Bandwidth value is : " + global_bw_in
                if global_bw_in == "20" or global_bw_in == "40":
                    pass
                else:
                    print "!!!!!PDV!!!!! Bandwidth not in desired range "+ global_bw_in
                    IsParamValid = False
                    

        elif global_band_selection_in == "5":
            global_source_in = global_source_in.upper()
            global_destination_in=global_destination_in.upper()
            if global_source_in.upper() =="W_N" or global_destination_in.upper() == "W_N":
                print "*****PDV***** Validating Dependency Band Selection is 5 and Source/Destination = W_N"
                
                global_mcs_in=str(global_mcs_in)
                mcs = global_mcs_in.split(" ")
                
                for eachMCS in mcs:
                    result = -1
                    try:
                        result = expectedMCS_5Gz_WN_WN.index(eachMCS)
                        result = str(result)
                        if(result >= 0):
                            print ("*****PDV***** MCS  in desired range ")
                            
                        else:
                            raise ValueError
                    except ValueError:
                        print "!!!!!PDV!!!!! MCS "+eachMCS+" Not in desired range "
                        IsParamValid = False

                
                for eachChannel in channel:
                    result = -1
                    try:
                        result = expectedChannel_5Gz.index(eachChannel)
                        if(result >= 0):
                            print ("*****PDV***** channel is in desired range ")
                            
                        else:
                            raise ValueError
                    except ValueError:
                        print "!!!!!PDV!!!!! Channel not in desired range "+ eachChannel
                        IsParamValid = False
                    
                    
                if global_bw_in == "20" or global_bw_in == "40":
                    print "Bandwidth is in desired range "
                    
                else:
                    print "!!!!!PDV!!!!! Bandwidth not in desired range "+ global_bw_in
                    IsParamValid = False
                    
                    
            elif global_source_in.upper() =="W_AC" or global_destination_in.upper() == "W_AC":
                print "*****PDV***** Validating Dependency Band Selection is 5 and Source/Destination = W_AC"
                
                global_mcs_in=str(global_mcs_in)
                mcs = global_mcs_in.split(" ")
                for eachMCS in mcs:
                    result = -1
                    try:
                        result = expectedMCS_5Gz_WAC_WAC.index(eachMCS)
                        if(result >= 0):
                            print ("*****PDV***** MCS  in desired range ")
                        else:
                            raise ValueError
                    except ValueError:
                        print "!!!!!PDV!!!!! MCS Not in desired range " + eachMCS
                        IsParamValid = False
                
                #print  channel
                  
                for eachChannel in channel:
                    result = -1
                    try:
                        result = expectedChannel_5Gz.index(eachChannel)
                        if(result >= 0):
                            print ("*****PDV***** channel is in desired range ")
                            
                        else:
                            raise ValueError
                    except ValueError:
                        print "!!!!!PDV!!!!! Channel not in desired range "+ eachChannel
                        IsParamValid = False
                
                #print "*****PDV***** input Bandwidth value is : " + global_bw_in
                if global_bw_in == "20" or global_bw_in == "40" or global_bw_in == "80":
                    print "Bandwidth is in desired range "
                    
                else:
                    print "!!!!!PDV!!!!! Bandwidth not in desired range "+ global_bw_in
                    IsParamValid = False
                    
        else:
            print "Please choose Either 2.4Gz or 5Gz band"
            sys.exit(0)
        return IsParamValid
