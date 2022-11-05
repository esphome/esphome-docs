Keyboard Component
==================

.. seo::
    :description: Instructions for setting up generic Keyboard in ESPHome.

The ``keyboard`` domain includes all platforms that should function like a keyboard
with up/down/set keys actions. 

.. _config-keyboard:

Base Keyboard Configuration
---------------------------

.. code-block:: yaml

    keyboard:
      - platform: ...
        name: "Keyboard Name"
        id: kbd

    binary_sensor:
      - platform: keyboard
        keyboard_id: kbd
        capslock:
          name: capslock
        numlock:
          name: numlock
        scrollock:
          name: scrollock


Configuration variables:

- **name** (**Required**, string): The name of the keyboard.
- **id** (**Optional**, :ref:`config-id`): The ID of the keyboard.
- **icon** (*Optional*, icon): Manually set the icon to use for the
  keyboard in the frontend.
- **internal** (*Optional*, boolean): Mark this component as internal. Internal components will
  not be exposed to the frontend (like Home Assistant). Only specifying an ``id`` without
  a ``name`` will implicitly set this to true.
- **disabled_by_default** (*Optional*, boolean): If true, then this entity should not be added to any client's frontend,
  (usually Home Assistant) without the user manually enabling it (via the Home Assistant UI).
  Defaults to ``false``.
- **entity_category** (*Optional*, string): The category of the entity.
  See https://developers.home-assistant.io/docs/core/entity/#generic-properties
  for a list of available options. Set to ``""`` to remove the default entity category.

Binary Sensor
-------------

A binary sensor platform to read keyboard's LEDs

Configuration variables:
************************

- **keyboard_id** (**Required**, :ref:`config-id`): The ID of the keyboard.
- **capslock** (*Optional*): Capslock LED status.

  - **name** (**Required**, string): The name for the capslock binary sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this binary sensor for use in lambdas.
  - All other options from :ref:`Binary sensor <config-binary_sensor>`.

- **numlock** (*Optional*): Numlock LED status.

  - **name** (**Required**, string): The name for the numlock binary sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this binary sensor for use in lambdas.
  - All other options from :ref:`Binary sensor <config-binary_sensor>`.

- **scrollock** (*Optional*): Scrollock LED status.

  - **name** (**Required**, string): The name for the scrollock binary sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this binary sensor for use in lambdas.
  - All other options from :ref:`Binary sensor <config-binary_sensor>`.

.. _keyboard-down_action:

``keyboard.down`` Action
*************************

This action mark keys as pressed on keyboard with the given ID when executed.

.. code-block:: yaml

    on_...:
      then:
        - keyboard.down:
            id: kbd
            keys: 
              - ShiftLeft
              - 5

Configuration variables:

- **id** (**Required**, :ref:`config-id`): The ID of the keyboard.
- **keys** (**Required**, list): a list of keycodes (integers) or keynames (strings).
  See `keymap.csv <https://github.com/tomaszduda23/esphome/blob/dev/esphome/components/keyboard/keymap.csv>`__
  and `hid.h <https://github.com/adafruit/Adafruit_TinyUSB_Arduino/blob/master/src/class/hid/hid.h>`__
- **type** (**Optional**, string): ``media_keys`` or ``keyboard``. Defaults to ``keyboard``.

.. _keyboard-up_action:

``keyboard.up`` Action
**************************

This action unmark keys as pressed on keyboard with the given ID when executed.

.. code-block:: yaml

    on_...:
      then:
        - keyboard.up:
            id: kbd
            keys: 
              - ShiftLeft
              - 5

Configuration variables:

- **id** (**Required**, :ref:`config-id`): The ID of the keyboard.
- **keys** (**Required**, list): a list of keycodes (integers) or keynames (strings).
  See `keymap.csv <https://github.com/tomaszduda23/esphome/blob/dev/esphome/components/keyboard/keymap.csv>`__
  and `hid.h <https://github.com/adafruit/Adafruit_TinyUSB_Arduino/blob/master/src/class/hid/hid.h>`__
