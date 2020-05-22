GPS Component
=============

.. seo::
    :description: Instructions for setting up GPS integration in ESPHome.
    :image: crosshair-gps.png

The ``gps`` component allows you to connect GPS modules to your ESPHome project.
Any GPS module that uses the standardized NMEA communication protocol will work.

.. figure:: images/gps-full.jpg
    :align: center
    :width: 50.0%

    GPS Module. Image by `Adafruit`_

.. _Adafruit: https://www.adafruit.com/product/746

For this integration to work you need to have set up a :ref:`UART bus <uart>`
in your configuration - only the RX pin should be necessary.

.. code-block:: yaml

    # Example configuration entry
    uart:
      rx_pin: D0
      baud_rate: 9600

    # Declare GPS module
    gps:

    # GPS as time source
    time:
      - platform: gps

Configuration variables:
------------------------

The component is split up in platforms.

First you need to define a global GPS module hub (as seen above).

Currently, the only data that can be extracted from GPS is the current time.
GPS can be used as a time platform to get the current date and time via the
very accurate GPS clocks that are also independent of any network connection.

See :doc:`time` for config options for the GPS time source.

See Also
--------

- :ref:`sensor-filters`
- `TinyGPS++ library <http://arduiniana.org/libraries/tinygpsplus/>`__
- :apiref:`gps/gps.h`
- :ghedit:`Edit`
