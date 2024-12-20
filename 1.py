import subprocess
import time
import pyautogui
import pyperclip
import random

# 상품명과 ID의 딕셔너리 생성
products = {
    "다온 화목난로":"88776421839",
    "화목난로 다온":"88776421839",
    "화목 다온 난로":"88776421839",
    "다온 화목난로":"88776421839",
    "화목난로 다온":"88776421839",
    "화목 다온 난로":"88776421839",
    "다온 화목난로":"88776421839",
    "화목난로 다온":"88776421839",
    # "센스토어 눈썰매":"87050631613",
    # "센스토어 장갑":"87085954788",
    # "센스토어 털장화":"86942365289",
    # "양봉모자": "84644315238"
}


'''
# 상품명과 ID의 딕셔너리 생성_메모장에서 불러오기
products = {}

# 파일 경로 설정
file_path = 'C:\\sellylist\\list.txt'  # 텍스트 파일의 경로를 지정

# 파일을 열고 읽기
with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        # 각 줄에서 키와 값을 분리
        key, value = line.strip().split(':')
        products[key] = value
'''


# Chrome 실행
subprocess.Popen([
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    'https://search.shopping.naver.com/home'
])

time.sleep(1)  # 페이지 로드 대기


# 딕셔너리 안에 상품수만큼 반복
for prod_nm, prod_id in products.items():
    # 상품명 검색
    pyautogui.click(x=500, y=200)  # 검색창 클릭 해상도에 따라 바뀔수있음, 위치바뀌면 아랫쪽 지우는곳도 바꿔야함.
    pyperclip.copy(prod_nm)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    pyautogui.press('enter')

    time.sleep(1)  # 검색 결과 로드 대기

    # 맨 하단 html을 받아오기 위해 스크롤
    for _ in range(5):  # 회전수
        pyautogui.scroll(-3000)  # 아래로 스크롤 (-300은 스크롤 양을 의미)
        time.sleep(0.2)  # 스크롤 간 대기 시간

    time.sleep(1)

    # 개발자도구 켜기
    pyautogui.hotkey('ctrl', 'shift', 'j')

    time.sleep(1)

    # 콘솔로 포커스 맞추기
    pyautogui.press('tab', presses=1)

    time.sleep(1)

    # JavaScript 코드 입력
    javascript_code = f"""
    const productElement = document.querySelector('a[data-i="{prod_id}"]');

    if (productElement) {{
        const rect = productElement.getBoundingClientRect();
        const topY = rect.top + window.scrollY; // 이미지 상단 Y 좌표

        // 최상단으로 스크롤
        window.scrollTo({{
            top: topY, // 이미지 상단으로 올리기
            behavior: 'smooth' // 부드러운 스크롤
        }});

        // 상단 좌표 출력
        console.log('이미지 상단 Y 좌표:', topY);
    }} else {{
        console.log('해당 이미지를 찾을 수 없습니다.');
    }}
    """

    # 클립보드에 JavaScript 코드 복사
    pyperclip.copy(javascript_code)

    # 붙여넣기
    pyautogui.hotkey('ctrl', 'v')

    # Enter 키를 눌러 실행
    pyautogui.press('enter')

    time.sleep(1)

    # 개발자도구 닫기
    pyautogui.hotkey('ctrl', 'shift', 'j')

    time.sleep(1)
    # 특정 좌표로 마우스 이동
    # pyautogui.moveTo(370, 200, duration=0.5)  # duration은 이동 시간

    base_x = 370
    base_y = 200

    # 난수 범위 설정
    offset_range = 10  # 좌우로 +-10 범위

    # 난수로 좌표 생성
    random_x = random.randint(base_x - offset_range, base_x + offset_range)
    random_y = random.randint(base_y - offset_range, base_y + offset_range)

    # 마우스를 난수 좌표로 이동
    pyautogui.moveTo(random_x, random_y, duration=0.5)

    # 상품이미지 클릭
    pyautogui.click()

    time.sleep(7200) # 상세페이지 뜨는 시간 고려해야함 다온테스트 2시간

    # 현재 탭 닫기
    pyautogui.hotkey('ctrl', 'w')

    time.sleep(1)  # 다음 검색을 위한 대기

    pyautogui.press('home')  # Home 키를 눌러 맨 위로 스크롤
    time.sleep(0.5)

    # 검색창에 포커스 및 기존검색어 지우기
    pyautogui.click(x=500, y=200)
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.5)
    pyautogui.press('delete')

'''# 반복작업이 끝나면 쿠키갱신을 위해 홈으로 복귀_랜덤작업 추가 후 종료
pyautogui.hotkey('ctrl', 'l')  # 주소창 선택
time.sleep(0.5)  # 대기 시간
pyperclip.copy('https://naver.com')  # 새 URL 복사
pyautogui.hotkey('ctrl', 'v')  # 주소창에 붙여넣기
pyautogui.press('enter')  # 엔터키로 이동'''