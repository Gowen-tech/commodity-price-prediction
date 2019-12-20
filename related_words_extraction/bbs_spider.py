import re
import urllib.request
from bs4 import BeautifulSoup
from tqdm import tqdm

def getPageContent(h):
	html = urllib.request.urlopen(h)
	# html = html.decode("gbk")
	return html.read().decode("gbk")

if __name__ == '__main__':

	of = open("./bbs_text.cor", "w")
	for page in range(1, 101):

		print("catching urls for page{}".format(page))

		html = "http://bbs.jrj.com.cn/futures,{}".format(page)
		main_page = getPageContent(html)
		reg = re.compile(r'<a href="(/msg,.*?)" class="acol" target="_blank">(.*?)</a></td>')
		urls = re.findall(reg, main_page)

		print("start crawling the context in each url...")

		base = "http://bbs.jrj.com.cn"
		# flag = 0
		for url, title in tqdm(urls):
			# if flag > 0:
			# 	break
			html = base + url
			content = getPageContent(html)
			soup = BeautifulSoup(content, "html.parser")
			soup = soup.find('div', class_='content', id="msgMainContent")
			for target in soup.find_all('p'):
				of.write(target.get_text().strip())
			of.write("\n")
			# flag += 1
	of.close()