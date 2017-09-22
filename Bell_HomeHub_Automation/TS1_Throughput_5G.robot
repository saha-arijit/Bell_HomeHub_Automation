*** Settings ***
Library           ../Bell_HomeHub_Automation_Libraries/TestCommandExecution.py

*** Test Cases ***
AC-TP-5G-80MHz4-4ss-36c
    [Setup]    Run Keywords    SetUserConfig

AC-TP-5G-40MHz4-4ss-36c

AC-TP-5G-40MHz-1ss-36c-7mcs
    [Setup]    Set User Config
    Set Execution Mode    Auto
    Execute Test Command
