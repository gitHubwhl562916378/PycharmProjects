import requests
import json
import random
import threading
import time

class RequestTester (threading.Thread):
    uri = ''

    def __init__(self, tester):
        threading.Thread.__init__(self)
        self.tester = tester

    def makeAddRequest(self):
        return ('{}', '')

    def makeRemoveRequest(self):
        return ('{}', '')

    def timeInterval(self):
        return 1

    def run(self):
        while True:
            headers = {'content-type': 'application/json',
           'User-Agent': 'test'}
            body, uri = self.makeAddRequest()
            #print("body=" + body)
            r = requests.post(uri, data = body, headers = headers)
            print(r.json())
            time.sleep(self.timeInterval())

            body, uri = self.makeRemoveRequest()
            #print("body=" + body)
            r = requests.post(uri, data = body, headers = headers)
            print(r.json())
            time.sleep(self.timeInterval())

            
class SeyeAnalysisCamTester (RequestTester):
    def __init__(self, tester):
        RequestTester.__init__(self, tester)

    def timeInterval(self):
        return 60

    def makeAddRequest(self):
        cams = []
        for cam in self.tester.getCams():
            cam_info = { 'id' : cam,
                         'roi': [0, 0, 1920, 1080],
                         'ip' : '192.168.2.97',
                         'password' : '123ABCabc',
                         'port' : 8000,
                         'protocol' : 'KoaLaRtsp',
                         'rtsp' : "rtsp://192.168.2.97:5554/" + str(cam),
                         'user' : 'admin',
                         'warn_area' : [{"points": [{"x": 0, "y": 0}, {"x": 1920, "y": 0}, {"x": 1920, "y": 1080}, {"x": 0, "y": 1080}], "type": 0}]}
            cams.append(cam_info)
        cam_rqst = {'cameras' :  cams}
        request = json.dumps(cam_rqst)
        print("add_cams =" + request)
        return (request, 'http://192.168.2.97:9090/api/v1/device/add_cameras')

    def makeRemoveRequest(self):
        cam_rqst = {'cameras' :  self.tester.getCams()}
        request = json.dumps(cam_rqst)
        print("remove_cam = " + request)
        return (request, 'http://192.168.2.97:9090/api/v1/device/remove_cameras')

class MainTester:
    def __init__(self) :
        self.seye_analysis = SeyeAnalysisCamTester(self)
        # self.set_param = SetParamsTester("http://127.0.0.1:6066/city_ai_service/v1/set_alarm_params", self)

    def getCams(self) :
        random.seed()
        cams = [52, 53, 58, 62, 63, 64, 65, 66, 67, 68, 69, 70]
        # for num in range(53, 58):
        #     cam_id = random.randint(5, 10)
        #     if (cams.count(cam_id) > 0) :
        #         continue
        #     cams.append(cam_id)
        return cams

    def run(self):
        self.seye_analysis.start()
        self.seye_analysis.join()

test = MainTester()
test.run()
