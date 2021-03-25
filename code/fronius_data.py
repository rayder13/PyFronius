# TODO Store Fronius JSON data for calculations?
# TODO Hourly/daily/weekly/monthly production data
# TODO Hourly/daily/weekly/monthly usage data
# TODO Hourly/daily/weekly/monthly relative usage data
# TODO Overall net positive or net negative supply and costing -/+

import json
import requests
import time
import sys

#Set debug on/off ---- maybe set to an arg for release debugging?
isDebug = False

# Fronius API 
# Inverter IP/Host address  ---- do i need to use meter endpoint or can i calculate everything i need from powerflow endpoint?
inverterAddr = "192.168.20.5"
inverterMtrEndPt = "/solar_api/v1/GetMeterRealtimeData.cgi?Scope=Device&DeviceId=0"
inverterPfEndPt = "/solar_api/v1/GetPowerFlowRealtimeData.fcgi"

# Options
requestInterval = 60 # Should be 60 seconds for remotely accurate readings

energyUsedHrAvg = 0
energyUsedHrRunning = 0
energyUsedHrCount = 0

# Run until closed out by the user or an uncaught error
while True:
    try :
        # Get Fronius JSON data and loads it into jsonPfData for use
        jsonResponse = requests.get("http://" + inverterAddr + inverterPfEndPt)
        jsonPfData = json.loads(jsonResponse.text)

        # From Fronius API documentation
        # P_Grid - this value is null if no meter is enabled ( + from grid , - to grid )
        # P_Load - this value is null if no meter is enabled ( + generator , - consumer )
        # P_PV - this value is null if inverter is not running ( + production ( default ) )
        # So...
        # "P_Grid" : 113.05, - drawing 113.05w FROM the grid
        # "P_Load" : -1223.05, - total load
        # "P_PV" : 1110, PV panels generating 1110w
        
        # Don't catch NULL for P_Load or P_Grid. If these values are null, you don't have a 
        # meter and can't log the production/usage data anyways
        froniusPLoad = jsonPfData['Body']['Data']['Site']['P_Load']
        froniusPGrid = jsonPfData['Body']['Data']['Site']['P_Grid']
        # Catch NULL as documentation says it will return NULL if the inverter is not running
        # e.g PV panels are not producing any power
        try :
            froniusPPv = jsonPfData['Body']['Data']['Site']['P_Pv']
        except KeyError :
            froniusPPv = 0

        if jsonPfData['Body']['Data']['Site']['P_Load'] >= 0 :
            print('Feeding in ' + str(froniusPLoad) + 'w to the grid')
            if energyUsedHrCount <= 60 :
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
            if energyUsedHrCount <= 60 :
                energyUsedHrCount += 1
                energyUsedHrRunning += int(froniusPLoad * -1)
                energyUsedHrAvg = energyUsedHrRunning / 60
            else :
                energyUsedHrCount = 1
                energyUsedHrRunning = 0
                energyUsedHrAvg = 0

            print('Wh average for the current hour: ' + str(energyUsedHrAvg))

            time.sleep(requestInterval)
    
    except KeyboardInterrupt :
        print('Ctrl-C Interrupt detected')
        sys.exit()
        