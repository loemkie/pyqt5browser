import wmi


def DnsDef():
    wmiService = wmi.WMI()
    colNicConfigs = wmiService.Win32_NetworkAdapterConfiguration(IPEnabled=True)
    if len(colNicConfigs) < 1:
        print("没有找到可用的网络适配器")
        exit()
    objNicConfig = colNicConfigs[0]
    arrDNSServers = ['218.85.152.99']
    returnValue = objNicConfig.SetDNSServerSearchOrder(DNSServerSearchOrder=arrDNSServers)
    if returnValue[0] == 0:
        print("修改成功")
    else:
        print("修改失败")
DnsDef()