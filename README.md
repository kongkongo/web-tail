# web-tail

用于将文件通过web的形式输出到前台.

第一个版本就是读取文件然后把文件输出到屏幕上.


## 接口
```
url
http://ip:port/log/
方法  POST
```
112

入口参数
```
{
	"content_type":"line", [line,char] line的单位是每次读取一行,char表示每次读取一个字符
	"log_namespace":"default", # 日志的目录空间,
	"log_name":"test_1.log", # 日志的名称
	"beg_index":0, # 读取文本的开始位置
	"length":5 # 读取文本的长度
}
```
返回参数
```
{
    "code": "200",
    "content": "0\n1\n22\n333\n4444\n",
    "msg": "nothing"
}
```
目前 code和msg没有任何实际意义,content为内容,当content为""时,表示文件已经读完了.
