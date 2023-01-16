import json

def file_put(f, key, value):
    if key is None or len(key) <= 0:
        return

    map = {}

    # 使用 open() 函数以只读模式打开我们的文本文件
    with open(f, 'r', encoding='UTF-8') as file:
        # 使用 read() 函数读取文件内容并将它们存储在一个新变量中
        data = file.read()
        map = json.loads(data)
    map[key] = value
    str = json.dumps(map)
    # 以只写模式打开我们的文本文件以写入替换的内容
    with open(f, 'w', encoding='UTF-8') as file:
        # 在我们的文本文件中写入替换的数据
        file.write(str)

def file_get(f, key):
    if key is None or len(key) <= 0:
        return None

    # 使用 open() 函数以只读模式打开我们的文本文件
    with open(f, 'r', encoding='UTF-8') as file:
        # 使用 read() 函数读取文件内容并将它们存储在一个新变量中
        data = file.read()
        map = json.loads(data)
        return map.get(key, None)

