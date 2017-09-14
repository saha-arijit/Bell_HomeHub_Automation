*** Settings ***
Library           ../Bell_HomeHub_Automation_Libraries/GenerateTestCaseLibrary.py

*** Test Cases ***
Generate_TestCases_All
    [Setup]    Run Keywords    SetUserConfig
    ...    AND    SetExecutionMode    Auto
    Set Test Documentation    To generate the test case combination for All
    Library Command    Tests Name (mention the test case Name)    Test Type (select from TP, RR, Lat or MaxClient)    Load Mode (Auto/Manual)    Direction (Bi-Direction = 1 / Uni-Direction = 0)    Band Selection (2.4 / 5)    Channel
    ...    Frame Size    Load Values (Calculated by ROBOTAutomation during execution if Load Mode set to Atuo)    Expected Connections    Source    Destination    Test Duration
    ...    MCS    SS    Channel Bandwidth    Guard Interval    Ethernet Port    Wireless Port
    ...    Group Type    Save PCAPS    Throughput Multiplier
    CreateTestCommand    \    TP    Auto    1    2.4    11
    ...    1518    \    \    ETH    W_N    5
    ...    7 6    1    40    short    generic_dut_1    generic_dut_0
    ...    802.11ac    YES    0.9
    CreateTestCommand    \    TP    Auto    1    2.4    1
    ...    1518    \    \    ETH    W_N    5
    ...    7    1    40    short    generic_dut_1    generic_dut_0
    ...    802.11ac    YES    0.9
    CreateTestCommand    \    LAT    Auto    1    2.4    11
    ...    1518    \    \    ETH    W_N    5
    ...    7 6    1    40    short    generic_dut_1    generic_dut_0
    ...    802.11ac    YES    0
    CreateTestCommand    \    LAT    Auto    1    2.4    1
    ...    1518    \    \    ETH    W_N    5
    ...    7    1    40    short    generic_dut_1    generic_dut_0
    ...    802.11ac    YES    0
    CreateTestCommand    \    RR    Auto    1    2.4    11
    ...    1518    \    \    ETH    W_N    5
    ...    7 6    1    40    short    generic_dut_1    generic_dut_0
    ...    802.11ac    YES    0
    CreateTestCommand    \    RR    Auto    1    2.4    1
    ...    1518    \    \    ETH    W_N    5
    ...    7    1    40    short    generic_dut_1    generic_dut_0
    ...    802.11ac    YES    0
    CreateTestCommand    \    MaxClient    Auto    0    2.4    11
    ...    512    \    102    ETH    W_N    5
    ...    7    1    40    short    generic_dut_1    generic_dut_0
    ...    802.11ac    YES    0
    log    Test command file creation completed

*** Keywords ***
