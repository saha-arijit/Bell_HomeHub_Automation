#########################################################################################################################################
# Description : TestCommandExeuction contains a library that will execute a test command (.bat) generated from generateTestCaseLibrary.
# Developer   : Govinda Revanwar
# Date        : -
# Modified By : Kiran Mandal
#########################################################################################################################################
"""
*TestCommandExeuction*  contains a library that will execute a test command (.bat) generated from generateTestCaseLibrary.
"""
from robot.libraries.BuiltIn import BuiltIn
import os
import glob
import warnings
from BatParseLibrary import parseBatFile 
from SecureCopyLibrary import executeCommandFile 
from fetchloads import getpps
from datetime import datetime, date
import datetime
from dateutil.parser import parse
import time
import re
#from datetime import *


global_execMode_in = "Auto"
ConfigFilePath = "userconfig.txt"
g_testcase_starttime = 0
g_testcase_stoptime = 0
TestCmdDestPath = "C:/Program Files (x86)/IxVeriWave/WaveAutomate/automation_6.11-118_2017.06.30.08-admin_windows/automation/conf/HH3000/"

TestRunnerFile = "../tools/runner.bat"
TestResultLogFile = "../Bell_Homehub_Automation_Files/output.txt"
def SetExecutionMode(var_execMode_in):
    """
        Function Name        : SetExecutionMode
        Function Description : This function will set the execution mode to Auto or manual.
        Inputs   : 
            var_execMode_in   - Auto or Manual
        Outputs  : 
            Sets the Execution mode
                
    """ 
    global global_execMode_in
    global_execMode_in = var_execMode_in

def SetUserConfig():
    """
        Function Name        : SetUserConfig
        Function Description : This function will read the configuration parameter from userconfig.txt file and use in exeuction .
        Inputs   : 
            
        Outputs  : 
            Configures the parameter from userconfig.txt
                
    """ 
    #This function will read the configuration parameter from user Config File
    global var_wahostname, var_wausername, var_wapassword, var_wasshkey, var_waport, var_dbhostname, var_dbpassword, var_dbusername, srvr_details
    try:
        configFile = open(ConfigFilePath, 'r')
        content = configFile.read()
        lines = content.split("\n")
    except IOError as e:
        err = "Input/Output error: %s" % ( str(e) )
        raise Exception(err)
    #print len(lines)
    for eachline in lines:
        #print eachline
        str1 = eachline
        #print str.find("var_ssid_in}")
        try:
            if (str1.find("var_wahostname}")>0):
                start = str1.index("}")
                end = str1.index("#")
                substr = str1[start+1:end]
                substr = substr.replace(" ","")
                substr.strip()
                var_wahostname = substr
            elif (str1.find("var_wausername}")>0):
                start = str1.index("}")
                end = str1.index("#")
                substr = str1[start+1:end]
                substr = substr.replace(" ","")
                substr.strip()
                var_wausername =  substr
            elif (str1.find("var_wapassword}")>0):
                start = str1.index("}")
                end = str1.index("#")
                substr = str1[start+1:end]
                substr = substr.replace(" ","")
                substr.strip()
                var_wapassword = substr
            elif (str1.find("var_waportnumber}")>0):
                
                start = str1.index("}")
                end = str1.index("#")
                substr = str1[start+1:end]
                substr = substr.replace(" ","")
                substr.strip()
                var_waport = substr
            elif (str1.find("var_dbusername}")>0):
                start = str1.index("}")
                end = str1.index("#")
                substr = str1[start+1:end]
                substr = substr.replace(" ","")
                substr.strip()
                var_dbusername = substr
            elif (str1.find("var_dbpassword}")>0):
                start = str1.index("}")
                end = str1.index("#")
                substr = str1[start+1:end]
                substr = substr.replace(" ","")
                substr.strip()
                var_dbpassword = substr
            elif (str1.find("var_dbhostname}")>0):
                start = str1.index("}")
                end = str1.index("#")
                substr = str1[start+1:end]
                substr = substr.replace(" ","")
                substr.strip()
                var_dbhostname = substr
        except ValueError as e:
            err = "Value Error is %s" % ( str(e) )
            raise Exception(err)
    #print ("*****TCE_SUC*****Password is: %s") %var_wapassword
    srvr_details = []
    srvr_details.append(var_wahostname)  #hostName - 0 
    srvr_details.append(var_waport) #port - 1
    srvr_details.append(var_wausername)  #userName - 2
    srvr_details.append(var_wapassword)  #paswd - 3
    srvr_details.append(var_dbhostname)  #dbHost - 4
    srvr_details.append(var_dbusername)  #dbUser - 5
    srvr_details.append(var_dbpassword)  #dbPwd - 6
    print (var_dbhostname + "   "+ var_dbpassword +"    " + var_dbusername)
    
