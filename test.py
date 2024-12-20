import subprocess
import time
import pyautogui
import pyperclip
import requests

# 딕셔너리 생성
products = {
    ("49366793749", "88178683251"): ["옷가게 멀티행거", "멀티행거 옷가게", "옷가게행거 멀티"],
    "87019033271": ["여자 센스토어", "센스토어 여자"],
    "87664075691": ["다온 휴양지원피스", "휴양지원피스 다온"],
    "82161110381": ["아크로스토어 거실장", "거실장 아크로스토어"],
    "85835596604": "premier 쓰레기통",
    "87643118570": "더하루 쓰레기통",
    "84296352614": "황진 신발보관장",
    "83559129009": "미니 뒷목마사지",
    "87591583178": "강한 밀봉집게",
    "83883525220": "헬멧이너두건",
    "88600353865": "MMJ  커튼",
    "87833604868": "위콘23 선풍기"
}

vpn = {
    "hotkyj": "111",
    "jangasd112": "222",
    "leejakka23": "333"
}

username = "95s6199"
password = "1234"

num_products_per_vpn = 3  # 각 VPN 당 검색할 상품 수
total_products = len(products)  # 총 상품 수
product_ids = list(products.keys())  # 상품 ID 리스트
current_index = 0  # 상품 인덱스 초기화

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
            time.sleep(1)  # 페이지 로드 대기

            # 개발자 도구 열기
            pyautogui.hotkey('ctrl', 'shift', 'j')  # 개발자도구 켜기
            time.sleep(0.5)

            # 현재 인덱스를 기준으로 상품 검색
            indices_to_search = []
            for j in range(num_products_per_vpn):
                indices_to_search.append(product_ids[(current_index + j) % total_products])

            # 각 상품 검색
            for prod_ids in indices_to_search:
                prod_nms = products[prod_ids]
                print(f"검색 중: {prod_nms}")

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
            # 반복작업이 끝나면 쿠키갱신을 위해 홈으로 복귀
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

            # 인덱스 업데이트
            current_index = (current_index + num_products_per_vpn) % total_products

        else:
            print(f"{vpn_name} 연결 실패. 5분 동안 대기합니다.")
            time.sleep(300)  # 5분 대기 후 다음 VPN으로 이동
