# File description
## Firmware files
*  check.zip
    * This is to quickly check that the flash memory and i2c chip are talking with the dongle correctly
*  bt\_cdc\_fs.zip
    * This is the firmware for the dongle for exposure tracing

## Python programs
These were all written on a mac... I attempted to automate the finding of the dongle serial port so I didn't have to type it.   The code will have to be modified for windows and linux.  
* check.py: Install firmware check.zip on the device and check that flash memory is working

* flash_stat.py:  Prints info about the flash writing and cache for the flash status while the exposure firmware is runniing.

* init.py:  Run this program after the check.py program... It installs the flash if called with an extra parameter (e.g. python init.py extra).   If it is called via "python init.py", then it will just initialize the device so that it is ready for exposure tracing.
    * clear memory
    * sets time on device
    * does NOT start writing to the flash

* read_flash.py:  DO NOT USE... doesn't work for some reason
* simple.py:  Simplified version of read_flash.py for extracting exposure data from flash memory on the carrier board.  Best to "stop" the logging of exposures to the flash memory before trying to download the data... It seems data gets corrupted if this is not done.
* start_write.py:  Starts writing BT results to flash memory
* stop_write.py:  Stops writing BT results to flash memory


