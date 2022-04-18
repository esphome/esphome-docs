LCD Menu
========

.. seo::
    :description: Instructions for setting up a simple hierarchical menu on text-based LCD displays.
    :image: lcd-menu.png

The ``lcd_menu`` component provides an infrastructure for setting up a hierarchical menu
on character-based LCD displays.

.. figure:: images/lcd-menu.png
    :align: center
    :width: 50.0%

For this integration to work you need to have set up a :ref:`lcd-pcf8574` or a :ref:`lcd-gpio`
in your configuration.

Overview
--------

The LCD menu component provides a menu primarily intended to be controlled by a rotary encoder
with a button. It allows to navigate a hierarchy of items and submenus with the ability
to change enumeration and numeric values and execute commands. The menu can be activated
and deactivated on demand, allowing alternating between using the screen for the menu
and other information.

The component needs to be connected to an instance of a character based LCD display, which
at the moment are :ref:`lcd-pcf8574` or a :ref:`lcd-gpio`. For the best results the GPIO
connection is recommended; the I²C one running at the speed according to the datasheet
will create perceptible delays especially when changing a numeric value using the rotary
encoder. Most PCF8574 adapters used with these displays will happily run at 200 or even
400 kHz though so if you are comfortable accepting risks from running your hardware
out of spec, you might want to try that.

.. code-block:: yaml

    # Example configuration entry
    display:
    - platform: lcd_pcf8574
        id: my_lcd
        ...
        user_characters:
          - position: 0
            data:
              - 0b00100
              - 0b01110
              - 0b10101
              - 0b00100
              - 0b00100
              - 0b00100
              - 0b11100
              - 0b00000
        lambda: |-
          id(my_lcd_menu).draw();
          if (!id(my_lcd_menu).is_active())
            it.print("Menu is not active");

    # Declare a LCD menu
    lcd_menu:
      id: my_lcd_menu
      display_id: my_lcd
      dimensions: 20x4
      active: True
      mark_back: 0x08
      mark_selected: 0x3e
      mark_editing: 0x2a
      mark_submenu: 0x7e
      on_enter:
        then:
          lambda: 'ESP_LOGI("lcd_menu", "root enter");'
      on_leave:
        then:
          lambda: 'ESP_LOGI("lcd_menu", "root leave");'
      menu:
        - type: back
          text: 'Back'
        - type: label
          text: 'Label 1'

Configuration variables:

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **display_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the LCD display.
- **dimensions** (**Required**, string): The dimensions of the display with the ``COLUMNSxROWS``
  format. This should match dimensions of the LCD display, you can however for example specify
  fewer lines and use the last one for a status one.
- **active** (*Optional*, boolean): Whether the menu should start as active, meaning accepting
  user interactions and displaying output. Defaults to ``True``.
- **mark_back**, **mark_selected**, **mark_editing**, **mark_submenu** (*Optional*, 0-255):
  Code of the character used to mark menu items going back one level, a selected one,
  the editing mode and item leading to a submenu. Defaults to ``0x5e`` (``^``), ``0x3e`` (``>``),
  ``0x2a`` (``*``) and ``0x7e`` (a right arrow). As the character set lacks a good looking
  up arrow, using a user defined character is advisable (use ``8`` to reference one at
  position ``0`` to avoid problems with zeros in a string).
- **menu** (**Required**): The first level of the menu.

Automations:

- **on_enter** (*Optional*, :ref:`Automation <automation>`): An automation to perform
  when the menu level (here the root one) is entered. See :ref:`lcd_menu-on_enter`.
- **on_leave** (*Optional*, :ref:`Automation <automation>`): An automation to perform
  when the menu level is not displayed anymore.
  See :ref:`lcd_menu-on_leave`.

Menu Items
----------

Overview
********

Label
*****

Menu
****

Back
****

Enum
****

Number
******

Command
*******


Automations
-----------

.. _lcd_menu-on_enter:

``on_enter``
************

This automation will be triggered when the menu level is entered, i.e. the component
draws its items on the display. The ``it`` parameter points to a ``MenuItem`` class
with the information of the menu item describing the displayed child items.
If present at the ``lcd_menu`` level it is an internally generated root menu item,
otherwise an user defined one. 


.. code-block:: yaml

    lcd_menu:
      ...
      menu:
        - type: menu
          text: 'Submenu 1'
          on_enter:
            then:
              lambda: 'ESP_LOGI("lcd_menu", "enter: %s", it->get_text().c_str());'

.. _lcd_menu-on_leave:

``on_leave``
************

