import time
import re
from imapclient import IMAPClient, exceptions
import pyzmail
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
import json
import os



def use_webdriver(website_address = 'https://claude.ai'):
    options = webdriver.ChromeOptions()
    options.use_chromium = False
    options.add_argument("--inprivate")
    driver = uc.Chrome(service=Service(r'chromedriver.exe'), options=options)
    driver.get(website_address)
    return driver

def send_email(driver, email_address):
    # 找到输入邮箱的元素并输入邮箱
    time.sleep(2.173)
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="email"]'))  # 替换成实际的元素 XPath
    )
    email_input.send_keys(email_address)  # 注意这里的缩进
    # 找到发送验证码按钮并点击
    try:
        send_code_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/main/section/form/button'))  # 替换成实际的元素 XPath
        )
    except:
        send_code_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/main/section/form/button'))  # 替换成实际的元素 XPath
        )
    time.sleep(2.15)
    send_code_button.click()


# 定义一个函数来获取邮箱的最新邮件标题
def get_latest_email_title(username, password):
    try:
        with IMAPClient(host='outlook.office365.com') as client:
            client.login(username, password)
            try:
                client.select_folder('INBOX')
            except:
                return 'LOGIN FAILED' 

            # 搜索最新的一封邮件
            messages = client.search('ALL')
            if not messages:
                return None

            latest_id = messages[-1]

            # 获取邮件内容
            raw_messages = client.fetch([latest_id], ['BODY[]', 'BODYSTRUCTURE'])
            message = pyzmail.PyzMessage.factory(raw_messages[latest_id][b'BODY[]'])

            # 返回邮件主题
            return message.get_subject()
    except exceptions.LoginError:
        return 'LOGIN FAILED'

def check_email(title, email_address):
    if title is not None:
        if title == 'LOGIN FAILED':
            print(f"Login failed for: {email_address}")
            return None
        else:
            match = re.search(r'\d{6}', title)
            if match:
                return match.group(0)
            
def fill_in_post_code(driver, code):
    code_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="code"]'))  # 替换成实际的元素 XPath
    )
    
    code_input.send_keys(code)  # 注意这里的缩进
    # 找到发送验证码按钮并点击
    try:
        send_code_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/main/section/form/button'))  # 替换成实际的元素 XPath
        )
    except:
        send_code_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/main/section/form/button'))  # 替换成实际的元素 XPath
        )
    send_code_button.click()

def start_new_chat(driver):
    # 点击start_newChat
    try:
        start_newChat_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/main/div[1]/div/div[2]/fieldset/div[2]/div/button'))  # 替换成实际的元素 XPath
        )
    except:
        start_newChat_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/main/div[1]/div/div[2]/fieldset/div[2]/div/button'))  # 替换成实际的元素 XPath
        )
    start_newChat_button.click()

def get_cookies(driver):
    # 获取当前页面的所有 cookies
    cookies = driver.get_cookies()

    # 查找名为 'sessionKey' 的 cookie
    session_key_value = None
    for cookie in cookies:
        if cookie['name'] == 'sessionKey':
            session_key_value = cookie['value']
            return session_key_value
    driver.quit()

def get_cookie(email_address, email_password):
    driver = use_webdriver()
    send_email(driver, email_address)
    time.sleep(8)
    try_login = 3
    while try_login > 0:
        title = get_latest_email_title(email_address, email_password)
        pass_code = check_email(title, email_address)
        if pass_code is None:
            try_login -= 1
            time.sleep(5)
        else:
            break
    if pass_code is None:
        driver.quit()
        return None
    if pass_code is not None:
        fill_in_post_code(driver, pass_code)
        try:
            start_new_chat(driver)
        except:
            driver.quit()
            return None
        cookie = get_cookies(driver)
        driver.quit()
    if cookie is None:
        driver.quit()
        return None
    return cookie

def load_config():
    with open('other_config.json', 'r') as f:
        config = json.load(f)
    return config

def write_cookies_to_config(cookies, config):
    with open(config['clewd_config_path'], 'r') as file:
        js_code = file.readlines()
        for cookie_line in range(len(js_code)):
            if "CookieArray" in js_code[cookie_line]:
                break
        for cookie in cookies:
            js_code.insert(cookie_line + 1, f"\t\t\"sessionKey={cookie}\",\n")
    with open(config['clewd_config_path'], 'w') as file:
        file.writelines(js_code)


if __name__ == "__main__":
    config = load_config()
    with open('emails.txt', 'r') as f:
        emails = f.readlines()
    with open('cookies.txt', 'w') as f:
            f.write('')
    cookies = []
    # get cookies
    for email in emails:
        email = email.strip()
        email_address = email.split('-')[0]
        email_password = email.split('-')[1]
        try:
            cookie = get_cookie(email_address, email_password)
        except:
            continue
        if cookie is None:
            continue
        with open('cookies.txt', 'a') as f:
            f.write(f'{email_address}: sessionKey={cookie}\n')
        cookies.append(cookie)
    # write cookies to config.json
    if len(cookies) == 0:
        print('No cookies found.')
    else:
        if 'clewd_config_path' in config.keys() and os.path.exists(config['clewd_config_path']):
            write_cookies_to_config(cookies, config)


