SHT3XD Temperature/Humidity Sensor
==================================

The SHT3XD component allows you to use your SHT3x-DIS i2c-enabled temperature+humidity+gas
sensor with esphomelib (`datasheet <https://cdn-shop.adafruit.com/product-files/2857/Sensirion_Humidity_SHT3x_Datasheet_digital-767294.pdf>`__,
`adafruit <https://www.adafruit.com/product/2857>`__). It requires i2c to be setup to work.

Example Usage
-------------

.. code-block:: cpp

    // Basic
    auto sht3xd = App.make_sht3xd_sensor("SHT31D Temperature", "SHT31D Humidity");

.. cpp:namespace:: nullptr

See :cpp:func:`Application::make_sht3xd_sensor`.

API Reference
-------------

.. doxygenclass:: sensor::SHT3XDComponent
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: sensor::SHT3XDTemperatureSensor
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: sensor::SHT3XDHumiditySensor
    :members:
    :protected-members:
    :undoc-members:

