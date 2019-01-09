import subprocess
import time
import inspect
from utils import *
from results import Results


CHECK_MODEM_STATUS = "mmcli -L | grep No | wc -l"
ZERO_STRING = "0"
ERROR_STRING = "error"
COMMAND_OK_CALLBACK = "response"
PIXIE_BOARDS_PASSWORD = "pixiepro"
SESSION_STATUS = "mmcli -m 0 --command='AT+QGPS?' | grep 'QGPS:' | awk '{print $3}'"
STOP_SESSION = "mmcli -m 0 --command='AT+QGPSEND'"
CONFIGURE_GPS_TRACKING = "mmcli -m 0 --command='AT+QGPS=1,30,50,0,1'"
GET_GPS_LOCATION = "mmcli -m 0 --command='AT+QGPSLOC?'"
GET_GPS_LOCATION_PRETTY = "mmcli -m 0 --command='AT+QGPSLOC=2' | grep '+QGPSLOC:'"
GET_CELL_ID = "mmcli -m 0 --location-get | grep 'Cell ID' | awk '{print $4}'"
GET_LOCATION_AREA_CODE = "mmcli -m 0 --location-get | grep 'Location area code' | awk '{print $5}'"
GET_MOBILE_NETWORK_CODE = "mmcli -m 0 --location-get | grep 'Mobile network code' | awk '{print $5}'"
GET_MOBILE_COUNTRY_CODE = "mmcli -m 0 --location-get | grep 'Mobile country code' | awk '{print $7}'"
GET_IMEI = "mmcli -m 0 | grep 'imei' | awk '{print $4}'"
GET_PROVIDER = "mmcli -m 0 | grep 'operator name' | awk '{print $4}'"
GET_PROVIDER_ID = "mmcli -m 0 | grep 'operator id' | awk '{print $4}'"
GET_SIGNAL_LEVEL = "mmcli -m 0 | grep 'signal quality' | awk '{print $4}'"

