import sys
import subprocess
from connector import Connector


class Monitor(object):
  def __init__(self,monconf,monid,hostname,instanceid):
    self.monid = monid
    self.description = monconf['description']
    self.metricname = monconf['metricName']
    self.namespace = monconf['nameSpace']
    self.units = monconf['units']
    self.dimensions = monconf['dimensions']
    self.command = monconf['command']

    if 'instanceid' in monconf:
      self.dimensions['InstanceId'] = monconf['instanceid']
    else:
      self.dimensions['InstanceId'] = instanceid

    if 'hostname' in monconf:
      self.dimensions['Hostname'] = monconf['hostname']
    else:
      self.dimensions['Hostname'] = hostname

    self.value = None

  def get_value(self):
    cmdparts = self.command.split('|')
    proc = None
    for idx, part in enumerate(cmdparts):
      if idx == 0:
        proc = subprocess.Popen(part, stdout=subprocess.PIPE, shell=True)
      else:
        proc = subprocess.Popen(part, stdin=proc.stdout, stdout=subprocess.PIPE, shell=True)
    return proc.communicate()[0].rstrip()

  def load_value(self):
    self.value = self.get_value()

  def print_metric(self):
    if self.value == None:
      self.load_value()

    for k in self.dimensions:
      if k == 'Hostname' or k == 'InstanceId':
        continue
      dimstr = k+"="+self.dimensions[k]+";"
      
    print '  ' + self.dimensions['InstanceId']+"|"+self.dimensions['Hostname']+"|"+self.namespace+"/"+self.metricname+" ["+dimstr+"] \033[94m\033[1m("+self.value+" "+self.units+")\033[0m"

  def inject_metric(self,quiet):
    if self.value == None:
      self.load_value()

    if quiet == False:
      self.print_metric()

    cw = Connector()
    retval = cw.inject(self.metricname,self.namespace,self.value,self.units,self.dimensions)
    
    if retval == -1:
      sys.stderr.write("\033[91mERROR: Monitor [" + self.monid + "] failed to be injected into CloudWatch.\n")
      sys.stderr.write("  -- Check JSON entry and that command is returning proper value and format.\033[0m\n")

