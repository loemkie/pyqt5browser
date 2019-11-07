def hostInit():
    outsides = ['10.100.81.215  ais-cloud-gateway.fore.run',
                '10.100.81.215  mc-app.fore.run',
                '10.100.81.215  ureport.fore.run',
                '10.100.81.215  eureka1.fore.run',
                '10.100.81.215  nexus.fore.run',
                '10.100.81.215  yapi.fore.run',
                '10.100.81.215  paas-master.fore.run',
                '10.100.81.215  ais-app.fore.run',
                '10.100.81.215  jenkins.fore.run',
                '10.100.81.215  iseek-cloud.fore.run',
                '10.100.81.215  ais-cloud-platform.fore.run',
                '10.100.81.215  uflo.fore.run',
                '10.100.81.215  ais-app-nginx.fore.run',
                '10.100.81.215  gogs.fore.run',
                '192.168.200.27  ais-cloud-gateway.mylike.okd',
                '192.168.200.28  ais-cloud-gateway.mylike.okd',
                '192.168.200.27  ais-app.mylike.okd',
                '192.168.200.28  ais-app.mylike.okd',
                '192.168.200.27  ais-cloud-platform.mylike.okd',
                '192.168.200.28  ais-cloud-platform.mylike.okd',
                '192.168.200.27  uflo.mylike.okd',
                '192.168.200.28  uflo.mylike.okd',
                '192.168.200.27  ais-app-nginx.mylike.okd',
                '192.168.200.28  ais-app-nginx.mylike.okd'
                ]

    output = open(r'C:\WINDOWS\system32\drivers\etc\HOSTS', 'w')
    for i in outsides:
        output.write(i)
        output.write("\n")
    output.close()

hostInit();