def ExecuteTestCommand():
    """
        Function Name        : ExecuteTestCommand
        Function Description : This function will execute the test commands.
        Inputs   : 
            
        Outputs  : 
            Executes the test commands.
            
    """ 
    ROBOT_CONTINUE_ON_FAILURE = True
    global var_wahostname, var_wausername, var_wapassword, var_wasshkey, var_waport, var_testType, var_mcs, list_mcs, var_direction, Directory
    var_direction = 0
    #Get calling Test case name from RIDE
    test_name = BuiltIn().get_variable_value("${TEST_NAME}")
    #test_name = FileName
    testCommandFileName = test_name+".bat"
    print (testCommandFileName)
    
    
    if(global_execMode_in == "Manual"):
        Directory = "../Bell_Homehub_Automation_TestCommand/TC_Manual"
        print( "******ETC***** Execution mode set to Manual and Test Command Directory is : ") + Directory
    
    elif(global_execMode_in == "Auto"):
        #Get latest modified directory
        
        Directory = sorted(glob.glob(os.path.join("../Bell_Homehub_Automation_TestCommand/", '*/')), key=os.path.getmtime)[-1]
        
        print ("*****ETC***** Last Modified Directory is: ")+ Directory
        
        if(Directory.find("TC_Manual")>0):
            Directory = sorted(glob.glob(os.path.join("../Bell_Homehub_Automation_TestCommand/", '*/')), key=os.path.getmtime)[-2]
            print ("*****ETC***** Last Modified Folder is TestCommand so picking second last created Directory : ")+ Directory
    else:
        raise AssertionError("!!!!!ETC!!!!! Execution mode is not  set to Manual or Auto so aborting Execution")
        
    isCommandFilePresent = False        
    isCommandFileExecuted = False
    FileName = Directory + testCommandFileName
    if os.path.isfile(FileName):
        isCommandFilePresent = True
        print ("*****ETC***** Test Command file present in path")       
        
    else:
        print ("!!!!!ETC!!!!! Test Command file is not present in path so aborting Execution")
        raise AssertionError("!!!!!ETC!!!!! Test Command file is not present in path so aborting Execution")
    
    
    
    if isCommandFilePresent == True :
        tempCommandFile = open(FileName, 'r')
        tempCommandFilecontent = tempCommandFile.read()
        lines = tempCommandFilecontent.split("\n")
        tempCommandFile.close()
        #print len(lines)
        for eachline in lines:
            #print eachline
            str1 = eachline
            try:
                if (str1.find("TP.tcl")>0):
                    var_testType = "TP"
                elif (str1.find("LAT.tcl")>0):
                    var_testType = "LAT"
                elif (str1.find("RR.tcl")>0):
                    var_testType = "RR"
                elif (str1.find("MaxClient.tcl")>0):
                    var_testType = "MaxClient"
                
                elif (str1.find("var mcs ")>0):
                    #print "MCS present in file"
                    start = str1.index("\"")
                    end = str1.index("\" ^")
                    substr = str1[start+1:end]
                    substr.strip()
                    var_mcs = substr
                    list_mcs = var_mcs.split(" ")
                    #print ("MCS is : " + var_mcs)
                    
                elif (str1.find("var frameSize ")>0):
                    #print "frameSize present in file"
                    start = str1.index("\"")
                    end = str1.index("\" ^")
                    substr = str1[start+1:end]
                    substr.strip()
                    var_frameSize = substr
                    list_frameSize = var_frameSize.split(" ")
                    #print ("FrameSize is : " + var_frameSize)
                    
                elif (str1.find("var save ")>0):
                    #print str1
                    start = str1.index("\"")
                    end = str1.index("\" ^")
                    substr = str1[start+1:end]
                    substr.strip()
                    var_Result_Dir = substr
                    if(str1.find("US")>0):
                        var_direction = 1
                        print ("*****ETC***** var_direction: %d")  %var_direction
                    
            except ValueError as e:
                err = "Value Error is %s" % ( str(e) )
                raise Exception(err)
        
        #print("*****ETC***** MCS Value : ")+ var_mcs
        print ("****ETC***** Test Type : ") +var_testType
        list_mcs = var_mcs.split(" ")
        #print list_mcs
        #GetUserConfig()
        #print "WaPort :" + var_waport
        if(var_testType =="TP" or var_testType == "MaxClient"):
            print(var_wahostname, var_wausername, var_wapassword, FileName, TestCmdDestPath, testCommandFileName, var_waport)
            isCommandFileExecuted = executeCommandFile(var_wahostname, var_wausername, var_wapassword, FileName, TestCmdDestPath, testCommandFileName, var_waport)
            #print ("TestType is : " + var_testType)
            #isCommandFileExecuted = True
        elif(var_testType =="RR" or var_testType == "LAT"):
            ## IF Test name contains RR then replace it with TP
            if(test_name.find("RR")>0):
                temp_testName = test_name.replace("RR", "TP")
            ## IF Test name contains LAT then replace it with TP
            elif(test_name.find("LAT")>0):
                temp_testName = test_name.replace("LAT", "TP")
            
            print ("Test Name to Found is %s" %temp_testName)
            TPValuesFile = Directory+"TPValues.txt"
            ## Check the TPValues.txt file is present or not. For obtaining previous execution test ID
            if os.path.isfile(TPValuesFile):
                try:
                    print ("TP Values File Present")
                    #readTP = open(Directory+"TPValues_"+st+".txt","r")
                    readTP = open(Directory+"TPValues.txt","r")
                    content = readTP.read()
                    lines = content.split("\n")
                    readTP.close(); 
                except IOError as e:
                    err = "Input/Output error: %s" % (str(e))
                    raise Exception(err)  
                #print ("\""+test_name+"\"")
                isPrevExecDataFound = False
                for eachline in lines:
                    #print (eachline)
                    try : 
                        list = eachline.split(" ")
                        #print ("Lenght of Lane is %d" %len(list))
                        #print (list)
                        ## If the Test name and DB Test_id is found then execute following block
                        if(len(list)==4):
                            #print ("Content of List " + str(list[0]))
                            print ("Test Name = " + list[0])
                            if(list[0] == temp_testName):
                                print ("TP Test Case found in Pase Execution")
                                #*********************************
                                #test_name_file = list[0]  # Fetching the corresponding TP test name from the "TPValues.txt" file 
                                #*********************************
                                #print test_name
                                #print test_nam
                                Direction = list[1]
                                #print (Direction)
                                TPValue = list[2]
                                #print (TPValue)
                                TestID = list[3]
                                print (TestID)
                                print("Before calling getpps")
                                print(TestID, list_mcs, list_frameSize)
                                #Calling Method to fetch the loads in RR or LAT
                                loads_value = getpps(TestID, list_mcs, list_frameSize)
                                print(loads_value[0])
                                openFile = open(FileName,"r")
                                fileContent = openFile.read()
                                replacedText = fileContent.replace("loads \"\"", "loads \""+str(loads_value[0])+"\"", 1)
                                openFile.close()
                                openFile = open(FileName,"w")
                                openFile.write(replacedText)
                                openFile.close()
                                isPrevExecDataFound = True
                       
                    except ValueError as e:
                        err = "Value Error is %s" % ( str(e) )
                        raise Exception(err)
                #print ("Throughout Value is %s and TestID is %s" %TPValue %TestID)
                if(isPrevExecDataFound == True):
                    print("Previous Execution of TP Test case found")
                    #print(var_wahostname, var_wausername, var_wapassword, FileName, TestCmdDestPath, testCommandFileName, var_waport)
                    isCommandFileExecuted = executeCommandFile(var_wahostname, var_wausername, var_wapassword, FileName, TestCmdDestPath, testCommandFileName, var_waport)
                    #isCommandFileExecuted = True
                else :
                    #print("!!!!!TCE!!!!! Previous execution of TP Test case not found in TP Values file")
                    isCommandFileExecuted = False
                    raise AssertionError("!!!!!TCE!!!!! Previous execution of TP Test case not found in TP Values file")

            else :
                isCommandFileExecuted = False
                #print("!!!!!TCE!!!!! TPValues.txt File is not present on command File path")
                raise AssertionError("!!!!!TCE!!!!! TPValues.txt File is not present on command File path")
        
        if(isCommandFileExecuted == True):
            print ("Command File is Executed")
            if(os.path.isfile(TestResultLogFile)):
                #print ("TestResult Log File is present in path")
                outputDS = "../Bell_Homehub_Automation_Files/output_DS.txt"
                outputUS = "../Bell_Homehub_Automation_Files/output_US.txt"
                try:
                    print ("direction is : %d" %var_direction)
                    
                    # *****************************  FOR BI - DIRECTIONAL **********************************
                    if(var_direction == 1):
                        print "Command Executeds, OutputFile PResent and Direction = 1"
                        with open(TestResultLogFile) as f:
                            DS, output, US = f.read().partition("/output.log\n")
                            #print (output)
                            with open(outputDS, "w") as f:
                                f.write(DS)
                                with open(outputUS, "w") as f:
                                    f.write(US)
                        ## Post Procesing For DS
                        print ("Check Execution status for DS")
                        TestRestultStatus = verifyTestExectionStatus(outputDS)
                        print ("Test Exeuction status is %r"  %TestRestultStatus)
                        if (TestRestultStatus == True):
                            elapsed_Time = getTestExecutionTime(outputDS)
                            print("before calling GetThroughputValue function")
                                 #****************************************
                            if (var_testType == "TP"):
                                ThroughputValue = GetThroughputValue(test_name)
                            else:
                                ThroughputValue = 0
                            #****************************************
                            print ("Throughput Value is : %s"  %ThroughputValue)
                            #saveExecutionStatusToFile(test_name, "DS", g_testcase_starttime, ThroughputValue, FileName, elapsed_Time)
                            print test_name + "\t" + "DS" + "\t" + str(g_testcase_starttime)+ "\t" + str(ThroughputValue) + "\t " + FileName + "\t" + str(elapsed_Time)
                            result_test_Id = parseBatFile(srvr_details, test_name, "DS", g_testcase_starttime, ThroughputValue, FileName, elapsed_Time)
                            if(var_testType == "TP"):
                                TPValuesFile = Directory+"TPValues.txt"
                                pattern = test_name + " DS " + ThroughputValue
                                subst = pattern +" " + str(result_test_Id) 
                                replaceStringInFile(TPValuesFile, pattern, subst)
                        else:
                            TestResultDir = var_Result_Dir + "\\" + getExecutionStartTime(outputDS)                            
                            raise AssertionError("!!!!!TCE!!!!! Test Case Excution status Failed. For More details check logs on WaveServer " + TestResultDir )
                            #return False
                        try :
                            os.remove(outputDS)
                        except :
                            print("Execution Log File Not Present ")
                        
                        ## Post Procesing for US 
                        print ("Check Execution status for US")
                        TestRestultStatus = verifyTestExectionStatus(outputUS)
                        print ("Test Exeuction status is %r"  %TestRestultStatus)
                        if (TestRestultStatus ==True):
                            elapsed_Time = getTestExecutionTime(outputUS)
                                 #****************************************
                            if (var_testType == "TP"):
                                ThroughputValue = GetThroughputValue(test_name)
                            else:
                                ThroughputValue = 0
                            #****************************************
                            
                            #saveExecutionStatusToFile(test_name, "US", g_testcase_starttime, ThroughputValue, FileName, elapsed_Time)
                            print "test_name" + "\t" + "US" + "\t" + str(g_testcase_starttime)+ "\t" + str(ThroughputValue) + "\t " + FileName + "\t" + str(elapsed_Time)
                            result_test_Id = parseBatFile(srvr_details, test_name, "US", g_testcase_starttime, ThroughputValue, FileName, elapsed_Time)
                            if(var_testType == "TP"):
                                TPValuesFile = Directory+"TPValues.txt"
                                pattern = test_name + " US " + ThroughputValue
                                subst = pattern +" " + str(result_test_Id) 
                                replaceStringInFile(TPValuesFile, pattern, subst)
                            
                        else:
                            TestResultDir = var_Result_Dir + "\\" + getExecutionStartTime(outputUS)                            
                            raise AssertionError("!!!!!TCE!!!!! Test Case Excution status Failed. For More details check logs on WaveServer " + TestResultDir )
                            return False
                        try :
                            os.remove(outputUS)
                            os.remove(TestResultLogFile)
                        except :
                            print("Execution Log File Not Present ")

                    # *********************     FOR UNI - DIRECTIONAL *************************8
                    else :
                        print "Command Executeds, OutputFile Present and Direction = 0."
                        TestRestultStatus = verifyTestExectionStatus(TestResultLogFile)
                        print ("Test Exeuction status is %r"  %TestRestultStatus)
                        if (TestRestultStatus ==True):
                            elapsed_Time = getTestExecutionTime(TestResultLogFile)
                            
                            #****************************************
                            if (var_testType == "TP"):
                                ThroughputValue = GetThroughputValue(test_name)
                            else:
                                ThroughputValue = 0
                            #****************************************

                            #saveExecutionStatusToFile(test_name, "DS", g_testcase_starttime, ThroughputValue, FileName, elapsed_Time)
                            print test_name + "\t" + "DS" + "\t" + str(g_testcase_starttime)+ "\t" + str(ThroughputValue) + "\t " + FileName + "\t" + str(elapsed_Time)
                            
                            result_test_Id = parseBatFile(srvr_details, test_name, "DS", g_testcase_starttime, ThroughputValue, FileName, elapsed_Time)
                            if(var_testType == "TP"):
                                TPValuesFile = Directory+"TPValues.txt"
                                pattern = test_name + " DS " + ThroughputValue
                                subst = pattern +" " + str(result_test_Id) 
                                replaceStringInFile(TPValuesFile, pattern, subst)
                            print "Completed Bat Parse"
                        else:
                            TestResultDir = var_Result_Dir + "\\" + str(getExecutionStartTime(TestResultLogFile))
                            raise AssertionError("....!!!!!TCE!!!!! Test Case Excution status Failed. For More details check logs on WaveServer " + TestResultDir )
                            return False
                    try :
                        os.remove(TestResultLogFile)
                        pass
                    except :
                        print("Execution Log File Not Present ")
                except IOError as e:
                    err = "Input/Output error: %s" % ( str(e) )
                    raise Exception(err)
            else :
                print ("Test Result Log File is not present on exepcted location")
        else :
            raise AssertionError("!!!!!TCE!!!!! Exeuction Of Command File Failed please check logs for more details")
    #tracker.print_diff()           
