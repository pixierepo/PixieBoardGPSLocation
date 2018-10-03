from PixieBoardGPSLocation import PixieBoardGPSLocation


def HowToUsePixieBoardGPSLocation():
	# Init Class
	pxbdGPS = PixieBoardGPSLocation()

	# Check if the Modem has been enabled
	isModemEnabled, out, error = pxbdGPS.CheckModemStatus()
	if isModemEnabled:
		# Enable AT Commands
		pxbdGPS.EnableATCommands()

		#Configure GPS Session
		pxbdGPS.ConfigureGPSTracking()

		#Get Location on class
		pxbdGPS.WaitUntilGPSIsAvailablePretty()

		print("UTC Time: {}\n" \
                "Latitude: {}\n" \
                "Longitude: {}\n" \
                "HorizontalPrecision: {}\n" \
                "Altitude: {}\n" \
                "Fix: {}\n" \
                "Cog: {}\n" \
                "SpeedOverGroundKmH: {}\n" \
                "SpeedOverGroundKnots: {}\n" \
                "Date: {}\n" \
                "Number Of Satellites: {}".format(pxbdGPS.UTCTime, pxbdGPS.Latitude,  pxbdGPS.Longitude, pxbdGPS.HorizontalPrecision, pxbdGPS.Altitude, pxbdGPS.Fix, pxbdGPS.Cog, pxbdGPS.SpeedOverGroundKmH, pxbdGPS.SpeedOverGroundKnots, pxbdGPS.Date, pxbdGPS.NumberOfSatellites)
	else:
		print("Execute:\nsudo enablePixieModem\nWait for 30 seconds ")
	