# Flask-Statsd

Generate and send Flask metrics in [Influx Statsd](https://github.com/influxdata/telegraf/tree/master/plugins/inputs/statsd#influx-statsd) format.


# Install
```bash
pip install flask-statsd-tags
```


# Usage Example
```python
# myapp.py
from flask import Flask, Blueprint
from flask_statsd import FlaskStatsd

app = Flask(__name__)
FlaskStatsd(app=app, host='localhost', port=8125)

@app.route('/app/download')
def app_download():
    return 'OK'

bp = Blueprint('blueprint', __name__)

@bp.route('/device/<device>/stats')
def device_stats(device):
    return 'OK'

app.register_blueprint(bp)
```

* Request `/app/download` `/device/android/stats`

    ```
    flask_statsd.myapp,endpoint=app_download,status_code=200,server=vagrant-ubuntu-trusty-64:0.467062|ms
    flask_statsd.myapp,endpoint=blueprint.device_stats,status_code=200,server=vagrant-ubuntu-trusty-64:0.467062|ms
    ```

* Request `/`

    ```
    flask_statsd.myapp,endpoint=None,status_code=404,server=vagrant-ubuntu-trusty-64:0.467062|ms
    ```
