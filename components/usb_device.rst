USB Device
==========

.. seo::
    :description: Instructions for setting up USB Device in ESPHome.

USB Device Configuration
------------------------

.. code-block:: yaml

    binary_sensor:
      - platform: usb_device
        mounted:
          name: USB is mounted
        ready:
          name: USB is ready
        suspended:
          name: USB is suspended

    switch:
      - platform: usb_device
        detach:
          name: Detach USB device
        wake_up:
          name: Wake up host


Binary Sensor
-------------

A binary sensor platform to read USB devices status

Configuration variables:
************************

- **mounted** (*Optional*): On if USB device is mounted.

  - **name** (**Required**, string): The name for the mounted binary sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this binary sensor for use in lambdas.
  - All other options from :ref:`Binary sensor <config-binary_sensor>`.

- **ready** (*Optional*): On if USB device is ready.

  - **name** (**Required**, string): The name for the ready binary sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this binary sensor for use in lambdas.
  - All other options from :ref:`Binary sensor <config-binary_sensor>`.

- **suspended** (*Optional*): On if USB device is suspended.

  - **name** (**Required**, string): The name for the suspended binary sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this binary sensor for use in lambdas.
  - All other options from :ref:`Binary sensor <config-binary_sensor>`.

Switch
-------------

A switch platform to control USB devices

Configuration variables:
************************

- **detach** (*Optional*): The switch can be used to disconnect USB device.

  - **name** (**Required**, string): The name for the detach switch.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this switch for use in lambdas.
  - All other options from :ref:`Switch <config-switch>`.

- **wake_up** (*Optional*): The switch can be used to wake up host if supported.

  - **name** (**Required**, string): The name for the wake_up switch.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this switch for use in lambdas.
  - All other options from :ref:`Switch <config-switch>`.

See Also
--------

- :doc:`/components/usb_hid`
- :ghedit:`Edit`
