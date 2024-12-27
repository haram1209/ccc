import os
import shutil
import subprocess
import time

import pyautogui
import pyperclip

# VPN 정보 로드
vpn = {}
file_path = 'C:\\sellylist\\vpn_list.txt'
with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        key, value = line.strip().split(':')
        vpn[key.strip()] = value.strip()  # 키와 값에 공백이 있을 수 있으므로 제거

username = "56a7234"
password = "1234"
# Chrome 프로필 경로 및 원본 폴더 이름 설정
chrome_profile_base_path = 'C:\\Users\\pc\\AppData\\Local\\Google\\Chrome\\'
profile_source_folder = 'XX'  # 복사할 원본 프로필 폴더 이름

# 각 VPN에 대해 처리
for vpn_key in vpn.keys():
    print(f"{vpn_key} 연결 중...")
    result = subprocess.run(f'rasdial "{vpn_key}" {username} {password}', shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"{vpn_key} 연결 완료.")
        time.sleep(1)  # 연결 후 대기

        # 프로필 폴더 복사
        source_path = os.path.join(chrome_profile_base_path, profile_source_folder)
        destination_path = os.path.join(chrome_profile_base_path, vpn_key)

        # 기존 프로필 폴더가 있으면 삭제
        if os.path.exists(destination_path):
            shutil.rmtree(destination_path)

        # 폴더 복사
        shutil.copytree(source_path, destination_path)
        print(f"{profile_source_folder}에서 {vpn_key}로 프로필 복사 완료.")
        time.sleep(1)  # 복사 후 대기

        # 크롬 실행
        command = [
            'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
            f'--user-data-dir={destination_path}',  # 복사한 프로필 경로 사용
            'https://naver.com'  # 실행할 URL
        ]
        subprocess.Popen(command)
        time.sleep(5)  # 크롬 실행 후 대기

        pyautogui.hotkey('ctrl', 'shift', 'i')  # 개발자 도구 열기
        time.sleep(1)  # 열리는 시간 대기

        # JavaScript 코드 붙여넣기
        js_code = "copy(document.cookie);"
        pyperclip.copy(js_code)  # 클립보드에 JavaScript 코드 복사
        pyautogui.hotkey('ctrl', 'v')  # 붙여 넣기
        pyautogui.press('enter')  # Enter 키를 눌러 실행
        time.sleep(2)  # 검사 후 대기
        # 클립보드에서 메시지 읽기
        cookies = pyperclip.paste()
        print("추출한 쿠키:")
        print(cookies)

        # 크롬 종료 (출력 억제)
        subprocess.run("taskkill /F /IM chrome.exe", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"{vpn_key} 크롬 종료 완료.")
        time.sleep(1)  # 종료 후 대기

        # VPN 연결 종료
        subprocess.run(f'rasdial "{vpn_key}" /disconnect', shell=True, stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)
        print(f"{vpn_key} 연결 종료 완료.")
        time.sleep(1)  # 종료 후 대기

    else:
        print(f"{vpn_key} 연결 실패.")
        time.sleep(1)  # 실패 후 대기
