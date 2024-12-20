import subprocess


def create_l2tp_vpn(vpn_name, vpn_server, username, password):
    try:
        # VPN 연결 생성
        subprocess.run(
            f'netsh interface ip set address name="{vpn_name}" source=static address=192.168.1.1 mask=255.255.255.0',
            shell=True, check=True)

        # VPN 생성 명령어
        command = (
            f'netsh add vpn "{vpn_name}" "{vpn_server}" "{username}" "{password}"'
        )
        subprocess.run(command, shell=True, check=True)

        print(f"{vpn_name} VPN이 생성되었습니다.")
    except subprocess.CalledProcessError as e:
        print(f"VPN 생성 중 오류 발생")


def get_vpn_info():
    # VPN 이름과 서버 주소를 쌍으로 설정
    vpn_info = {
        "VPN_hotkyj": "59.2.206.61",
        "vpn_shinski": "119.206.68.216"
    }

    # 고정된 사용자 이름과 비밀번호
    username = "95s6199"
    password = "1234"

    return vpn_info, username, password


# VPN 정보를 가져오기
vpn_info, username, password = get_vpn_info()

for vpn_name, vpn_server in vpn_info.items():
    create_l2tp_vpn(vpn_name, vpn_server, username, password)
