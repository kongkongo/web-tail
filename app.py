from flask import Flask
from flask import request
from flask_socketio import SocketIO
import os
from conf import config

app = Flask(__name__)
socketio = SocketIO(app)


# 和Vue-socketio配合使用时，使用下面的，避免跨域
# socketio = SocketIO(app , cors_allowed_origins="*")
def readline(file_obj, begin_index, length):
    """
    返回从某个位置开始,第x行数据
    begin_index 表示从第0行开始
    """
    i = 0
    while i < begin_index:
        file_obj.readline()
        i = i + 1
    ans = ""
    finished = False
    while i < begin_index + length:
        content = file_obj.readline()
        if content == "":
            finished = True
            break
        ans = ans + content
        i = i + 1
    return ans, finished


def readchar(file_obj, begin_index, length):
    finished = False
    file_obj.seek(begin_index, 0)
    content = file_obj.read(length)
    current_index = file_obj.tell()
    if current_index > begin_index + length:
            finished = True
    return content,finished


@app.route('/')
def hello():
    return 'Hello, World!'


def get_log_abs_path(log_namespace, log_name):
    """
    [获得日志的绝对路径]

    Args:
        log_namespace ([string]): [用于区分,不同类型的日志可能存放的路径不一样,]
        log_name ([type]): [日志文件的名字]
    """
    if log_namespace == "default":
        log_dir_path = config.LogConfiger.get_config_value("default")
    else:
        log_dir_path = config.LogConfiger.get_config_value(log_namespace)
    # log_name 可能要按照要求调整.
    return os.path.join(log_dir_path, log_name)


@app.route('/log/', methods=['POST'])
def get_log():
    """
    请求数据格式json.
    入口参数:
    content_type: char , line 一个字符字符的请求或者一行一行的请求,default=line
    log_name: 日志的名称
    log_namespace: 日志属于的模块类型,是训练的日志,还是其他的日志,默认是default,未来用于扩展字段.
    beg_index: 开始位置,
    length: 要读的内容
    返回参数:
    content:  读取数据的内容,
    next_index: int 下一个的位置
    msg:  返回一些消息,例如文件找不到,没有读文件的权限,已经到了底部了.
    code: 代码定义,消息是否已经到底部了.0
    """
    json_data = request.json
    content_type = json_data.get("content_type", "line")
    log_namespace = json_data.get("log_namespace", "default")
    log_name = json_data.get("log_name", "default")
    log_name = "{}.log".format(log_name)
    beg_index = json_data.get("beg_index", 0)
    length = json_data.get("length", 500)
    abs_file_path = get_log_abs_path(log_namespace, log_name)
    content = ""
    try:
        if not os.path.exists(abs_file_path):
            return {"content": content, "msg": "文件不存在", "code": "404"}

        if not os.path.isfile(abs_file_path):
            return {"content": content, "msg": "文件不存在", "code": "404"}

        with open(abs_file_path, "r") as log_file:
            if content_type == "char":
                content,finished = readchar(log_file, beg_index, length)

                if finished!=True:
                    return {"content": content, "msg": "文件中还有数据", "code": "201"}
                else:
                    return {"content": content, "msg": "文件已经读取完毕", "code": "204"}
            else:
                content,finished = readline(log_file, beg_index, length)
                if finished != True:
                    return {"content": content, "msg": "文件中还有数据", "code": "201"}
                else:
                    return {"content": content, "msg": "文件已经读取完毕", "code": "204"}

    except Exception as e:
        print(e)
        return {"content": content, "msg": "请求出错", "code": "500"}
    # 还有数据 code 201 msg 还有数据
    # 没有数据 code 204 msg 文件已经读完
    # 文件不存在 code 404  msg 读取的文件不存在。
    # return {"content": content, "msg": "Success", "code": "200"}

@app.route('/log/', methods = ['GET'])
def get_log_data():
    """
       请求数据格式json.
       入口参数:
       content_type: char , line 一个字符字符的请求或者一行一行的请求,default=line
       log_name: 日志的名称
       log_namespace: 日志属于的模块类型,是训练的日志,还是其他的日志,默认是default,未来用于扩展字段.
       beg_index: 开始位置,
       length: 要读的内容
       返回参数:
       content:  读取数据的内容,
       next_index: int 下一个的位置
       msg:  返回一些消息,例如文件找不到,没有读文件的权限,已经到了底部了.
       code: 代码定义,消息是否已经到底部了.0
   """

    content_type = request.args.get("content_type", "line")
    log_name = request.args.get('task_uuid',"default")
    log_name = "{}.log".format(log_name)
    log_namespace = request.args.get("log_namespace","default")
    beg_index = int(request.args.get("beg_index",0))
    length = int(request.args.get("length", 500))
    content=""
    abs_file_path = get_log_abs_path(log_namespace,log_name)
    try:
        if not os.path.exists(abs_file_path):
            return {"content": content, "msg": "文件不存在", "code": "404"}

        if not os.path.isfile(abs_file_path):
            return {"content": content, "msg": "文件不存在", "code": "404"}

        with open(abs_file_path, "r") as log_file:
            if content_type == "char":
                content, finished = readchar(log_file, beg_index, length)

                if finished != True:
                    return {"content": content, "msg": "文件中还有数据", "code": "201"}
                else:
                    return {"content": content, "msg": "文件已经读取完毕", "code": "204"}
            else:

                content, finished = readline(log_file, beg_index, length)
                if finished != True:
                    return {"content": content, "msg": "文件中还有数据", "code": "201"}
                else:
                    return {"content": content, "msg": "文件已经读取完毕", "code": "204"}

    except Exception as e:
        print(e)
        return {"content": content, "msg": "请求出错", "code": "500"}





if __name__ == '__main__':
    #配置文件中设置端口号
    port = config.PortConfiger.get_config_value('port')
    Flask.run(app, host='0.0.0.0', port=port)