#https://cloud.baidu.com/doc/OCR/s/Rjwvxzm3n 接口文档地址 百度云
from aip import AipOcr
""" 你的 APPID AK SK """
APP_ID = '16860486'
API_KEY = 'BIZkc8PB1G6IT84DHxaw0FrT'   #Access Key ID
SECRET_KEY = 'y7gLCydFdI50P3Mmyw1qXOHRRIGs2vbI' #Access Key Secret

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

# """ 读取图片 """
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

# """ 调用通用文字识别, 图片参数为本地图片 """
def basicGeneral(path):
    image = get_file_content(path)
    # """ 如果有可选参数 """
    options = {}
    options["language_type"] = "CHN_ENG"
    options["detect_direction"] = "true"
    options["detect_language"] = "true"
    options["probability"] = "true"
    result=client.basicGeneral(image, options)
    return result
# """ 调用通用文字识别, 图片参数为远程url图片 """
def basicGeneralUrl(url):
    options = {}
    options["language_type"] = "CHN_ENG"
    options["detect_direction"] = "true"
    options["detect_language"] = "true"
    options["probability"] = "true"

    # """ 带参数调用通用文字识别, 图片参数为远程url图片 """
    result= client.basicGeneralUrl(url, options)
    return result

# a=basicGeneralUrl('https://bbs.sgcn.com/code.php?hvJiCAxQ3MnU/bIPyv3vWhMaTXl9U8gqfcKUmkq0vTNnlFxd')
# print(a['words_result'][0]['words'])

# b=basicGeneral('E:\\untitled\\图片\\a')
# # print(b)