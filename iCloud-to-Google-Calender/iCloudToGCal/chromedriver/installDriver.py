import os


def add_to_path(path):
    """
    Adds a path to the PATH environment variable
    """
    import winreg
    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r'Environment',
        0,
        winreg.KEY_ALL_ACCESS
    )
    value, _ = winreg.QueryValueEx(key, 'PATH')
    if path not in value:
        value += f";{path}"
        winreg.SetValueEx(key, 'PATH', 0, winreg.REG_EXPAND_SZ, value)
    winreg.CloseKey(key)


def driver_location():
    """
    Returns the location of the chromedriver.exe
    uses brute force to find the location
    checks all paths in the PATH environment variable
    if it is not found it creates a folder in C:\\seleniumDriver
    and adds it to the PATH environment variable
    """
    for path in os.environ['PATH'].split(os.pathsep):
        if os.path.exists(os.path.join(path, 'chromedriver.exe')):
            return path
        if path == "C:\\seleniumDriver":
            os.makedirs("C:\\seleniumDriver", exist_ok=True)
            return path
    # C:\seleniumDriver
    os.makedirs("C:\\seleniumDriver", exist_ok=True)
    # append to path
    add_to_path("C:\\seleniumDriver")

    return "C:\\seleniumDriver"


def get_chrome_version():
    """
    Returns the version of the Chrome browser
    """
    import winreg
    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r'Software\Google\Chrome\BLBeacon'
    )
    value, _ = winreg.QueryValueEx(key, 'version')
    winreg.CloseKey(key)
    return int(value.split('.')[0])


def get_driver_version():
    """
    Returns the version of the chromedriver.exe
    """
    driver_path = driver_location()
    try:
        import subprocess
        output = subprocess.check_output(
            [driver_path + "\\chromedriver.exe", "--version"]
        )
        return int(output.decode().split(' ')[1].split('.')[0])
    except:
        return 0


def check_for_resources():
    """
    Checks if the resources folder exists
    if it does not exist it creates it
    """
    if not os.path.exists("C:\\icloud_resources"):
        from .GUI.create import create_desktop_icon
        create_desktop_icon()
        os.makedirs("C:\\icloud_resources")
    if not os.path.exists("C:\\icloud_resources\\record.json"):
        with open("C:\\icloud_resources\\record.json", "w") as f:
            f.write("{}")
    if not os.path.exists("C:\\icloud_resources\\cerdential.txt"):
        with open("C:\\icloud_resources\\cerdential.txt", "w") as f:
            f.write("")
    if not os.path.exists("C:\\icloud_resources\\attendance.json"):
        with open("C:\\icloud_resources\\attendance.json", "w") as f:
            f.write("{}")


def install_driver():
    """
    Installs the chromedriver.exe
    """
    chrome_version = get_chrome_version()
    driver_version = get_driver_version()
    # print(chrome_version,type(chrome_version))
    # print(driver_version,type(driver_version))
    driver_path = driver_location()
    if chrome_version == driver_version:
        return
    import requests
    import zipfile
    import io
    url = "https://chromedriver.chromium.org/downloads"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/80.0.3987.132 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    html = response.text.split("\n")
    version = -1
    for line in html:
        if f"ChromeDriver {chrome_version}" in line:
            version = line.split(' ')[-1]
            break
    if version == -1:
        raise Exception("Please update your Chrome browser and try again")
    url = f'https://chromedriver.storage.googleapis.com/{version}/chromedriver_win32.zip'
    response = requests.get(url, headers=headers)
    # remove all files in driver_path
    for file in os.listdir(driver_path):
        os.remove(os.path.join(driver_path, file))

    # extract new driver
    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
        zip_file.extractall(driver_path)



