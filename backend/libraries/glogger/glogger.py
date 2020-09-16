from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pytz
from google.oauth2 import service_account
import libraries.constants as Constants


SERVICE_ACCOUNT_FILE = os.path.join(os.path.dirname(__file__), 'service.json')

def write_log(*args):
	SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
	credentials = service_account.Credentials.from_service_account_file(
	        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

	if Constants.PRODUCTION:
		SPREADSHEET_ID = Constants.SETTINGS["glogger"]["log_sheetid_prod"]
	else:
		SPREADSHEET_ID = Constants.SETTINGS["glogger"]["log_sheetid_dev"]

	range_ = "A:A"  # TODO: Update placeholder value.

	# How the input data should be interpreted.
	value_input_option = 'USER_ENTERED'  # TODO: Update placeholder value.

	# How the input data should be inserted.
	insert_data_option = 'INSERT_ROWS'  # TODO: Update placeholder value.
	value_range_body = {
	    "values": [
	        args
	    ]
	}
	service = build('sheets', 'v4', credentials=credentials)
	request = service.spreadsheets().values().append(spreadsheetId=SPREADSHEET_ID, range=range_, valueInputOption=value_input_option, insertDataOption=insert_data_option, body=value_range_body)
	response = request.execute()

def improve_emotion(text,emotion):
	SERVICE_ACCOUNT_FILE = 'service.json'
	SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
	credentials = service_account.Credentials.from_service_account_file(
	        SERVICE_ACCOUNT_FILE, scopes=SCOPES)


	SPREADSHEET_ID = "1vnSpZmH57bcIb8Tp7XgK_Jh-4iFW99CBkxhqnasru5g"
	range_ = "A:A"  # TODO: Update placeholder value.

	# How the input data should be interpreted.
	value_input_option = 'USER_ENTERED'  # TODO: Update placeholder value.

	# How the input data should be inserted.
	insert_data_option = 'INSERT_ROWS'  # TODO: Update placeholder value.
	value_range_body = {
	    "values": [
	        [
	            text,emotion
	        ] 
	    ]
	}
	service = build('sheets', 'v4', credentials=credentials)
	request = service.spreadsheets().values().append(spreadsheetId=SPREADSHEET_ID, range=range_, valueInputOption=value_input_option, insertDataOption=insert_data_option, body=value_range_body)
	response = request.execute()