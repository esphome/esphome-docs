.. _graphical_menu:

Graphical Menu
==============

.. seo::
    :description: Instructions for setting up a simple hierarchical menu on displays.

The component provides an infrastructure for setting up a hierarchical menu
on Graphical LCD displays. This offers the user an interactive method to display
labels, control entities like ``switch``, ``select``, ``number``  available locally on the
ESPHome node, without the requirement of a network connection.

Overview
--------

The integration implements the :ref:`Display Menu <display_menu>` integration providing
a hierarchical menu primarily intended to be controlled either by a rotary encoder
with a button or a five-button joystick controller.

The component needs to be connected to an instance of a Graphical LCD display, like :ref:`ssd1306`.

.. code-block:: yaml

    # Example configuration entry

    font:
      - file: "gfonts://Anonymous Pro"
        id: Anonymous_Pro
        size: 14

    display:
      - platform: ssd1306_i2c
        id: oled
        model: "SH1106 128x64"
        lambda: |-
          id(oled_menu).draw();
          if (!id(oled_menu).is_active()){
            it.print(0, 0, id(Anonymous_Pro), "Menu is not active");
          }

    # Declare a LCD menu
    graphical_menu:
      id: oled_menu
      font: Anonymous_Pro
      display_id: oled
      active: false
      mode: rotary
      items:
        - type: command
          text: "Exit"
          on_value:
            - display_menu.hide:


    # Rotary encoder to provide navigation
    sensor:
      - platform: rotary_encoder
        ...
        filters:
          debounce: 30ms
        on_anticlockwise:
          - display_menu.up:
        on_clockwise:
          - display_menu.down:

    # A debounced GPIO push button is used to 'click'
    binary_sensor:
      - platform: gpio
        ...
        filters:
          - delayed_on: 30ms
          - delayed_off: 30ms
        on_press:
          - display_menu.enter:

Configuration variables:

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **display_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the LCD display.
- **mark_back** (*Optional*, 0-255): Code of the character used to mark menu items going back
  one level. As the character set lacks a good looking back arrow, using a user defined character
  is advisable (use ``8`` to reference one at  position ``0`` to avoid problems with zeros
  in a string). Defaults to ``0x5e`` (``^``).
- **mark_selected** (*Optional*, 0-255): Code of the character used to mark menu item selected.
  Defaults to ``0x3e`` (``>``).
- **mark_editing** (*Optional*, 0-255): Code of the character used to mark menu item editing mode.
  Defaults to ``0x2a`` (``*``).
- **mark_submenu** (*Optional*, 0-255): Code of the character used to mark menu item leading to a
  submenu. Defaults to ``0x7e`` (a right arrow).
- **font** (*Required*, :ref:`display-fonts`): Font used to generate menu. Ideally a monospaced font
- **color** (*Optional*, :ref:`config-color`): Color used for menu text

The rest of the configuration is described in the :ref:`Display Menu <display_menu>` component.
The menu inherits the dimensions of the connected LCD display and uses the entire area.

See Also
--------

- :ref:`i2c`
- :ref:`ssd1306-i2c`
- :ref:`lcd-gpio`
- :ref:`Display Menu <display_menu>`
- :doc:`/components/sensor/rotary_encoder`
- :doc:`/components/binary_sensor/index`
- :apiref:`lcd_menu/lcd_menu.h`
- :ghedit:`Edit`
