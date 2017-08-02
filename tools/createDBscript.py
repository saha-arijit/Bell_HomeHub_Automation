import pymysql

def create_schema_master():		# method to create schema master
	#Open database connection to create SCHEMA
	dbconn = pymysql.connect("localhost","root","arijit",)
	#Create cursor for db connection
	cursorConn = dbconn.cursor()
	# Query to create master schema
	queryCreateMasterSchema = "CREATE SCHEMA master"
	# execute above query
	cursorConn.execute(queryCreateMasterSchema)
	#commit changes to DB
	dbconn.commit()
	#closing of connection
	dbconn.close()
	#calling method to create schema results
	create_schema_result()

def create_schema_result():			# method to create schema results
	#Open database connection to create SCHEMA
	dbconn = pymysql.connect("localhost","root","arijit",)
	#Create cursor for db connection
	cursorConn = dbconn.cursor()
	# Query to create results schema
	queryCreateMasterSchema = "CREATE SCHEMA results"
	#Execute above query to create schema results
	cursorConn.execute(queryCreateMasterSchema)
	dbconn.commit()
	dbconn.close()
	#calling method to create tables in master schema
	create_tables_master()
	
def create_tables_master():
	#Open database connection to create TABLES for master schema
	db = pymysql.connect("localhost","root","arijit","master")
	#Create cursor for db connection
	cursor = db.cursor()
	# Query to wifi_test_param_main table under create master schema
	queryParamMain = "CREATE TABLE wifi_test_param_main( \
	  `test_id` INT NOT NULL AUTO_INCREMENT, \
	  `date_ts` VARCHAR(45) NULL, \
	  `test_name` VARCHAR(45) NULL, \
	  `test_type` VARCHAR(45) NULL, \
	  `ssid` VARCHAR(45) NULL, \
	  `pw` VARCHAR(45) NULL, \
	  `directory` TEXT NULL, \
	  `ap` VARCHAR(45) NULL, \
	  `apver` VARCHAR(45) NULL, \
	  `direction` VARCHAR(45) NULL, \
	  `channel` INT NULL, \
	  `expectConn` VARCHAR(45) NULL, \
	  `source` VARCHAR(45) NULL, \
	  `destination` VARCHAR(45) NULL, \
	  `duration` INT NULL, \
	  `ss` INT NULL, \
	  `bw` INT NULL, \
	  `gi` VARCHAR(45) NULL, \
	  `eth_dut` VARCHAR(45) NULL, \
	  `w_dut` VARCHAR(45) NULL, \
	  `w_grouptype` VARCHAR(45) NULL, \
	  `test_duration` VARCHAR(45) NULL, \
	  PRIMARY KEY (`test_id`))"
	cursor.execute(queryParamMain)
	db.commit()

	# Query to wifi_test_param_loads table under create master schema
	queryParamLoads = "CREATE TABLE wifi_test_param_loads ( \
	  `loads_id` INT NOT NULL AUTO_INCREMENT, \
	  `loads` INT NOT NULL, \
	  `test_id` INT NOT NULL, \
	  PRIMARY KEY (`loads_id`))"
	cursor.execute(queryParamLoads)
	db.commit()

	# Query to wifi_test_param_mcs table under create master schema
	queryParamMcs = "CREATE TABLE wifi_test_param_mcs ( \
	  `mcs_id` INT NOT NULL AUTO_INCREMENT, \
	  `mcs` INT NOT NULL, \
	  `test_id` INT NOT NULL, \
	  PRIMARY KEY (`mcs_id`))"
	cursor.execute(queryParamMcs)
	db.commit()

	# Query to wifi_test_param_framesize table under create master schema
	queryParamFramesize = "CREATE TABLE wifi_test_param_framesize ( \
	  `framesize_id` INT NOT NULL AUTO_INCREMENT, \
	  `framesize` INT NOT NULL, \
	  `test_id` INT NOT NULL, \
	  `mcs_id` INT NOT NULL, \
	  PRIMARY KEY (`framesize_id`))"
	cursor.execute(queryParamFramesize)
	db.commit()

	# Query to wifi_results_maxclient table under create master schema
	queryResultMaxClient = "CREATE TABLE wifi_results_maxclient ( \
	  `maxclient_id` INT NOT NULL AUTO_INCREMENT, \
	  `no_of_clients` INT NULL, \
	  `framesize_id` INT NULL, \
	  `test_id` INT NULL, \
	  `mcs_id` INT NULL, \
	  PRIMARY KEY (`maxclient_id`))"
	cursor.execute(queryResultMaxClient)
	db.commit()

	# Query to wifi_results_rr table under create master schema
	queryResultRR = "CREATE TABLE wifi_results_rr ( \
	  `rr_id` INT NOT NULL AUTO_INCREMENT, \
	  `estimatedpathlossdB` INT NULL, \
	  `groupoload_bps` FLOAT NULL, \
	  `forwardingrate_bps` FLOAT NULL, \
	  `frameloss_rate` FLOAT NULL, \
	  `framesize_id` INT NULL, \
	  `test_id` INT NULL, \
	  `mcs_id` INT NULL, \
	  PRIMARY KEY (`rr_id`))"	 
	cursor.execute(queryResultRR)
	db.commit()
	  
	# Query to wifi_results_tp table under create master schema
	queryResultTP = "CREATE TABLE wifi_results_tp ( \
	  `tp_id` INT NOT NULL AUTO_INCREMENT, \
	  `throughput_pps` FLOAT NULL, \
	  `throughput_bps` FLOAT NULL, \
	  `threshold_throughput_pps` FLOAT NULL, \
	  `framesize_id` INT NULL, \
	  `test_id` INT NULL, \
	  `mcs_id` INT NULL, \
	  PRIMARY KEY (`tp_id`))" 
	cursor.execute(queryResultTP)
	db.commit()

	# Query to wifi_results_lat table under create master schema
	queryResultLat = "CREATE TABLE wifi_results_lat ( \
	  `lat_id` INT NOT NULL AUTO_INCREMENT, \
	  `minimum_latency` FLOAT NULL, \
	  `maximum_latency` FLOAT NULL, \
	  `average_latency` FLOAT NULL, \
	  `framesize_id` INT NULL, \
	  `test_id` INT NULL, \
	  `mcs_id` INT NULL, \
	  PRIMARY KEY (`lat_id`))"
	cursor.execute(queryResultLat)
	db.commit()

	# Query to wifi_project table under create master schema
	queryWifiProjct = "CREATE TABLE wifi_project ( \
	  `project_id` INT NOT NULL AUTO_INCREMENT, \
	  `project_name` VARCHAR(50) NULL, \
	  PRIMARY KEY (`project_id`))"
	cursor.execute(queryWifiProjct)
	db.commit()

	# Query to wifi_project_test table under create master schema
	queryWifiProjctTest = "CREATE TABLE wifi_project_test ( \
	  `project_id` INT NOT NULL, \
	  `test_id` INT NOT NULL )"
	cursor.execute(queryWifiProjctTest)
	db.commit()
	db.close()
	#calling method to create tables in results schema
	create_tables_result()
	
