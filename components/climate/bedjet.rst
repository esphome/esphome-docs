BedJet
======

.. seo::
    :description: Instructions for setting up a BedJet climate device.
    :image: bedjet.png

The ``bedjet`` climate platform creates a climate device which can be used to control
a BedJet V3 Climate Comfort Sleep System.

This component supports the following functionality:

- Set the operating mode: off, heat, cool, turbo (boost)
- Set the desired target temperature
- Set the desired fan speed
- Start one of the saved memory presets, including "Biorhythm" programs
- Show the current status of the BedJet

This platform uses the BLE peripheral on an ESP32, so you also need to enable
this component. Please see the :doc:`/components/ble_client` docs for how to discover the MAC
address of your BedJet device, or you can find the list of paired MAC addresses in
the "DEVICE LIST" section of the BedJet mobile application.

.. code-block:: yaml

    ble_client:
      - mac_address: 11:22:33:aa:bb:cc
        id: ble_bedjet

    climate:
      - platform: bedjet
        id: my_bedjet_fan
        name: "My BedJet Fan"
        ble_client_id: ble_bedjet

Configuration variables:
------------------------

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **name** (**Required**, string): The name of the climate device.
- **ble_client_id** (**Required**, :ref:`config-id`): The ID of the BLE Client.
- **time_id** (*Optional*, :ref:`config-id`): The ID of a :ref:`Time Component <time>` which
  can be used to set the time on the BedJet device.
- **heat_mode** (*Optional*, string): The primary heating mode to use for `HVACMode.HEAT`:
  - ``"heat"`` (Default) - Setting ``hvac_mode=heat`` uses the BedJet "HEAT" mode.
  - ``"extended"`` - Setting ``hvac_mode=heat`` uses BedJet "EXT HEAT" mode.
  - Whichever is not selected will be made available as a custom preset.
- All other options from :ref:`Climate <config-climate>`.

lambda calls
************

From :ref:`lambdas <config-lambda>`, you can call methods to do some advanced stuff.

- ``.upgrade_firmware``: Check for and install updated BedJet firmware.

  .. code-block:: yaml

      button:
        - platform: template
          name: "Check Bedjet Firmware"
          on_press:
            then:
            - lambda: |-
                id(my_bedjet_fan).upgrade_firmware();

- ``.send_local_time``: If `time_id` is set, attempt to sync the clock now.

  .. code-block:: yaml

      button:
        - platform: template
          name: "Sync Clock"
          on_press:
            then:
            - lambda: |-
                id(my_bedjet_fan).send_local_time();

- ``.set_clock``: Set the BedJet clock to a specified time; works with or without a `time_id`.

  .. code-block:: yaml

      button:
        - platform: template
          name: "Set Clock to 10:10pm"
          on_press:
            then:
            - lambda: |-
                id(my_bedjet_fan).set_clock(22, 10);

Known issues:
-------------

.. warning::

    BedJet V2 and other devices are not currently supported. Only BedJet V3 is supported.

.. note::

    Only one client can be connected to the BedJet BLE service at a time, so you cannot
    use the BedJet mobile app to monitor or control the BedJet device while this component
    is connected. To use the mobile app, you should disconnect the ESP client first.

    To set up a (dis-)connect switch, see :doc:`/components/switch/ble_client`.

.. note::

    When more than one device is configured and connected, the ESP device may become
    overwhelmed and lead to timeouts while trying to install an updated version of the
    configuration. If this occurs, see the previous note about adding disconnect switches,
    and toggle those off while performing the installation. This will free up resources
    on the ESP and allow the installation to complete.

    Additionally, you may use an :ref:`ota.on_begin <ota-on_begin>` :ref:`Automation<automation>`
    to do this automatically:

    .. code-block:: yaml

        ota:
          on_begin:
            then:
              - logger.log: "Disconnecting clients for OTA update..."
              - switch.turn_off: bedjet_1_monitor
              - switch.turn_off: bedjet_2_monitor

See Also
--------

- :doc:`/components/ble_client`
- :doc:`/components/climate/index`
- :apiref:`bedjet/bedjet.h`
- :ghedit:`Edit`