class PixieBoardGPSLocation():

	def __init__(self):

		self.ModemStatus = ""

		self.UTCTime = ""
		self.Latitude = ""
		self.Longitude = ""
		self.HorizontalPrecision = ""
		self.Altitude = ""
		self.Fix = ""
		self.Cog = ""
		self.SpeedOverGroundKmH = ""
		self.SpeedOverGroundKnots = ""
		self.Date = ""
		self.NumberOfSatellites = ""
		self.CellId = ""
		self.LocationAreaCode = ""
		self.MobileNetworkCode = ""
		self.MobileCountryCode = ""
		self.IMEI = ""
		self.Provider = ""
		self.ProviderID = ""
		self.SignalLevel = ""

	def CheckModemStatus(self):
		(command_output, error) = self.SendShellCommand(CHECK_MODEM_STATUS)
		if self.ParseCheckForValueZero(command_output):
			return True, command_output, error
		else:
			return False, command_output, error

	def StopSession(self, shell_command=STOP_SESSION):
		sessionStatus, sessionOutput, sessionError = self.SessionStatus()
		if sessionStatus:
			(command_output, error) = self.SendShellCommand(shell_command)
			if self.ParseOKInMsg(command_output):
				return True, command_output, error
			else:
				return False, command_output, error
		else:
			return False, sessionOutput, sessionError

	def SessionStatus(self, shell_command=SESSION_STATUS):
		(command_output, error) = self.SendShellCommand(shell_command)
		if "1" in str(command_output):
			return True, command_output, error
		else:
			return False, command_output, error

	def GetCellId(self, shell_command=GET_CELL_ID):
		(command_output, error) = self.SendShellCommand(shell_command)
		self.CellId = self.ParseCommandLineValue(command_output)
		return self.CellId

	def GetLocationAreaCode(self, shell_command=GET_LOCATION_AREA_CODE):
		(command_output, error) = self.SendShellCommand(shell_command)
		self.LocationAreaCode = self.ParseCommandLineValue(command_output)
		return self.LocationAreaCode

	def GetMobileNetworkCode(self, shell_command=GET_MOBILE_NETWORK_CODE):
		(command_output, error) = self.SendShellCommand(shell_command)
		self.MobileNetworkCode = self.ParseCommandLineValue(command_output)
		return self.MobileNetworkCode

	def GetMobileCountryCode(self, shell_command=GET_MOBILE_COUNTRY_CODE):
		(command_output, error) = self.SendShellCommand(shell_command)
		self.MobileCountryCode = self.ParseCommandLineValue(command_output)
		return self.MobileCountryCode

	def GetIMEI(self, shell_command=GET_IMEI):
		(command_output, error) = self.SendShellCommand(shell_command)
		self.IMEI = self.ParseCommandLineValue(command_output)
		return self.IMEI

	def GetProvider(self, shell_command=GET_PROVIDER):
		(command_output, error) = self.SendShellCommand(shell_command)
		self.Provider = self.ParseCommandLineValue(command_output)
		return self.Provider

	def GetProviderID(self, shell_command=GET_PROVIDER_ID):
		(command_output, error) = self.SendShellCommand(shell_command)
		self.ProviderID = self.ParseCommandLineValue(command_output)
		return self.ProviderID

	def GetSignalLevel(self, shell_command=GET_SIGNAL_LEVEL):
		(command_output, error) = self.SendShellCommand(shell_command)
		self.SignalLevel = self.ParseCommandLineValue(command_output)
		return self.SignalLevel

	def SetCellProviderLocationData(self):
		self.GetCellId()
		self.GetLocationAreaCode()
		self.GetMobileNetworkCode()
		self.GetMobileCountryCode()
		self.GetIMEI()
		self.GetProvider()
		self.GetProviderID()
		self.GetSignalLevel()

	def ConfigureGPSTracking(self, shell_command=CONFIGURE_GPS_TRACKING):
		self.StopSession()
		(command_output, error) = self.SendShellCommand(shell_command)

	def GetGPSLocation(self, shell_command=GET_GPS_LOCATION):
		(command_output, error) = self.SendShellCommand(shell_command)
		if self.ParseErrorInMsg(command_output):
			return False, command_output, error
		else:
			self.ParseGPSLocation(command_output)
			return True, command_output, error

	def GetGPSLocationPretty(self, shell_command=GET_GPS_LOCATION_PRETTY):
		(command_output, error) = self.SendShellCommand(shell_command)
		if self.ParseOKInMsg(command_output):
			self.ParseGPSLocation(command_output)
			return True, command_output, error
		else:
			return False, command_output, error

	def WaitUntilGPSIsAvailablePretty(self):
		while True:
			signalReady, raw, error = self.GetGPSLocationPretty()
			if signalReady:
				break
			else:
				time.sleep(8)

	def NAttemptsToGetLocationPretty(self, attempts):
		attemptCounter = 0
		while True:
			print("Attempt: {}".format(attemptCounter))
			attemptCounter = attemptCounter + 1
			signalReady, raw, error = self.GetGPSLocationPretty()
			if signalReady:
				break
			elif attemptCounter == attempts:
				break
			else:
				time.sleep(8)

	def SendShellCommand(self, shellCommand):
		print("Excecuting: {}".format(shellCommand))
		command = subprocess.Popen([shellCommand], stdout=subprocess.PIPE, shell=True)
		(command_output, error) = command.communicate()
		print("Command Output: {}".format(command_output))
		return command_output, error

	def ParseGPSLocation(self, command_output):
		print(command_output)
		locationData = str(command_output).split(",")
		try:
			self.UTCTime = locationData[0][30:]
			self.Latitude = locationData[1]
			self.Longitude = locationData[2]
			self.HorizontalPrecision = locationData[3]
			self.Altitude = locationData[4]
			self.Fix = locationData[5]
			self.Cog = locationData[6]
			self.SpeedOverGroundKmH = locationData[7]
			self.SpeedOverGroundKnots = locationData[8]
			self.Date = locationData[9]
			self.NumberOfSatellites = locationData[10][0:2]
		except IndexError:
			print("index Error")
			self.UTCTime = 0
			self.Latitude = 0
			self.Longitude = 0
			self.HorizontalPrecision = 0
			self.Altitude = 0
			self.Fix = 0
			self.Cog = 0
			self.SpeedOverGroundKmH = 0
			self.SpeedOverGroundKnots = 0
			self.Date = 0
			self.NumberOfSatellites = 0
            

	def ParseOKInMsg(self, command_output):
		output = str(command_output)
		if COMMAND_OK_CALLBACK in output:
			return True
		else:
			return False
        
	def ParseErrorInMsg(self, command_output):
		output = str(command_output)
		if ERROR_STRING in output:
			return True
		else:
			return False

	def ParseCheckForValueZero(self, command_output):
		output = str(command_output)
		print(output)
		if ZERO_STRING in output:
			return True
		else:
			return False

	def ParseCommandLineValue(self, value_raw):
		value = str(value_raw)[3:-4]
		return value


