# -*- coding: utf-8 -*-
from java.lang import System

from org.python.util import JLineConsole, PythonInterpreter

import logging
import os.path
import sys
import time
from threading import Thread

class MyThread(Thread):
    # Run own thread to get things done
    def __init__(self, burp, options):
        Thread.__init__(self, name='jython-console')
        self.opts   = options
        self.burp   = burp

    def run(self):
        from java.net import URL

        # Add new scope
        if self.opts.add_to_scope:
            self.burp.includeInScope(URL(self.opts.add_to_scope))
            print("[--] Added new scope ...")

        # Send URL to spider
        if self.opts.send_to_spider:
            self.burp.sendToSpider(URL(self.opts.send_to_spider))
            print("[--] Starting spider ...")

        # Start interactive jython console
        if self.opts.interactive:
            from java.util import Properties
            pre_properties = System.getProperties()
            pre_properties['python.console'] = 'org.python.util.ReadlineConsole'
            post_properties = Properties()

            PythonInterpreter.initialize(pre_properties, post_properties, [])

            # Attach threaded console to BurpExtender
            self.burp.console = console = JLineConsole()
            console.set('Burp', self.burp)

            try:
                self.burp.stdout.write('Launching interactive session...\n')
            except Exception:
                sys.stdout.write('Launching interactive session...\n')

            ConsoleThread(console).start()

def start_burp(options, *args):
    sys.path.extend([os.path.join('java', 'src'), options.burp])

    from burp_extender import BurpExtender as MyBurpExtender, ConsoleThread
    from burp import StartBurp
    from pprint import pprint
    import BurpExtender

    from gds.burp.config import Configuration

    if options.debug:
        logging.basicConfig(
            filename='jython-burp.log',
            format='%(asctime)-15s - %(levelname)s - %(message)s',
            level=logging.DEBUG)

    elif options.verbose:
        logging.basicConfig(
            filename='jython-burp.log',
            format='%(asctime)-15s - %(levelname)s - %(message)s',
            level=logging.INFO)

    else:
        logging.basicConfig(
            filename='jython-burp.log',
            format='%(asctime)-15s - %(levelname)s - %(message)s',
            level=logging.WARN)

    # Set the BurpExtender handler to the Pythonic BurpExtender
    Burp = MyBurpExtender()
    Burp.config = Configuration(os.path.abspath(opt.config))
    Burp.opt = options
    Burp.args = args

    BurpExtender.setHandler(Burp)
    StartBurp.main(args)

    # In latest Burp, callbacks might not get registered immediately
    while not Burp.cb:
        time.sleep(0.1)

    # Disable Burp Proxy Interception on startup
    Burp.setProxyInterceptionEnabled(False)

    # Check for options and start new thread(s)
    MyThread(Burp, options).start()

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()

    parser.add_option('-B', '--load-burp', dest='burp',
                      help='Load Burp Jar from PATH', metavar='PATH')

    parser.add_option('-i', '--interactive',
                      action='store_true',
                      help='Run Burp in interactive mode (Jython Console)')

    parser.add_option('-f', '--file', metavar='FILE',
                      help='Restore Burp state from FILE on startup')

    parser.add_option('-d', '--debug',
                      action='store_true',
                      help='Set log level to DEBUG')

    parser.add_option('-v', '--verbose',
                      action='store_true',
                      help='Set log level to INFO')

    parser.add_option('-P', '--python-path',
                      default='',
                      help='Set PYTHONPATH used by Jython')

    parser.add_option('-C', '--config',
                      default='burp.ini',
                      help='Specify alternate jython-burp config file')

    parser.add_option('--disable-reloading',
                      action='store_true',
                      help='Disable hot-reloading when a file is changed')

    parser.add_option('--send-to-spider', type=str, help='Send URL to spider')
    parser.add_option('--add-to-scope', type=str, help='Add URL to scope')

    opt, args = parser.parse_args()

    if not opt.burp:
        print('Load Burp Error: Specify a path to your burp.jar with -B')
        parser.print_help()
        sys.exit(1)

    start_burp(opt, *args)
