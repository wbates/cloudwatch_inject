from systemid import SystemId
from monitor import Monitor
from monitorconfig import MonitorConfig


class MonitorSet(dict):
  def __init__(self):
    sysid = SystemId()
    hostname = sysid.hostname
    instanceid = sysid.instanceid

    mondata = MonitorConfig()
    for k in mondata.config:
      self[k] = Monitor(mondata.config[k],k,hostname,instanceid)

  def list_monitors(self):
    print "Available monitors:"
    for k in self:
      print "  \033[94m\033[1m" + k + "\033[0m - " + self[k].description

  def print_metrics(self):
    print "Current Monitor Metrics:"
    for k in self:
      self[k].print_metric()

  def inject_metrics(self,quiet=False):
    if quiet == False:
      print "Injecting Metrics:"

    for k in self:
      self[k].inject_metric(quiet)
