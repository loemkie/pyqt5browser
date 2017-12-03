pyinstaller --paths C:\Python35-32\Lib\site-packages\PyQt5\Qt\bin -D -w -y -i icon/m.ico standalone.py
set dir1=D:/mydocument/myprojects/python/mylike/pyqt5/dist/lib
set dir2=D:/mydocument/myprojects/python/mylike/pyqt5/dist/standalone
xcopy "%dir1%" "%dir2%" /e /y

"C:\Program Files (x86)\WinRAR\WinRAR.exe" a -ep1 D:\mydocument\myprojects\python\mylike\pyqt5\dist\mylike-p2_v2.2.rar ./dist\standalone
echo press file mylike-p2_v2.2.rar
pause