import os
import datetime
import random
import string
import time
import re
import traceback
import platform
import logging
import jwt

from DrissionPage import ChromiumPage, ChromiumOptions
from logging_config import init_log

init_log()

script_dir = os.path.dirname(os.path.abspath(__file__))

cpu_count = os.cpu_count()
logging.info(f"CPU 核心数: {cpu_count}")


def extract_jwt_info(token: str):
    """
    解析 JWT 并提取 address 和 oauth_username
    :param token: JWT 字符串
    :return: (address, oauth_username)
    """
    try:
        # 解析 JWT（不验证签名）
        decoded = jwt.decode(token, options={"verify_signature": False})

        # 提取 verified_credentials 数据
        verified_credentials = decoded.get("verified_credentials", [])

        # 初始化返回值
        address = None
        oauth_username = None

        for credential in verified_credentials:
            if credential.get("format") == "blockchain":
                address = credential.get("address")
            elif credential.get("format") == "oauth":
                oauth_username = credential.get("oauth_username")

        return address, oauth_username
    except Exception as e:
        traceback.print_exc()
        print("解析 JWT 失败:", e)
        return None, None

def time_random_file_name(base_dir=script_dir):
    # 获取当前的年月日时分秒
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    # 生成一个4位随机小写字母串
    random_letters_lower = ''.join(random.choices(string.ascii_lowercase, k=4))

    # 组合年月日时分秒和随机小写字母串
    result_string_lower = current_time + "_" + random_letters_lower
    # 组合文件夹路径
    folder_path = os.path.join(base_dir, result_string_lower)

    # 检查文件夹是否存在，如果不存在则创建
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    return folder_path


def check_exist_dir():
    for name in os.listdir(script_dir):
        path = os.path.join(script_dir, name)
        # 判断是否是以"2025"开头的文件夹
        if os.path.isdir(path) and re.match(r"^2025", name):
            logging.info("找到文件夹:", path)
            break  # 如果只需要找到一个，可以提前退出循环
    return path

def remove_quotes(s):
    # 使用 strip 去除首尾的引号
    if s.startswith('"') and s.endswith('"'):
        s = s[1:-1]  # 去掉首尾的引号
    return s


def login(page):
    try:
        sign_ele = page.ele('tag:div@@id=dynamic-widget@@class=dynamic-shadow-dom dynamic-widget__container')
        if not sign_ele:
            raise Exception("找不到sign in按钮")
        sign_ele.click()
        shadow_ele = page.ele('@@class=dynamic-shadow-dom@@data-testid=dynamic-modal-shadow').shadow_root
        # print(shadow_ele)
        input_ele = shadow_ele.ele('@id=email_field')
        if not input_ele:
            raise Exception("找不到邮箱输入框")
        email = input("请输入你的邮箱号：")
        if email is None or len(email) == 0:
            raise Exception("输入邮箱为空")
        input_ele.input(email)
        time.sleep(0.5)
        continue_ele = shadow_ele.ele('.typography typography--button-primary  typography--inherit  ')
        if not continue_ele:
            raise Exception("输入邮箱后无法下一步")
        continue_ele.click()
        code = input("请输入6位验证码：")
        if code is None or len(code) == 0:
            raise Exception("输入验证码有问题")
        code_parents_ele = shadow_ele.ele('.pin-field__container')
        if not code_parents_ele:
            raise Exception("找不到验证码输入框")
        code_ele_list = code_parents_ele.children()
        for index_2, code_ele in enumerate(code_ele_list):
            code_ele.input(code[index_2])
            time.sleep(0.1)

        time.sleep(5)
        print("验证码输入完毕")
        pass
    except Exception as e:
        traceback.print_exc()
        raise e



def work():
    global cpu_count
    page = None
    try:
        co = ChromiumOptions()
        if platform.system().lower() == 'windows':
            pass
        else:
            co = ChromiumOptions().set_paths(browser_path=r"/usr/bin/google-chrome")
            co.headless(True)
            co.set_argument('--no-sandbox')
        path = check_exist_dir()
        if path:
            co.set_user_data_path(path)
        else:
            co.set_user_data_path(r'/home/dp_data')
        page = ChromiumPage(addr_or_opts=co)
        page.set.download_path(".")

        list = page.get_tabs()
        for tab in list[1:]:
            tab.close()

        page.get('https://app.nexus.xyz/')


        mail = 'unknow'
        address = '0x00..0'
        # time.sleep(2)

        auth_token = page.local_storage('dynamic_authentication_token')
        if auth_token:
            auth_token = remove_quotes(auth_token)
        if auth_token is None:
            login(page)
            auth_token = page.local_storage('dynamic_authentication_token')
            auth_token = remove_quotes(auth_token)
        if auth_token:
            jwt_address, jwt_mail = extract_jwt_info(auth_token)
            if jwt_address:
                address = jwt_address
            if jwt_mail:
                mail = jwt_mail

        tab_list = []
        tab_list.append(page)

        for index_1 in range(cpu_count+1):
            tab = page.new_tab("https://app.nexus.xyz/")
            tab_list.append(tab)

        logging.info(f"CPU 核心数: {cpu_count} , 将启动{len(tab_list)}个标签页")


        try:
            time.sleep(3)
            while tab_list:
                for index_2, page in enumerate(tab_list):
                    off_button_ele = page.ele(".relative w-24 h-16 rounded-full cursor-pointer transition-colors duration-300 ease-in-out  border-4 border-gray-400 bg-[#ffffff]", timeout=5)
                    if off_button_ele:
                        off_button_ele.click(by_js=True)
                    else:
                        cycles_text_ele = page.ele('xpath:/html/body/div[3]/div[2]/main/main/div[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div[1]')
                        nex_points_ele = page.ele('xpath:/html/body/div[3]/div[2]/main/main/div[2]/div/div/div[1]/div[1]/div/div/div/div/div[3]/div[1]')
                        if cycles_text_ele and nex_points_ele:
                            cycles_text = cycles_text_ele.raw_text
                            nex_points_text = nex_points_ele.raw_text
                            current_time = datetime.datetime.now()

                            logging.info(f"[{current_time} 邮箱 {mail} 地址 {address} 标签页{index_2+1} 当前Cycles/s 为 {cycles_text}, 总 Nex points 为 {nex_points_text}]")
                    time.sleep(5)
                    if 'unknow' == mail:
                        auth_token = page.local_storage('dynamic_authentication_token')
                        if auth_token:
                            # print(auth_token)
                            jwt_address, jwt_mail = extract_jwt_info(auth_token)
                            if jwt_address:
                                address = jwt_address
                            if jwt_mail:
                                mail = jwt_mail
        except Exception as e:
            traceback.print_exc()
            if page:
                page.quit()
    except Exception as e:
        traceback.print_exc()
        if page:
            page.quit()
        raise e

if __name__ == '__main__':
    work()
