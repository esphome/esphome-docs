Improv via Serial
=================

.. seo::
    :description: Instructions for setting up Improv via Serial in ESPHome.
    :image: improv-social.png

The ``improv_serial`` component in ESPHome implements the open `Improv standard <https://www.improv-wifi.com/>`__
for configuring Wi-Fi on an ESPHome device by using a serial connection to the device, eg. USB.

The ``improv_serial`` component requires the serial ``logger`` to be configured.


.. code-block:: yaml

    # Example configuration entry
    wifi:
      # ...

    improv_serial:


No configuration variables.

See Also
--------

- :doc:`wifi`
- :doc:`captive_portal`
- :doc:`esp32_improv`
- `Improv Wi-Fi <https://www.improv-wifi.com/>`__
- :ghsources:`esphome/components/improv_serial`
- :ghedit:`Edit`
