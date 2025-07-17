import socket

#HOSTはhostname -Iで確認
HOST = ""
PORT = 50007 #受信側と同じポート番号を指定

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST,PORT))
    
    #120点を送る場合のテスト
    msg = r'''120'''
    
    s.sendall(msg.encode())
    print(msg," is sended")