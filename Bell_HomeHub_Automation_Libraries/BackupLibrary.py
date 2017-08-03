##################################################################################################################################
# Description : BackupLibrary contains the methods to create backup of results and master database both manually and automatically
# Developer   : Uma Shankar
# Date        : 17-July,2017
##################################################################################################################################

#Import required python libraries
import os
import time
import sys
import datetime
import subprocess
import SecureCopyLibrary
import Logger
from robot.api.deco import keyword

# Set the path location of the userconfig.txt file
drive = os.path.splitdrive(os.getcwd())
ConfigFilePath = drive[0]+"\Bell_HomeHub_Automation\Bell_HomeHub_Automation\userconfig.txt"

#This function will parse the configuration parameters specific to this library from userconfig.txt file and use in exeuction 	
def SetUserConfig():
	global waveHost, wavePortNmbr, waveUser, wavePaswd, dbusername, dbpassword, backup_path
	configFile = open(ConfigFilePath, 'r')
	content = configFile.read()
	lines = content.split("\n")
	for eachline in lines:
		#print eachline
		str = eachline
		#print str.find("var_ssid_in}")
		if (str.find("var_backuphostname}")>0):
			start = str.index("}")
			end = str.index("#")
			substr = str[start+1:end]
			substr = substr.replace(" ","")
			substr.strip()
			waveHost = substr
		elif (str.find("var_backupportnumber}")>0):
			start = str.index("}")
			end = str.index("#")
			substr = str[start+1:end]
			substr = substr.replace(" ","")
			substr.strip()
			wavePortNmbr = substr
		elif (str.find("var_backupusername}")>0):
			start = str.index("}")
			end = str.index("#")
			substr = str[start+1:end]
			substr = substr.replace(" ","")
			substr.strip()
			waveUser = substr
		elif (str.find("var_backuppassword}")>0):
			start = str.index("}")
			end = str.index("#")
			substr = str[start+1:end]
			substr = substr.replace(" ","")
			substr.strip()
			wavePaswd = substr
		elif (str.find("var_dbusername}")>0):
			start = str.index("}")
			end = str.index("#")
			substr = str[start+1:end]
			substr = substr.replace(" ","")
			substr.strip()
			dbusername = substr
		elif (str.find("var_dbpassword}")>0):
			start = str.index("}")
			end = str.index("#")
			substr = str[start+1:end]
			substr = substr.replace(" ","")
			substr.strip()
			dbpassword = substr
		elif (str.find("var_localDBBackup}")>0):
			start = str.index("}")
			end = str.index("#")
			substr = str[start+1:end]
			substr = substr.replace(" ","")
			substr.strip()
			backup_path = substr

# Runs the Automatic backup batch file from the scheduler			
def AutoRun(remoteLoc):
	SetUserConfig()
	ManualBackUp(backup_path, remoteLoc)
"""
Calling method "MySQL_Backup" to create a scheduled task for Automatic Backup of the databases.
Parameters passed :
	remoteBackUpPath		- 	Configurable path entered by the user to place the backup files of database in Wave Automation Server
	backup_type				-	Configurable value entered by the user to determine the type of backup that is to be executed
	backup_period 			- 	Configurable value entered by the user to determine the interval of the automatic backup task
	backup_action			- 	Start = Create a scheduled task for DB backup,  Stop = Delete an existing scheduled task
"""		
def MySQL_Backup(remoteBackUpPath, backup_type, backup_period, backup_action):
	
	if (len(remoteBackUpPath) <=0):
		raise Exception ("Value for path to store backup files cannot be empty.")
	if (len(backup_type) <= 0):
		raise Exception ("Value for type of backup to be executed cannot be left empty.")
	if (len(backup_period) <= 0):
		raise Exception ("Enter 'NA' for Manual Backup. Incase of Automatic Backup enter value for number of days.")
		
	if backup_type.lower() == 'manual':
		Logger.logMessage ("Initiating Manual BackUp.")
		ManualBackUp(backup_path, remoteBackUpPath)
	elif backup_type.lower() == 'automatic':
		
		if backup_action.lower() == 'start':
			Logger.logMessage ("Creating Scheduled task for Automatic BackUp.")
			try:
				int(backup_period)
			except ValueError:
				raise Exception ("Should enter a numeric value for Backup Period in case of Automatic Backup.")
			AutoBackUp(remoteBackUpPath, backup_period, backup_action)
			Logger.logMessage ("Completed creating Scheduled task for Automatic Backup.")
		elif backup_action.lower() == 'stop':	
			Logger.logMessage ("Removing existing Scheduled task for Automatic BackUp.")
			AutoBackUp(remoteBackUpPath, backup_period, backup_action)
			Logger.logMessage ("Scheduled Automatic Backup task removed.")
		else:
			raise Exception ("Invalid Entry for BackUp Action. Choose between Start and Stop.")
			#Logger.logMessage ("Invalid Entry for BackUp Action. Choose between Start and Stop.")
	else:
		raise Exception("Invalid Entry for BackUp type. Choose between Automatic and Manual")
		#Logger.logMessage ("Invalid Entry for BackUp type. Choose between Automatic and Manual")
