**1.python3.5.2 32位**
https://www.python.org/downloads/release/python-353/
**2.pywin32**
https://sourceforge.net/projects/pywin32/files/pywin32/Build%20219/
**3.pyqt5**
 pip3 install PyQt5 成功
https://riverbankcomputing.com/software/pyqt/download5
pip3 install PyQt5==5.7.1

或者python3.6.0/pyqt5 5.7.1

Pyqt5 5.8对中文输入法不支持切换
**4.安装python的默认加入path**
**6.打包exe**

    pip install pyinstaller
    
    pyinstaller --paths C:\Python35-32\Lib\site-packages\PyQt5\Qt\bin -F -w standalone.py--不带图标
    pyinstaller --paths C:\Python35-32\Lib\site-packages\PyQt5\Qt\bin -F -w -i icon/m.ico standalone.py --单个文件
    pyinstaller --paths C:\Python35-32\Lib\site-packages\PyQt5\Qt\bin -D -w -y -i icon/m.ico standalone.py 文件夹/自动覆盖
    （使用pycharm比较快，都不需要安装pyinstaller）
    
    QTWEBENGINEPROCESS_PATH=C:\Python35\Lib\site-packages\PyQt5\Qt\bin
    
    could-not-find-QtWebEngineProcess-exe
    http://python.6.x6.nabble.com/PyQt5-application-could-not-find-QtWebEngineProcess-exe-td5189667.html

**问题：
打包后运行文件会报缺失的文件，把这些文件复制到exe文件夹下的目录下
编译成单个文件，相关文件需要放到exe文件对应的目录下，
如果编译到单个文件夹下，加载时间变快，相关依赖文件需要放到exe同级目录下**
    2017/03/04  16:59<DIR>  dll
    2017/03/05  12:40<DIR>  icon
    2017/02/18  15:1710,127,200 icudtl.dat
    2017/02/18  15:1713,312 QtWebEngineProcess.exe
    2017/02/18  15:17 4,908,397 qtwebengine_devtools_resources.pak
    2017/02/18  15:17 3,025,599 qtwebengine_resources.pak
    2017/02/18  15:17   128,262 qtwebengine_resources_100p.pak
    2017/02/18  15:17   183,503 qtwebengine_resources_200p.pak
**
配置文件：**
pip install configparser

**日志文件：**
Log_util.py
filemode='a' --加入文件
filemode='w' --每次清楚

**打包报错：**
安装：pywin32-220.win32-py3.5.exe
https://sourceforge.net/projects/pywin32/files/pywin32/Build%20220/

Copied pythoncom35.dll to C:\Windows\SysWOW64\pythoncom35.dll

Copied pywintypes35.dll to C:\Windows\SysWOW64\pywintypes35.dll

**安装与netty对接**
cd D:\mydocument\study\netty\protobuf-python-3.0.0\protobuf-3.0.0\python
python setup.py install
