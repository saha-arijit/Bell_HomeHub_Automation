*** Settings ***
Library           ../Bell_HomeHub_Automation_Libraries/TestCommandExecution.py

*** Test Cases ***
N-LAT-2.4G-40MHz-1ss-11c-mcs
    [Setup]    Set User Config
    Set Execution Mode    Auto
    Execute Test Command

N-LAT-2.4G-40MHz-1ss-6c-mcs
    [Setup]    Set User Config
    Set Execution Mode    Auto
    Execute Test Command

N-LAT-2.4G-40MHz-1ss-6c-7mcs
    [Setup]    Set User Config
    Set Execution Mode    Auto
    Execute Test Command
