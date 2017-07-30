################################################################################################################################
# Description : BatParseLibrary contains the methods to parse .bat files and enter the values from it to tables in results schema
# Developer   : Arijit Saha
# Date        : 17-July,2017
################################################################################################################################

#Import required python libraries
import pymysql
import SecureCopyLibrary
import ResultParseLibrary
import Logger

#Inserting the Params values
def insertParams(srvr_details, params, date, testDuration):
	#Open database connection
	db = pymysql.connect(srvr_details[4],srvr_details[5],srvr_details[6],"results")
	#prepare a cursor object using cursor() method
	cursor = db.cursor()
	query = "INSERT INTO wifi_test_param_main(date_ts, test_name, test_type, ssid, pw, directory, ap , apver, direction, channel, expectConn, source, destination, \
		 duration, ss, bw, gi, eth_dut, w_dut, w_grouptype, test_duration) \
		 VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s', '%s', '%s', '%d', '%d', '%d', '%s', '%s', '%s', '%s', '%d')" % \
		 (date, params[0], params[1], params[2], params[3], params[4].replace('\\', '\\\\'), params[6], params[7], params[5], int(params[8]), params[9], params[10], \
		 params[11], int(params[12]), int(params[13]), int(params[14]), params[15], params[16], params[17], params[18], int(testDuration))
		
	#execute SQL query for inserting values                                  #change above after d
	cursor.execute(query)
	#commit changes made to database after inserting values
	db.commit()
	#disconnect from server
	db.close()

# Inserting the Mcs values	
def insertMcs(srvr_details, mcs, params, date):
	#Open database connection
	db = pymysql.connect(srvr_details[4],srvr_details[5],srvr_details[6],"results")
	#prepare a cursor object using cursor() method
	cursor = db.cursor()		
	query_test_id = "SELECT test_id FROM results.wifi_test_param_main WHERE test_name = '%s' AND direction = '%s' AND date_ts='%s'" % \
					(params[0] , params[5], date)
	
	#execute SQL query for fetching test_id
	cursor.execute(query_test_id)
	result_test_id = str(cursor.fetchone()[0])
	for i in range(len(mcs)):
		query = "INSERT INTO wifi_test_param_mcs(mcs, test_id) \
					VALUES ('%d', '%d')" % (int(mcs[i]), int(result_test_id))
		
		#execute SQL query for inserting values			
		cursor.execute(query)
		
		#commit changes made to database after inserting values
		db.commit()
	db.close()

# Inserting the loads values
def insertLoads(srvr_details, loads, params, date):
	#Open database connection
	db = pymysql.connect(srvr_details[4],srvr_details[5],srvr_details[6],"results")
	#prepare a cursor object using cursor() method
	cursor = db.cursor()		
	query_test_id = "SELECT test_id FROM results.wifi_test_param_main WHERE test_name = '%s' AND direction = '%s' AND date_ts='%s'" % \
					(params[0] , params[5], date)
	
	#execute SQL query for fetching test_id
	cursor.execute(query_test_id)
	result_test_id = str(cursor.fetchone()[0])
	for i in range(len(loads)):
		query = "INSERT INTO wifi_test_param_loads(loads, test_id) \
					VALUES ('%d', '%d')" % (int(loads[i]), int(result_test_id))
		
		#execute SQL query for inserting values
		cursor.execute(query)
		
		#commit changes made to database after inserting values
		db.commit()
	db.close()	

