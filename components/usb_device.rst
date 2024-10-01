USB Device
==========

.. seo::
    :description: Instructions for setting up USB Device in ESPHome.

USB Device Configuration
------------------------

.. code-block:: yaml

    binary_sensor:
      - platform: usb_device
        configured:
          name: USB is configured


Binary Sensor
-------------

A binary sensor platform to read USB devices status e.g. cdc logger

Configuration variables:
************************

- **configured** (*Optional*): On if USB device is configured.

  - **name** (**Required**, string): The name for the configured binary sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this binary sensor for use in lambdas.
  - All other options from :ref:`Binary sensor <config-binary_sensor>`.

See Also
--------

- :ghedit:`Edit`
