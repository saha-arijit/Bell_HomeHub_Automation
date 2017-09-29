import logging
import sys
import os
import time
from robot.libraries.BuiltIn import BuiltIn
import inspect
	
def logMessage(message):
	
	root = logging.getLogger()
	root.setLevel(logging.INFO)
	ch = logging.StreamHandler(sys.stdout)
	ch.setLevel(logging.INFO)
	#root.addHandler(ch)
	logging.info(message)
	
def logBackup(message):
	
	LOG_FILENAME = "C:\\Bell_HomeHub_Automation\\Bell_HomeHub_Automation_Results\\Backup"+time.strftime("%Y%m%d-%H%M%S",time.localtime())+".log"
	root = logging.basicConfig(filename=LOG_FILENAME, filemode='w',level=logging.INFO)
	ch = logging.StreamHandler(sys.stdout)
	ch.setLevel(logging.INFO)
	#root.addHandler(ch)
	logging.info(message)

def CreateLogFile(message):
    
    srcReportDir = BuiltIn().replace_variables('${OUTPUTDIR}')
    #logFileName = os.path.join(srcReportDir,"detailedLog_" +tStamp+ ".log")
    LOG_FILENAME = os.path.join(srcReportDir,"DetailedLog_"+time.strftime("%Y%m%d",time.localtime())+".log")
    logger = logging.getLogger()
    logFileHandler = logging.FileHandler(LOG_FILENAME)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    logFileHandler.setFormatter(formatter)
    logger.addHandler(logFileHandler)
    return logger

def messageLog(message):

    func = inspect.currentframe().f_back.f_code
    filename = func.co_filename.split('\\')
    #logging.info("%s: %s in %s:%i" % (
    logging.info("%s -> %s :: %s" % ( 
        filename[3], 
        func.co_name,
        message
        #func.co_firstlineno
    ))

def errorLog(message):

    func = inspect.currentframe().f_back.f_code
    filename = func.co_filename.split('\\')
    #logging.info("%s: %s in %s:%i" % (
    logging.error("%s -> %s :: %s" % ( 
        filename[3], 
        func.co_name,
        message
        #func.co_firstlineno
    ))