'''def verifyTestResourceAvailability(fileContent):
    if(fileContent.find("Reserving ports for the test")>0):
        if(fileContent.find("Schema Validation success on port")):
            if(fileContent.find("Completed: Ethernet link is up")):
                return True
            else:
                print "!!!!!TCE_VTRA!!!!! Ethernet Link is not Up"
                return False
        else:
            print "!!!!!TCE_VTRA!!!!! Schema Validation Text not found"
            return False
    else:
        print "!!!!!TCE_VTRA!!!!! Reserving Port for the Test Text not found"
        return False'''

def verifyTestExectionStatus(respFileContent):
    """
        Function Name        : verifyTestExectionStatus
        Function Description : This function will verify the execution status of test command.
        Inputs   : 
            respFileContent  - Command file (.bat)
        Outputs  : 
             verifies the Execution the test commands.
            
    """ 
    ReadFile = open(respFileContent,'r')
    ReadContentOfFile = ReadFile.read()
    ReadFile.close
    isTestPass = True
    try:
        if(var_testType == "TP"):
            if(len(list_mcs) > 1 ):
                for mcs in list_mcs:                
                    stringToFind = "PASS   unicast_unidirection "+mcs
                    print ("****CTC**** String to Find : "+stringToFind)
                    if(ReadContentOfFile.find(stringToFind) > 0):
                        #print "Test Case Passed for %s MCS" %mcs
                        pass
                        
                    else:
                        #print ("!!!!!CTC!!!!! Test Case Failed for %s MCS" %mcs)
                        isTestPass = False
            else :
                stringToFind = "PASS   unicast_unidirection "
                print ("****CTC**** String to Find : "+stringToFind)
                if(ReadContentOfFile.find(stringToFind) > 0):
                    #print "Test Case Passed for %s MCS" %mcs
                    pass                    
                else:
                    #print ("!!!!!CTC!!!!! Test Case Failed for %s MCS" %mcs)
                    isTestPass = False
        
        if(var_testType == "MaxClient"):
            stringToFind = "PASS   unicast_max_client_c"
            #print "****CTC**** String to Find : "+stringToFind
            mcs_Count = len(list_mcs)
            occ_count = ReadContentOfFile.count(stringToFind)
            #print( mcs_Count, occ_count)
            if(occ_count == mcs_Count):
                print ("Occurance os Expected String is : %d" %ReadContentOfFile.count(stringToFind))
                    
            else:
                print ("!!!!!CTC!!!!! Test Case Failed for %s MCS")
                isTestPass = False
        
        if(var_testType == "RR"):
            stringToFind = "PASS   rate_vs_range_s2"
            #print "****CTC**** String to Find : "+stringToFind
            mcs_Count = len(list_mcs)
            occ_count = ReadContentOfFile.count(stringToFind)
            print (mcs_Count, occ_count)
            if(occ_count == mcs_Count):
                print ("Occurance os Expected String is %d: "  %ReadContentOfFile.count(stringToFind))
                    
            else:
                print ("!!!!!CTC!!!!! Test Case Failed for MCS" )
                isTestPass = False

        if(var_testType == "LAT"):
            if(len(list_mcs) > 1 ):
                for mcs in list_mcs:                
                    stringToFind = "PASS   unicast_latency      "+mcs
                    print ("****CTC**** String to Find : "+stringToFind)
                    if(ReadContentOfFile.find(stringToFind) > 0):
                        #print "Test Case Passed for %s MCS" %mcs
                        pass
                        
                    else:
                        print ("!!!!!CTC!!!!! Test Case Failed for %s MCS" %mcs)
                        isTestPass = False
            else :
                stringToFind = "PASS   unicast_latency "
                print ("****CTC**** String to Find : "+stringToFind)
                if(ReadContentOfFile.find(stringToFind) > 0):
                    #print "Test Case Passed for %s MCS" %mcs
                    pass                    
                else:
                    #print ("!!!!!CTC!!!!! Test Case Failed for %s MCS" %mcs)
                    isTestPass = False
    except ValueError as e:
        err = "Value Error is %s" % ( str(e) )
        raise Exception(err)
                    
    return isTestPass

