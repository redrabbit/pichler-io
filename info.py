"""
Show basic runtime info from LG350 unit
"""

import pichler

device = pichler.Pichler()
datapoints = device.datapoint_read_list_values([59, 46, 33, 47, 32, 30])

print(
	{
		"level": datapoints[0],
		"supply_vol": datapoints[1],
		"supply_temp": int(str(datapoints[2])[1:]) / 10,
		"extract_vol": datapoints[3],
		"extract_temp": int(str(datapoints[4])[1:]) / 10,
		"outdoor_temp": int(str(datapoints[5])[1:]) / 10,
	}
)