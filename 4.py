import subprocess
import time
import pyautogui
import pyperclip
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

# 상품명과 ID의 딕셔너리 생성
products = {
    "눈썰매 센스토어": "87050631842",
    "로봇청소기": ("48167201619", "48168122525"),
    "센스토어 눈썰매": "87050631842"
}

def run_script():
    # Chrome 실행
    subprocess.Popen([
        'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
        # 특정프로필로 실행할때 경로
        # '--user-data-dir=' + 'C:\\Users\\hanju\\AppData\\Local\\Google\\Chrome\\jangasd112',
        'https://search.shopping.naver.com/home'
    ])

    time.sleep(1)

    for prod_nm, prod_ids in products.items():
        if isinstance(prod_ids, str):
            prod_ids = (prod_ids,)

        # 개발자 도구 열기
        pyautogui.hotkey('ctrl', 'shift', 'j')
        pyautogui.press('tab')
        time.sleep(1)

        # 상품명 검색
        javascript_search = f"""
        const searchBox = document.querySelector('input._searchInput_search_text_83jy9');
        if (searchBox) {{
            searchBox.click();
            searchBox.value = '{prod_nm}'; 
            const searchButton = document.querySelector('button._searchInput_button_search_wu9xq');
            if (searchButton) {{
                searchButton.click();
                }}else {{
                console.log("검색 버튼을 찾을 수 없습니다.");
            }}
        }} else {{
            console.log("검색창을 찾을 수 없습니다.");
        }}
        """
        pyperclip.copy(javascript_search)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')
        time.sleep(2)

        # 스크롤 처리
        for _ in range(5):
            javascript_scroll = """
                        window.scrollTo({
                            top: document.body.scrollHeight,
                            behavior: 'smooth'
                        });
                        """
            pyperclip.copy(javascript_scroll)
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.press('enter')
            time.sleep(0.5)

        # 상품 클릭
        for index, prod_id in enumerate(prod_ids):
            javascript_code = f"""
                    const productElement = document.querySelector('a[data-i="{prod_id}"]');
                    if (productElement) {{
                        const rect = productElement.getBoundingClientRect();
                        const topY = rect.top + window.scrollY; // 이미지 상단 Y 좌표
                        // 최상단으로 스크롤
                        window.scrollTo({{
                            top: topY, // 이미지 상단으로 올리기
                            behavior: 'smooth' // 부드러운 스크롤
                        }});
                        // 상단 좌표 출력
                        console.log('성공:', topY);
                        setTimeout(() => {{
                            productElement.click();
                            console.log('클릭했습니다.');
                        }}, 1000); // 1000ms = 1초
                    }} else {{
                        console.log('실패');
                    }}
                    """
            pyperclip.copy(javascript_code)
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.press('enter')
            # ID가 두 개일 때 새 창에서 개발자 도구 열기
            if len(prod_ids) > 1 and index == 0:
                time.sleep(3)  # 새 창 로드 대기
                pyautogui.hotkey('ctrl', 'shift', 'j')  # 새 창에서 개발자 도구 켜기
                pyautogui.press('tab', presses=1)  # 콘솔로 포커스 맞추기
                time.sleep(1)

                # 두 번째 ID에 대해 JavaScript 코드 다시 실행
                javascript_code_second = f"""
                                const productElement = document.querySelector('a[data-i="{prod_ids[1]}"]');

                                if (productElement) {{
                                    const rect = productElement.getBoundingClientRect();
                                    const topY = rect.top + window.scrollY; // 이미지 상단 Y 좌표

                                    // 최상단으로 스크롤
                                    window.scrollTo({{
                                        top: topY, // 이미지 상단으로 올리기
                                        behavior: 'smooth' // 부드러운 스크롤
                                    }});

                                    // 상단 좌표 출력
                                    console.log('성공:', topY);

                                    setTimeout(() => {{
                                        productElement.click();
                                        console.log('클릭했습니다.');
                                    }}, 1000); // 1000ms = 1초

                                }} else {{
                                    console.log('실패');
                                }}
                                """

                # 클립보드에 두 번째 JavaScript 코드 복사
                pyperclip.copy(javascript_code_second)

                # 붙여넣기
                pyautogui.hotkey('ctrl', 'v')

                # Enter 키를 눌러 실행
                pyautogui.press('enter')

                # 상세페이지 뜨는 시간 고려해야함 다온테스트 2시간
                time.sleep(10)

                # 두 개의 새 탭 닫기
                pyautogui.hotkey('ctrl', 'w')  # 첫 번째 탭 닫기
                time.sleep(0.5)  # 잠시 대기
                pyautogui.hotkey('ctrl', 'w')  # 두 번째 탭 닫기

            elif len(prod_ids) == 1:
                # 하나의 ID일 때 탭 닫기
                time.sleep(1)  # 클릭 후 대기
                pyautogui.hotkey('ctrl', 'w')  # 탭 닫기

            time.sleep(1)

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"성공: ({current_time} : {prod_nm})")


    # 홈으로 돌아가기
    pyautogui.hotkey('ctrl', 'l')
    time.sleep(0.5)
    pyperclip.copy('https://naver.com')
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')

def start_process():
    try:
        run_script()
        messagebox.showinfo("완료", "작업이 완료되었습니다.")
    except Exception as e:
        messagebox.showerror("오류", str(e))

# UI 설정
root = tk.Tk()
root.title("상품 검색 자동화")

start_button = tk.Button(root, text="검색 시작", command=start_process)
start_button.pack(pady=20)

exit_button = tk.Button(root, text="종료", command=root.quit)
exit_button.pack(pady=20)

root.mainloop()