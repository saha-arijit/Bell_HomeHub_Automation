*** Settings ***
Library           ../Bell_HomeHub_Automation_Libraries/GenerateTestCaseLibrary.py

*** Test Cases ***
AC-TP-5G-80MHz4-4ss-36c
    [Setup]    Run Keywords    SetUserConfig    #SetExecutionMode    Manual    #Library Command    Tests Name (mention the test case Name)
    ...    # Test Type (select from TP, RR, Lat or MaxClient)    Load Mode (Auto/Manual)    Direction (Bi-Direction = 1 / Uni-Direction = 0)    Band Selection (2.4 / 5)    Channel    # Frame Size
    ...    # Load Values (Calculated by ROBOTAutomation during execution if Load Mode set to Atuo)    Expected Connections    Source    Destination    Test Duration    # MCS
    ...    # SS    Channel Bandwidth    Guard Interval    Ethernet Port    Wireless Port    # Group Type
    ...    # Save PCAPS    Throughput Multiplier

AC-Lat-5G-80MHz4-4ss-36c

AC-RR-5G-80MHz-4ss-36c

N-MaxClient-2.4G-40MHz-4ss-1c
