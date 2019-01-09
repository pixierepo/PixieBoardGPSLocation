import subprocess
import time
import inspect
from utils import *
from results import Results


CHECK_MODEM_STATUS = "mmcli -L | grep No | wc -l"
ZERO_STRING = "0"
PIXIE_BOARDS_PASSWORD = "pixiepro"
SESSION_STATUS = "mmcli -m 0 --command='AT+QGPS?' | grep 'QGPS:' | awk '{print $3}'"
STOP_SESSION = "mmcli -m 0 --command='AT+QGPSEND'"
CONFIGURE_GPS_TRACKING = "mmcli -m 0 --command='AT+QGPS=1,30,50,0,1'"
GET_GPS_LOCATION = "mmcli -m 0 --command='AT+QGPSLOC?'"
GET_GPS_LOCATION_PRETTY = "mmcli -m 0 --command='AT+QGPSLOC=2'"
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

	@classmethod
	def CheckModemStatus():
		(command_output, error) = SendShellCommand(CHECK_MODEM_STATUS)
		if ParseCheckForValueZero(command_output):
			return True, command_output, error
		else:
			return False, command_output, error

	@classmethod
	def StopSession(shell_command=STOP_SESSION):
		sessionStatus, sessionOutput, sessionError = SessionStatus()
		if sessionStatus:
			(command_output, error) = SendShellCommand(shell_command)
			if ParseOKInMsg(command_output):
				return True, command_output, error
			else:
				return False, command_output, error
		else:
			return False, sessionOutput, sessionError

	@classmethod
	def SessionStatus(shell_command=SESSION_STATUS):
		(command_output, error) = PixieBoardGPSLocation.SendShellCommand(shell_command)
		if (str(command_output)[-4:-3]) == "1":
			return True, command_output, error
		else:
			return False, command_output, error

	@classmethod
	def GetCellId(shell_command=GET_CELL_ID):
		(command_output, error) = SendShellCommand(shell_command)
		self.CellId = ParseCommandLineValue(command_output)
		return self.CellId

	@classmethod
	def GetLocationAreaCode(shell_command=GET_LOCATION_AREA_CODE):
		(command_output, error) = SendShellCommand(shell_command)
		self.LocationAreaCode = ParseCommandLineValue(command_output)
		return self.LocationAreaCode

	@classmethod
	def GetMobileNetworkCode(shell_command=GET_MOBILE_NETWORK_CODE):
		(command_output, error) = SendShellCommand(shell_command)
		self.MobileNetworkCode = ParseCommandLineValue(command_output)
		return self.MobileNetworkCode

	@classmethod
	def GetMobileCountryCode(shell_command=GET_MOBILE_COUNTRY_CODE):
		(command_output, error) = SendShellCommand(shell_command)
		self.MobileCountryCode = ParseCommandLineValue(command_output)
		return self.MobileCountryCode

	@classmethod
	def GetIMEI(shell_command=GET_IMEI):
		(command_output, error) = SendShellCommand(shell_command)
		self.IMEI = ParseCommandLineValue(command_output)
		return self.IMEI

	@classmethod
	def GetProvider(shell_command=GET_PROVIDER):
		(command_output, error) = SendShellCommand(shell_command)
		self.Provider = ParseCommandLineValue(command_output)
		return self.Provider

	@classmethod
	def GetProviderID(shell_command=GET_PROVIDER_ID):
		(command_output, error) = SendShellCommand(shell_command)
		self.ProviderID = ParseCommandLineValue(command_output)
		return self.ProviderID

	@classmethod
	def GetSignalLevel(shell_command=GET_SIGNAL_LEVEL):
		(command_output, error) = SendShellCommand(shell_command)
		self.SignalLevel = ParseCommandLineValue(command_output)
		return self.SignalLevel

	@classmethod
	def SetCellProviderLocationData():
		GetCellId()
		GetLocationAreaCode()
		GetMobileNetworkCode()
		GetMobileCountryCode()
		GetIMEI()
		GetProvider()
		GetProviderID()
		GetSignalLevel()

	@classmethod
	def ConfigureGPSTracking(shell_command=CONFIGURE_GPS_TRACKING):
		StopSession()
		(command_output, error) = SendShellCommand(shell_command)
		if ParseOKInMsg(command_output):
			return True, command_output, error
		else:
			return False, command_output, error

	@classmethod
	def GetGPSLocation(shell_command=GET_GPS_LOCATION):
		(command_output, error) = SendShellCommand(shell_command)
		if ParseOKInMsg(command_output):
			ParseGPSLocation(command_output)
			return True, command_output, error
		else:
			return False, command_output, error

	@classmethod
	def GetGPSLocationPretty(shell_command=GET_GPS_LOCATION_PRETTY):
		(command_output, error) = SendShellCommand(shell_command)
		if ParseOKInMsg(command_output):
			ParseGPSLocation(command_output)
			return True, command_output, error
		else:
			return False, command_output, error

	@classmethod
	def WaitUntilGPSIsAvailablePretty():
		while True:
			signalReady, raw, error = GetGPSLocationPretty()
			if signalReady:
				break
			else:
				time.sleep(8)

	@classmethod
	def NAttemptsToGetLocationPretty(attempts):
		attemptCounter = 0
		while True:
			attemptCounter = attemptCounter + 1
			signalReady, raw, error = GetGPSLocationPretty()
			if signalReady:
				break
			elif attemptCounter == attempts:
				break
			else:
				time.sleep(8)

	@classmethod
	def SendShellCommand(shellCommand):
		print(shellCommand)
		logging.debug('Executing: ' + str(cmd))
		command = subprocess.Popen([shellCommand], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		stack = inspect.stack()
		fname = os.path.basename(stack[1][1])
		line = str(stack[1][2])
		caller = stack[1][3]
		Results.add_step(fname + '(' + line + '): ' + caller + '(): ' + cmd)
		res = '\n'.join(cmd_obj.communicate())
		print(res.strip())
		(command_output, error) = command.communicate()
		print(command_output)
		return command_output, error

	@classmethod
	def ParseGPSLocation(command_output):
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
            

	@classmethod
	def ParseOKInMsg(command_output):
		output = str(command_output)
		if COMMAND_OK_CALLBACK in output:
			return True
		else:
			return False

	@classmethod
	def ParseCheckForValueZero(command_output):
		output = str(command_output)
		print(output)
		if ZERO_STRING in output:
			return True
		else:
			return False

	@classmethod
	def ParseCommandLineValue(value_raw):
		value = str(value_raw)[3:-4]
		return value


