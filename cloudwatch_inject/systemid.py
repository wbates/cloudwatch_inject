import socket
import urllib2

class SystemId(object):
  def __init__(self):
    try:
      self.instanceid = urllib2.urlopen('http://169.254.169.254/latest/meta-data/instance-id', timeout = 1).read()
    except urllib2.URLError, e:
      self.instanceid = "None"

    self.hostname = socket.gethostname()
