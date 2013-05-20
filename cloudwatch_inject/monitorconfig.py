import os
import json
import glob
from injectconfig import InjectConfig


class MonitorConfig(object):
  def __init__(self):
    self.config = {}
    conf = InjectConfig()
    for filename in glob.glob(conf.confdir + "/*.json"):
      self.config = dict(self.config.items() + json.load(open(os.path.abspath(filename))).items())
