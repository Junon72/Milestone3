### test.py file was used to test the python installation, version and the path
import sys

# this line prints if python is installed correctly
def greet(greetings_to):
   greeting = 'Hello, {}'.format(greetings_to)
   return greeting
 
print(greet('World!'))

# this line will print out the current python path and the version of the python
print(sys.executable)