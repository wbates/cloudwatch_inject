from injectconfig import BotoConfig
BotoConfig.env_init()
import boto


class Connector(object):
  def __init__(self):
    self.cw = boto.connect_cloudwatch()

  def inject(self,metricname,namespace,value,units,dimensions):
    try:
      retval = self.cw.put_metric_data( namespace, metricname, value, None, units, dimensions )
    except boto.exception.BotoServerError, e:
      return -1
