############################################################################################################################
# Description : MySQLCopy contains the function to create a copy of the data from the results database to the Master database.
# Developer   : Anherudh Kamath
# Date        : 6-July,2017
############################################################################################################################
#Import required python libraries
import pymysql
import sys
import subprocess
import Logger

# MySQL database details for the results and master database for the copy to be done. 
# Make sure below user have appropriate privileges to take databases backup.

def DBParams(var_dbhostname, var_dbusername, var_dbpassword):
	global hostname, username, password
	hostname = var_dbhostname
	username = var_dbusername
	password = var_dbpassword
	
def MySQL_Copy(project_name, test_id):
	if len(project_name) <= 0 :
		raise Exception ("Project Name cannot be left blank.")
	Logger.logMessage("Starting the MySQL Copy Script")
	"""
	Function Name        : MySQLCopy
	Function Description : Copies the data from the results database to the master database for specific test_id
	Inputs   : 
		username                    - UserName to login to the database
		password					- Password to login to the database
		test_id						- Test ID for which the data needs to be copied from the results database to master database
		host						- Hostname or ip address of the system where the databases are hosted. By default the databse would be on the localhost
	Outputs  : returns True if the data has been successfully copied. Else returns False
	"""
	tablesResults = ['wifi_results_lat','wifi_results_maxclient','wifi_results_rr','wifi_results_tp','wifi_test_param_framesize','wifi_test_param_loads','wifi_test_param_main','wifi_test_param_mcs']
	tablesMaster = ['wifi_project','wifi_project_test','wifi_results_lat','wifi_results_maxclient','wifi_results_rr','wifi_results_tp','wifi_test_param_framesize','wifi_test_param_loads','wifi_test_param_main','wifi_test_param_mcs']
	
	#Open database connection to CREATE TABLES for result schema
	db = pymysql.connect(hostname,username,password,"results")
	#Create cursor for db connection
	cursor = db.cursor()
	Logger.logMessage("Inserting Project Name into table")
	
	#Check for no duplicate entry
	query_test_id = "SELECT project_id FROM master.wifi_project WHERE project_name = '%s'" % (project_name)
	cursor.execute(query_test_id)
	if cursor.fetchone() is None: 
		query = "INSERT INTO master.wifi_project(project_name) VALUES ('%s')" % (project_name)	
		
		#execute SQL query using execute() method.
		cursor.execute(query)
		#Fetch a single row using fetchone() method.
		db.commit()
		
		# Check whether the entered test_id exists in the wifi_test_param_main table in results schema
		query_test_id = "SELECT test_id FROM results.wifi_test_param_main WHERE test_id = '%s'" % (test_id)
		cursor.execute(query_test_id)
		if cursor.fetchone() is None :
			# Raise exception when the test_id entered is not present in wifi_test_param_main table
			raise Exception ("Data related to given Test ID: "+test_id+" does not exist.")
		else:		
			#Query to fetch project_id for the project name inserted
			query_test_id = "SELECT project_id FROM master.wifi_project WHERE project_name = '%s'" % (project_name)
			
			cursor.execute(query_test_id)
			result_proj_id = cursor.fetchone()[0]
			
			Logger.logMessage ("Inserting project id and test id into table") 
			query = "INSERT INTO master.wifi_project_test(project_id, test_id) VALUES ('%d', '%d')" % (result_proj_id, int(test_id))	
			
			#execute SQL query using execute() method.
			cursor.execute(query)
			#Fetch a single row using fetchone() method.
			db.commit()
	else :
		Logger.logMessage ("Project Name is already present")
		
		# Check whether the entered test_id exists in the wifi_test_param_main table in results schema
		query_test_id = "SELECT test_id FROM results.wifi_test_param_main WHERE test_id = '%s'" % (test_id)
		cursor.execute(query_test_id)
		if cursor.fetchone() is None :
			# Raise exception when the test_id entered is not present in wifi_test_param_main table
			raise Exception ("Data related to given Test ID: "+test_id+" does not exist.")
		else:	
			#Query to fetch project_id for the project name inserted
			query_test_id = "SELECT project_id FROM master.wifi_project WHERE project_name = '%s'" % (project_name)
			
			cursor.execute(query_test_id)
			result_proj_id = cursor.fetchone()[0]
			
			Logger.logMessage ("Inserting project id and test id into table") 
			query = "REPLACE INTO master.wifi_project_test(project_id, test_id) VALUES ('%d', '%d')" % (result_proj_id, int(test_id))	
			
			#execute SQL query using execute() method.
			cursor.execute(query)
			#Fetch a single row using fetchone() method.
			db.commit()
		
	Logger.logMessage ("Extracting values for Test ID " + test_id + " from tables.")
	for i in tablesResults:
		table = i
		#stdout =open('mysql_data.log', 'w')
		cursor.execute("SELECT * FROM results."+table+" WHERE test_id="+test_id+";")
	
	Logger.logMessage ("Data successfully copied from Results table to Master table for Test ID "+ test_id)
	for i in tablesResults:
		table = i
		#stdout = open('mysql_data.log', 'w')
		querycopyMySQL = "REPLACE master."+table+ " SELECT * FROM results."+table+" WHERE test_id="+test_id+""
		output = cursor.execute(querycopyMySQL)
		db.commit()
	db.close()