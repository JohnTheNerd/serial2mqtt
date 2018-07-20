import serial, json, traceback, os, multiprocessing, time, datetime
import paho.mqtt.client as mqtt
import paho.mqtt.publish as MQTTPublish

def processMessages(ttyName, mqttHost, mqttPort, timeout, retryCount, reconnectSeconds = 600):
  startTime = datetime.datetime.now()
  reconnectDelay = datetime.timedelta(seconds=reconnectSeconds)
  for i in range(1, retryCount):
    try:
      device = serial.Serial('/dev/' + ttyName, 9600, timeout=timeout)
    except:
      traceback.print_exc()
      time.sleep(5)
    break

  for i in range(1, retryCount):
    try:
      mqttClient = mqtt.Client()
      mqttClient.connect(mqttHost, mqttPort, timeout)
    except:
      traceback.print_exc()
      time.sleep(5)
    break

  while True:
    currentTime = datetime.datetime.now()
    if currentTime - startTime > reconnectDelay:
      mqttClient.reinitialise()
      startTime = datetime.datetime.now()
      mqttClient.connect(mqttHost, mqttPort, timeout)
    line = None
    parsedLine = None
    try:
      line = device.readline().decode('utf-8')
    except:
      traceback.print_exc()
      time.sleep(5)

    try:
      if line:
        parsedLine = json.loads(line)
    except:
      traceback.print_exc()
      time.sleep(1)

    try:
      if parsedLine:
        for topic in parsedLine.keys():
          mqttClient.publish(topic, parsedLine[topic])
    except:
      traceback.print_exc()

scriptPath = os.path.dirname(os.path.realpath(__file__))
configPath = os.path.join(scriptPath, 'config.json')
config = open(configPath).read()
config = json.loads(config)

if 'delay' in config:
  time.sleep(config['delay'])

if config['scan']:
  ttyName = []
  processes = []
  for i in os.listdir('/dev/'):
    if config['ttyName'] in i:
      ttyName.append(i)
  pool = multiprocessing.Pool(len(ttyName))
  for path in ttyName:
    processes.append(pool.apply_async(processMessages, [path, config['mqtt']['host'], config['mqtt']['port'], config['timeout'], config['retryCount']]))
  pool.close()
  pool.join()
else:
  processMessages(config['ttyName'], config['mqtt']['host'], config['mqtt']['port'], config['timeout'], config['retryCount'])