def create_tables_result():
	#Open database connection to CREATE TABLES for result schema
	db = pymysql.connect("localhost","root","arijit","results")
	#Create cursor for db connection
	cursor = db.cursor()

	# Query to wifi_test_param_main table under create results schema
	queryParamMain = "CREATE TABLE wifi_test_param_main( \
	  `test_id` INT NOT NULL AUTO_INCREMENT, \
	  `date_ts` VARCHAR(45) NULL, \
	  `test_name` VARCHAR(45) NULL, \
	  `test_type` VARCHAR(45) NULL, \
	  `ssid` VARCHAR(45) NULL, \
	  `pw` VARCHAR(45) NULL, \
	  `directory` TEXT NULL, \
	  `ap` VARCHAR(45) NULL, \
	  `apver` VARCHAR(45) NULL, \
	  `direction` VARCHAR(45) NULL, \
	  `channel` INT NULL, \
	  `expectConn` VARCHAR(45) NULL, \
	  `source` VARCHAR(45) NULL, \
	  `destination` VARCHAR(45) NULL, \
	  `duration` INT NULL, \
	  `ss` INT NULL, \
	  `bw` INT NULL, \
	  `gi` VARCHAR(45) NULL, \
	  `eth_dut` VARCHAR(45) NULL, \
	  `w_dut` VARCHAR(45) NULL, \
	  `w_grouptype` VARCHAR(45) NULL, \
	  `test_duration` VARCHAR(45) NULL, \
	  PRIMARY KEY (`test_id`))"
	cursor.execute(queryParamMain)
	db.commit()

	# Query to wifi_test_param_loads table under create results schema
	queryParamLoads = "CREATE TABLE wifi_test_param_loads ( \
	  `loads_id` INT NOT NULL AUTO_INCREMENT, \
	  `loads` INT NOT NULL, \
	  `test_id` INT NOT NULL, \
	  PRIMARY KEY (`loads_id`))"
	cursor.execute(queryParamLoads)
	db.commit()

	# Query to wifi_test_param_mcs table under create results schema
	queryParamMcs = "CREATE TABLE wifi_test_param_mcs ( \
	  `mcs_id` INT NOT NULL AUTO_INCREMENT, \
	  `mcs` INT NOT NULL, \
	  `test_id` INT NOT NULL, \
	  PRIMARY KEY (`mcs_id`))"
	cursor.execute(queryParamMcs)
	db.commit()

	# Query to wifi_test_param_framesize table under create results schema
	queryParamFramesize = "CREATE TABLE wifi_test_param_framesize ( \
	  `framesize_id` INT NOT NULL AUTO_INCREMENT, \
	  `framesize` INT NOT NULL, \
	  `test_id` INT NOT NULL, \
	  `mcs_id` INT NOT NULL, \
	  PRIMARY KEY (`framesize_id`))"
	cursor.execute(queryParamFramesize)
	db.commit()

	# Query to wifi_results_maxclient table under create results schema
	queryResultMaxClient = "CREATE TABLE wifi_results_maxclient ( \
	  `maxclient_id` INT NOT NULL AUTO_INCREMENT, \
	  `no_of_clients` INT NULL, \
	  `framesize_id` INT NULL, \
	  `test_id` INT NULL, \
	  `mcs_id` INT NULL, \
	  PRIMARY KEY (`maxclient_id`))"
	cursor.execute(queryResultMaxClient)
	db.commit()

	# Query to wifi_results_rr table under create results schema
	queryResultRR = "CREATE TABLE wifi_results_rr ( \
	  `rr_id` INT NOT NULL AUTO_INCREMENT, \
	  `estimatedpathlossdB` INT NULL, \
	  `groupoload_bps` FLOAT NULL, \
	  `forwardingrate_bps` FLOAT NULL, \
	  `frameloss_rate` FLOAT NULL, \
	  `framesize_id` INT NULL, \
	  `test_id` INT NULL, \
	  `mcs_id` INT NULL, \
	  PRIMARY KEY (`rr_id`))"
	cursor.execute(queryResultRR)
	db.commit()

	# Query to wifi_results_tp table under create results schema
	queryResultTP = "CREATE TABLE wifi_results_tp ( \
	  `tp_id` INT NOT NULL AUTO_INCREMENT, \
	  `throughput_pps` FLOAT NULL, \
	  `throughput_bps` FLOAT NULL, \
	  `threshold_throughput_pps` FLOAT NULL, \
	  `framesize_id` INT NULL, \
	  `test_id` INT NULL, \
	  `mcs_id` INT NULL, \
	  PRIMARY KEY (`tp_id`))"
	cursor.execute(queryResultTP)
	db.commit()
	
	# Query to wifi_results_lat table under create results schema
	queryResultLat = "CREATE TABLE wifi_results_lat ( \
	  `lat_id` INT NOT NULL AUTO_INCREMENT, \
	  `minimum_latency` FLOAT NULL, \
	  `maximum_latency` FLOAT NULL, \
	  `average_latency` FLOAT NULL, \
	  `framesize_id` INT NULL, \
	  `test_id` INT NULL, \
	  `mcs_id` INT NULL, \
	  PRIMARY KEY (`lat_id`));"
	cursor.execute(queryResultLat)
	db.commit()
	
	db.close()
	#calling method to create views for master schema
	create_views_master()

