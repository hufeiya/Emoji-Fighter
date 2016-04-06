import urllib,urllib2,re,os
class EmojiDownloader:

    def __init__(self,url,dirname):
        self.url = url
        self.dirname = dirname
        self.useProxy = False
        self.picUrlPrefix = 'http://qq.yh31.com/'
        self.allDone = False
        try:
            os.makedirs(dirname)
        except OSError:
            print "dir exsited."

    def __url_user_agent(self,url):
        if self.useProxy:
            proxy = {'http': '127.0.0.1:8123'}
            proxy_support = urllib2.ProxyHandler(proxy)
            # opener = urllib2.build_opener(proxy_support,urllib2.HTTPHandler(debuglevel=1))
            opener = urllib2.build_opener(proxy_support)
            urllib2.install_opener(opener)

        # i_headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        i_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.48'}
        req = urllib2.Request(url, headers=i_headers)
        try:
            html = urllib2.urlopen(req)
            if url == html.geturl():
                doc = html.read()
                return doc
            else:
                self.allDone = True
                return
        except urllib2.HTTPError:
            self.allDone = True
            return

    def __saveImage(self,imageUrl):
        u = urllib.urlopen(self.picUrlPrefix + imageUrl)
        data = u.read()
        splitPath = imageUrl.split('/')
        fName = splitPath.pop()
        print fName
        f = open(self.dirname + '/' + fName, 'wb')
        f.write(data)

    def downloadOnePage(self,pageUrl):
        html = self.__url_user_agent(pageUrl)
        if html is None:
            return
        picUrlList = re.findall('img src=\S*\.jpg|img src=\S*\.gif', html)
        if picUrlList:
            for i in picUrlList:
                self.__saveImage(i[9:])
        else:
            print "Not Match"

    def downloadAllPages(self,maxPageNum):
        for i in xrange(1,maxPageNum):
            if i == 1:
                self.downloadOnePage(self.url)
            else:
                self.downloadOnePage(self.url[:len(self.url)-5] + '_' + str(i) + '.html')
            if self.allDone:
                print 'all done, download ' + i + 'pages.'
                break

if __name__ == '__main__':

    downloader = EmojiDownloader('http://qq.yh31.com/zjbq/0551964.html','jinGuanZhang')
    downloader.downloadAllPages(50)
