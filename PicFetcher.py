import requests
from bs4 import BeautifulSoup
import os
import sys

keyword = '秀人网'
url = 'http://www.nanrencd.cc/tag/' + keyword

myHeader = {
	'Accept': 'image/png, image/svg+xml, image/*;q=0.8, */*;q=0.5',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'zh-CN,zh;q=0.8',
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

cur_path='E:/爬虫图片/'

def getHtmlText(url,header):
    try:
        r = requests.get(url, headers = header, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "error:" + r.status_code

def getInLocalDir(localPath):
	if os.path.exists(localPath):
		pass
	else:
	   os.mkdir(localPath)	   

getInLocalDir(cur_path + keyword )
cur_path = cur_path + keyword + '/'

t = getHtmlText(url,myHeader)

soup = BeautifulSoup(t,"html.parser")


#循环翻页直到找不到下一页为止,do-while
while True: 	
	divs = soup.find_all('div', class_="article")

	#获取一套图片标题-网址键值对
	downDic = {}
	for sDiv in divs:
		downUrl = sDiv.find('a').attrs['href']
		downTitle = sDiv.find('a').attrs['title']
		downDic[downTitle] = downUrl

	#针对上面每个键值对分别下载
	for key,val in downDic.items():
		t1 = getHtmlText(val, myHeader)
		soup1 = BeautifulSoup(t1,"html.parser")
		#获取页数
		pageSum = soup1.find('li', class_='page-total').string
		pageSum = int(pageSum[2:])
		print(pageSum)
		getInLocalDir(cur_path + key)
		pic_dir = cur_path + key + '/'
		os.chdir(cur_path + key)
		print(key)
		#循环获取每一页图片url，下载到本地
		pic_cnt = 0
		for page_index in range(1,pageSum+1):
			pic_link = val + '/' + str(page_index)
			cur_page = getHtmlText(pic_link, myHeader)
			soup1 = BeautifulSoup(cur_page,"html.parser")
			try:
				pic_src_list = soup1.find_all('img', alt=key)
				for pic in pic_src_list:
					pic_cnt += 1 
					pic_src = pic.attrs['src']
					pic_name = "%03d" % pic_cnt + ".jpg"
					f = open(pic_dir+pic_name,'wb')
					f.write(requests.get(pic_src,headers=myHeader).content)
			except Exception as e:
				print(e)
		os.chdir(cur_path + key)

	#获取下一预览页URL
	endflag = soup.find('a',class_='next')
	if endflag == None:
		break
	else:
		nextPage = int(soup.find('a',class_='current').string)+1
		url1 = url + "/page/" + str(nextPage)
		t = getHtmlText(url1,myHeader)
		soup = BeautifulSoup(t,"html.parser")