# TODO Store Fronius JSON data for calculations
# TODO Hourly/daily/weekly/monthly production data
# TODO Hourly/daily/weekly/monthly usage data
# TODO Hourly/daily/weekly/monthly data
# TODO Overall net positive or net negative supply and costing -/+

import json
import requests

#Set debug on/off
isDebug = True

# Fronius API 
# Inverter IP/Host address  ---- do i need to use meter endpoint or can i calculate everything i need from powerflow endpoint?
inverterAddr = "192.168.20.5"
inverterMtrEndPt = "/solar_api/v1/GetMeterRealtimeData.cgi?Scope=Device&DeviceId=0"
inverterPfEndPt = "/solar_api/v1/GetPowerFlowRealtimeData.fcgi"

# Options
requestInterval = 60 # 60 seconds


# Do all the things

# Get Fronius JSON data and loads it into jsonData for use
jsonResponse = requests.get("http://" + inverterAddr + inverterPfEndPt)
jsonPfData = json.loads(jsonResponse.text)
jsonResponse = requests.get("http://" + inverterAddr + inverterMtrEndPt)
jsonMtrData = json.loads(jsonResponse.text)

# Print out JSON data for debug
if isDebug :
    print(jsonPfData['Body']['Data']['Site']['P_Load'])
    print(jsonPfData['Body']['Data']['Site']['P_Grid'])
