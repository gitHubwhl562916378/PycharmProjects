# -*- coding: utf-8 -*-

import os,sys
import io,shutil
import urllib
import json
import http.server
import base64
import cv2
import numpy as np

PORT_NUMBER = 8089
IMG_BASE_PATH="alarm"
def onEceive(data):
    js_obj = json.loads(data)
    img_base64_content = js_obj["scene"]
    img_content = base64.b64decode(img_base64_content)
    img = cv2.imdecode(np.fromstring(img_content, np.uint8), cv2.IMREAD_COLOR)
    
    temp_obj = js_obj
    del temp_obj["scene"]

    scores = []
    if "scores" in js_obj:
        scores = js_obj["scores"]

    boxes = []
    if "boxes" in js_obj:
        boxes = js_obj["boxes"]
    else:
        if "faceBoxes" in js_obj:
            boxes = js_obj["faceBoxes"]
            value_array = temp_obj["values"]
            for person in value_array:
                face = person["face"]
                del face["face"]
    
    wash_car = []
    if "itemsInBox" in js_obj:
        js_item = js_obj["item"]
        if "extra" in js_item:
            wash_car = js_item["extra"]

    print(json.dumps(temp_obj))
    # rects =  [item + '-1' for rt_obj in boxes if not rt_obj.endswith('1')]
    rects = [((rt_obj["x"], rt_obj["y"]), (rt_obj["x"] + rt_obj["width"], rt_obj["y"] + rt_obj["height"])) for rt_obj in boxes]
    print("rects----- {}".format(rects))
    for (i, rt) in enumerate(rects, start=0):
        if js_obj["alarmType"] == "Parabolic":
            pass
        else:
            cv2.rectangle(img, rt[0], rt[1], (0,0,255), 2)
            
        if len(scores):
            cv2.putText(img, scores[i], (rt[0][0], rt[0][1]), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 1)
        if len(wash_car):
            water_state_label = "Water"
            wat_sta = wash_car[i]["hasWater"]
            if not wash_car[i]["hasWater"]:
                water_state_label = "No water"
            cv2.putText(img, water_state_label, (200, 300), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 0), 2)
            
            cv2.putText(img, "wash time " + str(wash_car[i]["washTime"]) + " s", (200, 400), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 0), 2)

    if "areas" in js_obj:
        areas = js_obj["areas"]
        pts = [np.array([[pt["x"], pt["y"]] for pt in area], np.int32).reshape(-1, 1, 2) for area in areas]
        print("areas--- {}".format(pts))
        cv2.polylines(img, pts, True, (255,255,0), 3)

    ability = js_obj["alarmType"]
    camera_id = js_obj["cameraId"]

    cv2.putText(img, ability, (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 0), 2)

    img_save_prefix = IMG_BASE_PATH+"/"+camera_id+"/"+ability
    os.makedirs(img_save_prefix, exist_ok=True)

    cv2.imwrite(img_save_prefix + "/" + str(js_obj["ts"]) + ".jpg", img)

    # file = open(IMG_BASE_PATH + "/" + str(IMG_INDEX) + ".jpg", 'wb')
    # IMG_INDEX += 1
    # file.write(img_content)
    # file.close()

class myHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        print('URL=',self.path)
        self.protocol_version = 'HTTP/1.1'
        self.send_response(200)
        self.send_header('Content-type','application/json;charset=UTF-8')
        self.end_headers()

        self.wfile.write("not support get")

    def do_POST(self):
        recvData = self.rfile.read(int(self.headers['Content-Length']))
        print(self.path, self.headers)
        self.protocol_version = 'HTTP/1.1'
        self.send_response(200)
        self.send_header('Content-type','application/json;charset=UTF-8')
        self.end_headers()
        if  self.path == '/oceanus/api/v1/receive':
            onEceive(recvData)

            json_res = {"code" : 200, "message": "OK"}
            json_response=json.dumps(json_res)
            self.wfile.write(json_response.encode())
        elif self.path == '/eureka/apps/osmagic-algo-dynamic':
            print(recvData)
            json_res = {"code" : 200, "message": "OK"}
            json_response=json.dumps(json_res)
            self.wfile.write(json_response.encode())
        self.close_connection

try:
    server = http.server.HTTPServer(('',PORT_NUMBER),myHandler)
    print('Started httpserver on port ' , PORT_NUMBER)
    server.serve_forever()

except KeyboardInterrupt:
    print('^C received, shutting down the web server')
    server.socket.close()
