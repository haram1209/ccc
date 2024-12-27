import argparse
import random
import subprocess
import time
from time import sleep
import pyautogui
import pyperclip
from datetime import datetime
import requests

# 딕셔너리 생성
# products = {
#     ("49366793749", "88178683251"): ["옷가게 멀티행거", "멀티행거 옷가게", "옷가게행거 멀티"],
#     "87019033271": ["여자 센스토어", "센스토어 여자"],
#     "87664075691": ["다온 휴양지원피스", "휴양지원피스 다온"],
#     "82161110381": ["아크로스토어 거실장", "거실장 아크로스토어"],
# }

# 딕셔너리 생성_메모장에서 불러오기
products = {}
file_path = 'C:\\sellylist\\list.txt'  # 텍스트 파일의 경로를 지정

with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        # 줄을 ':'로 나누어 키와 값을 분리
        key, value = line.strip().split(':')

        # 키가 튜플인지 확인하고 변환
        if ',' in key:
            # 키를 튜플로 변환
            key = tuple(key.split(','))

        # 값이 여러 개이면 리스트로 변환
        if ',' in value:
            products[key] = list(value.split(','))
        else:
            products[key] = [value]  # 하나의 상품명도 리스트로 저장

# vpn = {
#
#     "jjun042204": "111",
#     "hotkyj": "222",
#     "jjy5627": "333",
#     "onirac1104": "444",
#     "shinski": "555",  # 08:40 나옴
#     "glckhj": "666",
#     "humming_box": "777",
#     "seokhwan81": "888",
#     "jangasd112": "999",
#     "leejakka23": "101010",
#     # "ddvrof": "lii02iil"
# }
# chrome --user-data-dir="C:\Users\hanju\AppData\Local\Google\Chrome\1111"
# whale --user-data-dir="C:\Users\hanju\AppData\Local\Naver\Naver Whale\seokhwan81"
# msedge --user-data-dir="C:\\Users\\hanju\\AppData\\Local\\Microsoft\\Edge\\11"

vpn = {}
file_path = 'C:\\sellylist\\vpn_list.txt'  # VPN 정보를 저장한 텍스트 파일의 경로

with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        # 줄을 ':'로 나누어 키와 값을 분리
        key, value = line.strip().split(':')
        vpn[key.strip()] = value.strip()  # 키와 값에 공백이 있을 수 있으므로 제거

# 명령줄 인자 처리
parser = argparse.ArgumentParser(description="VPN 연결 스크립트")
parser.add_argument("--name", required=True, help="사용할 계정을 지정 (1~20)")
parser.add_argument("--agent", required=True, help="사용할 user-agent를 지정 (0은 user-agent 미사용)")
args = parser.parse_args()

vpn_id = {
    "1": "95s6199",  # 맨처음구입 로컬에서 돌리던 11개
    "2": "56a7234",
}

username = vpn_id.get(args.name.strip(','))
password = "1234"

num_products_per_vpn = 30  # 각 VPN 당 처리할 상품 수
total_products = len(products)
product_ids = list(products.keys())  # 상품 ID 리스트
current_index = 0  # 상품 인덱스 초기화

