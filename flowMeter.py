#!/usr/bin/env python
"""
 flowMeter.py 
 Steven Wohl

 An example to demonstrate the use of the BBIOServer library
 for PyBBIO.

 This creates the same interface as BBIOServer_test.py, except
 the pages use the 'mobile.css' stylesheet, making it mobile
 device friendly. 

 This example program is in the public domain.
"""

# First we must import PyBBIO: 
from bbio import *
# Then we can import BBIOServer:
from BBIOServer import *
from PhantStream import *
from time import gmtime, strftime
import os.path

# Now we create a server instance:
server = BBIOServer()
# Port 8000 is used by default, but can be specified when creating
# server instance:
#  server = BBIOServer(port_number)
# It also defaults to blocking mode, but if we wanted it to run
# non-blocking, i.e. the loop() routine continues as normal while 
# the server runs in the background, we could say:
#  server = BBIOServer(blocking=False)


value_name = "value"
variable_name= "variable"
time_field = "timestamp"
public_key = "Eb3mppJXprIADyddpErWU1AzX8ZD"
private_key = "Vvj7LL95LysmKDqq3zewUV3Kywe5"
server_url = "http://192.168.0.11:8280/"
p = PhantStream(public_key,private_key,server_url)
f = open('/home/steve/repo/python/pyWeb/newfile2.txt', 'r')

def phantSend(pin):
  """Takes the pin uses that to sends it value to phant server"""
  var = pin
  val = analogRead(var)
  time =  getTime()
  v = inVolts(val)
  samples = {
    time_field : getTime(),
    value_name : 1,
    variable_name: 'test'
  }
  p.send(samples)
  print p.send(samples)
  

def voltage(analog_pin):
  """ Takes analog reading from given pin and returns a string 
      of the voltage to 2 decimal places. """
  phantSend(analog_pin)
  return "%0.2f" % inVolts(analogRead(analog_pin))

def print_entry(text):
  """ Just prints the given text. """
  print "Text entered: \n  '%s'" % text

def getTime():
  """This is to get the current time"""
  return strftime("%Y-%m-%d %H:%M:%S", gmtime())
 
def setup():
  # Set the LEDs we'll be ontrolling as outputs:
  pinMode(USR2, OUTPUT)
  pinMode(USR3, OUTPUT)

  # Create our first page with the title 'PyBBIO Test', specifying the
  # mobile device stylesheet:
  home = Page("Flow Meter Test", stylesheet="mobile.css")
  # Add some text to the page:
  home.add_html(f.read())
  home.add_text("This is a test of the BBIOServer library for PyBBIO, "+\
                "using the 'mobile.css' mobile device stylesheet. " +\
                "Follow the links above to test the different pages.")
  home.add_text("Press submit to send thet points to the mass "+\
                "flow controllers in the chamber.")
  home.add_text("This is a test of the BBIOServer library for PyBBIO, "+\
                "using the 'mobile.css' mobile device stylesheet. " +\
                "Follow the links above to test the different pages.")
  home.add_text("Press submit to send thet points to the mass "+\
                "flow controllers in the chamber.")

                 
  # Create a new page to test the text input:
  text = Page("Chamber MFC Set Point", stylesheet="mobile.css")
  text.add_text("Press submit to send the new set points to the mass "+\
                "flow controllers in the chamber.")
  text.add_text("Press submit to send thet points to the mass "+\
                "flow controllers in the chamber.")


  # Create the text entry box on a new line; button will say 'Submit',
  # and when submitted the text in the box will be sent to print_entry():
  text.add_entry(lambda text: print_entry(text), "Submit", newline=True)

  # Create a new page for the control of RH
  rh = Page("Relative Humidity", stylesheet="mobile.css")
  rh.add_monitor(lambda: getTime(),  "System Time: ") 
  rh.add_text("Below are the three entries for controlling relative "+\
              "humidity generation.")

  rh.add_entry(lambda text:  print_entry(text), "MFC Water", newline=True)
  rh.add_monitor(lambda: pinState(USR3), "MFC Water Current SetPoint:")
  rh.add_monitor(lambda: pinState(USR3), "MFC Water Current Value:")

  rh.add_entry(lambda text:  print_entry(text), "MFC Air flow Rate", newline=True)
  rh.add_monitor(lambda: pinState(USR3), "MFC Air flow Setpoint:")
  rh.add_monitor(lambda: analogRead(AIN0), "MFC Air Current Value:")

  rh.add_entry(lambda text:  print_entry(text), "MFC Water", newline=True)
  rh.add_monitor(lambda: pinState(USR3), "MFC Water Current SetPoint:")
  rh.add_monitor(lambda: pinState(USR3), "MFC Water Current Value:")


  # Create a new page to test the buttons and monitors:
  io = Page("I/O", stylesheet="mobile.css")
 
  # Make a LED control section using a heading:
  io.add_heading("LED Control")
  io.add_text("Control the on-board LEDs", newline=True)

  # Add a button on a new line with the label 'Toggle USR2 LED' that will
  # call 'toggle(USR2)' when pressed:
  io.add_button(lambda: toggle(USR2), "Toggle USR2 LED", newline=True)

  # Add a monitor which will continually call 'pinState(USR2)' and 
  # display the return value in the form: 'current state: [value]':
  io.add_monitor(lambda: pinState(USR2), "current state:")

  # Same thing here with the other LED:
  io.add_button(lambda: toggle(USR3), "Toggle USR3 LED", newline=True)
  io.add_monitor(lambda: pinState(USR3), "current state:")

  # Create another section for ADC readings:
  io.add_heading("ADC Readings")
  io.add_text("Read some ADC inputs", newline=True)

  # Add a monitor to display the ADC value:
  io.add_monitor(lambda: analogRead(AIN0), "AIN0 value:", newline=True)

  # And one on the same line to display the voltage using the voltage()
  # function defined above. Because the units variable is used this time
  # the value will be displayed in the form: 'voltage: [value] v':
  io.add_monitor(lambda: voltage(AIN0), "voltage:", units="v")

  # Same thing here:
  io.add_monitor(lambda: analogRead(AIN1), "AIN1 value:", newline=True)
  io.add_monitor(lambda: voltage(AIN1), "voltage:", units="v")

  # Then start the server, passing it all the pages. The first page
  # passed in will be the home page:
  server.start(home, text, io, rh)


def loop():
  # We're running in blocking mode, so we won't get here until ctrl-c
  # is preseed. 
  print "\nServer has stopped"
  stop()



# Then run it the usual way:
run(setup, loop)

# Now, on a computer on the same network as you beaglebone, open your
# browser and navigate to:
#  your_beaglebone_ip:8000 
#  (replacing 8000 if you specified a different port)
# You should be redirected to your_beaglebone_ip:8000/pages/PyBBIOTest.html
