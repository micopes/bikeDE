from python.plugins.keys import API_KEY

import requests
import logging
import json


# TODO: partition - 한번에 최대 1000건 요청 가능. 1000건이 넘는 경우 나누어서 요청 필요
#  - 2625까지 존재(변경될 수도 있음. 신규로 생기거나 없어지는 경우) - 대응가능하도록 변경해야함.

start_index = 1
end_index = 1000
# url = f"http://openapi.seoul.go.kr:8088/{key}/json/bikeList/{start_index}/{end_index}/"

url = f"http://openapi.seoul.go.kr:8088/{API_KEY}/json/bikeList/{start_index}/{end_index}/"
# url2 = f"http://openapi.seoul.go.kr:8088/{key}/json/bikeList/1001/2000/"
# url3 = f"http://openapi.seoul.go.kr:8088/{key}/json/bikeList/2001/3000/"

# INFO-000: 정상 처리
# INFO-100: 인증키가 유효하지 않음
# INFO-200: 해당하는 데이터가 없음
# ERROR-xxx: 에러 (http://data.seoul.go.kr/dataList/OA-15493/A/1/datasetView.do 참조)

response = requests.get(url)

# 값이 존재하는 경우
# print(json.loads(response.text)['rentBikeStatus']['RESULT']['CODE']) # 이게 INFO-000


# response에 따른 결과값 받아서 사용.
logger = logging.getLogger(__name__)

result_code = json.loads(response.text)['rentBikeStatus']['RESULT']['CODE']
if result_code == 'INFO-000':
    logger.info("SUCCESS: processing success")
elif result_code == 'INFO-100':
    logger.info("FAIL: invalid authentication key")
elif result_code == 'INFO-200':
    logger.info("FAIL: no corresponding data")
else:
    logger.info("ERROR")

print(result_code)

# 값이 존재하지 않는 경우
# print(json.loads(response.text)['CODE']) # 이게 INFO-200 이 되면 break 걸면 되는데,



