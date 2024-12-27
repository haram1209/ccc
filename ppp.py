import os
import shutil
import subprocess
import argparse

# 명령줄 인자 처리
parser = argparse.ArgumentParser(description="VPN 연결 및 Chrome 프로필 설정 스크립트")
parser.add_argument("--v", required=True)
args = parser.parse_args()

# VPN 정보 로드
vpn = {}
file_path = 'C:\\sellylist\\vpn_list.txt'  # VPN 정보를 저장한 텍스트 파일의 경로

with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        # 줄을 ':'로 나누어 키와 값을 분리
        key, value = line.strip().split(':')
        vpn[key.strip()] = value.strip()  # 키와 값에 공백이 있을 수 있으므로 제거

# VPN 이름과 프로필 폴더명 설정
vpn_names = [str(i) for i in range(1, 12)]  # 1~11
chrome_profile_base_path = 'C:\\Users\\pc\\AppData\\Local\\Google\\Chrome\\'  # 기본 프로필 경로
profile_source_folder = 'XX'  # 복사할 원본 프로필 폴더 이름

# 각 VPN에 대해 처리
for vpn_key in vpn_names:
    # VPN 연결
    vpn_id = {
        "1": "95s6199",  # 맨처음구입 로컬에서 돌리던 11개
        "2": "56a7234",
    }

    username = vpn_id.get(args.v.strip(','))
    password = "1234"

    print(f"{vpn_key} 연결 중...")
    result = subprocess.run(f'rasdial "{vpn_key}" {username} {password}', shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"{vpn_key} 연결 완료.")

        # 프로필 폴더 복사
        source_path = os.path.join(chrome_profile_base_path, profile_source_folder)
        destination_path = os.path.join(chrome_profile_base_path, vpn_key)

        # 프로필 폴더가 존재하는지 확인
        if not os.path.exists(source_path):
            print(f"원본 프로필 폴더가 존재하지 않습니다: {source_path}")
            continue  # 루프를 계속 진행

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

        # 여기에 필요한 추가 작업 코드를 작성하세요.

    else:
        print(f"{vpn_key} 연결 실패: {result.stderr.strip()}")

    # 추가적인 대기 시간이나 다른 작업이 필요할 수 있습니다.
