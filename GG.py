import os
from bs4 import BeautifulSoup
from collections import defaultdict
import subprocess
import data
import util

def GG(id, pw):
    session = util.login(id, pw)
    print('로그인되었습니다')

    data = []
    i = 1
    while True:
        response = session.get(f'https://hi.hana.hs.kr/SYSTEM_Plan/SubjectClassRoom/SCR_Application/applicationMain.asp?searchopt=&searchkey=&page={i}')
        
        if '개설된 모임이 없습니다.' in response.text:
            break

        soup = BeautifulSoup(response.text, 'html.parser')

        for tr in soup.find_all('tr'):
            row = [td.get_text(strip=True) for td in tr.find_all('td') if not td.find('input')]
            if row and ('승인' in row):  # Exclude empty rows
                row = [row[i] for i in [6, 4, 1, 7]]
                row[0] = row[0][0]
                row[3] = row[3][:-4]
                data.append(row)
        print(f'page #{i}')
        i += 1

    grouping_dict = defaultdict(lambda: defaultdict(list))
    for item in data:
        grouping_dict[item[0]][item[1]].append(item)

    sorted_dict = dict(sorted(grouping_dict.items(), key=lambda x: (x[0], x[1].keys(), x[1].values())))

    sorted_list = []
    for main_key, sub_groups in sorted_dict.items():
        sub_group_list = []
        for sub_key, items in sorted(sub_groups.items(), key=lambda x: x[0]):
            sub_group_list.append([sub_key, items])
        sorted_list.append([main_key, sub_group_list])

    return util.pretty_print(sorted_list)

if __name__ == '__main__':
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'GG.txt')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(GG(data.id, data.pw))
    print('파일이 저장되었습니다')
    process = subprocess.Popen([file_path], shell=True)