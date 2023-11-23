from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 初始化浏览器
driver = webdriver.Chrome(r'D:\Code\edgedriver_win64\msedgedriver.exe')  # 根据你的浏览器选择相应的驱动程序

# 打开Outlook注册页面
driver.get('https://signup.live.com')

# 等待页面加载完成
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.ID, 'MemberName')))

# 输入账号信息
username = driver.find_element_by_id('MemberName')
username.send_keys('your_username')  # 替换为你的用户名

# 点击“下一步”按钮
next_button = driver.find_element_by_id('iSignupAction')
next_button.click()

# 等待页面加载完成
wait.until(EC.presence_of_element_located((By.ID, 'PasswordInput')))

# 输入密码
password = driver.find_element_by_id('PasswordInput')
password.send_keys('your_password')  # 替换为你的密码

# 确认密码
confirm_password = driver.find_element_by_id('RetypePassword')
confirm_password.send_keys('your_password')  # 替换为你的密码

# 点击“下一步”按钮
next_button = driver.find_element_by_id('iSignupAction')
next_button.click()

# 等待页面加载完成
wait.until(EC.presence_of_element_located((By.ID, 'FirstName')))

# 输入个人信息
first_name = driver.find_element_by_id('FirstName')
first_name.send_keys('your_first_name')  # 替换为你的名字

last_name = driver.find_element_by_id('LastName')
last_name.send_keys('your_last_name')  # 替换为你的姓氏

# 点击“下一步”按钮
next_button = driver.find_element_by_id('iSignupAction')
next_button.click()

# 等待页面加载完成
wait.until(EC.presence_of_element_located((By.ID, 'BirthMonth')))

# 输入生日信息
birth_month = driver.find_element_by_id('BirthMonth')
birth_month.send_keys('your_birth_month')  # 替换为你的生日月份

birth_day = driver.find_element_by_id('BirthDay')
birth_day.send_keys('your_birth_day')  # 替换为你的生日日期

birth_year = driver.find_element_by_id('BirthYear')
birth_year.send_keys('your_birth_year')  # 替换为你的生日年份

# 点击“下一步”按钮
next_button = driver.find_element_by_id('iSignupAction')
next_button.click()

# 等待页面加载完成
wait.until(EC.presence_of_element_located((By.ID, 'iOptinEmail')))

# 勾选“接收推广邮件”选项
optin_email = driver.find_element_by_id('iOptinEmail')
optin_email.click()

# 点击“下一步”按钮
next_button = driver.find_element_by_id('iSignupAction')
next_button.click()

# 等待注册完成
wait.until(EC.url_contains('https://account.microsoft.com'))

# 打印注册成功信息
print("Outlook邮箱注册成功！")

# 关闭浏览器
driver.quit()