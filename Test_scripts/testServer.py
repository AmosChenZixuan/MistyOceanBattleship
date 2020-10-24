from pywss import Pyws, route
import json

'''
此脚本用来回应游戏页面的创建房间申请。监听客户端的创建房间申请，与host用户名
并返回房间号以及host用户
'''

@route('/mistyocean')
def requestRoom(request, data):
    name = data
    print(name)
    data = {"roomNumber":4399,"hostUser":name}
    return json.dumps(data,ensure_ascii=False)

if __name__ == '__main__':
    ws = Pyws(__name__, address='127.0.0.1', port=4399)
    ws.serve_forever()
    
