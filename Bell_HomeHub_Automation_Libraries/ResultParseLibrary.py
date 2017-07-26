##########################################################################################################################################
# Description : ResultParseLibrary contains the methods to parse .csv Result files and enter the values from it to tables in results schema
# Developer   : Arijit Saha
# Date        : 17-July,2017
##########################################################################################################################################

#Import required python libraries
import pymysql
import SecureCopyLibrary
import Logger

# Parses the result files and inserts the values to database
def insertResult(srvr_details, result_test_id, throughput_multiplier, testname, mFolder):
	db = pymysql.connect(srvr_details[4],srvr_details[5],srvr_details[6],"results")
	cursor = db.cursor()	
	query_test_id = "SELECT test_type, direction, directory, date_ts FROM results.wifi_test_param_main WHERE test_id = '%s'" % (result_test_id)
	cursor.execute(query_test_id)
	result_test_type = cursor.fetchall()
	for rows in result_test_type:
		param_main_testType = rows[0]
		param_main_direction = rows[1]
		param_main_directory = rows [2]
		param_main_date = rows[3]
		
		# Code block for RR type test cases and Direction should be DownStream
		Logger.logMessage ("Fetching and parsing .csv files from Results for "+ testname + " Please wait, execution in progress.....")
		if (param_main_testType == 'RR' and param_main_direction == 'DS'):
			
			query_mcs_id = "SELECT mcs_id, mcs FROM results.wifi_test_param_mcs WHERE test_id = '%d'" % (result_test_id)
			cursor.execute(query_mcs_id)
			result_count = cursor.fetchall()
			for rows in result_count:
				mcs_val_id = rows[0]
				mcs_val = rows[1]
				if (len(result_count)>1):
					remote_directory = param_main_directory + "\\"+ param_main_date+"\\rate_vs_range_s2\\"+mFolder+"="+str(mcs_val)+"\\RateVsRange_S2\Results_rate_vs_range_s2.csv"
					local_directory = SecureCopyLibrary.getFileFromWaveServer(srvr_details[0], srvr_details[1], srvr_details[2], srvr_details[3], remote_directory.replace('\\','/'))
				else:
					remote_directory = param_main_directory + "\\"+ param_main_date+"\\rate_vs_range_s2\RateVsRange_S2\Results_rate_vs_range_s2.csv"
					local_directory = SecureCopyLibrary.getFileFromWaveServer(srvr_details[0], srvr_details[1], srvr_details[2], srvr_details[3], remote_directory.replace('\\','/'))
				with open(local_directory, 'r') as file:
					rr_result = []
					for row in file: 
						words = row.split(',')
						for x in words:
							if '-50' in x or '-60' in x or '-70' in x or '-80' in x or '-90' in x or '-100' in x:
								frame = int(words[0])
								
								query_frame_id = "SELECT framesize_id FROM results.wifi_test_param_framesize WHERE test_id = '%d' AND mcs_id = '%d' \
													AND framesize='%d'" % (result_test_id, mcs_val_id, frame)
								cursor.execute(query_frame_id)
								result_rr_frmeID = cursor.fetchone()[0]
								
								rr_result.append(float(words[11].strip('\n'))) #lossdB
								rr_result.append(float(words[7])) #oload
								rr_result.append(float(words[9])) #fRate
								rr_result.append(float(words[10])) #loss
								rr_result.append(result_rr_frmeID)
								rr_result.append(result_test_id)
								rr_result.append(mcs_val_id)
								
								query = "INSERT INTO wifi_results_rr(estimatedpathlossdB, groupoload_bps, forwardingrate_bps, frameloss_rate, framesize_id, test_id, mcs_id) \
											VALUES ('%f', '%f', '%f', '%f', '%d', '%d', '%d')" % (rr_result[0], rr_result[1], rr_result[2], rr_result[3], rr_result[4], \
											rr_result[5], rr_result[6])

								#execute SQL query using execute() method.
								cursor.execute(query)

								#Fetch a single row using fetchone() method.
								db.commit()
								
								del rr_result[:]
								
			param_main_folder = ""
				
		# Result parse and store script for MaxClient test type
		if (param_main_testType == 'MaxClient'):
			remote_directory = param_main_directory + "\\"+ param_main_date+"\\unicast_max_client_capacity\MaximumClientCapacity\Results_unicast_maximum_client_capacity.csv"
			local_directory = SecureCopyLibrary.getFileFromWaveServer(srvr_details[0], srvr_details[1], srvr_details[2], srvr_details[3], remote_directory.replace('\\','/'))
			
			query_mcs_id = "SELECT mcs_id, mcs FROM results.wifi_test_param_mcs WHERE test_id = '%d'" % (result_test_id)
			cursor.execute(query_mcs_id)
			result_count = cursor.fetchall()
			for rows in result_count:
				mcs_val_id = rows[0]
				mcs_val = rows[1]
	
			query_frame_id = "SELECT framesize_id, framesize FROM results.wifi_test_param_framesize WHERE test_id = '%d' AND mcs_id = '%d'" % (result_test_id, mcs_val_id)
			cursor.execute(query_frame_id)
			result_max_frmeID = cursor.fetchall()
			for rows in result_max_frmeID:
				frame_val_id = rows[0]
				frame_val = str(rows[1])
							
			with open(local_directory, 'r') as file:
				max_result = []
				for row in file: 
					words = row.split(',')
					for x in words:
						if frame_val in x :
							max_result.append(int(words[9].strip(' ')))
							max_result.append(frame_val_id)
							max_result.append(result_test_id)
							max_result.append(mcs_val_id)
							
							
							query = "INSERT INTO wifi_results_maxclient(no_of_clients, framesize_id, test_id, mcs_id) \
									VALUES ('%d', '%d', '%d', '%d')" % (max_result[0], max_result[1], max_result[2], max_result[3])

							#execute SQL query using execute() method.
							cursor.execute(query)

							#Fetch a single row using fetchone() method.
							db.commit()
								
							del max_result[:]
							
		if (param_main_testType == 'TP'):
			
			query_mcs_id = "SELECT mcs_id, mcs FROM results.wifi_test_param_mcs WHERE test_id = '%d'" % (result_test_id)
			cursor.execute(query_mcs_id)
			result_count = cursor.fetchall()
			for rows in result_count:
				mcs_val_id = rows[0]
				mcs_val = rows[1]
				
				if (len(result_count)>1):
					remote_directory = param_main_directory + "\\"+ param_main_date+"\\unicast_unidirectional_throughput\\"+mFolder+"="+str(mcs_val)+"\\Throughput\Results_unicast_throughput.csv"
					local_directory = SecureCopyLibrary.getFileFromWaveServer(srvr_details[0], srvr_details[1], srvr_details[2], srvr_details[3], remote_directory.replace('\\','/'))
				else:
					remote_directory = param_main_directory + "\\"+ param_main_date+"\\unicast_unidirectional_throughput\Throughput\Results_unicast_throughput.csv"
					local_directory = SecureCopyLibrary.getFileFromWaveServer(srvr_details[0], srvr_details[1], srvr_details[2], srvr_details[3], remote_directory.replace('\\','/'))
					
				query_frame_id = "SELECT framesize_id, framesize FROM results.wifi_test_param_framesize WHERE test_id = '%d' AND mcs_id = '%d'" % (result_test_id, mcs_val_id)
				cursor.execute(query_frame_id)
				result_max_frmeID = cursor.fetchall()
				for rows in result_max_frmeID:
					frame_val_id = rows[0]
					frame_val = str(rows[1])
					
					with open(local_directory, 'r') as file:
						tp_result = []
						for row in file: 
							words = row.split(',')
							for x in words:
								if frame_val == x :
									#if int(frame_val)==int(words[0]) and int(frame_val) not in  :
									tp_result.append(float(words[6].strip(' ')))
									tp_result.append(float(words[7].strip(' ')))
									tp_result.append(float(words[6].strip(' '))* float(throughput_multiplier))
									tp_result.append(frame_val_id)
									tp_result.append(result_test_id)
									tp_result.append(mcs_val_id)
									
									query = "INSERT INTO wifi_results_tp(throughput_pps, throughput_bps, threshold_throughput_pps, framesize_id, test_id, mcs_id) \
									VALUES ('%f', '%f', '%f', '%d', '%d', '%d')" % (tp_result[0], tp_result[1], tp_result[2], tp_result[3], tp_result[4], tp_result[5])

									#execute SQL query using execute() method.
									cursor.execute(query)

									#Fetch a single row using fetchone() method.
									db.commit()
									
									del tp_result[:]
				#print param_main_directory
				param_main_folder = ""
				
		if (param_main_testType == 'LAT'):
		
			query_mcs_id = "SELECT mcs_id, mcs FROM results.wifi_test_param_mcs WHERE test_id = '%d'" % (result_test_id)
			cursor.execute(query_mcs_id)
			result_count = cursor.fetchall()
			for rows in result_count:
				mcs_val_id = rows[0]
				mcs_val = rows[1]
				
				if (len(result_count)> 1):
					remote_directory = param_main_directory + "\\"+ param_main_date+"\\unicast_latency\\"+mFolder+"="+str(mcs_val)+"\\Latency\Results_unicast_latency.csv"
					local_directory = SecureCopyLibrary.getFileFromWaveServer(srvr_details[0], srvr_details[1], srvr_details[2], srvr_details[3], remote_directory.replace('\\','/'))
				else:
					remote_directory = param_main_directory + "\\"+ param_main_date+"\\unicast_latency\Latency\Results_unicast_latency.csv"
					local_directory = SecureCopyLibrary.getFileFromWaveServer(srvr_details[0], srvr_details[1], srvr_details[2], srvr_details[3], remote_directory.replace('\\','/'))
				query_frame_id = "SELECT framesize_id, framesize FROM results.wifi_test_param_framesize WHERE test_id = '%d' AND mcs_id = '%d'" % (result_test_id, mcs_val_id)
				cursor.execute(query_frame_id)
				result_max_frmeID = cursor.fetchall()
				for rows in result_max_frmeID:
					frame_val_id = rows[0]
					frame_val = str(rows[1])
					
					with open(local_directory, 'r') as file:
						tp_lat = []
						for row in file: 
							words = row.split(',')
							for x in words:
								if frame_val == x :
									tp_lat.append(float(words[4].strip(' ')))
									tp_lat.append(float(words[5].strip(' ')))
									tp_lat.append(float(words[6].strip(' ')))
									tp_lat.append(frame_val_id)
									tp_lat.append(result_test_id)
									tp_lat.append(mcs_val_id)
									
									query = "INSERT INTO wifi_results_lat(minimum_latency, maximum_latency, average_latency, framesize_id, test_id, mcs_id) \
									VALUES ('%f', '%f', '%f', '%d', '%d', '%d')" % (tp_lat[0], tp_lat[1], tp_lat[2], tp_lat[3], tp_lat[4], tp_lat[5])

									#execute SQL query using execute() method.
									cursor.execute(query)

									#Fetch a single row using fetchone() method.
									db.commit()
									
									del tp_lat[:]
				param_main_folder = ""
	db.close()	