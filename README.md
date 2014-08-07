# Flask-Webhook

Yet another Redis extension for Flask. `Flask-Webhook` makes use of Flask Blueprints and allows easy creation of application webhooks.

[![Latest Version](https://pypip.in/version/Flask-Webhook/badge.png)]
(https://pypi.python.org/pypi/Flask-Webhook/)
[![Downloads](https://pypip.in/download/Flask-Webhook/badge.png)]
(https://pypi.python.org/pypi/Flask-Webhook/)
[![Download format](https://pypip.in/format/Flask-Webhook/badge.png)]
(https://pypi.python.org/pypi/Flask-Webhook/)
[![License](https://pypip.in/license/Flask-Webhook/badge.png)]
(https://pypi.python.org/pypi/Flask-Webhook/)


## Supported Platforms

* OSX and Linux.
* Python 2.7
* [Flask](http://flask.pocoo.org/) 0.10.1

Probably works with other versions as well.

## Quickstart

Install:
```bash
pip install Flask-Webhook
```

Example:
```python
from flask import Flask
from flask.ext.webhook import WebHook

app = Flask(__name__)

#create webhook object (name and app are optional)
#if app is not passed in in the constructor, my_webhook.init_app(app) is needed.
my_webhook = WebHook(name='optional_webhook_name', url_prefix='/webhooks' app=app)
my_webhook.add_route('/something', methods=['GET', 'POST'])

#define a function handler to be called by the webhook
def some_function(hookrequest):
  do something with the request object received by the webhook

#attach your function handler to the webhook.
#you can attach as many as you want and they all are going to be called
# () should not be included 
my_webhook.handlers['some_name_for_your_handler'] = some_function
```


## Factory Example

```python
# extensions.py
from flask.ext.webhook import WebHook

my_webhook = WebHook(url_prefix='/webhooks')
```

```python
# application.py
from flask import Flask
from extensions import my_webhook

def some_function(request):
    do something

def some_other_function(request):
    do something else

def create_app():
    app = Flask(__name__)
    my_webhook.add_route('/something', methods=['GET', 'POST'])
    my_webhook.handlers['action1'] = some_function
    my_webhook.handlers['action2'] = some_other_function
    my_webhook.init_app(app)
    return app
```

```python
# manage.py
from application import create_app

app = create_app()
app.run()
```

## Changelog

#### 0.1.0

* Initial release.
