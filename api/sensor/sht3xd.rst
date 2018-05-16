SHT3XD Temperature/Humidity Sensor
==================================

.. warning::

    This sensor is experimental has not been tested yet. If you can verify it works (or if it doesn't),
    notify me on `discord <https://discord.gg/KhAMKrd>`__.

The SHT3XD component allows you to use your SHT3x-DIS i2c-enabled temperature+humidity+gas
sensor with esphomelib (`datasheet <https://cdn-shop.adafruit.com/product-files/2857/Sensirion_Humidity_SHT3x_Datasheet_digital-767294.pdf>`__,
`adafruit <https://www.adafruit.com/product/2857>`__). It requires i2c to be setup to work.

Example Usage
-------------

.. code-block:: cpp

    // Basic
    auto sht3xd = App.make_sht3xd_sensor("SHT31D Temperature", "SHT31D Humidity");

    // Advanced
    // default accuracy is high
    sht3xd.sht3xd->set_accuracy(sensor::SHT3XD_ACCURACY_LOW);

.. cpp:namespace:: nullptr

See :cpp:func:`Application::make_sht3xd_sensor`.

API Reference
-------------

.. doxygenclass:: sensor::SHT3XDComponent
    :members:
    :protected-members:
    :undoc-members:

.. doxygenenum:: sensor::SHT3XDAccuracy

.. doxygenclass:: sensor::SHT3XDTemperatureSensor
    :members:
    :protected-members:
    :undoc-members:

.. doxygenclass:: sensor::SHT3XDHumiditySensor
    :members:
    :protected-members:
    :undoc-members:

