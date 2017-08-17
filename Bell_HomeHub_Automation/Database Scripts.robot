*** Settings ***
Library           ../Bell_HomeHub_Automation_Libraries/StoreLibrary.py    # Library file for Store Result Script
Library           ../Bell_HomeHub_Automation_Libraries/BackupLibrary.py    # Library file for Backup Script
Library           ../Bell_HomeHub_Automation_Libraries/CopyLibrary.py    # Library file for Copy Script
Resource          userconfig.txt    # Global Variables

*** Variables ***

*** Test Cases ***
MySQL Store Result
    [Setup]    StoreLibrary.SCPDetails    ${var_wahostname}    ${var_waportnumber}    ${var_wausername}    ${var_wapassword}    ${var_dbhostname}
    ...    ${var_dbusername}    ${var_dbpassword}    # Get Details for SCP to Wave Automation Server
    Library Command    Test Name    Location of .bat file    Direction    Result TimeStamp    Throughput Multiplier
    MySQL_Store_Result    AC-TP-80MHz4    C:/IxVeriwave/automation4.6/automation/conf/H3000/HH3000-Rel1_2_3-auto_conf.bat    DS    20170519-122527    0.9
    MySQL_Store_Result    AC-TP-80MHz4    C:/IxVeriwave/automation4.6/automation/conf/H3000/HH3000-Rel1_2_3-auto_conf.bat    US    20170519-131317    0.9
    MySQL_Store_Result    AC-Lat-80MHz2    C:/IxVeriwave/automation4.6/automation/conf/H3000/HH3000-Rel1_2_3-auto_conf.bat    DS    20170519-142429    0
    MySQL_Store_Result    AC-Lat-80MHz2    C:/IxVeriwave/automation4.6/automation/conf/H3000/HH3000-Rel1_2_3-auto_conf.bat    US    20170519-143031    0
    MySQL_Store_Result    AC-RR-80MHz1    C:/IxVeriwave/automation4.6/automation/conf/H3000/HH3000-Rel1_2_3-auto_conf.bat    DS    20170519-143634    0
    MySQL_Store_Result    AC-RR-80MHz1    C:/IxVeriwave/automation4.6/automation/conf/H3000/HH3000-Rel1_2_3-auto_conf.bat    US    20170519-145030    0
    MySQL_Store_Result    AC-MaxClient-80MHz4    C:/IxVeriwave/automation4.6/automation/conf/H3000/HH3000-Rel1_2_3-auto_conf.bat    DS    20170519-145125    0
    MySQL_Store_Result    AC-MaxClient-80MHz4    C:/IxVeriwave/automation4.6/automation/conf/H3000/HH3000-Rel1_2_3-auto_conf.bat    US    20170519-150123    0

MySQL Backup
    [Setup]    SetUserConfig    # Get connection details for Database
    Library Command    Remote Location to store DB Backup file    Backup Type    Backup Period (In Days)    Backup Action
    MySQL_Backup    /D:/BackUp/    Automatic    2    Start

MySQL Copy
    [Setup]    DBParams    ${var_dbhostname}    ${var_dbusername}    ${var_dbpassword}    # Get connection details for Database
    Library Command    Project Name    Test Case ID
    MySQL_Copy    My project1    2

*** Keywords ***
