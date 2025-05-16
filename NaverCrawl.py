# 필요한 라이브러리 임포트
import requests  # HTTP 요청을 보내기 위한 라이브러리
import json  # JSON 데이터 처리를 위한 라이브러리
from bs4 import BeautifulSoup  # HTML 파싱을 위한 라이브러리
import pandas as pd  # 데이터 처리를 위한 라이브러리
import re  # 정규표현식을 사용하기 위한 라이브러리
import openpyxl  # 엑셀 파일 처리를 위한 라이브러리

# 네이버 개발자 센터에서 발급받은 API 인증 정보
client_id = "yR8aViAqV5NyEjZpfo74"  # 네이버 API 클라이언트 ID
client_secret = "SQ_PTt2epk"  # 네이버 API 클라이언트 시크릿

# 사용자로부터 검색어 입력 받기
query = input("검색할 키워드를 입력하세요: ")  # 검색할 키워드 입력
display = 10  # 한 번에 가져올 검색 결과 개수 (최대 100개까지 설정 가능)

# 네이버 뉴스 검색 API URL 생성
url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display={display}"

headers = {
    "X-Naver-Client-Id": client_id,
    "X-Naver-Client-Secret": client_secret,
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    news_data = response.json()
    
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "네이버 뉴스 검색 결과"
    ws.append(["제목", "본문"])
    
    if 'items' in news_data:
        # 검색 결과가 있는 경우 처리 시작
        for item in news_data['items']:
            # HTML 강조 태그(<b></b>)를 제거하여 제목과 본문 텍스트 추출
            title = item['title'].replace("<b>", "").replace("</b>", "")
            content = item['description'].replace("<b>", "").replace("</b>", "")
            
            # BeautifulSoup을 사용하여 남아있는 HTML 태그를 제거하고 순수 텍스트 추출
            clean_title = BeautifulSoup(title, "html.parser").text
            clean_content = BeautifulSoup(content, "html.parser").text
            
            # 추출한 제목과 본문을 콘솔에 출력
            print(f"제목: {clean_title}")
            print(f"본문: {clean_content}")
            
            # 추출한 제목과 본문을 엑셀 워크시트에 추가
            ws.append([clean_title, clean_content])
        
        # 반복문 바깥에서 한 번만 파일 저장
        file_name = f"{query}_news.xlsx"
        wb.save(file_name)
        print(f"'{file_name}' 파일에 저장되었습니다.")
    else:
        # 검색 결과가 없는 경우 메시지 출력
        print("검색 결과가 없습니다.")
else:
    # API 요청이 실패한 경우 오류 코드와 함께 메시지 출력
    print("API 요청 실패:", response.status_code)