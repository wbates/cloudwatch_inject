import os

class InjectConfig(object):
  def __init__(self):
    self.basedir = os.path.abspath(os.path.dirname(__file__) + "/../")
    self.confdir = os.path.abspath(self.basedir + "/etc/")

class BotoConfig(object):
  @staticmethod
  def env_init():
    config = InjectConfig()
    os.environ['BOTO_CONFIG'] = os.path.abspath(config.confdir + "/config.ini")
