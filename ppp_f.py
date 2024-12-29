import subprocess
import time
import pyautogui
import pyperclip
import requests
import argparse

# VPN 정보 로드
vpn = {}
file_path = 'C:\\sellylist\\vpn_list.txt'
with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        key, value = line.strip().split(':')
        vpn[key.strip()] = value.strip()

vpn_id = {
    "1": "95s6199",
    "2": "56a7234",
}

# 커맨드라인 인자 처리
parser = argparse.ArgumentParser()
parser.add_argument('--v', choices=vpn_id.keys(), required=True, help='사용할 유저네임 번호')
args = parser.parse_args()

username = vpn_id.get(args.v.strip(','))
password = "1234"

# Firefox의 프로필 기본 경로
firefox_profile_base_path = 'C:\\Users\\pc\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\'


# 현재 IP 확인 함수
def get_current_ip():
    try:
        response = requests.get("https://api.ipify.org")
        return response.text
    except requests.RequestException:
        return "IP 확인 실패"


# Firefox 프로필 생성
def create_firefox_profile(profile_name):
    command1 = [
        'C:\\Program Files\\Mozilla Firefox\\firefox.exe',
        '-no-remote',
        '-CreateProfile',
        profile_name
    ]
    subprocess.run(command1)
    time.sleep(2)


# 각 VPN에 대해 처리
for vpn_key in vpn.keys():
    for attempt in range(3):  # 최대 3회 재시도
        print(f"{vpn_key} 연결 중... (시도 {attempt + 1}/3)")
        result = subprocess.run(f'rasdial "{vpn_key}" {username} {password}', shell=True, capture_output=True,
                                text=True)

        if result.returncode == 0:
            print(f"{vpn_key} 연결 완료.")
            current_ip = get_current_ip()  # 현재 IP 확인
            print(f"현재 IP: {current_ip}")
            time.sleep(1)  # 연결 후 대기

            # 새로운 프로필 이름 설정
            profile_name = vpn_key  # VPN 키를 프로필 이름으로 사용
            create_firefox_profile(profile_name)  # 프로필 생성

            # Firefox 실행
            command = [
                'C:\\Program Files\\Mozilla Firefox\\firefox.exe',
                '-no-remote',
                '-P', profile_name,
                'https://naver.com'  # 실행할 URL
            ]
            subprocess.Popen(command)
            time.sleep(5)  # Firefox 실행 후 대기

            # 개발자 도구 열기
            pyautogui.hotkey('ctrl', 'shift', 'i')  # 개발자 도구 열기
            time.sleep(1)

            # JavaScript 코드 붙여넣기
            js_code = "copy(document.cookie);"
            pyperclip.copy(js_code)  # 클립보드에 JavaScript 코드 복사
            pyautogui.hotkey('ctrl', 'v')  # 붙여넣기
            time.sleep(1)
            pyautogui.press('enter')  # Enter 키를 눌러 실행
            time.sleep(2)  # 검사 후 대기

            # 클립보드에서 쿠키 읽기
            try:
                cookies = pyperclip.paste()
                if cookies:
                    print("추출한 쿠키:")
                    print(cookies)
                else:
                    print("쿠키를 수집할 수 없습니다. 클립보드가 비어 있습니다.")
            except Exception as e:
                print(f"클립보드 접근 중 오류 발생: {e}")

            # Firefox 종료
            subprocess.run("taskkill /F /IM firefox.exe", shell=True, stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
            print(f"{vpn_key} Firefox 종료 완료")
            time.sleep(1)  # 종료 후 대기

            # VPN 연결 종료
            subprocess.run(f'rasdial "{vpn_key}" /disconnect', shell=True, stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
            print(f"{vpn_key} 연결 종료 완료.")
            time.sleep(1)  # 종료 후 대기

            break  # 연결 성공 시 루프 종료

        else:
            print(f"{vpn_key} 연결 실패.")
            time.sleep(1)  # 실패 후 대기

    else:
        print(f"{vpn_key} 연결이 3회 시도 후 실패했습니다.")
