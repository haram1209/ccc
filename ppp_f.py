import os
import shutil
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
        vpn[key.strip()] = value.strip()  # 키와 값에 공백이 있을 수 있으므로 제거

vpn_id = {
    "1": "95s6199",  # 맨처음구입 로컬에서 돌리던 11개
    "2": "56a7234",
}

# 커맨드라인 인자 처리
parser = argparse.ArgumentParser()
parser.add_argument('--v', choices=vpn_id.keys(), required=True, help='사용할 유저네임 번호')
args = parser.parse_args()

username = vpn_id.get(args.v.strip(','))
password = "1234"

# Firefox 프로필 경로 및 원본 폴더 이름 설정
firefox_profile_base_path = 'C:\\Users\\pc\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\'


# 현재 IP 확인 함수
def get_current_ip():
    try:
        response = requests.get("https://api.ipify.org")
        return response.text
    except requests.RequestException:
        return "IP 확인 실패"


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

            # 프로필 폴더 찾기
            source_path = None
            for folder in os.listdir(firefox_profile_base_path):
                if folder.endswith('.XX'):  # 폴더 이름이 .XX로 끝나는지 확인
                    source_path = os.path.join(firefox_profile_base_path, folder)
                    break

            if not source_path:
                print("복사할 프로필 폴더를 찾을 수 없습니다.")
                continue

            destination_path = os.path.join(firefox_profile_base_path, vpn_key)

            # 기존 프로필 폴더가 있으면 삭제
            if os.path.exists(destination_path):
                shutil.rmtree(destination_path)

            # 폴더 복사
            shutil.copytree(source_path, destination_path)
            print(f"{source_path}에서 {vpn_key}로 프로필 복사 완료.")
            time.sleep(1)  # 복사 후 대기

            # Firefox 종료
            subprocess.run("taskkill /F /IM firefox.exe", shell=True, stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
            print("Firefox 종료 완료.")

            # 프로필 매니저 실행
            subprocess.Popen(['C:\\Program Files\\Mozilla Firefox\\firefox.exe', '-P', vpn_key])
            time.sleep(5)  # 프로필 매니저 실행 후 대기

            # Firefox로 URL 열기
            command = [
                'C:\\Program Files\\Mozilla Firefox\\firefox.exe',
                '-no-remote',
                '-P', vpn_key,
                'https://naver.com'  # 실행할 URL
            ]
            subprocess.Popen(command)

            # 개발자 도구 열기
            pyautogui.hotkey('ctrl', 'shift', 'i')  # 개발자 도구 열기
            time.sleep(1)  # 열리는 시간 대기

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

            # Firefox 종료 (출력 억제)
            subprocess.run("taskkill /F /IM firefox.exe", shell=True, stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
            print(f"{vpn_key} Firefox 종료완료")
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
