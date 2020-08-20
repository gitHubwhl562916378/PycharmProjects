from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from framework import FrameWorkService
from framework.ttypes import *
from framework.constants import *

transport = TSocket.TSocket('127.0.0.1', 9090)
transport = TTransport.TBufferedTransport(transport)
protocol = TBinaryProtocol.TBinaryProtocol(transport)
client = FrameWorkService.Client(protocol)

transport.open()
client.set_log_level(2)
client.enable_log("FaceTraceDetection")
for num in range(0,1):
    print(num)
    client.enable_algo_ability(num, 1, 0)

print("load plugin "+ str(client.load_plugin('FaceTraceDetection')))
print("load plugin "+ str(client.load_plugin('FaceSnap')))
aibilyties = [ai_ability('FaceTraceDetection',''),ai_ability('FaceSnap','')]
client.enable_ai_ability(1, aibilyties)

client.start_decode(1,"rtsp://192.168.2.66/person.avi", 0)
transport.close()