Introduction
------------
This is a fork of [jython-burp-api](https://github.com/mwielgoszewski/jython-burp-api). 
Make sure you check that project for futher information. I've forked it in order
to add my own extensions. 


Extensions
------------
* autoburp

  Automate Burp using jython. I've added own command line arguments to 
  the original run.py script.


Installation / Running
------------
Following steps are required:

a) Clone project

 $ git clone https://github.com/dorneanu/jython-burp-api
 
b) Download Jython standalone 

 $ wget http://search.maven.org/remotecontent?filepath=org/python/jython-standalone/2.5.3/jython-standalone-2.5.3.jar
 $ ln -s jython-standalone-2.5.3.jar jython.jar
 
c) Download BurpSuite Pro 

d) Run my extension

 $ java -jar ../jython.jar -Dpython.path=Lib/  testing.py -B burpsuite_pro.jar -h
 ...


Examples
------------
In order to automate the passive/active scanning in Burp make sure you 
activate those options in order to scan what's within your previously defined
scope. Now using my extension you can

 * add some URL to the scope
 * send that URL to the spidering machine
 
While Burp is spidering your target it will be automatically scanning 
the URLs found within the scope. This is how I do it:

 $ java -jar ../jython.jar -Dpython.path=Lib/  testing.py -B burpsuite_pro.jar --send-to-spider http://heise.de --add-to-scope http://heise.de -i 
 [--] Added new scope ...
 [--] Starting spider ...
