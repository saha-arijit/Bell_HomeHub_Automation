*** Settings ***
Library           ../Bell_HomeHub_Automation_Libraries/GenerateTestCaseLibrary.py

*** Test Cases ***
Generate_TestCases_All
    [Setup]    Run Keywords    SetUserConfig
    ...    AND    SetExecutionMode    Auto
    Set Test Documentation    To generate the test case combination for All
    Library Command    Tests Name (mention the test case Name)    Test Type (select from TP, RR, Lat or MaxClient)    Load Mode (Auto/Manual)    Direction (Bi-Direction = 1 / Uni-Direction = 0)    # Band Selection (2.4 / 5)    Channel
    ...    # Frame Size    Load Values (Calculated by ROBOTAutomation during execution if Load Mode set to Atuo)    Expected Connections    Source    # Destination    Test Duration
    ...    # MCS    SS    Channel Bandwidth    Guard Interval    # Ethernet Port    Wireless Port
    ...    # Group Type    Save PCAPS    Throughput Multiplier
    CreateTestCommand    AC-TP-5G-80MHz4-4ss-36c    TP    Auto    1    5    36
    ...    1518 1024 512 64    \    102    ETH    W_AC    60
    ...    9 8 7 3 1    4    80    short    generic_dut_1    generic_dut_0
    ...    802.11ac    YES    0.9
    #CreateTestCommand    \    TP    Auto    0    5    36
    ...    # 1518 1024 512 64    \    102    ETH    W_AC    60
    ...    # 9 8 7 3 1    2    40    short    generic_dut_1    generic_dut_0
    ...    # 802.11ac    YES    0.9
    #CreateTestCommand    AC-Lat-5G-80MHz4-4ss-36c    LAT    Auto    1    5    36
    ...    # 1518 1024 512 64    \    102    ETH    W_AC    60
    ...    # 9 8 7 3 1    2    80    short    generic_dut_1    generic_dut_0
    ...    # 802.11ac    YES    0.9
    #CreateTestCommand    \    LAT    Auto    1    5    36
    ...    # 1518 1024 512 64    \    102    ETH    W_AC    60
    ...    # 9 8 7 3 1    2    40    short    generic_dut_1    generic_dut_0
    ...    # 802.11ac    YES    0.9
    #CreateTestCommand    AC-RR-5G-80MHz-4ss-36c    RR    Auto    0    5    36
    ...    # 1518 1024 512 64    \    102    ETH    W_AC    60
    ...    # 9 8 7 3 1    1    80    short    generic_dut_1    generic_dut_0
    ...    # 802.11ac    YES    0.9
    #CreateTestCommand    \    RR    Auto    0    5    36
    ...    # 1518 1024 512 64    \    102    ETH    W_AC    60
    ...    # 9 8 7 3 1    2    40    short    generic_dut_1    generic_dut_0
    ...    # 802.11ac    YES    0.9
    #CreateTestCommand    AC-MaxClient-5G-80MHz-4ss-36c    MaxClient    Auto    1    5    36
    ...    # 1518 1024 512 64    \    102    ETH    W_AC    60
    ...    # 9 8 7 3 1    4    80    short    generic_dut_1    generic_dut_0
    ...    # 802.11ac    YES    0.9
    #CreateTestCommand    \    MaxClient    Auto    1    5    36
    ...    # 1518 1024 512 64    \    102    ETH    W_AC    60
    ...    # 9 8 7 3 1    4    80    short    generic_dut_1    generic_dut_0
    ...    # 802.11ac    YES    0.9

*** Keywords ***
