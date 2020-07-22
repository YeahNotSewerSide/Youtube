import requests
import urllib.parse
import random

class Videos:
    def __init__(self):
        
        self.session = requests.Session()
        self.base_url = 'https://www.youtube.com'
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'}
        self.session.get(self.base_url+'/?pbj=1',headers=self.headers)
        self.prev_url = self.base_url
        self.session_token = ''
        self.visitor_data = ''
        self.sessionID = ''
        self.csn = ''
        self.clickTrackingParams = ''
        self.continuation = ''
        self.api_key = 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8'
    def parse_main_videos_info(self,data:dict)->dict:#{id:viewcount} Only videos and only main info
        
        out = {}
        try:
            for item in data[1]['response']['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']:
                parse = ''
                dt = ''
                print(item['videoRenderer']['videoId'])
                if 'videoRenderer' not in item.keys():
                    continue
                try:
                    parse = (item['videoRenderer']['viewCountText']['simpleText'].split(' '))[0]
                    try:
                        dt = parse.replace(',','')
                    except:
                        dt = parse.replace('.','')
                except:
                    continue #if stream
                try:
                    out[item['videoRenderer']['videoId']] = int(dt)
                except:
                    out[item['videoRenderer']['videoId']] = 0
                
            return out
       
        except:
            try:
                for item in data[1]['response']['continuationContents']['itemSectionContinuation']['contents']:
                    parse = ''
                    dt = ''
                    print(item['videoRenderer']['videoId'])
                    if 'videoRenderer' not in item.keys():
                        continue
                    try:
                        parse = (item['videoRenderer']['viewCountText']['simpleText'].split(' '))[0]
                        try:
                            dt = parse.replace(',','')
                        except:
                            dt = parse.replace('.','')
                    except:
                        continue #if stream
                    try:
                        out[item['videoRenderer']['videoId']] = int(dt)
                    except:
                        out[item['videoRenderer']['videoId']] = 0
                    
                return out
            except:
                pass
        try:
            for item in data['onResponseReceivedCommands'][0]['appendContinuationItemsAction']['continuationItems'][0]['itemSectionRenderer']['contents']:
                parse = ''
                dt = ''
                print(item['videoRenderer']['videoId'])
                if 'videoRenderer' not in item.keys():
                    continue
                try:
                    parse = (item['videoRenderer']['viewCountText']['simpleText'].split(' '))[0]
                    try:
                        dt = parse.replace(',','')
                    except:
                        dt = parse.replace('.','')
                except Exception as e:
                    continue #if stream
                try:
                    out[item['videoRenderer']['videoId']] = int(dt)                   
                except Exception as e:
                    out[item['videoRenderer']['videoId']] = 0
                
            return out
        except Exception as e:
            return out


        

    def get_videos(self,req:str):
        headers = self.headers.copy()
        headers.update({
                       'Origin':self.base_url,
                       'Referer':self.prev_url,
                       'X-SPF-Previous':self.prev_url,
                       'X-SPF-Referer':self.prev_url,
                       'X-YouTube-Ad-Signals':'dt=1584096069922&flash=0&frm&u_tz=120&u_his=9&u_java&u_h=1080&u_w=1920&u_ah=1040&u_aw=1920&u_cd=24&u_nplug&u_nmime&bc=29&bih=585&biw=1903&brdim=-8%2C-8%2C-8%2C-8%2C1920%2C0%2C1936%2C1056%2C1920%2C585&vis=1&wgl=true&ca_type=image',
                       'X-YouTube-Client-Name':'1',
                       'X-YouTube-Client-Version':'2.20200312.05.00',
                       'X-YouTube-Device':'cbr=Firefox&cbrver=74.0&cos=Windows&cosver=6.1',
                       'X-YouTube-Page-CL':'300349245',
                       'X-YouTube-Page-Label':'youtube.ytfe.desktop_20200311_5_RC0',
                       'X-YouTube-STS':'18332',
                       'X-YouTube-Time-Zone':'Europe/Bucharest',
                       'X-YouTube-Utc-Offset':'120',
                       'X-YouTube-Variants-Checksum':'5bab881c2eae92c1f0ba56374e524bb9'
                       })
        res = True
        if self.prev_url != self.base_url: 
            headers.update({'X-Goog-Visitor-Id':self.visitor_data,
                            'X-Origin':self.base_url})
            request_data = {'context':{'client':{'hl':'en',
                                                 'gl':'US',
                                                 'visitorData':self.visitor_data,
                                                 'userAgent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0,gzip(gfe)',
                                                 'clientName':'WEB',
                                                 'clientVersion':'2.20200720.00.02',
                                                 'osName':'Windows',
                                                 'osVersion':'6.1',
                                                 'browserName':'Firefox',
                                                 'browserVersion':'78.0',
                                                 'screenWidthPoints':1920,
                                                 'screenHeightPoints':374,
                                                 'screenPixelDensity':1,
                                                 'utcOffsetMinutes':180,
                                                 'userInterfaceTheme':'USER_INTERFACE_THEME_LIGHT'},
                                       'request':{'sessionId':self.sessionID,
                                                  'sessionIndex':'2',
                                                  'internalExperimentFlags':[],
                                                  'consistencyTokenJars':[]},
                                       'user':{},
                                       'clientScreenNonce':self.csn,
                                       'clickTracking':{'clickTrackingParams':self.clickTrackingParams}},
                            'continuation':self.continuation}
            data = self.session.post(self.base_url+f'/youtubei/v1/search?key={self.api_key}',headers=headers,json=request_data).json()            
            try:
                self.clickTrackingParams = data['onResponseReceivedCommands'][0]['clickTrackingParams']
                self.continuation = data['onResponseReceivedCommands'][0]['appendContinuationItemsAction']['continuationItems'][1]['continuationItemRenderer']['continuationEndpoint']['continuationCommand']['token']
            except:
                res = False
            #parse data
        else:                      
            data = self.session.get(self.base_url+f'/results?search_query={req}&pbj=1',headers=headers).json()
            self.session_token = data[1]['xsrf_token'] 
            self.sessionId = random.randint(0,6852209091371828659)
            try:
                self.visitor_data = data[1]['response']['responseContext']['webResponseContextExtensionData']['ytConfigData']['visitorData']
                self.csn = data[1]['response']['responseContext']['webResponseContextExtensionData']['ytConfigData']['csn']
                self.clickTrackingParams = data[1]['response']['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['trackingParams']
                self.continuation = data[1]['response']['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][1]['continuationItemRenderer']['continuationEndpoint']['continuationCommand']['token']
            except:
                res = False
            self.prev_url = self.base_url+urllib.parse.quote(f"/results?search_query={req}&pbj=1",safe='/=:?&%')
        return [data,res]



#Yep, right there
#pgtoken = data[1]['response']['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['continuations'][0]['nextContinuationData']['continuation']
#itct = data[1]['response']['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['continuations'][0]['nextContinuationData']['clickTrackingParams']

if __name__ == '__main__':
    vd = Videos()
    out = []
    while True:
        data = vd.get_videos('nude')
        dt = vd.parse_main_videos_info(data[0])
        for key,item in vd.parse_main_videos_info(data[0]).items():
            if item < 100:
                out.append((key,item))
        if not data[1]:
            break
    print(out)


        