def getTestExecutionTime(respFileContent):
    """
        Function Name        : getTestExecutionTime
        Function Description : This function will Get the test execution time.
        Inputs   : 
            respFileContent  - Command file (.bat)
        Outputs  : 
             Gets the Execution the test commands.      
    """
    try :
        ReadFile = open(respFileContent,'r')
        ReadContentOfFile = ReadFile.read()
        ReadFile.close
    except IOError as e:
        err = "Input/Output error: %s" % ( str(e) )
        raise Exception(err)
        
    global g_testcase_stoptime, g_testcase_starttime
    lines = ReadContentOfFile.split("\n")
    if(lines):
        for eachline in lines:
            #print eachline
        
            if (eachline.find("Starting automated test run at")>0):
               #print ("Found Exe Started Time")
                start = eachline.index("run at")
                end = eachline.index(".")
                g_testcase_starttime = eachline[start+6:end]
                g_testcase_starttime = g_testcase_starttime.strip()
                #g_testcase_starttime = g_testcase_starttime.replace("-","")
                temp_testcase_starttime = g_testcase_starttime.replace("-","")
                
            elif (eachline.find("Automated test run completed at")>0):
                start = eachline.index("ted at")
                end = eachline.index(".")
                g_testcase_stoptime = eachline[start+6:end]
                g_testcase_stoptime = g_testcase_stoptime.strip()
                g_testcase_stoptime = g_testcase_stoptime.replace("-", "")
                  
                
    print ("*****GTET***** Execution Started at :"+g_testcase_starttime)
    #print "*****GTET***** Execution Completed at :"+g_testcase_stoptime
    #starttime_object = datetime.strptime(temp_testcase_starttime, '%Y%m%d%H%M%S')
    starttime_object = datetime.datetime.strptime(temp_testcase_starttime, '%Y%m%d%H%M%S')
    
    #stoptime_object = datetime.strptime(g_testcase_stoptime, '%Y%m%d%H%M%S')
    stoptime_object = datetime.datetime.strptime(g_testcase_stoptime, '%Y%m%d%H%M%S')
    
    elapsed_Time =  stoptime_object - starttime_object
    print ("****GTET****** Total Test Execution Time is : " + str (elapsed_Time))
    
    return str(elapsed_Time)
