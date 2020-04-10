import pandas as pd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow,Flow
from google.auth.transport.requests import Request
import os
import pickle


def Create_Service(client_secret_file, api_service_name, api_version, *scopes):

    global service
    SCOPES = [scope for scope in scopes[0]]

    cred = None

    if os.path.exists('token_write.pickle'):
        with open('token_write.pickle', 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, SCOPES)
            cred = flow.run_local_server()

        with open('token_write.pickle', 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(api_service_name, api_version, credentials=cred)
        print(api_service_name, 'service created successfully')
        # return service
    except Exception as e:
        print(e)
        # return None


def Export_Data_To_Sheets(df, SAMPLE_SPREADSHEET_ID_input, SAMPLE_RANGE_NAME):

    response_date = service.spreadsheets().values().update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID_input,
        valueInputOption='RAW',
        range=SAMPLE_RANGE_NAME,
        body=dict(
            majorDimension='ROWS',
            values=df.T.reset_index().T.values.tolist())
    ).execute()
    print('Sheet successfully Updated')


def main():

    share_link = 'https://docs.google.com/spreadsheets/d/1Bd5Uw5zPu1TLklLKPEKiIcvojCiYnz4L2J3Vhaa79kQ/edit?usp=sharing'

    # change this by your sheet ID
    SAMPLE_SPREADSHEET_ID_input = '1Bd5Uw5zPu1TLklLKPEKiIcvojCiYnz4L2J3Vhaa79kQ'

    # change the range if needed
    SAMPLE_RANGE_NAME = 'A1:AA1000'

    Create_Service('credentials.json', 'sheets', 'v4', ['https://www.googleapis.com/auth/spreadsheets'])

    df = pd.DataFrame([[0, 0], [0, 0]])

    Export_Data_To_Sheets(df, SAMPLE_SPREADSHEET_ID_input, SAMPLE_RANGE_NAME)

if __name__ =="__main__":
    main()