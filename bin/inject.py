#!/usr/bin/env python

import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/../"))

from optparse import OptionParser
from cloudwatch_inject.injectconfig import InjectConfig
from cloudwatch_inject.monitorset import MonitorSet

def main():
  # Usage and options parsing
  usage = "usage: %prog [options]"
  epilog = "Note: running with no options will cause all metrics to be injected."
  parser = OptionParser(usage=usage,epilog=epilog)
  parser.add_option("-l", "--list", help="List available monitors", action="store_true", default=False, dest="monlist")
  parser.add_option("-d", "--display-only", help="Only display metric and value, do not inject into CloudWatch", action="store_true", default=False, dest="disponly")
  parser.add_option("-q", "--quiet", help="Only inject into CloudWatch, do not display any output", action="store_true", default=False, dest="injectonly")
  parser.add_option("-m", "--monitor", help="Specify comma-delimited list of monitors to run", default=None, dest="monitor")
  (options, args) = parser.parse_args()

  # Instantiate configuration

  # Instantiate full monitoring object
  monitorset = MonitorSet()

  # If list is requested, only list the available monitors and exit
  if options.monlist == True:
    monitorset.list_monitors()
    exit()

  if options.monitor != None:
    for mon in options.monitor.split(','):
      try:
        if options.disponly == True:
          monitorset[mon].print_metric()
        else:
          monitorset[mon].inject_metric(options.injectonly)
      except KeyError, e:
        sys.stderr.write("\033[91mERROR: Monitor [" + mon + "] does not appear to exist.\033[0m\n")
    exit()


  if options.disponly == True:
    monitorset.print_metrics()
    exit()

  monitorset.inject_metrics(options.injectonly)

if __name__ == "__main__":
  main()
