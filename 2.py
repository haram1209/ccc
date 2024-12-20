import subprocess
import time
import pyautogui
import pyperclip
import random
from datetime import datetime




'''
# 상품명과 ID의 딕셔너리 생성
products = {
    "화목난로 다온":"887764218390000",
    "센스토어 눈썰매":"87050631613",
    "센스토어 장갑":"87085954788",
    "센스토어 털장화":"86942365289",
    "양봉모자": "84644315238"
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



# Chrome 실행
subprocess.Popen([
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    # 특정프로필로 실행할때 경로
    '--user-data-dir=' + 'C:\\Users\\hanju\\AppData\\Local\\Google\\Chrome\\jangasd112',
    'https://search.shopping.naver.com/home'
])

time.sleep(1)


# 딕셔너리 안에 상품수만큼 반복
for prod_nm, prod_id in products.items():

    # 개발자도구 켜기
    pyautogui.hotkey('ctrl', 'shift', 'j')

    # 콘솔로 포커스 맞추기
    pyautogui.press('tab', presses=1)

    time.sleep(1)

    # 상품명 검색
    javascript_search = f"""
    const searchBox = document.querySelector('input._searchInput_search_text_83jy9');

    if (searchBox) {{
        searchBox.click();
        searchBox.value = '{prod_nm}'; 

        const searchButton = document.querySelector('button._searchInput_button_search_wu9xq');
        if (searchButton) {{
            searchButton.click();
            }}else {{
            console.log("검색 버튼을 찾을 수 없습니다.");
        }}
    }} else {{
        console.log("검색창을 찾을 수 없습니다.");
    }}
    """

    # 클립보드에 JavaScript 코드 복사
    pyperclip.copy(javascript_search)

    # 붙여넣기
    pyautogui.hotkey('ctrl', 'v')

    # Enter 키를 눌러 실행
    pyautogui.press('enter')

    # 검색 결과 로드 대기
    time.sleep(2)


    # 하단으로 스크롤하는 JavaScript 코드 5번 반복
    for _ in range(5):
        javascript_scroll = """
            window.scrollTo({
                top: document.body.scrollHeight,
                behavior: 'smooth'
            });
            """

        # 클립보드에 스크롤 JavaScript 코드 복사
        pyperclip.copy(javascript_scroll)

        # 붙여넣기
        pyautogui.hotkey('ctrl', 'v')

        # Enter 키를 눌러 실행
        pyautogui.press('enter')

        # 각 스크롤 사이 대기 시간
        time.sleep(0.5)



    time.sleep(2)

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
        console.log('성공:', topY);
        
        
    }} else {{
        console.log('실패');
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


    #클릭할 좌표로 이동
    base_x = 370
    base_y = 170

    # 난수 범위 설정
    offset_range = 25

    # 난수로 좌표 생성
    random_x = random.randint(base_x - offset_range, base_x + offset_range)
    random_y = random.randint(base_y - offset_range, base_y + offset_range)
    # 마우스 최대한 자연스럽게
    def human_click(x, y):
        # 부드럽게 이동 0.3초에서 0.7초 사이의 랜덤한 시간
        pyautogui.moveTo(x, y, duration=random.uniform(0.3, 0.7))
        # 클릭 전에 약간의 대기
        time.sleep(random.uniform(0.1, 0.3))
        pyautogui.click()
    human_click(random_x, random_y)

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"성공: ({current_time} : {prod_nm} : {prod_id})")


    # 상세페이지 뜨는 시간 고려해야함 다온테스트 2시간
    time.sleep(4)

    # 현재 탭 닫기
    pyautogui.hotkey('ctrl', 'w')

    # 다음 검색을 위한 대기
    time.sleep(1)

    # Home 키를 눌러 맨 위로 스크롤
    pyautogui.press('home')

    time.sleep(0.5)



# 반복작업이 끝나면 쿠키갱신을 위해 홈으로 복귀_랜덤작업 추가 후 종료
pyautogui.hotkey('ctrl', 'l')  # 주소창 선택
time.sleep(0.5)  # 대기 시간
pyperclip.copy('https://naver.com')
pyautogui.hotkey('ctrl', 'v')
pyautogui.press('enter')