def getExecutionStartTime(respFileContent):
    """
        Function Name        : getExecutionStartTime
        Function Description : This function will Get the test execution Start time.
        Inputs               : respFileContent  - Command file (.bat)
        Outputs              : Gets the Execution the test commands.      
    """
    try:
        ReadFile = open(respFileContent,'r')
        ReadContentOfFile = ReadFile.read()
        ReadFile.close
    except IOError as e:
        err = "Input/Output error: %s" % ( str(e) )
        raise Exception(err)
    
    global g_testcase_starttime
    lines = ReadContentOfFile.split("\n")
    if(lines):
        for eachline in lines:
            if (eachline.find("Starting automated test run at")>0):
                #print ("Found Exe Started Time")
                start = eachline.index("run at")
                end = eachline.index(".")
                g_testcase_starttime = eachline[start+6:end]
                g_testcase_starttime = g_testcase_starttime.strip()
                
    
    return g_testcase_starttime

   
def saveExecutionStatusToFile(test_name, direction, timestamp, mcs, TestResultStatus, elapsed_Time):
    """
        Function Name        : saveExecutionStatusToFile
        Function Description : This function will Save the execution status into a file
        Inputs   : 
            test_name         - Test Case Name.
            direction         - Uni- Directional or Bi-Directional.
            timestamp         - system Timestamp.
            mcs               - mcs values.
            TestResultStatus  - Status of the test command execution.
            elapsed_Time      - time of test command execution.
        Outputs  : 
            Saves the execution status to a file.       
    """
    print ("In Save Execution Status File")
    execStatusFileName = Directory +"ExecutionStatus.txt"
    try:
        if(os.path.isfile(execStatusFileName)):
            print ("Execution Status File already present ")
            execStatusFile = open(execStatusFileName, "a")
            execStatusFile.write(test_name+ "\t"+ str(var_direction)+ "\t" + str(timestamp)+"\t"+ mcs +"\t"+str(TestResultStatus) + "\t" + str(elapsed_Time))
            execStatusFile.write("\n")
        else :
            execStatusFile = open(execStatusFileName, "w")
            execStatusFile.write("test_name\t"+ "direction\t" + "timestamp\t"+ "mcs\t"+"TestResultStatus\t" + "Elapsed Time\t")
            execStatusFile.write("\n")
            execStatusFile.write(test_name+ "\t"+ str(var_direction)+ "\t" + str(timestamp)+"\t"+ mcs +"\t"+str(TestResultStatus) + "\t" + str(elapsed_Time))
            execStatusFile.write("\n")
    except IOError as e:
        err = "Input/Output error: %s" % ( str(e) )
        raise Exception(err)