- **type** (**Optional**, string): ``media_keys`` or ``keyboard``. Defaults to ``keyboard``.

.. _keyboard-set_action:

``keyboard.set`` Action
************************

This action set pressed keys (all other keys are released) on keyboard with the given ID when executed.
Do not specify ``keys`` to release all keys.

.. code-block:: yaml

    on_...:
      then:
        - keyboard.set:
            id: kbd
            keys: 0x0224
            type: media_keys

Configuration variables:

- **id** (**Required**, :ref:`config-id`): The ID of the keyboard.
- **keys** (**Optional**, list): a list of keycodes (integers) or keynames (strings).
  See `keymap.csv <https://github.com/tomaszduda23/esphome/blob/dev/esphome/components/keyboard/keymap.csv>`__
  and `hid.h <https://github.com/adafruit/Adafruit_TinyUSB_Arduino/blob/master/src/class/hid/hid.h>`__
- **type** (**Optional**, string): ``media_keys`` or ``keyboard``. Defaults to ``keyboard``.

Example
-------

TV control with https://www.wemos.cc/en/latest/s2/s2_mini.html

.. code-block:: yaml

    esp32:
      board: esp32-s2-saola-1
      framework:
        type: arduino
        version: 2.0.5
        platform_version: 5.2.0

    #...

    button:
      - platform: template
        name: "Volume up"
        on_press:
          then:
            - keyboard.set:
                id: kbd
                keys: 0x00E9
                type: media_keys
            - delay: 50ms
            - keyboard.set:
                id: kbd
                type: media_keys
      - platform: template
        name: "Volume down"
        on_press:
          then:
            - keyboard.set:
                id: kbd
                keys: 0x00EA
                type: media_keys
            - delay: 50ms
            - keyboard.set:
                id: kbd
                type: media_keys
      - platform: template
        name: "Power"
        on_press:
          then:
            - keyboard.set:
                id: kbd
                keys: 0x0030
                type: media_keys
            - delay: 50ms
            - keyboard.set:
                id: kbd
                type: media_keys
      - platform: template
        name: "Home"
        on_press:
          then:
            - keyboard.set:
                id: kbd
                keys: Home
            - delay: 50ms
            - keyboard.set:
                id: kbd
      - platform: template
        name: "Up"
        on_press:
          then:
            - keyboard.set:
                id: kbd
                keys: ArrowUp
            - delay: 50ms
            - keyboard.set:
                id: kbd
      - platform: template
        name: "Down"
        on_press:
          then:
            - keyboard.set:
                id: kbd
                keys: ArrowDown
            - delay: 50ms
            - keyboard.set:
                id: kbd
      - platform: template
        name: "Left"
        on_press:
          then:
            - keyboard.set:
                id: kbd
                keys: ArrowLeft
            - delay: 50ms
            - keyboard.set:
                id: kbd
      - platform: template
        name: "Right"
        on_press:
          then:
            - keyboard.set:
                id: kbd
                keys: ArrowRight
            - delay: 50ms
            - keyboard.set:
                id: kbd
      - platform: template
        name: "Back"
        on_press:
          then:
            - keyboard.set:
                id: kbd
                keys: 0x0224
                type: media_keys
            - delay: 50ms
            - keyboard.set:
                id: kbd
                type: media_keys
      - platform: template
        name: "Ok"
        on_press:
          then:
            - keyboard.set:
                id: kbd
                keys: Enter
            - delay: 50ms
            - keyboard.set:
                id: kbd

    keyboard:
      - platform: hid
        name: Blue kbd
        hid_id: usb_hid
        id: kbd

    hid:
      - platform: usb_device
        id: usb_hid
        type:
          composite:
            - keyboard
            - media_keys

See Also
--------

- :ghedit:`Edit`

.. toctree::
    :maxdepth: 1
    :glob:

    *
