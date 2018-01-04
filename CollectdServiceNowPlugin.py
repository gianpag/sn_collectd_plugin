import collectd
import random
import time
import requests
import socket

# Global variables for collectd.conf configuration paramaeters
MID_WEBSERVER_ADDRESS = ''
USERNAME = ''
PASSWORD = ''


def getConfig(config):
    for node in config.children:
        key = node.key.lower()
        val = node.values[0]
        if key == 'mid_webserver_address':
            global MID_WEBSERVER_ADDRESS
            MID_WEBSERVER_ADDRESS = val
        elif key == 'username':
            global USERNAME
            USERNAME = val
        elif key == 'password':
            global PASSWORD
            PASSWORD = val
        else:
            collectd.info('Unrecognized key: "%s"' % key)


def sendDataToMid(pluginName, value):
    url = 'http://' + MID_WEBSERVER_ADDRESS + "/api/mid/sa/metrics"
    collectd_hostname = socket.getfqdn()
    ResourceName = 'webServer'
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    timeStr = str(int(time.time()) * 1000)
    valueStr = str(value)
    message = "[{\"timestamp\": " + timeStr + ",\"value\": " + valueStr
    message += ", \"node\" : \"" + collectd_hostname
    message += "\", \"metric_type\": \"" + pluginName
    message += "\", \"resource\": \"" + ResourceName
    message += "\", \"source\": \"CollectD\","
    message += "\"ci_identifier\": {\"MonitoringObjectType\": \"webServer\","
    message += "\"MonitoringObjectName\": \"GpWebServer1\","
    message += "\"name\": \"GpWebServer1\"}}]"

    '''
    collectd.info(message + '\n\nFQDN: ' + socket.getfqdn() + '\n\nHostname: '
                  + socket.gethostname())
    '''

    r1 = r1 = requests.Session()
    res = r1.post(
        url,
        headers=headers,
        auth=(USERNAME, PASSWORD),
        data=message
    )

    r1_status_code = str(res.status_code)

    # collectd.info('Send To ServiceNow Mid http response: ' + r1_status_code + '\n')


'''
def read(data=None):
    vl = collectd.Values(type='gauge')
    vl.plugin = 'Random'
    vl.dispatch(values=[str(16000 + random.randint(0, 1999))])
'''


def write(vl, data=None):
    metricname = ''
    for i in vl.values:
        metricname = vl.plugin
        if vl.plugin_instance != '':
            metricname += '/'
            metricname += str(vl.plugin_instance)
        else:
            metricname += '/'
            metricname += str(vl.plugin)

        if vl.type != '':
            metricname += '/'
            metricname += str(vl.type)
        if vl.type_instance != '':
            metricname += '/'
            metricname += str(vl.type_instance)

        sendDataToMid(metricname, i)


# collectd.register_read(read)
collectd.register_config(getConfig)
collectd.register_write(write)
