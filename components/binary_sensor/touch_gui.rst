Touch GUI
=========

.. seo::
    :description: Instructions for setting up a GUI using virtual buttons on touch screens.
    :image: touch-gui.png

.. _touch_gui-component:

Component/Hub
-------------

The ``touch_gui`` component creates a global hub for implementing a GUI using virtual buttons
on touch screens. The component is software only and needs to be connected to components
providing the input and the output.

On the output side it is connected to a :ref:`display <display-engine>` where it draws
the GUI elements. On the input side it exposes an action where a touch screen reports
the coordinates of the touch. The ``touch_gui`` evaluates those and changes the states
of the virtual buttons accordingly.

.. code-block:: yaml

    # Example configuration entry
    touch_gui:
      id: gui
      display_id: tft
      update_interval: 100ms
      button_colors:
        background: color_button_background
        active_background: color_button_activated
        foreground: color_button_text
        active_foreground: color_button_text
        border: color_button_text
      button_font: sans20
      button_lambda: |-
        if (it.get_type() != touch_gui::TOUCH_GUI_BUTTON_TYPE_AREA) {
          it.get_display()->circle(it.get_x_center(), it.get_y_center(), 20, it.get_border_color());
          it.get_display()->filled_circle(it.get_x_center(), it.get_y_center(), 19, it.get_background_color_to_use());
          it.get_display()->print(it.get_x_center(), it.get_y_center(), it.get_font(), it.get_foreground_color_to_use(),
            display::TextAlign::CENTER, it.get_text().c_str());
        }
      on_update:
        then:
          - component.update: tft


Configuration variables
***********************

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID for code generation.
- **display_id** (*Optional*, :ref:`config-id`): ID of the :ref:`display <display-engine>` where to draw the GUI elements.
- **update_interval** (*Optional*, :ref:`config-time`): The period to run timed tasks such as releasing a momentary button. Defaults to ``50ms``.
- **button_colors** (*Optional*): Groups the colors of the buttons
- **background** (*Optional*, :ref:`config-id`): ID of the background color of an inactive button. Defaults to ``COLOR_OFF``.
- **active_background** (*Optional*, :ref:`config-id`): ID of the background color of an active button. Defaults to ``COLOR_ON``.
- **foreground** (*Optional*, :ref:`config-id`): ID of the foreground color of an inactive button. Defaults to ``COLOR_ON``.
- **active_foreground** (*Optional*, :ref:`config-id`): ID of the foreground color of an active button. Defaults to ``COLOR_OFF``.
- **border** (*Optional*, :ref:`config-id`): ID of the color ti draw the button's border with. Defaults to ``COLOR_ON``.
- **button_font** (*Optional*, :ref:`config-id`): ID of the font to draw the button's text with. No default.
- **button_lambda** (*Optional*, :ref:`lambda <config-lambda>`): A custom lambda to draw the button. The lambda is passed an ``it`` parameter
  representing the button to draw. See the :apiref:`TouchGUIButton <touch_gui/gui.h>` and :apiref:`BinarySensor <binary_sensor/binary_sensor.h>`
  APIs for the list of member variables and methods. Defaults to an internal method drawing a simple rectangle with a border defined
  by the configured colors, font and text.

.. _touch_gui-on_update:

``on_update`` Action
********************

This automation will be triggered when a virtual button changes the visible state. It is normally wired to the
:ref:`component.update <component-update_action>` action of the display.

.. _touch_gui-touch:

``touch_gui.touch`` Action
**************************

This is an :ref:`Action <config-action>` for reporting a touch screen event to the ``touch_gui``. It is normally
wired to a touch screen input component.

.. code-block:: yaml

    on_...:
      then:
        - touch_gui.touch:
            id: gui
            x: !lambda 'return x;'
            y: !lambda 'return y;'
            touched: !lambda 'return touched;'

Configuration variables:

- **id** (*Optional*, :ref:`config-id`): The ID of the touch gui to control.
- **x** (*Optional*, integer, :ref:`templatable <config-templatable>`): The x coordinate of the touch. Defaults to ``0``.
- **y** (*Optional*, integer, :ref:`templatable <config-templatable>`): The y coordinate of the touch. Defaults to ``0``.
- **touched** (*Optional*, boolean, :ref:`templatable <config-templatable>`): True if the touch screen was touched, false if released. Defaults to ``true``.

.. _touch_gui-activate_button:

``touch_gui.activate_button`` Action
************************************

This is an :ref:`Action <config-action>` for simulating a touch event on a button.

.. code-block:: yaml

    on_...:
      then:
        - touch_gui.activate_button:
            id: gui
            button: button0
        - touch_gui.activate_button: button1

Configuration variables

- **id** (*Optional*, :ref:`config-id`): The ID of the touch gui to control.
- **button** (**Required**, :ref:`config-id`, :ref:`templatable <config-templatable>`): The button to activate.

.. _touch_gui-buttons:

Virtual Buttons
---------------

The ``touch_gui`` hub manages a set of virtual buttons implemented as :ref:`binary sensors <config-binary_sensor>`.

.. code-block:: yaml

    binary_sensor:
      - platform: touch_gui
        id: btn_blinds_livingroom
        touch_gui_id: gui
        type: toggle
        x_min: 2
        y_min: 30
        x_max: 120
        y_max: 86
        pages:
          - page_covers
        colors:
          background: color_bg
          active_background: color_abg
          foreground: color_fg
          active_foreground: color_afg
          border: color_b
        font: roomnames20
        text: 'Living room'
        lambda: |-
          it.get_display()->circle(it.get_x_center(), it.get_y_center(), 20, it.get_border_color());
          it.get_display()->filled_circle(it.get_x_center(), it.get_y_center(), 19, it.get_background_color_to_use());
          it.get_display()->print(it.get_x_center(), it.get_y_center(), it.get_font(), it.get_foreground_color_to_use(),
            display::TextAlign::CENTER, it.get_text().c_str());

