# -*- coding: utf-8 -*-
from socket import *
import google.protobuf
import msg_pb2

class TcpClient:
    # 测试，连接本机
    HOST = '127.0.0.1'
    # 设置侦听端口
    PORT = 9999
    BUFSIZ = 4096
    ADDR = (HOST, PORT)

    def __init__(self):
        self.client = socket(AF_INET, SOCK_STREAM)
        self.client.connect(self.ADDR)

        while True:
            data = input('>')
            # if not data:
            #     break
            # python3传递的是bytes，所以要编码
            # self.client.send(data.encode('utf8'))
            xmlData = "<?xml version=\"1.0\" encoding=\"utf-8\" ?>\n<Transfer attribute=\"Connect\">\n<outer to=\"15980882896\"/>\n<ext id=\"8109\"/>\n</Transfer>";
            xmlData="200"
            #b'\x00\x00\x00\x07\x08\x02\x12\x03200'
            #b'\x08\x01\x12\x03200'
            # xmlData.encode();
            msg = msg_pb2.Msg();
            msg.id = "1";
            msg.cmd = xmlData;
            # self.client.sendall(msg.SerializeToString())
            self.client.sendall(msg.SerializeToString())
            print('send data ' + xmlData)

            print('发送信息到%s：%s' % (self.HOST, data))
            if data.upper() == "QUIT":
                break
            data = self.client.recv(self.BUFSIZ)
            if not data:
                break
            rsp = msg_pb2.Msg();
            rspMsg = rsp.ParseFromString(data)
            print(rsp)



if __name__ == '__main__':
    client = TcpClient()