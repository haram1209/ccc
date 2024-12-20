import subprocess
import time
import pyautogui
import pyperclip
import requests

# 딕셔너리 생성
products = {
    "1234": "상품1", "1235": "상품2", "1236": "상품3",
    "1237": "상품4", "1238": "상품5", "1239": "상품6",
    "1240": "상품7", "1241": "상품8", "1242": "상품9",
    "1243": "상품10", "1244": "상품11", "1245": "상품12",
    "1246": "상품13", "1247": "상품14", "1248": "상품15",
    "1249": "상품16", "1250": "상품17", "1251": "상품18",
    "1252": "상품19", "1253": "상품20"
}

vpn = {
    "hotkyj": "hotkyj",
    "jangasd112": "jangasd112",
    "leejakka23": "leejakka23"
}

username = "95s6199"
password = "1234"
max_retries = 3  # 최대 반복 횟수

while True:  # 무한 반복
    for vpn_name, profile in vpn.items():
        attempts = 0  # 시도 횟수
        max_attempts = 2  # 최대 재시도 횟수
        connected = False  # 연결 여부

        while attempts <= max_attempts:
            print(f"{vpn_name} 연결 중...")
            result = subprocess.run(f'rasdial "{vpn_name}" {username} {password}', shell=True, capture_output=True,
                                    text=True)

            if result.returncode == 0:
                print(f"{vpn_name} 연결 완료.")
                connected = True
                # 현재 IP 주소 가져오기
                try:
                    current_ip = requests.get('https://api.ipify.org').text
                    print(f"현재 IP 주소: {current_ip}")
                except Exception as e:
                    print(f"IP 주소를 가져오는 중 오류 발생: {e}")

                break  # 연결 성공 시 루프 종료

            else:
                print(f"{vpn_name} 연결 실패: {result.stderr.strip()}")
                attempts += 1
                time.sleep(10)  # 대기 후 재시도

        if connected:
            profile_path = f'C:\\Users\\hanju\\AppData\\Local\\Google\\Chrome\\{profile}'
            subprocess.Popen([
                'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
                '--user-data-dir=' + profile_path,
                'https://search.shopping.naver.com/home'
            ])

            # 각 상품을 3회 반복하여 검색
            for _ in range(3):  # 상품 검색 3회 반복
                for prod_id, prod_nms in products.items():
                    print(f"검색 중: {prod_nms}")

                    # 개발자 도구 열기
                    pyautogui.hotkey('ctrl', 'shift', 'j')
                    time.sleep(0.2)
                    time.sleep(0.5)

                    # 상품명 검색 JavaScript
                    search = f"""
                    const searchBox = document.querySelector('input._searchInput_search_text_83jy9');
                    if (searchBox) {{
                        searchBox.click();
                        searchBox.value = '{prod_nms}'; 
                        const searchButton = document.querySelector('button._searchInput_button_search_wu9xq');
                        if (searchButton) {{
                            searchButton.click();
                        }}
                    }}"""

                    pyperclip.copy(search)  # 클립보드에 JavaScript 코드 복사
                    pyautogui.hotkey('ctrl', 'v')  # 붙여넣기
                    pyautogui.press('enter')  # Enter 키를 눌러 실행
                    time.sleep(2)  # 검색 결과 로드 대기

            time.sleep(3)
            # 쿠키 갱신을 위해 NAVER로 이동
            pyautogui.hotkey('ctrl', 'l')  # 주소창 선택
            time.sleep(0.5)  # 대기 시간
            pyperclip.copy('https://naver.com')
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.press('enter')
            time.sleep(3)  # 페이지가 로딩될 수 있도록 대기

            # Chrome 종료
            print(f"{profile} 프로필 Chrome 종료 중...")
            pyautogui.hotkey('ctrl', 'w')  # 현재 탭 닫기
            time.sleep(1)  # 대기 시간

            # VPN 해제
            print(f"{vpn_name} 연결 해제 중...")
            subprocess.Popen(f'rasdial "{vpn_name}" /disconnect', shell=True)
            time.sleep(5)  # 해제 대기

        else:
            print(f"{vpn_name} 연결 실패. 5분 동안 대기합니다.")
            time.sleep(300)  # 5분 대기 후 다음 VPN으로 이동
