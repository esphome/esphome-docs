NeoKey Light
===================

.. seo::
    :description: Instructions for setting up NeoKey lights in ESPHome.

The ``neokey`` light platform drives four NeoPixel RGB LEDs. This component requires a NeoKey hub to be configured.

.. code-block:: yaml

    # Example configuration entry
    neokey:

    light:
      - platform: neokey
        name: "Keyboard Backlight"

Configuration variables:
------------------------

- **name** (**Required**, string): The name of the light.
- **neokey_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the NeoKey hub.
- All other options from :ref:`Light <config-light>`.

To control the LEDs individually, you can setup a light partition for each LED.

.. code-block:: yaml

    # Example configuration entry
    neokey:

    light:
      - platform: neokey
        id: backlight
        internal: true
      - platform: partition
        name: "Key 1 Light"
        segments:
          - id: backlight
            from: 0
            to: 0
      - platform: partition
        name: "Key 2 Light"
        segments:
          - id: backlight
            from: 1
            to: 1
      - platform: partition
        name: "Key 3 Light"
        segments:
          - id: backlight
            from: 2
            to: 2
      - platform: partition
        name: "Key 4 Light"
        segments:
          - id: backlight
            from: 3
            to: 3

Multiple breakout boards are supported as well. Just specify them under the neokey hub.

.. code-block:: yaml

    # Example configuration entry
    neokey:
      - id: board_1 # Default address is 0x30 if not specified.
      - id: board_2
        address: 0x31

    light:
      - platform: neokey
        neokey_id: board_1
        name: "Keyboard Backlight 1"
      - platform: neokey
        neokey_id: board_2
        name: "Keyboard Backlight 2"


See Also
--------

- :doc:`/components/neokey_1x4`
- :doc:`/components/light/index`
- :doc:`/components/light/rgb`
- :ghedit:`Edit`