def GetThroughputValue(test_name):
    #ts = time.time()
    #st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d')
    TPValue = ""
    try:
        #readTP = open(Directory+"TPValues_"+st+".txt","r")
        readTP = open(Directory+"TPValues.txt","r")
        content = readTP.read()
        lines = content.split("\n")
        readTP.close();
        
    except IOError as e:
        err = "Input/Output error: %s" % ( str(e) )
        raise Exception(err)  
    #print ("\""+test_name+"\"")
    for eachline in lines:
        #print (eachline)
        
        try:
            list = eachline.split(" ")
            
            #print ("Content of List " + str(list[0]))
            if(str(list[0]) == test_name):
                #print ("TP Value Found  for test name in line")
                TPValue = list[2]
            
        except ValueError as e:
            err = "Value Error is %s" % ( str(e) )
            raise Exception(err)
    print ("Throughout Value is " + TPValue)
    return TPValue

def replaceStringInFile(file, pattern, subst):
    # Read contents from file as a single string
    file_handle = open(file, 'r')
    file_string = file_handle.read()
    file_handle.close()

    # Use RE package to allow for replacement (also allowing for (multiline) REGEX)
    file_string = (re.sub(pattern, subst, file_string))

    # Write contents to file.
    # Using mode 'w' truncates the file.
    file_handle = open(file, 'w')
    file_handle.write(file_string)
    file_handle.close()