# Inserting the framesize values	
def insertFrames(srvr_details, frames, params, throughput_multiplier, testname, mFolder, date):
	#Open database connection
	db = pymysql.connect(srvr_details[4],srvr_details[5],srvr_details[6],"results")
	#prepare a cursor object using cursor() method
	cursor = db.cursor()		
	query_test_id = "SELECT test_id FROM results.wifi_test_param_main WHERE test_name = '%s' AND direction = '%s' AND date_ts='%s'" % \
					(params[0] , params[5], date)
	
	#execute SQL query to fetch test_id
	cursor.execute(query_test_id)
	result_test_id = cursor.fetchone()[0]
	query_mcs_id = "SELECT mcs_id FROM results.wifi_test_param_mcs WHERE test_id = '%d'" % (result_test_id)
	
	#execute SQL query to fetch mcs_id
	cursor.execute(query_mcs_id)
	result_count = cursor.fetchall()
	for rows in result_count:
		for i in range(len(frames)):
			query_frames = "INSERT INTO wifi_test_param_framesize(framesize, test_id, mcs_id) \
							VALUES ('%d','%d','%d')" % (int(frames[i]), result_test_id, int(rows[0]))
			
			#execute SQL query for inserting values
			cursor.execute(query_frames)
			
			#commit changes made to database after inserting values
			db.commit()
	db.close()
	Logger.logMessage ("Completed inserting data into Frames table for " + testname)
	Logger.logMessage ("Starting to parse Results folder for " + testname)
	
	"""
	Calling method "insertResult" from ResultParseLibrary to insert data into results tables
	Parameters passed :
		srvr_details			- Server details as list for Database connection details.
		result_test_id			- Test ID that has been fetched from wifi_test_param_main for foreign key reference in Results tables
		throughput_multiplier 	- Throughput multipler value valid for TP test cases only.
		testname 				- Name of the test case being executed.
	"""
	ResultParseLibrary.insertResult(srvr_details, result_test_id, throughput_multiplier, testname, mFolder)

