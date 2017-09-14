import os
import pymysql

### EXAMPLE VALUES.........   THE ACTUAL VALUES TO BE PASSED TO getpps() method as arguments
test_name   = 'AC-TP-80MHz4'
direction   = 'DS'
timestamp   = '20170519-122527'
mcs         = [9]    # running for one mcs at a time
frame_size  = [1518, 1024, 512, 64]

# Set the path location of the userconfig.txt file
drive = os.path.splitdrive(os.getcwd())
ConfigFilePath = drive[0]+"\Bell_HomeHub_Automation\Bell_HomeHub_Automation\userconfig.txt"

def SetUserConfig():
    global dbhostname, dbusername, dbpassword
    configFile = open(ConfigFilePath, 'r')
    content = configFile.read()
    lines = content.split("\n")
    for eachline in lines:
        #print eachline
        str = eachline
        #print str.find("var_ssid_in}")
        if (str.find("var_dbusername}")>0):
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
        elif (str.find("var_dbhostname}")>0):
            start = str.index("}")
            end = str.index("#")
            substr = str[start+1:end]
            substr = substr.replace(" ","")
            substr.strip()
            dbhostname = substr

"""
Calling method "getpps" to fetch the loads values for .bat files
Parameters passed :
    testname        - Name of the test case being executed.
    direction       - Downstream/ Upstream value for the test case
    timestamp       - Date which has timestamp value
    mcs             - MCS values as list.
    frame_size      - Frames values as list. 
"""
#def getpps(test_name, direction, timestamp, mcs, frame_size):
def getpps(test_id, mcs, frame_size):

    SetUserConfig()
    print("In GetPPS function")
    
    #this will have the loads values to be inserted into .bat file
    loads = []

    #this will store the other pps values
    other_loads = []

    db = pymysql.connect(dbhostname, dbusername, dbpassword,"results")
    cursor = db.cursor()
    # fetching the test_id from the given test name
    #query_test_id = "SELECT test_id FROM results.wifi_test_param_main WHERE test_name = '%s' AND direction = '%s' AND date_ts = '%s'" % \
    #               (test_name , direction, timestamp)
    
    #execute SQL query for fetching test_id
    #cursor.execute(query_test_id)
    #result_test_id = cursor.fetchone()[0]
    result_test_id = int(test_id)

    for mcs_val in mcs :
        #mcs_val = int(mcs_val)
        # fetching the mcs_id from the given mcs for fetched test_id
        query_mcs_id = "SELECT mcs_id FROM results.wifi_test_param_mcs WHERE test_id = '%d' AND mcs = '%d'" % (result_test_id, int(mcs_val))
        cursor.execute(query_mcs_id)
        result_mcs_id = cursor.fetchone()[0]

        for frames in frame_size :

            #frames = int(frames)
            # fetching the frame_size_id from the given frame_size for particular mcs for fetched test_id
            query_frame_id = "SELECT framesize_id FROM results.wifi_test_param_framesize WHERE test_id = '%d' AND mcs_id = '%d' AND framesize = '%d'" % \
                            (result_test_id, result_mcs_id, int(frames))
            cursor.execute(query_frame_id)
            result_max_frmeID = cursor.fetchone()[0]
            
            # fetching the threshold_throughout_pps value for each framesize, for each mcs, for each test_id    
            query_frame_id = "SELECT threshold_throughput_pps FROM results.wifi_results_tp WHERE test_id = '%d' AND mcs_id = '%d' AND framesize_id = '%d'" % \
                            (result_test_id, result_mcs_id, result_max_frmeID)
            cursor.execute(query_frame_id)
            tt_pps = cursor.fetchone()[0]

            loads.append(tt_pps)    

    #pass this loads list to your code
    print loads
    return loads



## MAIN METHOD
if __name__ == '__main__':
    getpps(test_name, direction, timestamp, mcs, frame_size)

