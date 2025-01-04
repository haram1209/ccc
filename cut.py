import pandas as pd

# 엑셀 파일에서 데이터 불러오기
file_path = r'C:\test\test.xlsx'  # 엑셀 파일 경로
df = pd.read_excel(file_path)

# 열 이름 명확히 지정
df.columns = ['상품코드', '몰코드', '키워드']  # 열 이름 설정

# NaN 값 제거
df = df.dropna(subset=['상품코드'])  # '상품코드'에서 NaN 값을 포함한 행 제거

# 최대 중복 수 설정
max_duplicates = 5  # 예: 최대 5개 중복 허용

# 중복 제한
df_limited = df.groupby('상품코드').head(max_duplicates).reset_index(drop=True)

# 결과를 엑셀 파일로 저장
output_file_path = r'C:\test\cut.xlsx'  # 출력 파일 경로
df_limited.to_excel(output_file_path, index=False)

print(f"중복이 제한된 데이터가 {output_file_path}에 저장되었습니다.")
