############################################################################################################################
# Description : StoreLibrary contains the methods for fetching and parsing the .bat files
# Developer   : Arijit Saha
# Date        : 17-July,2017
############################################################################################################################

#Import required python libraries
import os
import BatParseLibrary
import SecureCopyLibrary
import Logger

#List initialization to store Wave Automation Server details from common parameters userconfig.txt file
srvr_details = []

#Fetches the .bat file from the Wave Automation Server	
def Location_Of_Bat_File(var_locofbat):
	global filePath
	Logger.logMessage("Trying to fetch " + var_locofbat + " from Wave Automation Server")
	"""
	Calling method "getFileFromWaveServer" from SecureCopyLibrary to fetch the .bat file from the Wave Automation Server.
	Parameters passed :
		waveHost				-	Host address of the Wave Automation Server
		wavePortNmbr			-	SCP port number of the Wave Automation Server
		waveUser				-	Username of the Wave Automation Server
		wavePaswd				-	Password of the Wave Automation Server
		var_locofbat			-	User configurable value for the location of .bat file in the Wave Automation Server
	"""	
	filePath = SecureCopyLibrary.getFileFromWaveServer(srvr_details[0], srvr_details[1], srvr_details[2], srvr_details[3], var_locofbat)
	Logger.logMessage("Completed fetching of .bat file from Wave Automation " + srvr_details[0] + "    "+ filePath)	# Method to fetch .bat file from Wave Automation to local

# Reads the values from common parameters from the userconfig.txt as configured by user
def SCPDetails(var_wahostname, var_waportnumber, var_wausername, var_wapassword, var_dbhostname, var_dbusername, var_dbpassword): 
	srvr_details.append(var_wahostname)		#hostName - 0	
	srvr_details.append(var_waportnumber)	#port - 1
	srvr_details.append(var_wausername)		#userName - 2
	srvr_details.append(var_wapassword)		#paswd - 3
	srvr_details.append(var_dbhostname)		#dbHost - 4
	srvr_details.append(var_dbusername)		#dbUser - 5
	srvr_details.append(var_dbpassword)		#dbPwd - 6

# Parse and store values of .bat file	
def MySQL_Store_Result(var_test_name_in, var_locofbat, var_test_direction, var_date_ts, var_throughput_multiplier_in):
	
	#Calling method to parse the location of .bat file and fetch in from Wave Automation Server
	Location_Of_Bat_File(var_locofbat)
	
	Logger.logMessage ("Starting to parse .bat file for " + var_test_name_in)
	"""
	Calling method "parseBatFile" from BatParseLibrary to parse the .bat file fetched from Wave Automation Server.
	Parameters passed :
		srvr_details						-	List which contains the Wave Automation Server details as parsed from common parameters
		var_test_name_in					-	User configurable value that determine test name for which the values needs to be parsed from .bat file
		var_test_direction					-	User configurable value that determine test direction for the same test case
		var_date_ts							-	Result timestamp in which the results for the particular test has been stored
		var_throughput_multiplier_in		-	User configurable value for throughput multiplier applicable for TP test cases only
		filePath							-	Location of .bat file in local Robot Automation server after being fetched from remote
	"""
	BatParseLibrary.parseBatFile(srvr_details, var_test_name_in, var_test_direction, var_date_ts, var_throughput_multiplier_in, filePath)
	