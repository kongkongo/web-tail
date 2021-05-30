


with open("test/test_1.log","r") as test_file:
    start=0
    end=0
    
    char=test_file.readline()
    print(char)
    while char !="\n":
        char=test_file.read(1)

    line=test_file.read(3)
    print(line)
    line=test_file.read(3)
    print(line)



def readline(file_obj,begin_index,length):
    """
    返回从某个位置开始,第x行数据
    begin_index 表示从第0行开始
    """
    i=0
    while i<begin_index:
        file_obj.readline()
        i=i+1
    ans=""
    while i<begin_index+length:
        content=file_obj.readline()
        if content=="":
            break
        ans=ans+content
        i=i+1
    return ans 

def readchar(file_obj,begin_index,length):
    file_obj.seek(begin_index,0)
    content=file_obj.read(length)
    print(content)
    return content


with open("test/test_1.log","r") as test_file:
    start=0
    end=0
    readchar(test_file,0,20)
    test_file.seek(0,0)
    readline(test_file,1,3)
    one_line= test_file.readline()
    line_num=1
    start=0
    while one_line:
        print(line_num,test_file.tell(),start,len(one_line))
        line_num=line_num+1
        one_line= test_file.readline()