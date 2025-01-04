import pandas as pd
import random

# 엑셀 파일에서 데이터 불러오기
file_path = r'C:\test\test.xlsx'  # 엑셀 파일 경로
df = pd.read_excel(file_path)

# 열 이름 명확히 지정
df.columns = ['상품코드', '몰코드', '키워드']  # 열 이름 설정

# NaN 값 제거
df = df.dropna(subset=['상품코드'])  # '상품코드'에서 NaN 값을 포함한 행 제거

# 상품 코드의 최대 중복 수 계산
value_counts = df['상품코드'].value_counts()
max_count = value_counts.max()  # 최대 중복 수

# 키워드를 임의로 가져오기
keywords = df['키워드'].dropna().unique().tolist()  # 키워드 리스트

# 저장소 초기화 (최대 갯수를 330으로 설정)
max_storage_size = 330
storage = {i: [] for i in range(1, max_count + 1)}

# 몰코드 출현 횟수 관리
molkode_counts = {i: {} for i in range(1, max_count + 1)}

# 포함되지 못한 파일 갯수
not_stored_count = 0
not_stored_data = []  # 포함되지 못한 데이터 저장

# 중복 데이터 우선 분배
duplicate_data = df[df.duplicated(subset=['상품코드'], keep=False)]
non_duplicate_data = df[~df.duplicated(subset=['상품코드'], keep=False)]

# 몰코드로 그룹화하여 카운트
molkode_grouped = df.groupby(['몰코드']).size().reset_index(name='카운트')
molkode_grouped = molkode_grouped.sort_values(by='카운트', ascending=False)  # 카운트 기준 내림차순 정렬

# 중복 데이터 나누기
for _, row in duplicate_data.iterrows():
    stored = False
    for storage_index in range(1, max_count + 1):
        if len(storage[storage_index]) < max_storage_size:
            if row['상품코드'] not in [item['상품코드'] for item in storage[storage_index]]:
                current_molkode_count = molkode_counts[storage_index].get(row['몰코드'], 0)
                if current_molkode_count < 22:
                    storage[storage_index].append({
                        '상품코드': row['상품코드'],
                        '몰코드': row['몰코드'],
                        '키워드': row['키워드'],
                        '중복횟수': value_counts[row['상품코드']]
                    })
                    molkode_counts[storage_index][row['몰코드']] = current_molkode_count + 1
                    stored = True
                    break
    if not stored:
        not_stored_count += 1
        not_stored_data.append({
            '상품코드': row['상품코드'],
            '몰코드': row['몰코드'],
            '키워드': row['키워드'],
            '중복횟수': value_counts[row['상품코드']]
        })

# 몰코드로 그룹화하여 나머지 데이터 나누기
for _, group in molkode_grouped.iterrows():
    molkode = group['몰코드']
    count = group['카운트']

    filtered_df = non_duplicate_data[non_duplicate_data['몰코드'] == molkode]

    for _, row in filtered_df.iterrows():
        stored = False
        for storage_index in range(1, max_count + 1):
            if len(storage[storage_index]) < max_storage_size:
                if row['상품코드'] not in [item['상품코드'] for item in storage[storage_index]]:
                    current_molkode_count = molkode_counts[storage_index].get(molkode, 0)
                    if current_molkode_count < 22:
                        storage[storage_index].append({
                            '상품코드': row['상품코드'],
                            '몰코드': row['몰코드'],
                            '키워드': row['키워드'],
                            '중복횟수': value_counts[row['상품코드']]
                        })
                        molkode_counts[storage_index][molkode] = current_molkode_count + 1
                        stored = True
                        break
        if not stored:
            not_stored_count += 1
            not_stored_data.append({
                '상품코드': row['상품코드'],
                '몰코드': row['몰코드'],
                '키워드': row['키워드'],
                '중복횟수': value_counts[row['상품코드']]
            })

# 로그 출력
for storage_index, items in storage.items():
    print(f"저장소 {storage_index}: {len(items)}개 파일 저장됨")
    for item in items:
        print(f"  상품코드: {item['상품코드']}, 몰코드: {item['몰코드']}, 키워드: {item['키워드']}, 중복횟수: {item['중복횟수']}")

print(f"포함되지 못한 파일 갯수: {not_stored_count}개")
for data in not_stored_data:
    print(f"포함되지 못한 데이터 - 상품코드: {data['상품코드']}, 몰코드: {data['몰코드']}, 키워드: {data['키워드']}, 중복횟수: {data['중복횟수']}")

# 엑셀로 아웃풋
output_data = {f'저장소 {i}': [] for i in range(1, max_count + 1)}
prod_code = 99991000001
for storage_index, items in storage.items():
    while len(items) < max_storage_size:
        random_keyword = random.choice(keywords)  # 임의의 키워드 선택
        items.append({
            '상품코드': prod_code,
            '몰코드': "",
            '키워드': random_keyword,
            '중복횟수': 0
        })
        prod_code += 1
    for item in items:
        output_data[f'저장소 {storage_index}'].append({
            '상품코드': item['상품코드'],
            '몰코드': item['몰코드'],
            '키워드': item['키워드'],
            '중복횟수': item['중복횟수']
        })

# 각 저장소의 데이터를 DataFrame으로 변환 및 정렬
output_dfs = {}
for storage_index in range(1, max_count + 1):
    output_dfs[storage_index] = pd.DataFrame(output_data[f'저장소 {storage_index}'])

# 몰코드 출현 횟수 추가 및 정렬
for storage_index in output_dfs.keys():
    molkode_occurrences = {}
    for item in output_data[f'저장소 {storage_index}']:
        molkode = item['몰코드']
        if molkode in molkode_occurrences:
            molkode_occurrences[molkode] += 1
        else:
            molkode_occurrences[molkode] = 1

    # 출현 횟수를 DataFrame에 추가
    output_dfs[storage_index]['몰코드 출현 횟수'] = output_dfs[storage_index]['몰코드'].map(molkode_occurrences)

    # 몰코드 출현 횟수 및 몰코드 기준으로 정렬
    output_dfs[storage_index] = output_dfs[storage_index].sort_values(by=['몰코드 출현 횟수', '몰코드'], ascending=[False, True])

    # 1부터 22까지 반복적으로 추가
    output_dfs[storage_index]['F열'] = [i % 22 + 1 for i in range(len(output_dfs[storage_index]))]

# F열 기준으로 오름차순 정렬
for storage_index in output_dfs.keys():
    output_dfs[storage_index] = output_dfs[storage_index].sort_values(by='F열', ascending=True)

# 엑셀 파일로 저장
output_file_path = r'C:\test\output.xlsx'  # 아웃풋 파일 경로
with pd.ExcelWriter(output_file_path) as writer:
    for storage_index, output_df in output_dfs.items():
        output_df.to_excel(writer, sheet_name=f'저장소 {storage_index}', index=False)

print(f"저장소 데이터가 {output_file_path}에 저장되었습니다.")

# 텍스트 파일로 아웃풋
for storage_index, output_df in output_dfs.items():
    text_file_path = fr'C:\test\저장소_{storage_index}.txt'  # 텍스트 파일 경로
    with open(text_file_path, 'w', encoding='utf-8') as f:
        for _, row in output_df.iterrows():
            f.write(f"{row['상품코드']}:{row['키워드']}\n")

print("저장소별 텍스트 파일이 생성되었습니다.")
