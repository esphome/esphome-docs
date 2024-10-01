USB Device
==========

ESP32S2 and ESP32S3 allow to develop USB devices. One of the examples of USB device is ``USB_CDC`` :doc:`logger component </components/logger>`.

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

A binary sensor platform to read USB devices status

Configuration variables:
************************

- **configured** (*Optional*): On if USB device is configured.

  - **name** (**Required**, string): The name for the configured binary sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this binary sensor for use in lambdas.
  - All other options from :ref:`Binary sensor <config-binary_sensor>`.

See Also
--------

- :ref:`logger`
- :ghedit:`Edit`