"""
Calling method "parseBatFile" to parse the values from .bat file
Parameters passed :
	srvr_details			- Server details as list for Database connection details.
	testname 				- Name of the test case being executed.
	direction				- Downstream/ Upstream value for the test case
	date					- Date which has timestamp value
	throughput_multiplier 	- Throughput multipler value valid for TP test cases only.
	filename				- filepath for the .bat file
"""
def parseBatFile(srvr_details, testname, direction, date, throughput_multiplier, filename, testDuration):
	with open(filename, 'r') as file:
		params = []
		for line in file:
			words = line.split(',')
			for x in words:
				if 'AC' in x and x.startswith('::') or 'N' in x and x.startswith('::'):
					params.append(x[2:].strip('\n')) 
					if 'AC' in x:
						mFolder = "VhtDataMcs"
					if 'N' in x: 
						mFolder = "DataMcsIndex"
				if 'TP.tcl' in x:
					params.append('TP')
				if 'Lat.tcl' in x:
					params.append('LAT')
				if 'RR.tcl' in x:
					params.append('RR')
				if 'MaxClient.tcl' in x:
					params.append('MaxClient')
				if 'ssid' in x:
					ssid = x.split()
					params.append(ssid[2].strip('"'))
					continue									# Move out of the interation because the condition "ss" will be as it will as both "ssid" field and "ss" field contains the "ss" 
				if 'pw'in x:
					pw = x.split()
					params.append(pw[2].strip('"'))
				if 'save' in x:
					save = x.split()
					params.append(save[2].strip('"'))
					params.append(save[2].strip('" ')[-2:])
				if 'ap' in x:
					ap = x.split()
					params.append(ap[2].strip('"'))
					continue
				if 'apver' in x:
					apver = x.split()
					params.append(apver[2].strip('"'))
				if 'channel' in x:
					channel = x.split()
					params.append(channel[2].strip('"'))
				if 'expectConn' in x:
					eConn = x.split()
					params.append(eConn[2].strip('"'))
				if 'source' in x:
					source = x.split()
					params.append(source[2].strip('"'))
				if 'destination' in x:
					destination = x.split()
					params.append(destination[2].strip('"'))
				if 'duration' in x:
					duration = x.split()
					params.append(duration[2].strip('"'))
				if 'ss' in x:
					ss = x.split()
					params.append(ss[2].strip('"'))
				if 'bw' in x:
					bw = x.split()
					params.append(bw[2].strip('"'))
				if 'gi' in x:
					gi = x.split()
					params.append(gi[2].strip('"'))
				if 'eth_dut' in x:
					eth_dut = x.split()
					params.append(eth_dut[2].strip('"'))
				if 'w_dut' in x:
					w_dut = x.split()
					params.append(w_dut[2].strip('"'))
				if 'w_grouptype' in x:
					w_grouptype = x.split()
					params.append(w_grouptype[2].strip('"'))
				if 'frameSize' in x:
					frameSize = x.split()
					frames = []   						 # initialize list for storing the frameSize values, Then the list will be iterated to insert data into DB
					for i in range(len(frameSize)):
						if frameSize[i] != '--var' and frameSize[i] != 'frameSize' and frameSize[i] != '^' and frameSize[i] != ' "':
							if frameSize[i].strip('"') != '':
								frames.append(frameSize[i].strip('" '))				# "frameSize" data value to be inserted into DB field after extracting the "test_id" for each test case		
				if 'mcs' in x:
					mcs_val = x.split()
					mcs = []							# initialize list for storing the mcs values, Then the list will be iterated to insert data into DB
					for i in range(len(mcs_val)):
						if mcs_val[i] != '--var' and mcs_val[i] != 'mcs' and mcs_val[i] != '^' and mcs_val[i] != ' "':
							if mcs_val[i].strip('"') != '':
								mcs.append(mcs_val[i].strip('" '))                # "mcs" data value to be inserted into DB field after extracting the "test_id" for each test case
				if 'loads' in x: 
					loads_val = x.split()
					loads = []							# initialize list for storing the loads values, Then the list will be iterated to insert data into DB
					for i in range(len(loads_val)):
						if loads_val[i] != '--var' and loads_val[i] != 'loads' and loads_val[i] != '^' and loads_val[i] != ' "':
							if loads_val[i].strip('"') != '':
								loads.append(loads_val[i].strip('"'))				# "loads" data value to be inserted into DB field after extracting the "test_id" for each test case
				if 'AC' not in x and x.startswith('::') and 'N' not in x and x.startswith('::'):
					if (params[0] == testname and params[5] == direction):
						"""
						Calling method "insertParams" to insert data into wifi_test_param_main table
						Parameters passed :
							srvr_details	- Server details as list for Database connection details
						 	params			- Parameters parsed from .bat file as list,
							date			- Date which has timestamp value
						"""
						Logger.logMessage ("Inserting data into Params Main table for " + testname)
						insertParams(srvr_details, params, date, testDuration)
						Logger.logMessage ("Completed inserting data into Params Main table for " + testname)
						
						"""
						Calling method "insertMcs"to insert data into wifi_test_param_mcs table
						Parameters passed :
							srvr_details	- Server details as list for Database connection details
							mcs 			- MCS values as list for the particular test
						 	params			- Parameters parsed from .bat file as list,
						"""
						Logger.logMessage ("Inserting data into MCS table for " + testname)
						insertMcs(srvr_details, mcs, params, date)
						Logger.logMessage ("Completed inserting data into MCS table for " + testname)
						
						"""
						Calling method "insertLoads" to insert data into wifi_test_param_loads table
						Parameters passed :
							srvr_details	- Server details as list for Database connection details
							loads 			- Loads values as list for the particular test
						 	params			- Parameters parsed from .bat file as list
						"""
						if len(loads) > 0:
							Logger.logMessage ("Inserting data into Loads tables for " + testname)
							insertLoads(srvr_details, loads, params, date)
							Logger.logMessage ("Completed inserting data into Loads table for " + testname)
							
						"""
						Calling method "insertFrames" to insert data into wifi_test_param_framesize table
						Parameters passed :
							srvr_details			- Server details as list for Database connection details.
							frames 					- Frames values as list for the particular test.
						 	params					- Parameters parsed from .bat file as list.
							throughput_multiplier 	- Throughput multipler value valid for TP test cases only.
							testname 				- Name of the test case being executed.
						"""	
						Logger.logMessage ("Inserting data into Frames tables for " + testname)	
						insertFrames(srvr_details, frames, params, throughput_multiplier, testname, mFolder, date)
						Logger.logMessage ("Completed parsing of .csv files of Results and values inserted to table for " + testname)	
						Logger.logMessage ("Moving to next test case")
					del params[:]
					
					continue