*** Settings ***
Library           ../Bell_HomeHub_Automation_Libraries/TestCommandExecution.py

*** Test Cases ***
AC-RR-5G-80MHz-4ss-36c

AC-RR-5G-40MHz-4ss-36c

AC-RR-5G-40MHz-1ss-44c-7mcs
    [Setup]    Set User Config
    Set Execution Mode    Auto
    Execute Test Command