Common configuration variables
******************************

- **id** (*Optional*, :ref:`config-id`): The ID of the button.
- **touch_gui_id** (*Optional*, :ref:`config-id`): The ID of the touch gui the button is part of.
- **type** (**Required**, string): The type of the button. One of ``momentary``, ``toggle``, ``radio``, and ``area``.
  See below for the functionality and configuration of each.
- **x_min** (**Required**, integer): The left x coordinate of the button's sensitive area.
- **x_max** (**Required**, integer): The right x coordinate of the button's sensitive area.
- **y_min** (**Required**, integer): The top y coordinate of the button's sensitive area.
- **y_max** (**Required**, integer): The bottom y coordinate of the button's sensitive area.
- **z_order** (*Optional*, integer): The z order of the button. Zero is farthest from the viewer, 255 nearest. Defaults to ``50``.
- **pages** (*Optional*, , :ref:`config-id`): The list of pages the button should be displayed on. A single page can
  be also specified as a value of the ``pages`` variable on the same line. Defaults to all pages.
- **colors** (*Optional*): Groups the colors of the button.
- **background** (*Optional*, :ref:`config-id`): ID of the background color of an inactive button. Defaults to the hub component's one.
- **active_background** (*Optional*, :ref:`config-id`): ID of the background color of an active button. Defaults to the hub component's one.
- **foreground** (*Optional*, :ref:`config-id`): ID of the foreground color of an inactive button. Defaults to the hub component's one.
- **active_foreground** (*Optional*, :ref:`config-id`): ID of the foreground color of an active button. Defaults to the hub component's one.
- **border** (*Optional*, :ref:`config-id`): ID of the color ti draw the button's border with. Defaults to the hub component's one.
- **font** (*Optional*, :ref:`config-id`): ID of the font to draw the button's text with. Defaults to the hub component's one.
- **text** (*Optional*, string, :ref:`templatable <config-templatable>`): Text to draw as the button's label.
- **lambda** (*Optional*, :ref:`lambda <config-lambda>`): A custom lambda to draw the button. The lambda is passed an ``it`` parameter
  representing the button to draw. See the :apiref:`TouchGUIButton <touch_gui/gui.h>` and :apiref:`BinarySensor <binary_sensor/binary_sensor.h>`
  APIs for the list of member variables and methods. If the lambda is not specified but it is for the hub, the hub's one is used.
  Defaults to an internal method drawing a simple rectangle with a border defined by the configured colors, font and text.

.. note::

    Complicated GUIs might involve dozens of buttons. If you get crashes while the setup phase is executed probably the stack
    size is too small. Find the ``main.cpp`` file of your framework such as ``~/.platformio/packages/framework-arduinoespressif32@3.10004.210126/cores/esp32/main.cpp``
    and try to enlarge it.

.. _touch_gui-momentary-button:
  
Momentary button
****************

A momentary button reacts with a transition to an activated state when the touch is registered and a return to an inactive
state a moment later. The common usage is executing actions using the button's
:ref:`binary_sensor.on_press <binary_sensor-on_press>` automation.

.. code-block:: yaml

    binary_sensor:
      - platform: touch_gui
        type: momentary
        ...

Configuration variables
^^^^^^^^^^^^^^^^^^^^^^^

- **touch_time** (*Optional*, :ref:`config-time`): The interval after which to release the button. The button is also released
  if the touch is released or if the page shown changes. Defaults to ``100ms``.


.. _touch_gui-toggle-button:

Toggle button
*************

A toggle button toggles the state when touched. Usually the state is then evaluated in other automations using the
:ref:`binary_sensor.is_on <binary_sensor-is_on_condition>` condition.

.. code-block:: yaml

    binary_sensor:
      - platform: touch_gui
        type: toggle
        initial: true
        ...

Configuration variables
^^^^^^^^^^^^^^^^^^^^^^^

- **initial** (*Optional*, boolean): The initial state of the button. Defaults to ``false``.


.. _touch_gui-radio-group-button:

Radio group button
******************

A radio button is part of a group where exactly one of the buttons in the group is activated. If a button from
is activated the previously activated one of the same group will be deactivated first and then the new
one activates.

.. code-block:: yaml

    binary_sensor:
      - platform: touch_gui
        type: radio
        radio_group: 1
        initial: true
        text: 'Automatic'
        ...
      - platform: touch_gui
        type: radio
        radio_group: 1
        text: 'Manual'
        ...

Configuration variables
^^^^^^^^^^^^^^^^^^^^^^^

- **radio_group** (**Required**, positive integer): The group the button belongs to.
- **initial** (*Optional*, boolean): The initial state of the button. There should be exactly one button with the
  ``initial: true``. If there is none the first one encountered will be activated. If there are more the first
  of them encountered remains activated. Defaults to ``false``.

.. _touch_gui-area-button:

Area button
***********

The area button represents a button without a visible part, that can be used for example to overlay over the whole
display or graphical elements drawn in another way. Other than that the behavior is same as the
:ref:`momentary button <touch_gui-momentary-button>`.

See Also
--------

- :doc:`/components/binary_sensor/index`
- :apiref:`touch_gui/gui.h`
- :ghedit:`Edit`
