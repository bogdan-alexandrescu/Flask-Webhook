"""Flask extension leveraging Blueprints for creating application webhooks.

https://github.com/Bogdan-Alexandrescu/Flask-Webhook
https://pypi.python.org/pypi/Flask-Webhook
"""
import sys

from flask import Blueprint, jsonify, make_response, request


__author__ = '@balex'
__license__ = 'MIT'
__version__ = '0.1.0'


class FlaskWebhookHandleException(BaseException): pass


class WebHook(object):
  """The JIRA hook blueprint and handler."""

  def __init__(self, url_prefix, name=None, log=None, app=None):
    """Construct the JIRAHook Blueprint."""
    self._app = app
    self._log = log
    self._name = name
    self._blueprint = Blueprint(self._name, __name__, url_prefix=url_prefix)
    self.handlers = dict()
    if app is not None:
      self.init_app(app)

  def add_route(self, route, methods):
    self._blueprint.add_url_rule(route, view_func=self._run_endpoint_handlers, methods=methods)
    if self._app:
      self.init_app(self._app)

  @property
  def hook(self):
      return self._blueprint
  
  def _run_endpoint_handlers(self):
    """Calls the event handlers handlers attached to the webhook object and returns a json response.

    """
    for key, func in self.handlers.items():
      try:
        func(request)
      except Exception:
        if self._log:
          self._log.error( "Caught exception while handling '%s': %s" % (key, sys.exc_info()) )
        raise FlaskWebhookHandleException( "Caught exception while handling '%s': %s" % (key, sys.exc_info()) )

    return_message = (dict(status='success', message="'%s' was triggered successfully" % self._name) 
      if self._name else dict(status='success'))

    if self._log:
      self._log.info(return_message)
    return make_response(jsonify(return_message), 200)

  def init_app(self, app):
    """Method used to register the webhooks on the flask app object"""
    app.register_blueprint(self._blueprint)