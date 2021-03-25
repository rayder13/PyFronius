# TODO Store Fronius JSON data for calculations
# TODO Hourly/daily/weekly/monthly production data
# TODO Hourly/daily/weekly/monthly usage data
# TODO Hourly/daily/weekly/monthly data
# TODO Overall net positive or net negative supply and costing -/+

import json
import requests
import time

#Set debug on/off ---- maybe set to an arg for release debugging?
isDebug = False

# Fronius API 
# Inverter IP/Host address  ---- do i need to use meter endpoint or can i calculate everything i need from powerflow endpoint?
inverterAddr = "192.168.20.5"
inverterMtrEndPt = "/solar_api/v1/GetMeterRealtimeData.cgi?Scope=Device&DeviceId=0"
inverterPfEndPt = "/solar_api/v1/GetPowerFlowRealtimeData.fcgi"

# Options
requestInterval = 10 # 60 seconds

energyUsedHrAvg = 0
energyUsedHrRunning = 0
energyUsedHrCount = 0

# Do all the things

# Get Fronius JSON data and loads it into jsonData for use
#jsonResponse = requests.get("http://" + inverterAddr + inverterPfEndPt)
#jsonPfData = json.loads(jsonResponse.text)
jsonResponse = requests.get("http://" + inverterAddr + inverterMtrEndPt)
jsonMtrData = json.loads(jsonResponse.text)

# Print out JSON data for debug
if isDebug :
    print(jsonPfData['Body']['Data']['Site']['P_Load'])
    print(jsonPfData['Body']['Data']['Site']['P_Grid'])

while True:
    jsonResponse = requests.get("http://" + inverterAddr + inverterPfEndPt)
    jsonPfData = json.loads(jsonResponse.text)

    froniusPLoad = jsonPfData['Body']['Data']['Site']['P_Load']
    froniusPGrid = jsonPfData['Body']['Data']['Site']['P_Grid']
    #global energyUsedHrAvg
    #global energyUsedHrRunning
    #global energyUsedHrCount

    if jsonPfData['Body']['Data']['Site']['P_Load'] >= 0 :
        print('Feeding in ' + str(froniusPLoad) + 'w to the grid')
        if energyUsedHrCount <= 600 :
            energyUsedHrCount += 1
            energyUsedHrRunning += int(froniusPLoad)
            energyUsedHrAvg = energyUsedHrRunning / energyUsedHrCount
        else :
            energyUsedHrCount = 1
            energyUsedHrRunning = 0
            energyUsedHrAvg = 0
            
        print('kWh average for the current hour: ' + str(energyUsedHrAvg))

        time.sleep(requestInterval)

    elif jsonPfData['Body']['Data']['Site']['P_Load'] < 0 :
        print('Drawing ' + str(froniusPLoad * -1) + 'w from the grid')
        if energyUsedHrCount <= 600 :
            energyUsedHrCount += 1
            energyUsedHrRunning += int(froniusPLoad * -1)
            energyUsedHrAvg += energyUsedHrRunning / ((energyUsedHrCount * requestInterval) * 60)
        else :
            energyUsedHrCount = 1
            energyUsedHrRunning = 0
            energyUsedHrAvg = 0

        print('kWh average for the current hour: ' + str(energyUsedHrAvg))

        time.sleep(requestInterval)