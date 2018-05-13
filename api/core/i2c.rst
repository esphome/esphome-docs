I2CComponent
============

To make i2c devices easier to implement in esphomelib, there's a special I2CComponent implementing
a bunch of i2c helper functions on top of the Arduino Wire library. It is also the preferred way
of using i2c peripherals since it implements timeouts, verbose logs for debugging issues, and
for the ESP32 the ability to have multiple i2c busses in operation at the same time.

API Reference
-------------

.. doxygenclass:: I2CComponent
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: I2CDevice
    :members:
    :protected-members:
    :undoc-members:
