NeoKey Light
===================

.. seo::
    :description: Instructions for setting up NeoKey lights in ESPHome.

The ``neokey`` binary sensor platform reads four key switches. This component requires a NeoKey hub to be configured.

.. code-block:: yaml

    # Example configuration entry
    neokey:

    binary_sensor:
      - platform: neokey
        name: "Key 1"
        key: 0
      - platform: neokey
        name: "Key 2"
        key: 1
      - platform: neokey
        name: "Key 3"
        key: 2
      - platform: neokey
        name: "Key 4"
        key: 3

Configuration variables:
------------------------

- **name** (**Required**, string): The name of the binary sensor.
- **neokey_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the NeoKey hub. Required if more than one hub.
- All other options from :ref:`Binary Sensor <config-binary_sensor>`.

Multiple breakout boards are supported as well. Just specify them under the neokey hub.

.. code-block:: yaml

    # Example configuration entry
    neokey:
      - id: board_1 # Default address is 0x30 if not specified.
      - id: board_2
        address: 0x31

    binary_sensor:
      - platform: neokey
        neokey_id: board_1
        name: "Key 1"
        key: 0
      - platform: neokey
        neokey_id: board_1
        name: "Key 2"
        key: 1
      - platform: neokey
        neokey_id: board_1
        name: "Key 3"
        key: 2
      - platform: neokey
        neokey_id: board_1
        name: "Key 4"
        key: 3
      - platform: neokey
        neokey_id: board_2
        name: "Key 5"
        key: 0
      - platform: neokey
        neokey_id: board_2
        name: "Key 6"
        key: 1
      - platform: neokey
        neokey_id: board_2
        name: "Key 7"
        key: 2
      - platform: neokey
        neokey_id: board_2
        name: "Key 8"
        key: 3


See Also
--------

- :doc:`/components/neokey_1x4`
- :doc:`/components/binary_sensor/index`
- :ghedit:`Edit`
