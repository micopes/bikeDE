import boto3
import json
import requests
import pandas as pd

from keys import API_KEY

class GetApiOperator():
    def get_api(self, service, date):
        # date = '20220721' # ex) YEARMMDDHH 형식
        url = []
        for i in range(10):
            # API에서 1000개 단위로 받도록 구성되어 있다.
            url_temp = f'http://openapi.seoul.go.kr:8088/{API_KEY}/json/{service}/{1+1000*i}/{1000*(i+1)}/{date}'
            response = requests.get(url_temp)
            try:
                result_code = json.loads(response.text)['getStationListHist']['RESULT']['CODE'] # 어떤 API인지에 따라 첫 인덱스 변경 필요.
                # 응답 완료 및 레코드 존재(1개 이상)
                if result_code == 'INFO-000':
                    url.append(url_temp)
            except:
                break

        return url

    def get_dh(self, url):
        # date, hour 파라미터
        response = requests.get(url[0])
        date_hour = json.loads(response.text)['getStationListHist']['row'][0]['stationDt']

        date = date_hour[:4] + '-' + date_hour[4:6] + '-' + date_hour[6:8] # 2022-07-26
        hour = date_hour[8:] # 20

        partition_date = f'date={date}'
        partition_hour = f'hour={hour}' # date만 있는 경우에는 사용 불가능할 수도 -> 재사용 가능하게 변경 필요.

        return partition_date, partition_hour

    def to_parquet(self, url):
        df = 0
        for i in range(len(url)):
            content = pd.read_json(url[i])
            row = content.loc['row'][0]
            if i == 0:
                df = pd.DataFrame(row)
            else:
                temp = pd.DataFrame(row)
                df = pd.concat([df, temp])

        # type 변경
        df = df.astype({'shared':'float64'})
        df.shared = df.shared*0.01

        # column명 변경
        df.columns = ['stand_count', 'station_name', 'parking_bike_count', 'stand_ratio', 'station_latitude',
                      'station_longitude', 'station_id', 'date_hour']

        # date, hour 나누기
        df['date'] = df['date_hour'].str.slice(start=0, stop=8)
        df['hour'] = df['date_hour'].str.slice(start=8, stop=10)
        df.drop(['date_hour'], axis = 1, inplace = True)
        df['date'] = df['date'].str.slice(start=0, stop=4) + '-' + df['date'].str.slice(start=4, stop=6) + '-' + df['date'].str.slice(start=6, stop=8)

        return df

    
