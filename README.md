# 多国语言翻译脚本

## 支持环境：
python 3.7.5 +
pip

## 环境安装：
```
pip install -r requirement.txt
```

### 请注意，需要编辑库文件位置如： vim /Users/admin/venv/py37/lib/python3.7/site-packages/google_trans_new/google_trans_new.py

```
第151行

原来：
response = (decoded_line + ']')

修改为：
response = decoded_line 


```


### 启动：
python MutiLanGen.py [os:ios,and,h5] path/to/the/xx.bundle
```
example:
python MutiLanGen.py ios xx.bundle
python MutiLanGen.py h5 ./
python MutiLanGen.py and ./
```

## 文件命名格式定义：

* ios xxx.bundule/[lan].lproj/Localizable.strings (例如中文(zh-Hans)为例：xxx.bundule/zh-Hans.lproj/Localizable.strings)
* android [lan]_strings.xml (例如中文(zh-Hans)为例：zh-Hans_string.xml)
* h5 [js]_strings.xml (例如中文(zh-Hans)为例：zh-Hans.js)

会在目录下寻找是否有该文件，如果没有，则创建，如果有，则插入倒数第二行


## 编辑 arm.json

```
{
    "zh":{
        "key":"带翻译文本"
    }
}
```

### 设计原理：
1. 通过解析arm.json -> google翻译生成英文内容
2. 通过1.产生的文件进行批量翻译
3. 翻译完成以后，去原有的文件上面匹配字符串，并写入最近的相似的字段中。如果含有一模一样的key,则跳过

注意： 对于js，字段还是会校验，因为分了模块化，所以不做模块解析，只会插入最后倒数第二个数据

### 中间会生成：
1. en.json 
2. total.json
