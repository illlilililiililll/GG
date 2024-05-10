import requests
from random import randint

def login(login_id, login_pw):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    headers = {'User-Agent': user_agent,
               'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"}
    session = requests.Session()
    session.headers.update(headers)

    url_login_page = 'https://hi.hana.hs.kr/member/login.asp'

    try:
        session.get(url_login_page)
    except ConnectionError:
        print('인터넷 연결이 원활하지 않습니다. ')
        return

    url_login_proc = 'https://hi.hana.hs.kr/proc/login_proc.asp'
    login_data = {'login_id': login_id, 'login_pw': login_pw, 'x': str(randint(10, 99)), 'y': str(randint(10, 99))}
    res = session.post(url_login_proc, headers={'Referer': url_login_page}, data=login_data)
    if '로그인 정보가' in res.text:
        return
    return session

def pretty_print(data):
    output_str = ""
    for time_block in data:
        time = time_block[0]
        output_str += f"{time}타임\n"
        for room_data in time_block[1]:
            room = room_data[0]
            output_str += f"\t{room}    {len(room_data[1])}명\n"
            for student_data in room_data[1]:
                student_name = student_data[3]
                activity = student_data[2]
                output_str += f"\t\t{student_name}, {activity}\n"
            output_str += '\n'
    return output_str.strip()