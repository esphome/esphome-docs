.. _graphical_display_menu:

Graphical Display Menu
======================

.. seo::
    :description: Instructions for setting up a simple hierarchical menu on displays.
    :image: lcd_menu.png

The component provides an infrastructure for setting up a hierarchical menu
on graphical displays. This offers the user an interactive method to display 
labels, control entities like ``switch``, ``select``, ``number``  available locally on the 
ESPHome node, without the requirement of a network connection.

.. figure:: images/lcd_menu.png
    :align: center
    :width: 60.0%

Overview
--------

The integration implements the :ref:`Display Menu <display_menu>` integration providing
a hierarchical menu primarily intended to be controlled either by a rotary encoder
with a button or a five-button joystick controller.

The component needs to be connected to an instance of a display supporting ESPHome's rendering 
engine such as :doc:`E-Paper displays <../display/waveshare_epaper>` or :doc:`OLED displays <../display/ssd1306>`.

.. code-block:: yaml

    # Example configuration entry
    display:
      - platform: waveshare_epaper
        id: my_display_component
        pages:
        - id: graph_page
          lambda: |-
            it.print(0, 0, id(my_font), "My menu is not currently active");

    font:
      - file: ...
        id: my_font
        size: 16

    graphical_display_menu:
      id: my_graphical_display_menu
      display: my_display_component
      display_updater: my_display_component
      active: false
      mode: rotary
      items:
        ...

    # Rotary encoder to provide navigation
    sensor:
      - platform: rotary_encoder
        ...
        filters:
          debounce: 30ms
        on_anticlockwise:
          - display_menu.up: my_graphical_display_menu
        on_clockwise:
          - display_menu.down: my_graphical_display_menu

    # A debounced GPIO push button is used to 'click'
    binary_sensor:
      - platform: gpio
        ...
        filters:
          - delayed_on: 30ms
          - delayed_off: 30ms
        on_press:
      - if:
          condition:
            display_menu.is_active: my_graphical_display_menu
          then:
            - display_menu.enter: my_graphical_display_menu
          else:
            - display_menu.show:  my_graphical_display_menu

Configuration variables:

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **display** (:ref:`config-id`): ID of the display to render to
- **display_updater** (*Optional*, :ref:`config-id`): If specified this component will have be
  used to update the display when the menu changes. This is useful for displays such as E-Ink
  that have slow refresh rates when used with `display_interval: never`.
- **foreground_color** (*Optional*, :ref:`config-color`): Specifies the foreground color to use.
  Defaults to COLOR_ON
- **background_color** (*Optional*, :ref:`config-color`): Specifies the background color to use.
  Defaults to COLOR_OFF

Controlling Menu Rendering
--------------------------

By default menu items with a value will be rendered between a set of parenthesis. This can be
controlled via the `menu_item_value` parameter.

- **menu_item_value** (*Optional*, :ref:`config-lambda`): Specifies how to render values for
  menu items that have values (eg. Selects, numbers). Defaults to rendering the value as 
  "(value here)". Receives the menu item as the parameter `it`.

.. code-block:: yaml

    graphical_display_menu:
      menu_item_value: !lambda |-
        // Will render your menu item value as "My menu label ~my value here~""
        std::string label = " ~";
        label.append(it->get_value_text());
        label.append("~");
    
        return label;

.. note::
    Ensure that all characters you use in the menu_item_value are available glyphs for your :ref:`font <display-fonts>`


The rest of the configuration is described in the :ref:`Display Menu <display_menu>` component.
The menu inherits the dimensions of the connected display and uses the entire area. It creates its
own page on initialisation and will confine all drawing to that :ref:`page <display-pages>`. As such you can use 
the display for other purposes hide/show the display as needed.

See Also
--------

- :ref:`Display Menu <display_menu>`
- :ref:`Display <display-engine>`
- :ref:`display-fonts`
- :ref:`display-pages`
- :apiref:`graphical_display_menu/graphical_display_menu.h`
- :ghedit:`Edit`
