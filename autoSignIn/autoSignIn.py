import requests  
from bs4 import BeautifulSoup  
import http.cookiejar
import os

userid = '259933'
url = 'http://99.1.36.189/'
pyPath = os.path.split(os.path.realpath(__file__))[0]
s = requests.Session()

getHeader = {
    'Cache-Control':'max-age=0',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'Accept-Encoding': 'gzip,deflate,sdch',
	'Accept-Language': 'zh-CN,zh;q=0.8',
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'
}

def saveCookie(requestContent, filepath):
	new_cookie_jar = http.cookiejar.LWPCookieJar('localcookie.txt')
	#从cookie中获取字典格式
	requests.utils.cookiejar_from_dict({c.name: c.value for c in requestContent.cookies}, new_cookie_jar)
	#保存至本地文件
	new_cookie_jar.save(filepath, ignore_discard=True, ignore_expires=True)

def loadCookie(filepath):
	
	load_cookiejar = http.cookiejar.LWPCookieJar()
	#从文件中加载cookies(LWP格式)
	load_cookiejar.load(filepath, ignore_discard=True, ignore_expires=True)
	#工具方法转换成字典
	load_cookies = requests.utils.dict_from_cookiejar(load_cookiejar)
	#工具方法将字典转换成RequestsCookieJar，赋值给session的cookies.
	cookies = requests.utils.cookiejar_from_dict(load_cookies)
	return cookies

try:
	localcookie = loadCookie(pyPath + '/cookies/localcookie.txt')
except Exception as e:
	print(e)
	isExistLocalCookie = 'false'
	requestURL = s.get(url, headers = getHeader)
	if requestURL.status_code == 200:
		saveCookie(requestURL, pyPath + './cookies/localcookie.txt')
else:
	isExistLocalCookie = 'true'
	requestURL = s.get(url, headers = getHeader, cookies=localcookie)

urlContext = requestURL.text

soup = BeautifulSoup(urlContext,"html.parser")

#print(soup.prettify())

#get相关参数;
eventval = soup.find(id='__EVENTVALIDATION').attrs['value']
viewstate = soup.find(id='__VIEWSTATE').attrs['value']
viewgen = soup.find(id='__VIEWSTATEGENERATOR').attrs['value']

#get福州分行的id
tds = soup.find('td',text="福州分行")
td = tds.previous_sibling.previous_sibling
signUser = td.contents[0].attrs['name']

td1 = td.previous_sibling
signId = td1.contents[1].attrs['name']

postdata = {                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
	'__EVENTVALIDATION':eventval,
	'__VIEWSTATE':viewstate,
	'__VIEWSTATEGENERATOR':viewgen,
	signId:'签到',
	signUser:userid
	}

if isExistLocalCookie == 'false':
	postresult = s.post(url, data = postdata, headers = getHeader)
else: 
	postresult = s.post(url, data = postdata, headers = getHeader, cookies=localcookie)

#print(postresult.text)