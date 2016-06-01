# Flask-Statsd
收集每个请求的性能数据，发送到 statsd。数据的key是把 url_route 里面的匹配部分删去，
把 / 替换成 . ，并且在前面增加 app_name 。同时会自动增加 `status_code` `server`
tag。

# Install
```bash
pip install flask-statsd-tags
```

# Send data
```python
@route('/app/download')
def download():
    pass

@route('/app/<device>/stats')
def device_download(device):
    pass
```

* 访问 `/app/download`，会自动向 Statsd 发送 

    ```
    myapp.app.download.count,status_code=200,server=vagrant-ubuntu-trusty-64:1|c
    myapp.app.download.time,status_code=200,server=vagrant-ubuntu-trusty-64:0.467062|ms
    myapp.request.count,status_code=200,server=vagrant-ubuntu-trusty-64:1|c
    myapp.request.time,status_code=200,server=vagrant-ubuntu-trusty-64:0.467062|ms
    ```

* 访问 `/app/android/stats`，会自动发送

    ```
    myapp.app.stats.count,status_code=200,server=vagrant-ubuntu-trusty-64:1|c
    myapp.app.stats.time,status_code=200,server=vagrant-ubuntu-trusty-64:0.467062|ms
    myapp.request.count,status_code=200,server=vagrant-ubuntu-trusty-64:1|c
    myapp.request.time,status_code=200,server=vagrant-ubuntu-trusty-64:0.467062|ms
    ```


# 使用
```python
from flask import Flask
from flask.ext.statsd import FlaskStatsd

app = Flask(__name__)
FlaskStatsd(app=app, host='localhost', port=8125, prefix='')

```

# Statsd
Statsd 使用的 Influxdb 扩展的格式，支持 tag。
