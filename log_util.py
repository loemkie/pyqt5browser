import logging;
class LogUtil():
    def __init__(self):
        logging.basicConfig(level=logging.INFO,
                            filename='./log/mylike-p2.log',
                            filemode='a',
                            format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s');
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
        console.setFormatter(formatter)
        # 将定义好的console日志handler添加到root logger
        logging.getLogger('').addHandler(console)
    def info(self,msg):
        logging.info(msg);
    def error(self,msg):
        logging.error(msg);
