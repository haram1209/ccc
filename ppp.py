import os
import shutil
import subprocess
import time
import argparse

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
    # VPN 연결
    print(f"{vpn_key} 연결 중...")
    result = subprocess.run(f'rasdial "{vpn_key}" {username} {password}', shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"{vpn_key} 연결 완료.")

        # 프로필 폴더 복사
        source_path = os.path.join(chrome_profile_base_path, profile_source_folder)
        destination_path = os.path.join(chrome_profile_base_path, vpn_key)

        # 기존 프로필 폴더가 있으면 삭제
        if os.path.exists(destination_path):
            shutil.rmtree(destination_path)

        # 폴더 복사
        shutil.copytree(source_path, destination_path)
        print(f"{profile_source_folder}에서 {vpn_key}로 프로필 복사 완료.")

        # 크롬 실행
        command = [
            'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
            f'--user-data-dir={chrome_profile_base_path}',
            f'--profile-directory={vpn_key}',
            'https://daum.net'  # 실행할 URL
        ]
        subprocess.Popen(command)

        # 5초 대기 후 크롬 종료
        time.sleep(5)
        # 크롬 종료
        os.system("taskkill /F /IM chrome.exe")

    else:
        print(f"{vpn_key} 연결 실패: {result.stderr.strip()}")
