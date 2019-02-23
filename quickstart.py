from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
# SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
# SAMPLE_RANGE_NAME = 'Class Data!A2:E'


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    spreadsheet = {
        'properties': {
            'title': "Test Sheet"
        }
    }

    spreadsheet = service.spreadsheets().create(body=spreadsheet).execute()

    SPREADSHEET_ID = spreadsheet.get('spreadsheetId')

    print('Spreadsheet ID: {0}'.format(SPREADSHEET_ID))

    SHEET = spreadsheet['sheets'][0]

    batch_update_spreadsheet_request_body = {
        "requests": [{
            "updateSheetProperties": {
                "properties": {
                    "sheetId": 0,
                    "title": "Test Tab",
                },
                "fields": "title",
            }
        }]
    }

    request = service.spreadsheets().batchUpdate(spreadsheetId=SPREADSHEET_ID,
                                                 body=batch_update_spreadsheet_request_body)
    response = request.execute()

    print(response)

    values = [
        [1],
        [2],
        [4],
        [5],
        [4]
        # Additional rows ...
    ]
    range_name = "A1:A5"
    body = {
        'values': values
    }

    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID, range=range_name,
        valueInputOption="USER_ENTERED", body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))


if __name__ == '__main__':
    main()
