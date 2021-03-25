import json
import requests

# Fronius inverter IP/Host address
inverterAddr = "192.168.20.5"
# Selected Fronius JSON endpoint
inverterEndPt = "/solar_api/v1/GetMeterRealtimeData.cgi?Scope=Device&DeviceId=0"

# Get Fronius JSON data and loads it into jsonData for use
jsonResponse = requests.get("http://" + inverterAddr + inverterEndPt)
jsonData = json.loads(jsonResponse.text)

# Print out JSON data for debug  !!!Only for debugging!!!
print(jsonData)

# Store Fronius JSON data for calculations



# **Hourly/daily/weekly/monthly production data

# **Hourly/daily/weekly/monthly usage data

# **Hourly/daily/weekly/monthly data