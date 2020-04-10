import urllib3
import json
from write2sheet import *


url = 'https://data.nsw.gov.au/data/api/3/action/datastore_search_sql?sql=SELECT * from "21304414-1ff1-4243-a5d2-f52778048b29"'

share_link = 'https://docs.google.com/spreadsheets/d/1Bd5Uw5zPu1TLklLKPEKiIcvojCiYnz4L2J3Vhaa79kQ/edit?usp=sharing'

# change this by your sheet ID
SAMPLE_SPREADSHEET_ID_input = '1Bd5Uw5zPu1TLklLKPEKiIcvojCiYnz4L2J3Vhaa79kQ'

# change the range if needed
SAMPLE_RANGE_NAME = 'A1:AA1000'


def main():

    # read data from government's page

    http = urllib3.PoolManager()
    r = http.request('GET', url)
    print('Status code: ', r.status)

    data_dic = json.loads(r.data.decode('utf-8'))
    data = data_dic['result']['records']

    df = pd.DataFrame(data)
    df = pd.DataFrame(df['postcode'])
    df['cases'] = df.postcode.map(df.postcode.value_counts())
    df = df.drop_duplicates()
    df = df.dropna()

    # save to file
    Create_Service('credentials.json', 'sheets', 'v4', ['https://www.googleapis.com/auth/spreadsheets'])

    Export_Data_To_Sheets(df, SAMPLE_SPREADSHEET_ID_input, SAMPLE_RANGE_NAME)

if __name__ =="__main__":
    main()