def create_views_master(): # method to create views under master schema

	#Open database connection to create VIEWS for master schema
	db = pymysql.connect("localhost","root","arijit","master")
	#Create cursor for db connection
	cursor = db.cursor()
	# Query to create wifi_test_param_view under master schema
	queryMasterViewMain = "CREATE VIEW `wifi_test_param_view` AS \
		SELECT main.test_id, project_id, test_name, test_type, ssid, pw, directory, ap, apver, direction, channel, framesize, loads, \
		expectConn, source, destination, duration, mcs, ss, bw, gi, eth_dut, w_dut, w_grouptype, test_duration FROM wifi_test_param_main AS main \
		JOIN wifi_test_param_mcs AS p_mcs ON main.test_id = p_mcs.test_id \
		LEFT JOIN wifi_test_param_loads AS p_loads ON main.test_id = p_loads.test_id \
		JOIN wifi_test_param_framesize AS p_frames ON p_mcs.mcs_id = p_frames.mcs_id \
		JOIN wifi_project_test AS pj_test ON main.test_id = pj_test.test_id \
		ORDER BY test_id, mcs, loads, framesize DESC"
	cursor.execute(queryMasterViewMain)
	db.commit()
	# Query to create wifi_results_tp_view under master schema
	queryMstrViewTP = "CREATE VIEW `wifi_results_tp_view` AS \
		SELECT r_tp.test_id, p_main.test_name, project_id, mcs, framesize, throughput_pps, throughput_bps, threshold_throughput_pps FROM wifi_results_tp AS r_tp \
		JOIN wifi_test_param_mcs AS p_mcs ON p_mcs.mcs_id = r_tp.mcs_id \
		JOIN wifi_test_param_framesize as p_frames ON p_frames.framesize_id = r_tp.framesize_id \
		JOIN wifi_test_param_main AS p_main ON p_main.test_id = r_tp.test_id \
		JOIN wifi_project_test AS pj_test ON r_tp.test_id = pj_test.test_id"
	cursor.execute(queryMstrViewTP)
	db.commit()
	# Query to create wifi_results_lat_view under master schema
	queryMstrViewLAT = "CREATE VIEW `wifi_results_lat_view` AS \
		SELECT r_lat.test_id, p_main.test_name, project_id, date_ts, mcs, framesize, minimum_latency, maximum_latency, average_latency \
		FROM wifi_results_lat AS r_lat \
		JOIN wifi_test_param_mcs AS p_mcs ON p_mcs.mcs_id = r_lat.mcs_id \
		JOIN wifi_test_param_framesize as p_frames ON p_frames.framesize_id = r_lat.framesize_id \
		JOIN wifi_test_param_main as p_main ON p_main.test_id = r_lat.test_id \
		JOIN wifi_project_test AS pj_test ON r_lat.test_id = pj_test.test_id"
	cursor.execute(queryMstrViewLAT)
	db.commit()
	# Query to create wifi_results_rr_view under master schema
	queryMstrViewRR = "CREATE VIEW `wifi_results_rr_view` AS \
		SELECT r_rr.test_id, p_main.test_name, project_id, date_ts, mcs, framesize, estimatedpathlossdB, groupoload_bps, forwardingrate_bps, frameloss_rate \
		FROM wifi_results_rr AS r_rr \
		JOIN wifi_test_param_mcs AS p_mcs ON p_mcs.mcs_id = r_rr.mcs_id \
		JOIN wifi_test_param_framesize as p_frames ON p_frames.framesize_id = r_rr.framesize_id \
		JOIN wifi_test_param_main as p_main ON p_main.test_id = r_rr.test_id \
		JOIN wifi_project_test AS pj_test ON r_rr.test_id = pj_test.test_id"
	cursor.execute(queryMstrViewRR)
	db.commit()
	# Query to create wifi_results_maxclient_view table under master schema
	queryMstrViewMax = "CREATE VIEW `wifi_results_maxclient_view` AS \
		SELECT r_max.test_id, p_main.test_name, project_id, date_ts, mcs, framesize, no_of_clients FROM wifi_results_maxclient AS r_max \
		JOIN wifi_test_param_mcs AS p_mcs ON p_mcs.mcs_id = r_max.mcs_id \
		JOIN wifi_test_param_framesize as p_frames ON p_frames.framesize_id = r_max.framesize_id \
		JOIN wifi_test_param_main as p_main ON p_main.test_id = r_max.test_id \
		JOIN wifi_project_test as pj_test ON r_max.test_id = pj_test.test_id"
	cursor.execute(queryMstrViewMax)
	db.commit()
	db.close()
	#calling method to create views for results schema
	create_views_result()

