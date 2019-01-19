from mitmproxy import io
from mitmproxy.exceptions import FlowReadException


class mitmproxy_api():

    def __init__(self, host, filename):
        # TODO add host validation
        self.host = host
        self.filename = filename
        self.info = []

    def __getHeaders(self, headers):
        setCookieList = []
        for header in headers:
            if header[0].lower().decode("utf-8") == 'set-cookie':
                setCookieList.append(header[1].decode("utf-8"))

        headersDict = dict(headers)
        decodedDict = {k.decode("utf-8"): v.decode("utf-8") for k, v in headersDict.items()}
        if len(setCookieList) > 0:
            decodedDict['Set-Cookie'] = setCookieList
        return decodedDict

    def getDataFile(self):
        requestData = {}
        responseData = {}
        dictData = {}
        try:
            with open(self.filename, "rb") as file:
                data = io.FlowReader(file)
                try:
                    for item in data.stream():
                        if item.request.host == self.host:
                            if item.response is not None:
                                requestData['url'] = item.request.pretty_url
                                requestData['method'] = item.request.method
                                requestData['headers'] = self.__getHeaders(item.request.headers.fields)
                                requestData['body'] = item.request.content.decode("utf-8")
                                responseData['headers'] = self.__getHeaders(item.response.headers.fields)
                                responseData['status_code'] = item.response.status_code
                                dictData['request'] = requestData.copy()
                                dictData['response'] = responseData.copy()
                                self.info.append(dictData.copy())
                except FlowReadException as e:
                    print("Error! {} File can't be processed".format(e))
        except FileNotFoundError as e:
            print("Error! {}: {}".format(e.strerror, e.filename))

    def getUrlCodeAndHeaders(self):
        dictData = {}
        listUrlsAndHeaders = []

        for item in self.info:
            req = item['request']
            resp = item['response']
            dictData['url'] = req['url']
            dictData['headers'] = resp['headers']
            dictData['status_code'] = resp['status_code']
            listUrlsAndHeaders.append(dictData.copy())
            dictData = {}
        return listUrlsAndHeaders

    def getPostUrlsAndBody(self):
        dictData = {}
        listUrlsAndBody = []
        for item in self.info:
            req = item['request']
            if req['method'] == 'POST':
                dictData['url'] = req['url']
                dictData['body'] = req['body']
                listUrlsAndBody.append(dictData.copy())
                dictData = {}
        return listUrlsAndBody

    def getFolders(self):
        folders = []
        for item in self.info:
            req = item['request']
            folder = req['url'].rsplit('/', 1)[0]
            while folder[-1] != '/':
                if folder not in folders:
                    folders.append(folder)
                folder = folder.rsplit('/', 1)[0]
        return (folders)
