import subprocess
import pyautogui
import pyperclip
import time

subprocess.Popen([
    'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
    # '--user-data-dir=' + 'C:\\Users\\hanju\\AppData\\Local\\Google\\Chrome\\2222',
    # '--user-agent=' + mobile_user_agent,  # 모바일 사용자 에이전트 적용
    # '--window-size=1000,1000',  # iPhone 6/7/8 크기
    # '--disable-infobars',  # 정보 바 비활성화
    # '--auto-open-devtools-for-tabs',  # 개발자 도구 자동 열기
    'https://search.shopping.naver.com/home'  # 열 URL
])

time.sleep(2)

pyautogui.hotkey('ctrl', 'shift', 'j')  # 개발자도구 켜기
time.sleep(0.2)
pyautogui.press('tab', presses=1)  # 콘솔로 포커스 맞추기

time.sleep(0.5)

search = f"""
            const searchBox = document.querySelector('input._searchInput_search_text_83jy9');
            if (searchBox) {{
                searchBox.click();
                searchBox.value = '1234'; 
                const searchButton = document.querySelector('button._searchInput_button_search_wu9xq');
                if (searchButton) {{
                    searchButton.click();
                }}
            }}"""

pyperclip.copy(search)  # 클립보드에 JavaScript 코드 복사
pyautogui.hotkey('ctrl', 'v')  # 붙여넣기
pyautogui.press('enter')  # Enter 키를 눌러 실행
time.sleep(2)  # 검색 결과 로드 대기

# 하단으로 스크롤하는 JavaScript 코드 5번 반복
for _ in range(5):
    scroll = """
        window.scrollTo({
            top: document.body.scrollHeight,
            behavior: 'smooth'
        });
        """
    pyperclip.copy(scroll)  # 클립보드에 스크롤 JavaScript 코드 복사
    pyautogui.hotkey('ctrl', 'v')  # 붙여 넣기
    pyautogui.press('enter')  # Enter 키를 눌러 실행
    time.sleep(0.5)  # 각 스크롤 사이 대기 시간
time.sleep(1)
