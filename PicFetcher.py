import requests
from bs4 import BeautifulSoup
import os
import sys

class PicFetcher(object):
	def __init__(self, keyword, header, url, path):
		self.keyword = keyword
		self.myHeader = header
		self.url = url
		self.cur_path = path

    #get网页html文本
	def getHtmlText(self, url, header):
		try:
			r = requests.get(url, headers = header, timeout=60)
			r.raise_for_status()
			r.encoding = r.apparent_encoding
			return r.text
		except:
			return "error:" + r.status_code

    #创建目录    
	def getInLocalDir(self, localPath):
		if os.path.exists(localPath):
			pass
		else:
	 		os.mkdir(localPath)	   
	
	#抓取某一个url的所有图片
	def FetchSingal(self, url, header, cur_path, key):
		t1 = self.getHtmlText(url, header)
		soup1 = BeautifulSoup(t1,"html.parser")
		#获取页数
		pageSum = soup1.find('li', class_='page-total')
		#有可能存在只有一页的情况
		if pageSum == None:
			pageSum = 1
		else:
			pageSum = pageSum.string
			pageSum = int(pageSum[2:])
		print(pageSum)
		self.getInLocalDir(cur_path + key)
		pic_dir = cur_path + key + '/'
		os.chdir(cur_path + key)
		#循环获取每一页图片url，下载到本地
		pic_cnt = 0
		for page_index in range(1,pageSum+1):
			pic_link = url + '/' + str(page_index)
			cur_page = self.getHtmlText(pic_link, header)
			soup1 = BeautifulSoup(cur_page,"html.parser")
			try:
				pic_src_list = soup1.find_all('img', alt=key)
				for pic in pic_src_list:
					pic_cnt += 1 
					pic_src = pic.attrs['src']
					pic_name = "%03d" % pic_cnt + ".jpg"
					if os.path.exists(pic_dir+pic_name) == False:
						f = open(pic_dir+pic_name,'wb')
						f.write(requests.get(pic_src,headers=header).content)
			except Exception as e:
				print(e)
		os.chdir(cur_path + key)

	#按关键字全部抓取,可从任意一个起始url开始直到抓完为止
	def FetchAllByTag(self, tag, startUrl):
		cur_path = self.cur_path + tag + '/'
		self.getInLocalDir(cur_path)
		
		t = self.getHtmlText(startUrl, self.myHeader)

		soup = BeautifulSoup(t, "html.parser")

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
				key = key.replace('/',' ')
				print(key)
				
				self.FetchSingal(val,self.myHeader,cur_path,key)

			#获取下一预览页URL
			endflag = soup.find('a',class_='next')
			if endflag == None:
				break
			else:
				nextPage = int(soup.find('a',class_='current').string)+1
				url1 = self.url + "/page/" + str(nextPage)
				t = self.getHtmlText(url1,self.myHeader)
				soup = BeautifulSoup(t,"html.parser")


if __name__	== '__main__':

	keyword = '头条女神'
	url = 'http://www.nanrencd.cc/tag/' + keyword
	url1 = 'http://www.nanrenxp.com/tag/%E5%A4%B4%E6%9D%A1%E5%A5%B3%E7%A5%9E/page/20'

	myHeader = {
		'Accept': 'image/png, image/svg+xml, image/*;q=0.8, */*;q=0.5',
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': 'zh-CN,zh;q=0.8',
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'
	}

	cur_path='E:/爬虫图片/'

	pf = PicFetcher(keyword, myHeader, url, cur_path)
	pf.FetchAllByTag(keyword, url1)