while True:  # 무한 반복 사용할때는 아랫부분 전체 들여쓰기 할것
    for vpn_key, profile in vpn.items():
        attempts = 0  # 시도 횟수
        max_attempts = 2  # 최대 재시도 횟수
        connected = False  # 연결 여부

        while attempts <= max_attempts:
            print(f"{vpn_key} 연결 중...")
            result = subprocess.run(f'rasdial "{vpn_key}" {username} {password}', shell=True, capture_output=True,
                                    text=True)

            if result.returncode == 0:
                print(f"{vpn_key} 연결 완료.")
                connected = True
                # 현재 IP 주소 가져오기
                try:
                    current_ip = requests.get('https://api.ipify.org').text
                    print(f"현재 IP 주소: {current_ip}")
                    sleep(1)
                except Exception as e:
                    print(f"IP 주소를 가져오는 중 오류 발생: {e}")
                break  # 연결 성공 시 루프 종료

            else:
                print(f"{vpn_key} 연결 실패: {result.stderr.strip()}")
                attempts += 1
                time.sleep(10)  # 대기 후 재시도

        if connected:
            # agent 값 검증 및 설정
            user_agents = {
                "130": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
                "128": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            }
            try:
                agent_value = int(args.agent)
            except ValueError:
                raise ValueError("agent 값은 정수여야 합니다.")

            # agent 값 검증
            if agent_value not in range(0, 200):
                raise ValueError("지원되지 않는 agent 값입니다. 0~200 사이의 정수를 입력하세요.")

            # user-agent 가져오기 (0이면 None)
            user_agent = user_agents.get(str(agent_value), None) if agent_value != 0 else None

            print(f"사용할 User-Agent: {user_agent}")

            profile_path = f'C:\\Users\\pc\\AppData\\Local\\Google\\Chrome\\{profile}'  # 크롬
            # profile_path = f'C:\\Users\\hanju\\AppData\\Local\\Naver\\Naver Whale\\{profile}'  # 웨일
            # profile_path = f'C:\\Users\\hanju\\AppData\\Local\\Microsoft\\Edge\\{profile}'  # 엣지 엣지일 경우 개발자도구 포커스 맞추기 켜야함
            command = [
                'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',  # 크롬 실행 파일 경로
                '--user-data-dir=' + profile_path,  # 사용자 데이터 디렉토리
                'https://search.shopping.naver.com/home'  # 실행할 URL
            ]
            time.sleep(100)
            # user-agent 추가 (0이 아닌 경우에만)
            if user_agent:
                command.insert(2, '--user-agent=' + user_agent)

            # 브라우저 실행
            subprocess.Popen(command)
            time.sleep(1)

            pyautogui.hotkey('ctrl', 'shift', 'j')  # 개발자도구 켜기
            time.sleep(0.2)
            # pyautogui.press('tab', presses=1)  # 콘솔로 포커스 맞추기
            time.sleep(0.5)

            # 기존코드 딕셔너리 안에 상품수만큼 반복
            # for prod_ids, prod_nms in products.items():
            #     random_nm = random.choice(prod_nms)
            #     if isinstance(prod_ids, str):
            #         prod_ids = (prod_ids,)  # prod_ids가 문자열인지 튜플인지 확인 문자열을 튜플로 변환

            # 현재 인덱스를 기준으로 상품 검색
            indices_to_search = []
            for j in range(num_products_per_vpn):
                indices_to_search.append(product_ids[(current_index + j) % total_products])

            for prod_ids in indices_to_search:
                prod_nms = products[prod_ids]
                random_nm = random.choice(prod_nms)
                if isinstance(prod_ids, str):
                    prod_ids = (prod_ids,)  # prod_ids가 문자열인지 튜플인지 확인 문자열을 튜플로 변환
                # 상품명 검색
                search = f"""
                const searchBox = document.querySelector('input._searchInput_search_text_83jy9');
                if (searchBox) {{
                    searchBox.click();
                    searchBox.value = '{random_nm}'; 
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

                # JavaScript 코드 입력
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                for index, prod_id in enumerate(prod_ids):
                    check = f"""
                        const productElement = document.querySelector('a[data-i="{prod_ids[0]}"]');
                        let message;   
                        if (productElement) {{
                            message = 'true';
                        }} else {{
                            message = 'false';
                        }}
                        const tempTextarea = document.createElement('textarea');
                        tempTextarea.value = message; 
                        document.body.appendChild(tempTextarea); 
                        tempTextarea.select();
                        tempTextarea.setSelectionRange(0, 99999); 
                        document.execCommand('copy'); 
                        document.body.removeChild(tempTextarea);
                        """
                    pyperclip.copy(check)  # 클립보드에 JavaScript 코드 복사
                    pyautogui.hotkey('ctrl', 'v')  # 붙여 넣기
                    pyautogui.press('enter')  # Enter 키를 눌러 실행
                    time.sleep(2)  # 검사 후 대기
                    # 클립보드에서 메시지 읽기
                    message = pyperclip.paste()

                    # 요소 발견 여부에 따라 처리
                    if message == 'true':
                        click1 = f"""
                            const productElement = document.querySelector('a[data-i="{prod_ids[0]}"]');
                            const rect = productElement.getBoundingClientRect();
                            const topY = rect.top + window.scrollY;
                            window.scrollTo({{
                                top: topY,
                                behavior: 'smooth'
                            }});
                            setTimeout(() => {{
                                productElement.click();
                            }}, 1000); // 1000ms = 1초
                        """

                        pyperclip.copy(click1)  # 클립보드에 클릭 JavaScript 코드 복사
                        pyautogui.hotkey('ctrl', 'v')  # 붙여넣기
                        pyautogui.press('enter')  # Enter 키를 눌러 실행
                        if len(prod_ids) == 1:
                            print(f"{current_time} : {prod_ids[0]} : {random_nm} 클릭완료.")
                        time.sleep(2)  # 클릭 후 대기


                    else:
                        time.sleep(1)
                        print(f"{current_time} : {prod_ids[0]} : {random_nm} 못찾음. 다음 상품으로 진행합니다.")
                        # pyautogui.hotkey('ctrl', 'shift', 'j')
                        time.sleep(1)
                        break  # 다음 상품으로 넘어가기 위해 루프 종료

                    # 카탈로그일때 때 새 탭에서 개발자 도구 열기
                    if len(prod_ids) > 1:
                        time.sleep(3)  # 새 창 로드 대기
                        # pyautogui.hotkey('ctrl', 'shift', 'j')  # 새 탭에서 개발자 도구 켜기
                        # time.sleep(0.2)
                        # pyautogui.press('tab', presses=1)  # 콘솔로 포커스 맞추기
                        # time.sleep(0.5)
                        # 카탈로그 안에서 상품클릭
                        check2 = f"""
                            const productElement = document.querySelector('a[data-i="{prod_ids[1]}"]');
                            let message;

                            if (productElement) {{
                                message = 'true2';
                            }} else {{
                                message = 'false2';
                            }}
                            const tempTextarea = document.createElement('textarea');
                            tempTextarea.value = message; 
                            document.body.appendChild(tempTextarea); 
                            tempTextarea.select();
                            tempTextarea.setSelectionRange(0, 99999); 
                            document.execCommand('copy'); 
                            document.body.removeChild(tempTextarea);
                                """
                        pyperclip.copy(check2)  # 클립보드에 JavaScript 코드 복사
                        pyautogui.hotkey('ctrl', 'v')  # 붙여 넣기
                        pyautogui.press('enter')  # Enter 키를 눌러 실행
                        time.sleep(2)  # 검사 후 대기
                        # 클립보드에서 메시지 읽기
                        message = pyperclip.paste()

                        # 요소 발견 여부에 따라 처리
                        if message == 'true2':
                            click2 = f"""
                                const productElement = document.querySelector('a[data-i="{prod_ids[1]}"]');
                                const rect = productElement.getBoundingClientRect();
                                const topY = rect.top + window.scrollY;
                                window.scrollTo({{
                                    top: topY,
                                    behavior: 'smooth'
                                }});
                                setTimeout(() => {{
                                    productElement.click();
                                }}, 1000); // 1000ms = 1초
                            """

                            pyperclip.copy(click2)  # 클립보드에 클릭 JavaScript 코드 복사
                            pyautogui.hotkey('ctrl', 'v')  # 붙여넣기
                            pyautogui.press('enter')  # Enter 키를 눌러 실행
                            print(f"{current_time} : 카탈로그 : {prod_ids[1]} : {random_nm} 클릭완료.")
                            time.sleep(2)  # 클릭 후 대기


                        else:
                            time.sleep(1)
                            print(f"{current_time} : 카탈로그 : {prod_ids[1]} : {random_nm} 못찾음. 다음 상품으로 진행합니다.")
                            # pyautogui.hotkey('ctrl', 'shift', 'j')
                            time.sleep(1)
                            break  # 다음 상품으로 넘어가기 위해 루프 종료

                        # 카탈로그 상세페이지 열고 대기
                        time.sleep(6)

                        pyautogui.hotkey('ctrl', 'w')  # 첫 번째 탭 닫기
                        time.sleep(0.5)  # 잠시 대기
                        pyautogui.hotkey('ctrl', 'w')  # 두 번째 탭 닫기
                        time.sleep(0.5)
                        # pyautogui.hotkey('ctrl', 'shift', 'j')
                        break

                    elif len(prod_ids) == 1:
                        # 단일상품 탭 닫기
                        time.sleep(5)  # 단일상품 상세페이지 열고 대기
                        pyautogui.hotkey('ctrl', 'w')  # 탭 닫기
                        time.sleep(0.5)
                        # pyautogui.hotkey('ctrl', 'shift', 'j')
                        time.sleep(1)
                        break

            # 반복작업이 끝나면 쿠키갱신을 위해 홈으로 복귀_랜덤작업 추가 후 종료
            pyautogui.hotkey('ctrl', 'shift', 'j')  # 개발자도구 끄기
            time.sleep(0.5)
            pyautogui.hotkey('ctrl', 'l')  # 주소창 선택
            time.sleep(0.5)  # 대기 시간
            pyperclip.copy('https://naver.com')
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.press('enter')
            # NAVER 페이지 로딩 대기
            time.sleep(5)  # 페이지가 로딩될 수 있도록 대기

            # Chrome 종료
            print(f"{profile} 프로필 Chrome 종료 중...")
            pyautogui.hotkey('ctrl', 'w')  # 현재 탭 닫기
            time.sleep(5)  # 대기 시간

            # VPN 해제 시도
            print(f"{vpn_key} 연결 해제 중...")
            disconnect_success = False

            for _ in range(3):  # 3번 시도
                disconnect_result = subprocess.run(f'rasdial "{vpn_key}" /disconnect', shell=True, capture_output=True,
                                                   text=True)
                if disconnect_result.returncode == 0:
                    print(f"{vpn_key} 연결 해제 완료.")
                    disconnect_success = True
                    time.sleep(120)  # 상품이 얼마 없어서 50분 쉬도록 세팅
                    break  # 해제 성공 시 루프 종료

                print(f"{vpn_key} 연결 해제 실패: {disconnect_result.stderr.strip()}")
                time.sleep(10)  # 10초 대기 후 재시도
            if not disconnect_success:
                print(f"{vpn_key} 연결 해제를 3번 시도했으나 실패했습니다. 프로그램을 종료합니다.")
                exit(1)  # 프로그램 종료

            current_index = (current_index + num_products_per_vpn) % total_products

        else:
            print(f"{vpn_key} 연결 실패. 9분 동안 대기합니다.")
            time.sleep(1200)  # 9분 대기 후 다음 VPN으로 이동, 지금은 상품이 얼마없어서 20분 쉬도록 세팅
            current_index = (current_index + num_products_per_vpn) % total_products
