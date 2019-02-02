# serial2mqtt
A Python 3 microservice that streams LDJSON (Line-Delimitered JSON) data from a serial port to a given MQTT broker.

The JSON data must be one object, with each key being the topic you'd like to send data to. In the example below, the topics `Temperature`, `Humidity`, and `Heat Index` will be notified of their respective values.

Example: `{"Temperature": 24.00, "Humidity": 81.20, "Heat Index": 24.58}`

## Usage

- Clone this repository.

- Install all the requirements by running `pip3 install pyserial paho-mqtt`

- Modify config.json to match your preferences. ttyName gets appended to `/dev/` to get your device name.

    - If scan is enabled, the application will launch a separate thread for any device containing the value of ttyName. Useful if you don't _exactly_ know which device serial2mqtt needs to talk to.

- Run main.py!

There is an example serial2mqtt.service file you can copy to `/etc/systemd/system/` (after changing the paths) and run `sudo systemctl enable serial2mqtt` to have this service continuously run for you!

It also runs on Docker. You could create a config.json file and run:

```
docker build -t serial2mqtt .
docker run --device=/dev/ttyACM0 serial2mqtt    # add "--restart always" to continuously restart
```
