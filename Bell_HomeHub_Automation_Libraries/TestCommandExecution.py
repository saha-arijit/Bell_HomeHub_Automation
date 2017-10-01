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
import Logger
#from datetime import *


global_execMode_in = "Auto"
ConfigFilePath = "userconfig.txt"
g_testcase_starttime = 0
g_testcase_stoptime = 0
TestCmdDestPath = "C:/Program Files (x86)/IxVeriWave/WaveAutomate/automation_6.11-118_2017.06.30.08-admin_windows/automation/conf/HH3000/"
loggerTest = Logger.CreateLogFile(__name__)

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
        #print( "******ETC***** Execution mode set to Manual and Test Command Directory is : ") + Directory
        Logger.messageLog ("Execution mode has been set to Manual and the Test Directory is :" + Directory)
    
    elif(global_execMode_in == "Auto"):
        #Get latest modified directory
        
        Directory = sorted(glob.glob(os.path.join("../Bell_Homehub_Automation_TestCommand/", '*/')), key=os.path.getmtime)[-1]
        
        #print ("*****ETC***** Last Modified Directory is: ")+ Directory
        Logger.messageLog ("Last Modified directory is : " + Directory)
        
        if(Directory.find("TC_Manual")>0):
            Directory = sorted(glob.glob(os.path.join("../Bell_Homehub_Automation_TestCommand/", '*/')), key=os.path.getmtime)[-2]
            #print ("*****ETC***** Last Modified Folder is TestCommand so picking second last created Directory : ")+ Directory
            Logger.messageLog ("Last Modified Directory for Automatic Execution mode is :" + Directory)
    else:
        Logger.errorLog ("Aborting execution as either of AUTO or MANUAL was not found for execution mode.")
        raise AssertionError("Aborting execution as invalid execution mode found. Please enter either AUTO or MANUAL.")
        
    isCommandFilePresent = False        
    isCommandFileExecuted = False
    FileName = Directory + testCommandFileName
    if os.path.isfile(FileName):
        isCommandFilePresent = True
        #print ("*****ETC***** Test Command file present in path")  
        Logger.messageLog ("Test Command file has been found in the directory.")
        
    else:
        Logger.errorLog ("Test command file with the mentioned test case name could not be found in folder.")
        #print ("!!!!!ETC!!!!! Test Command file is not present in path so aborting Execution")
        raise AssertionError("Test command file with the mentioned test case name could not be found in " + Directory)
    
    
    
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
        #print ("****ETC***** Test Type : ") +var_testType
        Logger.messageLog ("Current test type for execution : " + var_testType)
        list_mcs = var_mcs.split(" ")
        #print list_mcs
        #GetUserConfig()
        #print "WaPort :" + var_waport
        if(var_testType =="TP" or var_testType == "MaxClient"):
            Logger.messageLog ("Starting execution for : " + testCommandFileName + " on IxVeriWave server " + var_wahostname + ".  Please wait....")
            print(var_wahostname, var_wausername, var_wapassword, FileName, TestCmdDestPath, testCommandFileName, var_waport)
            #isCommandFileExecuted = executeCommandFile(var_wahostname, var_wausername, var_wapassword, FileName, TestCmdDestPath, testCommandFileName, var_waport)
            #print ("TestType is : " + var_testType)
            isCommandFileExecuted = True
        elif(var_testType =="RR" or var_testType == "LAT"):
            ## IF Test name contains RR then replace it with TP
            if(test_name.find("RR")>0):
                temp_testName = test_name.replace("RR", "TP")
                Logger.messageLog ("Checking for the presence of " + test_name + " for the execution of " + temp_testName)
            ## IF Test name contains LAT then replace it with TP
            elif(test_name.find("LAT")>0):
                temp_testName = test_name.replace("LAT", "TP")
                Logger.messageLog ("Checking for the presence of " + test_name + " for the execution of " + temp_testName)
            
            #print ("Test Name to Found is %s" %temp_testName)
            TPValuesFile = Directory+"TPValues.txt"
            ## Check the TPValues.txt file is present or not. For obtaining previous execution test ID
            Logger.messageLog ("Checking for the presence of TPValues.txt file to fetch Test_ID value.")
            if os.path.isfile(TPValuesFile):
                try:
                    #print ("TP Values File Present")
                    #readTP = open(Directory+"TPValues_"+st+".txt","r")
                    Logger.messageLog ("Presence of TPValues.txt file has been validated successfully.")
                    readTP = open(Directory+"TPValues.txt","r")
                    Logger.messageLog ("Reading data from TPValues.txt file.")
                    content = readTP.read()
                    lines = content.split("\n")
                    readTP.close(); 
                except IOError as e:
                    err = "Input/Output error: %s" % (str(e))
                    raise Exception(err)  
                #print ("\""+test_name+"\"")
                Logger.messageLog ("Checking for the successful execution of " + test_name +" test command previous to " + temp_testName)
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
                            #print ("Test Name = " + list[0])
                            if(list[0] == temp_testName):
                                Logger.messageLog (list[0] + "  has been successfully executed before  " + temp_testName)
                                #print ("TP Test Case found in Pase Execution")
                                #*********************************
                                #test_name_file = list[0]  # Fetching the corresponding TP test name from the "TPValues.txt" file 
                                #*********************************
                                #print test_name
                                #print test_nam
                                Direction = list[1]
                                Logger.messageLog ("Direction found for corresponding TP test case execution :" + Direction)
                                #print (Direction)
                                TPValue = list[2]
                                Logger.messageLog ("Throughout Value found for corresponding TP test case execution :" + TPValue)
                                #print (TPValue)
                                TestID = list[3]
                                Logger.messageLog ("Fetched Test Id from database for corresponding TP test case execution :" + TestID)
                                #print (TestID)
                                #print("Before calling getpps")
                                #print(TestID, list_mcs, list_frameSize)
                                #Calling Method to fetch the loads in RR or LAT
                                Logger.messageLog ("Calling method to fetch LOADS value for :" + test_name)
                                loads_value = getpps(TestID, list_mcs, list_frameSize)
                                #print ("Print Loads Value")
                                #print(loads_value)
                                Logger.messageLog ("Completed fetching LOADS value for :" + test_name)
                                loadsValue = " ".join(str(x) for x in loads_value)
                                #print(loadsValue)
                                Logger.messageLog ("Opening " + test_name + " Test Command file to write the Loads value.")
                                openFile = open(FileName,"r")
                                fileContent = openFile.read()
                                Logger.messageLog ("Reading existing data from Loads in the Test Command file.")
                                replacedText = fileContent.replace("loads \"\"", "loads \""+loadsValue+"\"", 1)
                                openFile.close()
                                openFile = open(FileName,"w")
                                openFile.write(replacedText)
                                openFile.close()
                                Logger.messageLog ("Completed writing the value for Loads in the Test Command file for :" + test_name)
                                isPrevExecDataFound = True
                                Logger.messageLog ("Setting flag value for 'isPrevExecDataFound' to 'True'.")
                       
                    except ValueError as e:
                        err = "Value Error is %s" % ( str(e) )
                        raise Exception(err)
                #print ("Throughout Value is %s and TestID is %s" %TPValue %TestID)
                Logger.messageLog ("Checking for flag value 'isPrevExecDataFound'.")
                if(isPrevExecDataFound == True):
                    #print("Previous Execution of TP Test case found")
                    Logger.messageLog ("Flag Value for 'isPrevExecDataFound' has been found to be 'True'. " + test_name +" is ready for execution.")
                    Logger.messageLog ("Starting execution of "+test_name+ ". Please wait while the execution is in progress on IxVeriWave server on " + var_wahostname)
                    #print(var_wahostname, var_wausername, var_wapassword, FileName, TestCmdDestPath, testCommandFileName, var_waport)
                    isCommandFileExecuted = executeCommandFile(var_wahostname, var_wausername, var_wapassword, FileName, TestCmdDestPath, testCommandFileName, var_waport)
                    #isCommandFileExecuted = True
                    Logger.messageLog ("Setting flag value for 'isCommandFileExecuted' to 'True'.")
                    Logger.messageLog ("Completed execution of " + test_name + " successfully.")
                else :
                    #print("!!!!!TCE!!!!! Previous execution of TP Test case not found in TP Values file")
                    Logger.errorLog ("Flag Value for 'isPrevExecDataFound' has been found to be 'False'. Aborting execution for " + test_name +".")
                    isCommandFileExecuted = False
                    Logger.errorLog ("Setting flag value for 'isCommandFileExecuted' to 'False'.")
                    Logger.errorLog ("Previous execution of corresponding TP test case not found.")    
                    raise AssertionError("Previous execution of TP Test case not found in TP Values file.")

            else :
                isCommandFileExecuted = False
                Logger.errorLog ("Setting flag value for 'isCommandFileExecuted' to 'False'.")
                #print("!!!!!TCE!!!!! TPValues.txt File is not present on command File path")
                Logger.errorLog ("'TPValues.txt' has not been found in the Test Command file path.")
                raise AssertionError(" TPValues.txt File is not present on command File path.")
        
        if(isCommandFileExecuted == True):
            Logger.messageLog ("Flag Value for 'isCommandFileExecuted' has been found to be 'True'. ")
            #print ("Command File is Executed")
            Logger.messageLog ("Searching for the Test Result Log file fetched from Wave Server.")
            if(os.path.isfile(TestResultLogFile)):
                Logger.messageLog ("Test Result Log file has been found successfully.")
                #print ("TestResult Log File is present in path")
                outputDS = "../Bell_Homehub_Automation_Files/output_DS.txt"
                Logger.messageLog ("Created Result Output text file for DownStream direction.")
                outputUS = "../Bell_Homehub_Automation_Files/output_US.txt"
                Logger.messageLog ("Created Result Output text file for UpStream direction.")
                try:
                    Logger.messageLog ("Value entered by user for direction configuration in Test Command : %d" %var_direction)
                    #print ("direction is : %d" %var_direction)
                    
                    # *****************************  FOR BI - DIRECTIONAL **********************************
                    if(var_direction == 1):
                        Logger.messageLog ("Proceeding with Result file processing for Bi-Directional Test Case.")
                        #print "Command Executeds, OutputFile PResent and Direction = 1"
                        with open(TestResultLogFile) as f:
                            Logger.messageLog ("Opening Test Result Log file.")
                            DS, output, US = f.read().partition("/output.log\n")
                            #print (output)
                            Logger.messageLog ("Reading contents of Test Result Log file.")
                            with open(outputDS, "w") as f:
                                f.write(DS)
                                Logger.messageLog ("Writing the contents of DS to DownStream result test file.")
                                with open(outputUS, "w") as f:
                                    Logger.messageLog ("Writing the contents of US to UpStream result test file.")
                                    f.write(US)
                        ## Post Procesing For DS
                        Logger.messageLog ("Trying to check the execution status for DS execution.")
                        #print ("Check Execution status for DS")
                        TestResultStatus = verifyTestExectionStatus(outputDS)
                        Logger.messageLog ("Successfully checked the execution status for DS execution. \
                                                Setting value flag for 'TestResultStatus' to : " + str(TestResultStatus))
                        #print ("Test Exeuction status is %r"  %TestResultStatus)
                        if (TestResultStatus == True):
                            Logger.messageLog ("Test Result execution status has been found to be : " + str(TestResultStatus))
                            Logger.messageLog ("Trying to check the duration for the execution of the test command file.")
                            elapsed_Time = getTestExecutionTime(outputDS)
                            Logger.messageLog ("Duration for the execution of the test command file is : " + str(elapsed_Time))
                            #print("before calling GetThroughputValue function")
                                 #****************************************
                            Logger.messageLog ("Trying to check Test Type and if required fetch Throughput value.")
                            if (var_testType == "TP"):
                                Logger.messageLog ("Test Type has been found to be : " + var_testType)
                                Logger.messageLog ("Trying to fetch the Throughput value from TPValues.txt file.")
                                ThroughputValue = GetThroughputValue(test_name)
                                Logger.messageLog ("Value of Throughput found from TPValues.txt file :" + ThroughputValue)
                            else:
                                Logger.messageLog ("Test Type has been found to be : " + var_testType +". Not required to fetch Throughput value.")
                                ThroughputValue = 0
                                Logger.messageLog ("Setting value of Throughput to 0.")
                            #****************************************
                            #print ("Throughput Value is : %s"  %ThroughputValue)
                            #saveExecutionStatusToFile(test_name, "DS", g_testcase_starttime, ThroughputValue, FileName, elapsed_Time)
                            #print test_name + "\t" + "DS" + "\t" + str(g_testcase_starttime)+ "\t" + str(ThroughputValue) + "\t " + FileName + "\t" + str(elapsed_Time)
                            Logger.messageLog ("Trying to call method to parse .bat file and store the details to database.")
                            result_test_Id = parseBatFile(srvr_details, test_name, "DS", g_testcase_starttime, ThroughputValue, FileName, elapsed_Time)
                            Logger.messageLog ("Successfully executed parsing of .bat file")
                            Logger.messageLog ("Test ID fetched from database for the parsed test command is : " + str(result_test_Id))
                            if(var_testType == "TP"):
                                Logger.messageLog ("Test type has been found to be : " + var)                                
                                TPValuesFile = Directory+"TPValues.txt"
                                pattern = test_name + " DS " + ThroughputValue
                                subst = pattern +" " + str(result_test_Id) 
                                Logger.messageLog ("Calling method to store the TestID value fetched from database in TPValues.txt file.")
                                replaceStringInFile(TPValuesFile, pattern, subst)
                                Logger.messageLog ("Successfully stored the TestID of in TPValues.txt file for execution of RR/LAT test commands.")
                        else:
                            TestResultDir = var_Result_Dir + "\\" + getExecutionStartTime(outputDS)                            
                            Logger.errorLog ("Test Case execution failed. Please check the logs on Wave server.")
                            raise AssertionError("Test Case Excution status Failed. For More details check logs on WaveServer " + TestResultDir )
                            #return False
                        try :
                            os.remove(outputDS)
                            Logger.messageLog ("Removed UpStream Test Result log file from local server.")
                            pass
                        except :
                            #print("Execution Log File Not Present ")
                            Logger.errorLog ("Execution log file could not be found.")
                        
                        ## Post Procesing for US
                        #print ("Check Execution status for US")
                        Logger.messageLog ("Trying to check the execution status for US execution.")
                        TestResultStatus = verifyTestExectionStatus(outputUS)
                        #print ("Test Exeuction status is %r"  %TestResultStatus)
                        Logger.messageLog ("Successfully checked the execution status for US execution. \
                                                Setting value flag for 'TestResultStatus' to : " + str(TestResultStatus))
                        if (TestResultStatus ==True):
                            Logger.messageLog ("Test Result execution status has been found to be : " + str(TestResultStatus))
                            Logger.messageLog ("Trying to check the duration for the execution of the test command file.")
                            elapsed_Time = getTestExecutionTime(outputUS)
                            Logger.messageLog ("Duration for the execution of the test command file is : " + str(elapsed_Time))
                                 #****************************************
                            Logger.messageLog ("Trying to check Test Type and if required fetch Throughput value.")
                            if (var_testType == "TP"):
                                Logger.messageLog ("Test Type has been found to be : " + var_testType)
                                Logger.messageLog ("Trying to fetch the Throughput value from TPValues.txt file.")
                                ThroughputValue = GetThroughputValue(test_name)
                                Logger.messageLog ("Value of Throughput found from TPValues.txt file :" + ThroughputValue)
                            else:
                                Logger.messageLog ("Test Type has been found to be : " + var_testType +". Not required to fetch Throughput value.")
                                ThroughputValue = 0
                                Logger.messageLog ("Setting value of Throughput to 0.")
            
                            #****************************************
                            
                            #saveExecutionStatusToFile(test_name, "US", g_testcase_starttime, ThroughputValue, FileName, elapsed_Time)
                            #print "test_name" + "\t" + "US" + "\t" + str(g_testcase_starttime)+ "\t" + str(ThroughputValue) + "\t " + FileName + "\t" + str(elapsed_Time)
                            Logger.messageLog ("Trying to call method to parse .bat file and store the details to database.")
                            result_test_Id = parseBatFile(srvr_details, test_name, "US", g_testcase_starttime, ThroughputValue, FileName, elapsed_Time)
                            Logger.messageLog ("Successfully executed parsing of .bat file")
                            Logger.messageLog ("Test ID fetched from database for the parsed test command is : " + str(result_test_Id))
                            if(var_testType == "TP"):
                                Logger.messageLog ("Test type has been found to be : " + var_testType)
                                TPValuesFile = Directory+"TPValues.txt"
                                pattern = test_name + " US " + ThroughputValue
                                subst = pattern +" " + str(result_test_Id) 
                                Logger.messageLog ("Calling method to store the TestID value fetched from database in TPValues.txt file.")
                                replaceStringInFile(TPValuesFile, pattern, subst)
                                Logger.messageLog ("Successfully stored the TestID of in TPValues.txt file for execution of RR/LAT test commands.")
                            
                        else:
                            TestResultDir = var_Result_Dir + "\\" + getExecutionStartTime(outputUS)  
                            Logger.errorLog ("Test Case execution failed. Please check the logs on Wave server.")                          
                            raise AssertionError("Test Case Excution status Failed. For More details check logs on WaveServer " + TestResultDir )
                            return False
                        try :
                            os.remove(outputUS)
                            Logger.messageLog ("Removed UpStream Test Result log file from local server.")
                            #os.remove(TestResultLogFile)
                        except :
                            #print("Execution Log File Not Present ")
                            Logger.errorLog ("Execution log file could not be found.")

                    # *********************     FOR UNI - DIRECTIONAL *************************8
                    else :
                        Logger.messageLog ("Proceeding with Result file processing for Uni-Directional Test Case.")
                        #print "Command Executeds, OutputFile Present and Direction = 0."
                        Logger.messageLog ("Trying to check the execution status for Uni-Directional execution.")
                        TestResultStatus = verifyTestExectionStatus(TestResultLogFile)
                        Logger.messageLog ("Successfully checked the execution status for DS execution. \
                                                Setting value flag for 'TestResultStatus' to : " + str(TestResultStatus))
                        #print ("Test Exeuction status is %r"  %TestResultStatus)
                        if (TestResultStatus ==True):
                            Logger.messageLog ("Test Result execution status has been found to be : " + str(TestResultStatus))
                            Logger.messageLog ("Trying to check the duration for the execution of the test command file.")
                            elapsed_Time = getTestExecutionTime(TestResultLogFile)
                            Logger.messageLog ("Duration for the execution of the test command file is : " + str(elapsed_Time))
                            #****************************************
                            Logger.messageLog ("Trying to check Test Type and if required fetch Throughput value.")
                            if (var_testType == "TP"):
                                Logger.messageLog ("Test Type has been found to be : " + var_testType)
                                Logger.messageLog ("Trying to fetch the Throughput value from TPValues.txt file.")
                                ThroughputValue = GetThroughputValue(test_name)
                                Logger.messageLog ("Value of Throughput found from TPValues.txt file :" + ThroughputValue)
                            else:
                                Logger.messageLog ("Test Type has been found to be : " + var_testType +". Not required to fetch Throughput value.")
                                ThroughputValue = 0
                                Logger.messageLog ("Setting value of Throughput to 0.")
                            #****************************************

                            #saveExecutionStatusToFile(test_name, "DS", g_testcase_starttime, ThroughputValue, FileName, elapsed_Time)
                            #print test_name + "\t" + "DS" + "\t" + str(g_testcase_starttime)+ "\t" + str(ThroughputValue) + "\t " + FileName + "\t" + str(elapsed_Time)
                            Logger.messageLog ("Trying to call method to parse .bat file and store the details to database.")
                            result_test_Id = parseBatFile(srvr_details, test_name, "DS", g_testcase_starttime, ThroughputValue, FileName, elapsed_Time)
                            Logger.messageLog ("Successfully executed parsing of .bat file")
                            Logger.messageLog ("Test ID fetched from database for the parsed test command is : " + str(result_test_Id))
                            if(var_testType == "TP"):
                                Logger.messageLog ("Test type has been found to be : " + var_testType)
                                TPValuesFile = Directory+"TPValues.txt"
                                pattern = test_name + " DS " + ThroughputValue
                                subst = pattern +" " + str(result_test_Id)
                                Logger.messageLog ("Calling method to store the TestID value fetched from database in TPValues.txt file.")
                                replaceStringInFile(TPValuesFile, pattern, subst)
                                Logger.messageLog ("Successfully stored the TestID of in TPValues.txt file for execution of RR/LAT test commands.")
                        else:
                            TestResultDir = var_Result_Dir + "\\" + str(getExecutionStartTime(TestResultLogFile))
                            Logger.errorLog ("Test Case execution failed. Please check the logs on Wave server.")                          
                            raise AssertionError("Test Case Execution status Failed. For More details check logs on WaveServer " + TestResultDir )
                            return False
                    try :
                        os.remove(TestResultLogFile)
                        Logger.messageLog ("Removed DownStream Uni Directional Test Result log file from local server.")
                    except :
                        #print("Execution Log File Not Present ")
                        Logger.errorLog ("Execution log file could not be found as it was not present in local server.")

                except IOError as e:
                    err = "Input/Output error: %s" % ( str(e) )
                    raise Exception(err)
            else :
                #print ("Test Result Log File is not present on exepcted location")
                Logger.messageLog ("Test Result Log file could not be found in the local server. Please check Wave server for details.")
        else :
            Logger.errorLog ("Execution Of Command File Failed. Please check the logs for more details.")
            raise AssertionError("Execution Of Command File Failed. Please check the logs for more details.")

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
            respFileContent  - Test Result Log File 
        Outputs  : 
             verifies the Execution the test commands.
            
    """ 
    Logger.messageLog ("Reading the Test Result Log file to check the status of command file execution.")
    ReadFile = open(respFileContent,'r')
    ReadContentOfFile = ReadFile.read()
    ReadFile.close
    Logger.messageLog ("Setting the default value of flag 'isTestPass' to 'True'.")
    isTestPass = True
    try:
        if(var_testType == "TP"):
            Logger.messageLog ("Test Type for the current execution is : " + var_testType)
            if(len(list_mcs) > 1 ):
                Logger.messageLog ("Test Case has been defined with multiple MCS values.")
                for mcs in list_mcs:                
                    stringToFind = "PASS   unicast_unidirection "+mcs
                    #print ("****CTC**** String to Find : "+stringToFind)
                    if(ReadContentOfFile.find(stringToFind) > 0):
                        #print "Test Case Passed for %s MCS" %mcs
                        Logger.messageLog ("Test has executed successfully for MCS value : " + mcs)
                    else:
                        #print ("!!!!!CTC!!!!! Test Case Failed for %s MCS" %mcs)
                        Logger.errorLog ("Test command has failed executing for MCS value : " + mcs)
                        isTestPass = False
                        Logger.errorLog ("Setting flag value for 'isTestPass' to 'False'.")
            else :
                Logger.messageLog ("Test Case has been defined with single MCS value.")
                stringToFind = "PASS   unicast_unidirection "
                #print ("****CTC**** String to Find : "+stringToFind)
                if(ReadContentOfFile.find(stringToFind) > 0):
                    #print "Test Case Passed for %s MCS" %mcs
                    Logger.messageLog ("Test has executed successfully for MCS value : " + mcs)
                else:
                    #print ("!!!!!CTC!!!!! Test Case Failed for %s MCS" %mcs)
                    Logger.errorLog ("Test command has failed executing for MCS value : " + mcs)
                    isTestPass = False
                    Logger.errorLog ("Setting flag value for 'isTestPass' to 'False'.")
        
        if(var_testType == "MaxClient"):
            Logger.messageLog ("Test Type for the current execution is : " + var_testType)
            stringToFind = "PASS   unicast_max_client_c"
            #print "****CTC**** String to Find : "+stringToFind
            mcs_Count = len(list_mcs)
            occ_count = ReadContentOfFile.count(stringToFind)
            #print( mcs_Count, occ_count)
            if(occ_count == mcs_Count):
                #print ("Occurance of Expected String is : %d" %ReadContentOfFile.count(stringToFind))
                Logger.messageLog ("Test has executed successfully for MCS value : " + mcs)
            else:
                Logger.errorLog ("Test command has failed executing for MCS value : " + mcs)
                #print ("!!!!!CTC!!!!! Test Case Failed for %s MCS")
                isTestPass = False
                Logger.errorLog ("Setting flag value for 'isTestPass' to 'False'.")

        
        if(var_testType == "RR"):
            Logger.messageLog ("Test Type for the current execution is : " + var_testType)
            stringToFind = "PASS   rate_vs_range_s2"
            #print "****CTC**** String to Find : "+stringToFind
            mcs_Count = len(list_mcs)
            occ_count = ReadContentOfFile.count(stringToFind)
            print (mcs_Count, occ_count)
            if(occ_count == mcs_Count):
                #print ("Occurance os Expected String is %d: "  %ReadContentOfFile.count(stringToFind))
                Logger.messageLog ("Test has executed successfully for MCS value : " + mcs)    
            else:
                #print ("!!!!!CTC!!!!! Test Case Failed for MCS" )
                Logger.errorLog ("Test command has failed executing for MCS value : " + mcs)
                isTestPass = False
                Logger.errorLog ("Setting flag value for 'isTestPass' to 'False'.")

        if(var_testType == "LAT"):
            Logger.messageLog ("Test Type for the current execution is : " + var_testType)
            if(len(list_mcs) > 1 ):
                Logger.messageLog ("Test Case has been defined with multiple MCS values.")
                for mcs in list_mcs:                
                    stringToFind = "PASS   unicast_latency      "+mcs
                    print ("****CTC**** String to Find : "+stringToFind)
                    if(ReadContentOfFile.find(stringToFind) > 0):
                        #print "Test Case Passed for %s MCS" %mcs
                        Logger.messageLog ("Test has executed successfully for MCS value : " + mcs)
                    else:
                        #print ("!!!!!CTC!!!!! Test Case Failed for %s MCS" %mcs)
                        Logger.errorLog ("Test command has failed executing for MCS value : " + mcs)
                        isTestPass = False
                        Logger.errorLog ("Setting flag value for 'isTestPass' to 'False'.")
            else :
                Logger.messageLog ("Test Case has been defined with Single MCS values.")
                stringToFind = "PASS   unicast_latency "
                #print ("****CTC**** String to Find : "+stringToFind)
                if(ReadContentOfFile.find(stringToFind) > 0):
                    #print "Test Case Passed for %s MCS" %mcs
                    Logger.messageLog ("Test has executed successfully for MCS value : " + mcs)
                    pass                    
                else:
                    Logger.errorLog ("Test command has failed executing for MCS value : " + mcs)    
                    #print ("!!!!!CTC!!!!! Test Case Failed for %s MCS" %mcs)
                    isTestPass = False
                    Logger.errorLog ("Setting flag value for 'isTestPass' to 'False'.")
    except ValueError as e:
        err = "Value Error is %s" % ( str(e) )
        raise Exception(err)

    Logger.messageLog ("Setting flag value for 'isTestPass' to 'True'.")
    return isTestPass

def getTestExecutionTime(respFileContent):
    """
        Function Name        : getTestExecutionTime
        Function Description : This function will Get the test execution time.
        Inputs   : 
            respFileContent  - Test Result Log file.
        Outputs  : 
             Gets the Execution the test commands.      
    """
    try :
        Logger.messageLog ("Reading the Test Result Log file to check Total time for execution.")
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
                Logger.messageLog ("Searching for execution start time.")
                #print ("Found Exe Started Time")
                start = eachline.index("run at")
                end = eachline.index(".")
                g_testcase_starttime = eachline[start+6:end]
                g_testcase_starttime = g_testcase_starttime.strip()
                #g_testcase_starttime = g_testcase_starttime.replace("-","")
                temp_testcase_starttime = g_testcase_starttime.replace("-","")
                Logger.messageLog ("Execution started at : " + g_testcase_starttime)
                
            elif (eachline.find("Automated test run completed at")>0):
                Logger.messageLog ("Searching for Execution Completion time.")
                start = eachline.index("ted at")
                end = eachline.index(".")
                g_testcase_stoptime = eachline[start+6:end]
                g_testcase_stoptime = g_testcase_stoptime.strip()
                g_testcase_stoptime = g_testcase_stoptime.replace("-", "")
                Logger.messageLog ("Execution stopped at : " + g_testcase_stoptime)
            
    #print ("*****GTET***** Execution Started at :"+g_testcase_starttime)
    #print "*****GTET***** Execution Completed at :"+g_testcase_stoptime
    #starttime_object = datetime.strptime(temp_testcase_starttime, '%Y%m%d%H%M%S')
    starttime_object = datetime.datetime.strptime(temp_testcase_starttime, '%Y%m%d%H%M%S')
    
    #stoptime_object = datetime.strptime(g_testcase_stoptime, '%Y%m%d%H%M%S')
    stoptime_object = datetime.datetime.strptime(g_testcase_stoptime, '%Y%m%d%H%M%S')
    
    elapsed_Time =  stoptime_object - starttime_object
    #print ("****GTET****** Total Test Execution Time is : " + str (elapsed_Time))
    Logger.messageLog ("Total time taken for execution : " + str(elapsed_Time))
    return str(elapsed_Time)


def getExecutionStartTime(respFileContent):
    """
        Function Name        : getExecutionStartTime
        Function Description : This function will Get the test execution Start time.
        Inputs               : respFileContent  - Command file (.bat)
        Outputs              : Gets the Execution the test commands.      
    """
    try:
        Logger.messageLog ("Reading the Test Result Log file to check Start time for execution.")
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
                
    Logger.messageLog ("Execution Start time is :" + g_testcase_starttime)
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
    Logger.messageLog ("In method to save execution status to text file.")
    execStatusFileName = Directory +"ExecutionStatus.txt"
    Logger.messageLog ("Searching for test execution status text file.")
    try:
        if(os.path.isfile(execStatusFileName)):
            Logger.messageLog ("Test Execution status text file is present.")
            print ("Execution Status File already present ")
            execStatusFile = open(execStatusFileName, "a")
            execStatusFile.write(test_name+ "\t"+ str(var_direction)+ "\t" + str(timestamp)+"\t"+ mcs +"\t"+str(TestResultStatus) + "\t" + str(elapsed_Time))
            execStatusFile.write("\n")
        else :
            Logger.messageLog ("Creating Test Execution status text file.")
            execStatusFile = open(execStatusFileName, "w")
            execStatusFile.write("test_name\t"+ "direction\t" + "timestamp\t"+ "mcs\t"+"TestResultStatus\t" + "Elapsed Time\t")
            Logger.messageLog ("Writing headers 'Test Name',  'Direction',  'TimeStamp', 'MCS',  'Test Result Status',  'Elapsed Time'")
            execStatusFile.write("\n")
            execStatusFile.write(test_name+ "\t"+ str(var_direction)+ "\t" + str(timestamp)+"\t"+ mcs +"\t"+str(TestResultStatus) + "\t" + str(elapsed_Time))
            Logger.execution ("Inserting value for each of the headers mentioned in the file for the current command file execution.")
            execStatusFile.write("\n")
    except IOError as e:
        err = "Input/Output error: %s" % ( str(e) )
        raise Exception(err)
    Logger.messageLog ("Completed inserting test execution details to test execution text file.")


def GetThroughputValue(test_name):
    #ts = time.time()
    #st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d')
    TPValue = ""
    try:
        #readTP = open(Directory+"TPValues_"+st+".txt","r")
        readTP = open(Directory+"TPValues.txt","r")
        content = readTP.read()
        Logger.messageLog ("Opening and reading TPValues.txt file for the Throughput value.")
        lines = content.split("\n")
        readTP.close();
        
    except IOError as e:
        err = "Input/Output error: %s" % ( str(e) )
        raise Exception(err)
    #print ("\""+test_name+"\"")
    for eachline in lines:
        try:
            list = eachline.split(" ")
            
            #print ("Content of List " + str(list[0]))
            if(str(list[0]) == test_name):
                #print ("TP Value Found  for test name in line")
                TPValue = list[2]
            
        except ValueError as e:
            err = "Value Error is %s" % ( str(e) )
            raise Exception(err)
    #print ("Throughout Value is " + TPValue)
    Logger.messageLog ("Throughput Value found in the TPValues.txt file : " + TPValue)
    return TPValue

def replaceStringInFile(file, pattern, subst):
    # Read contents from file as a single string
    Logger.messageLog ("Reading the existing contents from file.")
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
    Logger.messageLog ("Updated the existing contents of file with the new contents.")
