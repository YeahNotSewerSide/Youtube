import requests
import urllib.parse


class Videos:
    def __init__(self):
        self.session_token = ''
        self.session = requests.Session()
        self.base_url = 'https://www.youtube.com'
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'}
        self.session.get(self.base_url+'/?pbj=1',headers=self.headers)
        self.prev_url = self.base_url
    def parse_main_videos_info(self,data:dict)->dict:#{id:viewcount} Only videos and only main info
        out = {}
        try:
            for item in data[1]['response']['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']:
                if 'videoRenderer' not in item.keys():
                    continue
                try:
                    parse = (item['videoRenderer']['viewCountText']['simpleText'].split(' '))[0]
                    dt = parse.replace('.','')
                except:
                    continue #if stream
                try:
                    out[item['videoRenderer']['videoId']] = int(dt)
                except:
                    out[item['videoRenderer']['videoId']] = 0
        except:
            try:
                for item in data[1]['response']['continuationContents']['itemSectionContinuation']['contents']:
                    if 'videoRenderer' not in item.keys():
                        continue
                    try:
                        parse = (item['videoRenderer']['viewCountText']['simpleText'].split(' '))[0]
                        dt = parse.replace('.','')
                    except:
                        continue #if stream
                    try:
                        out[item['videoRenderer']['videoId']] = int(dt)
                    except:
                        out[item['videoRenderer']['videoId']] = 0
            except:
                pass
        return out

    def get_videos(self,req:str,pgtoken='',itct=''):
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

        if self.session_token != '' and pgtoken != '':           
            data = self.session.post(self.base_url+f'/results?search_query={req}&pbj=1&ctoken={pgtoken}&continuation={pgtoken}&itct={itct}',data=f'urllib.parse.quote(self.session_token)',headers=headers).json()
            
        else:                      
            data = self.session.get(self.base_url+f'/results?search_query={req}&pbj=1',headers=headers).json()
            self.session_token = data[1]['xsrf_token'] 
            self.prev_url = self.base_url+urllib.parse.quote(f"/results?search_query={req}&pbj=1",safe='/=:?&%')
        return data



#Yep, right there
#pgtoken = data[1]['response']['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['continuations'][0]['nextContinuationData']['continuation']
#itct = data[1]['response']['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['continuations'][0]['nextContinuationData']['clickTrackingParams']




        