"""
Calling method "ManualBackUp" to create a scheduled task for Manual Backup of the databases.
Parameters passed :
	backup_path				-	Local path in Robot Automation Server for storing the backup files after creation
	remoteBackUpPath		- 	Configurable path entered by the user to place the backup files of database in Wave Automation Server
"""	
def ManualBackUp(backup_path, remoteBackUpPath):		
	database=['results','master']
	# Getting current datetime to create seprate backup folder like "12012013-071334".
	Logger.logMessage ("Fetching current time stamp value for backup folder")
	DATETIME = time.strftime('%m%d%Y-%H%M%S')
	BACKUP_PATH = backup_path + DATETIME

	# Checking if backup folder already exists or not. If not exists will create it.
	Logger.logMessage("Checking Backup Folder in Local Server")
	if not os.path.exists(BACKUP_PATH):
		Logger.logMessage("Creating Backup Folder in Local Server")
		os.makedirs(BACKUP_PATH)
	else :
		Logger.logMessage("Backup Directory already exists in local server")
		
	for db in database:
		dumpcmd = "mysqldump -u " + dbusername + " -p" + dbpassword + " " + db + " > " + BACKUP_PATH + "/" + db + ".sql"
		os.system(dumpcmd)
		Logger.logMessage ("Backup of " + db + " created in Local server")
		Logger.logMessage ("Inititaing Secure Copy of "+ db + " BackUp file to Wave Server")
		
		"""
		Calling method "putFileToWaveServer" from SecureCopyLibrary to create a scheduled task for Automatic Backup of the databases.
		Parameters passed :
			waveHost				-	Host address of server to store Database Backup
			wavePortNmbr			-	SCP port number of server to store Database Backup
			waveUser				-	Username of server to store Database Backup
			wavePaswd				-	Password of server to store Database Backup
			backup_path				-	Local path in Robot Automation Server for storing the backup files after creation
			timestamp				-	Timestamp value for creating a folder to store the backup files to.
			remoteBackUpPath		- 	Configurable path entered by the user to place the backup files of database in server to store Database Backup
		"""	
		SecureCopyLibrary.putFileToWaveServer(waveHost, wavePortNmbr, waveUser, wavePaswd, BACKUP_PATH + "/" + db + ".sql", DATETIME, remoteBackUpPath)
		Logger.logMessage ("Completed Secure Copy of "+ db + " BackUp file to Wave Server")

	Logger.logMessage ("Manual Backup completed")

"""
Calling method "AutoBackUp" to create a scheduled task for Automatic Backup of the databases.
Parameters passed :
	remoteBackUpPath		- 	Configurable path entered by the user to place the backup files of database in Wave Automation Server
	backup_period 			- 	Configurable value entered by the user to determine the interval of the automatic backup task
	backup_action			- 	Start = Create a scheduled task for DB backup,  Stop = Delete an existing scheduled task 
"""	
						
def AutoBackUp(remoteBackUpPath, backup_period, backup_action):
	#Check for existing tasks to be present
	commandCheck = ['schtasks.exe', '/QUERY', '/TN', 'DB_AutoBackup']
	procCheck = subprocess.Popen(commandCheck, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	existingTask = procCheck.stdout.read()
	#if existing tasks are not present, then create the task
	if backup_action.lower() == 'stop':
		command = ['schtasks.exe','/DELETE','/TN', 'DB_AutoBackup', '/F']
		proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		stdout_value = proc.stdout.read()
	
	# Creation or modification of scheduled task
	if 	backup_action.lower() == 'start':	
		# Creates a scheduled task when no task by the same name is present	
		if 'DB_AutoBackup' not in existingTask:
			drive = os.path.splitdrive(os.getcwd())
			command='schtasks /Create /SC daily /mo %s /TN DB_AutoBackup /ST 00:00 /TR "\\"%s\\Bell_HomeHub_Automation\\Bell_HomeHub_Automation_Libraries\\AutoBackUp.bat\\" %s'%(backup_period, drive[0] ,remoteBackUpPath)
			os.system(command)
			
		#if existing tasks are present, then delete the existing task and create a new task	
		if 'DB_AutoBackup' in existingTask:
			Logger.logMessage ("Modifying existing Backup Task")
			command = ['schtasks.exe','/DELETE','/TN', 'DB_AutoBackup', '/F']
			proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
			stdout_value = proc.stdout.read()
			drive = os.path.splitdrive(os.getcwd())
			command='schtasks /Create /SC daily /mo %s /TN DB_AutoBackup /ST 00:00 /TR "\\"%s\\Bell_HomeHub_Automation\\Bell_HomeHub_Automation_Libraries\\AutoBackUp.bat\\" %s'%(backup_period, drive[0] ,remoteBackUpPath)
			os.system(command)

if __name__ == "__main__":
	AutoRun(sys.argv[1])
	