def create_views_result(): 
	#Open database connection to create VIEWS for result schema
	db = pymysql.connect("localhost","root","arijit","results")
	#Create cursor for db connection
	cursor = db.cursor()
	# Query to create wifi_test_param_view under results schema
	queryRsltViewMain = "CREATE VIEW `wifi_test_param_view` AS \
			SELECT main.test_id, date_ts, test_name, test_type, ssid, pw, directory, ap, apver, direction, channel, framesize, loads, \
			expectConn, source, destination, duration, mcs, ss, bw, gi, eth_dut, w_dut, w_grouptype, test_duration FROM results.wifi_test_param_main AS main \
			 JOIN results.wifi_test_param_mcs AS p_mcs ON main.test_id = p_mcs.test_id \
			 LEFT JOIN results.wifi_test_param_loads AS p_loads ON main.test_id = p_loads.test_id \
			 JOIN results.wifi_test_param_framesize AS p_frames ON p_mcs.mcs_id = p_frames.mcs_id \
			 ORDER BY test_id, mcs, loads, framesize DESC"
	cursor.execute(queryRsltViewMain)
	db.commit()
	# Query to create wifi_results_tp_view under results schema
	queryRsltViewTP = "CREATE VIEW `wifi_results_tp_view` AS \
			SELECT r_tp.test_id, p_main.test_name, date_ts, mcs, framesize, throughput_pps, throughput_bps, threshold_throughput_pps FROM results.wifi_results_tp AS r_tp \
			 JOIN wifi_test_param_mcs AS p_mcs ON p_mcs.mcs_id = r_tp.mcs_id \
			 JOIN wifi_test_param_framesize as p_frames ON p_frames.framesize_id = r_tp.framesize_id \
			 JOIN wifi_test_param_main as p_main ON p_main.test_id = r_tp.test_id"
	cursor.execute(queryRsltViewTP)
	db.commit()
	# Query to create wifi_results_lat_view under results schema
	queryRsltViewLAT = "CREATE VIEW `wifi_results_lat_view` AS \
			SELECT r_lat.test_id, p_main.test_name, date_ts, mcs, framesize, minimum_latency, maximum_latency, average_latency \
			 FROM wifi_results_lat AS r_lat \
			 JOIN wifi_test_param_mcs AS p_mcs ON p_mcs.mcs_id = r_lat.mcs_id \
			 JOIN wifi_test_param_framesize as p_frames ON p_frames.framesize_id = r_lat.framesize_id \
			 JOIN wifi_test_param_main as p_main ON p_main.test_id = r_lat.test_id"
	cursor.execute(queryRsltViewLAT)
	db.commit()
	# Query to create wifi_results_rr_view under results schema
	queryRsltViewRR = "CREATE VIEW `wifi_results_rr_view` AS \
			SELECT r_rr.test_id, p_main.test_name, date_ts, mcs, framesize, estimatedpathlossdB, groupoload_bps, forwardingrate_bps, frameloss_rate \
			 FROM wifi_results_rr AS r_rr \
			 JOIN wifi_test_param_mcs AS p_mcs ON p_mcs.mcs_id = r_rr.mcs_id \
			 JOIN wifi_test_param_framesize as p_frames ON p_frames.framesize_id = r_rr.framesize_id \
			 JOIN wifi_test_param_main as p_main ON p_main.test_id = r_rr.test_id"
	cursor.execute(queryRsltViewRR)
	db.commit()
	# Query to create wifi_results_maxclient_view under results schema
	queryRsltViewMax = "CREATE VIEW `wifi_results_maxclient_view` AS \
			SELECT r_max.test_id, p_main.test_name, date_ts, mcs, framesize, no_of_clients FROM results.wifi_results_maxclient AS r_max \
			 JOIN wifi_test_param_mcs AS p_mcs ON p_mcs.mcs_id = r_max.mcs_id \
			 JOIN wifi_test_param_framesize as p_frames ON p_frames.framesize_id = r_max.framesize_id \
			 JOIN wifi_test_param_main as p_main ON p_main.test_id = r_max.test_id"
	cursor.execute(queryRsltViewMax)
	db.commit()
	db.close()

if __name__ == '__main__': #main method to start execution of program
	create_schema_master()	# calling method to create master schema