This automation will be triggered when the menu level is exited, i.e. the component
does not draw its items on the display anymore. The ``it`` parameter points to
a ``MenuItem`` class with the information of the menu item. If present at the
``lcd_menu`` level it is an internally generated root menu item, otherwise
an user defined one. It does not matter whether the level was left due to entering
the submenu or going back to the parent menu.

.. code-block:: yaml

    lcd_menu:
      ...
      menu:
        - type: menu
          text: 'Submenu 1'
          on_leave:
            then:
              lambda: 'ESP_LOGI("lcd_menu", "leave: %s", it->get_text().c_str());'

.. _lcd_menu-on_value:

``on_value``
************

This automation will be triggered when the value edited through the menu changed value
or a command was triggered.

.. code-block:: yaml

    lcd_menu:
      ...
      menu:
        - type: enum
          text: 'Enum Item'
          enum:
            - 'Red'
            - 'Green'
            - 'Blue'
          variable: my_enum_1
          on_value:
            then:
              lambda: 'ESP_LOGI("lcd_menu", "enum value: %s, %d, %s", it->get_text().c_str(), id(my_enum_1), it->get_enum_text().c_str());'

.. lcd_menu-up_action:

``lcd_menu.up`` Action
**********************

This is an :ref:`Action <config-action>` for navigating up in a menu. The action
is usually wired to an anticlockwise turn of a rotary encoder.

.. code-block:: yaml

    sensor:
      - platform: rotary_encoder
        ...
        on_anticlockwise:
          - lcd_menu.up:

Configuration variables:

- **id** (*Optional*, :ref:`config-id`): The ID of the menu to navigate.

.. lcd_menu-down_action:

``lcd_menu.down`` Action
************************

This is an :ref:`Action <config-action>` for navigating down in a menu. The action
is usually wired to a clockwise turn of a rotary encoder.

.. code-block:: yaml

    sensor:
      - platform: rotary_encoder
        ...
        on_clockwise:
          - lcd_menu.down:

Configuration variables:

- **id** (*Optional*, :ref:`config-id`): The ID of the menu to navigate.

.. lcd_menu-enter_action:

``lcd_menu.enter`` Action
*************************

This is an :ref:`Action <config-action>` for triggering a selected menu item, resulting
in an action depending on the type of the item - entering a submenu, starting/stopping
editing or triggering a command. The action is usually wired to a press button
of a rotary encoder. In case of mechanical one it is strongly advisable to debounce
it using a filter.

.. code-block:: yaml

    binary_sensor:
      - platform: gpio
        ...
        filters:
          - delayed_on: 10ms
          - delayed_off: 10ms
        on_press:
          - lcd_menu.enter:

Configuration variables:

- **id** (*Optional*, :ref:`config-id`): The ID of the menu to navigate.

.. lcd_menu-show_action:

``lcd_menu.show`` Action
************************

This is an :ref:`Action <config-action>` for showing an inactive menu. The state
of the menu remains unchanged, i.e. the menu level shown at the moment it was hidden
is restored, as is the selected item. The following snippet shows the menu if it is
inactive, otherwise triggers the selected item.

.. code-block:: yaml

    on_press:
      - if:
          condition:
            lcd_menu.is_active:
          then:
            - lcd_menu.enter:
          else:
            - lcd_menu.show:

Configuration variables:

- **id** (*Optional*, :ref:`config-id`): The ID of the menu to show.

.. lcd_menu-hide_action:

``lcd_menu.hide`` Action
************************

This is an :ref:`Action <config-action>` for hiding the menu. A hidden menu
does not react to ``draw()`` and does not process navigation actions.

.. code-block:: yaml

    lcd_menu:
      ...
      menu:
        - type: command
          text: 'Hide'
          on_value:
            then:
              - lcd_menu.hide:

Configuration variables:

- **id** (*Optional*, :ref:`config-id`): The ID of the menu to hide.

.. lcd_menu-show_main_action:

``lcd_menu.show_main`` Action
*****************************

This is an :ref:`Action <config-action>` for showing the root level of the menu.

.. code-block:: yaml

    lcd_menu:
      ...
      menu:
        - type: command
          text: 'Show Main'
          on_value:
            then:
              - lcd_menu.show_main:

Configuration variables:

- **id** (*Optional*, :ref:`config-id`): The ID of the menu to hide.

.. _lcd_menu-is_active:

``lcd_menu.is_active`` Condition
********************************

This :ref:`Condition <config-condition>` checks if the given menu is active, i.e.
shown on the display and processing navigation events.

.. code-block:: yaml

    on_press:
      - if:
          condition:
            lcd_menu.is_active:
          ...

See Also
--------

- :apiref:`lcd_menu/lcd_menu.h`
