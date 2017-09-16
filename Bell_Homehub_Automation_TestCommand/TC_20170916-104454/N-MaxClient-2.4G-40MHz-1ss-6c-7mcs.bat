::N-MaxClient-2.4G-40MHz-1ss-6c-7mcs
tclsh ..\..\bin\vw_auto.tcl -f MaxClient.tcl ^
--var ssid "BELL110" ^
--var pw "testtest" ^
--var save "C:\WifiResults\HH3000\testtest\BELL110\MaxClient\DS" ^
--var ap "HH3000" ^
--var apver "testtest" ^
--var channel "6" ^
--var frameSize "512" ^
--var loads "" ^
--var expectConn "102" ^
--var source "W_N" ^
--var destination "ETH" ^
--var duration "5" ^
--var mcs "7" ^
--var ss "1" ^
--var bw "40" ^
--var gi "short" ^
--var eth_dut "generic_dut_1" ^
--var w_dut "generic_dut_0" ^
--var w_grouptype "802.11ac" ^
--savepcaps ^
--debug 2
::
::N-MaxClient-2.4G-40MHz-1ss-6c-7mcs
tclsh ..\..\bin\vw_auto.tcl -f MaxClient.tcl ^
--var ssid "BELL110" ^
--var pw "testtest" ^
--var save "C:\WifiResults\HH3000\testtest\BELL110\MaxClient\US" ^
--var ap "HH3000" ^
--var apver "testtest" ^
--var channel "6" ^
--var frameSize "512" ^
--var loads "" ^
--var expectConn "102" ^
--var source "ETH" ^
--var destination "W_N" ^
--var duration "5" ^
--var mcs "7" ^
--var ss "1" ^
--var bw "40" ^
--var gi "short" ^
--var eth_dut "generic_dut_1" ^
--var w_dut "generic_dut_0" ^
--var w_grouptype "802.11ac" ^
--savepcaps ^
--debug 2
::