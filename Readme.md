# Auto Get cookie from email and address
## 运行环境
python 3.9.8
下载对应版本的chrome_driver并保存到该目录下，文件名应为：chromedriver.exe
下载地址：
https://googlechromelabs.github.io/chrome-for-testing/#stable
python对应包的安装，在cmd里输入：
pip install -r requirements.txt
## files
### emails.txt

username@outlook.com-密码
1111111111@outlook.com-111111111
2222222@outlook.com-2222222
333333333@outlook.com-333333
44444444@outlook.com-444444444

### other_config.json
{
    # clewd里配置cookie的文件的路径，假如不写或者路径不对就不把找到的cookie往里写
    "clew_config_path": "D:\\Code\\clewd\\config.js",
    # 如果是add模式，就增加新找到的cookie，如果是replace模式，就把原来的cookie都删除了，填写新找到的cookie，不写的话默认是add模式,replace模式暂时没写，所以只有add模式
    "mode": "add"
}

## 运行
python get_cookies.py

### 运行结果
如果配置好了other_config.json，会自动写入config.js
如果没有的话，会产生一个cookies.txt文件，把抓到的cookie写进去
如果某个邮箱对应的cl2账号已经超过限制了，不能打开新的chat了，那就抓不到对应的cookie了


# 只是写给大家自用的，请不要用于商业用途