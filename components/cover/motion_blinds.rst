Motion Blinds Cover
===================

.. seo::
    :description: Setting up Motion Blinds/BLE covers in ESPHome.

The ``motion_blinds`` cover platform allows you to control a motion blinds
based BLE cover motor (see `MotionBlinds <https://motionblinds.com/>`__). The platform connects to the device over the
ESP32's BLE peripheral and both controls and fetches the position and state of the motor.

.. note::

    This component does NOT support the motion blinds wifi bridge, it connects
    directly to the motor over BLE.

.. code-block:: yaml

    # Example configuration entry

    time:
      - platform: homeassistant
        id: homeassistant_time

    ble_client:
      - mac_address: AA:BB:CC:DD:EE:FF
        id: motion_blinds_kitchen

    cover:
      - platform: motion_blinds
        name: "Kitchen blinds"
        ble_client_id: motion_blinds_kitchen
        time_id: homeassistant_time

Setup
-----

The Motion Blinds should first be setup first with the smartphone app
following the instructions, so that the speed, direction, limits,
etc are programmed in (this component does not yet support setting these).

Once setup, configure the yaml per the above example, using the MAC
address of your device.
See :ref:`Setting up devices <esp32_ble_tracker-setting_up_devices>` for
how to discover the MAC address.

Configuration variables:
------------------------

- **name** (**Required**, string): The name of the cover.
- **ble_client_id** (**Required**, :ref:`config-id`): The id of the ``ble_client`` entry associated with the device.
- **time_id** (**Required**): The id of the ``time`` entry associated with the device.
- **invert_position** (*Optional*, boolean): Inverts the position value to and from the device. Set if ESPHome is swapping around the open/close state of the cover.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Cover <config-cover>`.


.. note::

    The BLE stack on the ESP32 has a limit of three connected devices.


See Also
--------

- :doc:`index`
- :ref:`automation`
- :apiref:`motion_blinds/cover/motion_blinds_cover.h`
- :ghedit:`Edit`
