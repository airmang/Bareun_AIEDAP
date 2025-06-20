# 필요한 라이브러리 임포트
import requests  # HTTP 요청을 보내기 위한 라이브러리
import json  # JSON 데이터 처리를 위한 라이브러리
from bs4 import BeautifulSoup  # HTML 파싱을 위한 라이브러리
import pandas as pd  # 데이터 처리를 위한 라이브러리
import re  # 정규표현식을 사용하기 위한 라이브러리

# 네이버 개발자 센터에서 발급받은 API 인증 정보
client_id = "yR8aViAqV5NyEjZpfo74"  # 네이버 API 클라이언트 ID
client_secret = "SQ_PTt2epk"  # 네이버 API 클라이언트 시크릿

# 사용자로부터 검색어 입력 받기
query = input("검색할 키워드를 입력하세요: ")  # 검색할 키워드 입력
display = 10  # 한 번에 가져올 검색 결과 개수 (최대 100개까지 설정 가능)

# 네이버 뉴스 검색 API URL 생성
url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display={display}"

# API 요청에 필요한 헤더 설정
headers = {
    "X-Naver-Client-Id": client_id,  # 네이버 API 인증을 위한 클라이언트 ID
    "X-Naver-Client-Secret": client_secret,  # 네이버 API 인증을 위한 클라이언트 시크릿
}

# 네이버 API에 검색 요청 보내기
response = requests.get(url, headers=headers)  # GET 요청으로 뉴스 검색 결과 받아오기

# API 요청이 성공한 경우 (상태 코드 200)
if response.status_code == 200:
    # API 응답 결과를 JSON 형식으로 파싱
    data = response.json()
    # 검색 결과를 저장할 리스트 초기화
    news_data = []
    
    # 검색된 뉴스 개수 출력
    print(f"총 {len(data['items'])}개의 뉴스를 찾았습니다.")
    
    # 검색된 각 뉴스 항목에 대해 반복
    for item in data['items']:
        # 뉴스 제목에서 HTML 태그 제거 (예: <b></b> 등)
        title = re.sub('<.*?>', '', item['title'])
        # 원본 기사 링크 가져오기 (없으면 네이버 뉴스 링크 사용)
        original_link = item['originallink'] or item['link']
        
        # 뉴스 웹사이트에 접속하여 본문 가져오기
        article_res = requests.get(original_link, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'  # 브라우저처럼 보이게 하는 설정
        })
        
        # HTML 파싱을 위한 BeautifulSoup 객체 생성
        article_soup = BeautifulSoup(article_res.text, 'html.parser')
        
        # 뉴스 본문 추출
        content = ""  # 본문 내용을 저장할 변수 초기화
        # 일반적인 뉴스 사이트의 본문 영역 선택자로 본문 찾기
        article_body = article_soup.select_one('#articleBody, #newsEndContents, .news_content')
        if article_body:  # 본문을 찾은 경우
            # HTML에서 텍스트만 추출하고 앞뒤 공백 제거
            content = article_body.get_text(strip=True)
            # 연속된 공백을 하나의 공백으로 변경
            content = re.sub(r'\s+', ' ', content).strip()
        
        # 추출한 정보를 딕셔너리로 만들어 리스트에 추가
        news_data.append({
            'title': title,  # 뉴스 제목
            'content': content,  # 뉴스 본문
            'link': original_link  # 원본 기사 링크
        })
    
    # 수집한 뉴스 데이터를 데이터프레임으로 변환
    df = pd.DataFrame(news_data)
    
    # 결과를 엑셀 파일로 저장
    filename = f"{query}_뉴스_{len(df)}건.xlsx"  # 파일명 생성 (검색어와 건수 포함)
    df.to_excel(filename, index=False)  # 인덱스 없이 엑셀 파일로 저장
    print(f"결과를 {filename}에 저장했습니다.")  # 저장 완료 메시지 출력
    
else:
    # API 요청이 실패한 경우 에러 메시지 출력
    print(f"API 호출 실패: {response.status_code}")  # HTTP 상태 코드와 함께 실패 메시지 출력 