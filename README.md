AR Drone Interface for Python
=========
(Anyone who tries to use this repository is just asking for trouble.)


How to use this package
---------

```python
# import the package
from ardrone import *

# initialize the connection
drone = ARDrone()
drone.start()

# write your control function!
@use_ardrone(drone)
def foo():
    t                           # takeoff
    l                           # move left
    l +0.5                      # move left with an optional argument
    l +0.5 & u                  # move left AND move up
    h                           # hover
    for i in range(6):          # normal control structures are also available
        r                       # move right
    h
    y                           # and don't forget to land
    # full command list is available in ardrone.header.SHORTHAND_COMMAND

foo()
```


Dependencies
---------
Python 2.7
python-clformat
python-easy-bytecode


LICENSE
---------

This software is published under the terms of the WTFPL License, Version 2.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

