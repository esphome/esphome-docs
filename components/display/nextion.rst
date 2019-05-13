Nextion TFT LCD Display
=======================

.. seo::
    :description: Instructions for setting up Nextion TFT LCD displays
    :image: nextion.jpg

The ``nextion`` display platform allows you to use Nextion LCD displays (`datasheet <https://nextion.itead.cc/resources/datasheets/>`__,
`iTead <https://www.itead.cc/display/nextion.html>`__)
with ESPHome.

.. figure:: images/nextion-full.jpg
    :align: center
    :width: 75.0%

    Nextion LCD Display.

As the communication with the Nextion LCD display is done using UART, you need to have an :ref:`UART bus <uart>`
in your configuration with ``rx_pin`` both the ``tx_pin`` set to the respective pins on the display.
Additionally, you need to set the baud rate to 9600.

.. code-block:: yaml

    # Example configuration entry
    uart:
      rx_pin: D0
      tx_pin: D1
      baud_rate: 9600


    display:
      - platform: nextion
        lambda: |-
          it.set_component_value("gauge", 50);
          it.set_component_text("textview", "Hello World!");

Configuration variables:
------------------------

- **uart_id** (*Optional*, :ref:`config-id`): The ID of the :ref:`UART bus <uart>` you wish to use for this display.
  Use this if you want to use multiple UART buses at once.
- **lambda** (*Optional*, :ref:`lambda <config-lambda>`): The lambda to use for rendering the content on the nextion display.
  See :ref:`display-nextion_lambda` for more information.
- **update_interval** (*Optional*, :ref:`config-time`): The interval to call the lambda to update the display.
  Defaults to ``5s``.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.

.. _display-nextion_lambda:

Making a Display File
---------------------

First, you need to use the `Nextion Editor <https://nextion.itead.cc/resources/download/nextion-editor/>`__ to
create a display file. Itead have made lots of tools to help you make a GUI. To enable touch for specific components, for example a button, you will need to select the component,
then move over to the event window. Click the checkbox that say "Send Component ID" in
both "Touch Press Event" and "Touch Release Event". Now the display will send data when
someone touches your component.

Rendering Lambda
----------------

With Nextion displays, a dedicated chip on the display itself does the whole rendering. ESPHome can only
send *instructions* to the display to tell it *how* to render something and *what* to render.

In the rendering ``lambda``, you have 3 main methods
you can call to populate data on the display:

.. code-block:: yaml

    display:
      - platform: nextion
        # ...
        lambda: |-
          // set the "value" of a component - value is always an integer
          // for example gauges represent their status using integers from 0 to 100
          it.set_component_value("gauge", 50);

          // set the text of a component
          it.set_component_text("textview", "Hello World!");

          // set the text of a component with formatting
          it.set_component_text_printf("textview", "The uptime is: %.1f", id(uptime_sensor).state);

These are all the avaliable lambda calls you can do to the nextion display:

+--------------------------------------------+-----------------------------------------------------------------------------------------+---------+
| Call                                       | Description                                                                             | Example |
+============================================+=========================================================================================+=========+
| ``set_component_text``                     | Set the text of a component to a static string.                                         |         |
+--------------------------------------------+-----------------------------------------------------------------------------------------+---------+
| ``set_component_text_printf``              | Set the text of a component to a formatted string, eg sensor value.                     |         |
+--------------------------------------------+-----------------------------------------------------------------------------------------+---------+
| ``set_component_value``                    | Set the integer value of a component                                                    |         |
+--------------------------------------------+-----------------------------------------------------------------------------------------+---------+
| ``set_component_background_color``         | Set the background color of a component                                                 |         |
+--------------------------------------------+-----------------------------------------------------------------------------------------+---------+
| ``set_component_pressed_background_color`` | Set the pressed background color of a component.                                        |         |
+--------------------------------------------+-----------------------------------------------------------------------------------------+---------+
| ``set_component_font_color``               | Set the font color of a component.                                                      |         |
+--------------------------------------------+-----------------------------------------------------------------------------------------+---------+
| ``set_component_pressed_font_color``       | Set the font color when a component is pressed.                                         |         |
+--------------------------------------------+-----------------------------------------------------------------------------------------+---------+
| ``set_component_coordinates``              | Set the coordinates of a component on screen.                                           |         |
+--------------------------------------------+-----------------------------------------------------------------------------------------+---------+
| ``set_component_font``                     | Set the font id for a component.                                                        |         |
+--------------------------------------------+-----------------------------------------------------------------------------------------+---------+
| ``set_nextion_rtc_time``                   | Send the current time to the nextion display.                                           |         |
+--------------------------------------------+-----------------------------------------------------------------------------------------+---------+
| ``goto_page``                              | Show the page with a given name.                                                        |         |
+--------------------------------------------+-----------------------------------------------------------------------------------------+---------+
| ``hide_component``                         | hide_component.                                                                         |         |
+--------------------------------------------+-----------------------------------------------------------------------------------------+---------+
| ``show_component``                         | Show a component.                                                                       |         |
+--------------------------------------------+-----------------------------------------------------------------------------------------+---------+
| ``enable_component_touch``                 | Enable touch for a component.                                                           |         |
+--------------------------------------------+-----------------------------------------------------------------------------------------+---------+
| ``disable_component_touch``                | Disable touch for a component.                                                          |         |
+--------------------------------------------+-----------------------------------------------------------------------------------------+---------+
| ``add_waveform_data``                      | Add waveform data to a waveform component.                                              |         |
+--------------------------------------------+-----------------------------------------------------------------------------------------+---------+
| ``display_picture``                        | Display a picture at coordinates.                                                       |         |
+--------------------------------------------+-----------------------------------------------------------------------------------------+---------+
| ``fill_area``                              | Fill a rectangle with a color.                                                          |         |
+--------------------------------------------+-----------------------------------------------------------------------------------------+---------+
| ``line``                                   | Draw a line on the screen.                                                              |         |
+--------------------------------------------+-----------------------------------------------------------------------------------------+---------+
| ``rectangle``                              | Draw a rectangle outline.                                                               |         |
+--------------------------------------------+-----------------------------------------------------------------------------------------+---------+
| ``circle``                                 | Draw a circle outline.                                                                  |         |
+--------------------------------------------+-----------------------------------------------------------------------------------------+---------+
| ``filled_circle``                          | Draw a filled circled.                                                                  |         |
+--------------------------------------------+-----------------------------------------------------------------------------------------+---------+
| ``set_backlight_brightness``               | Set the brightness of the backlight.                                                    |         |
+--------------------------------------------+-----------------------------------------------------------------------------------------+---------+
| ``set_touch_sleep_timeout``                | Set the touch sleep timeout of the display.                                             |         |
+--------------------------------------------+-----------------------------------------------------------------------------------------+---------+
| ``send_command_no_ack``                    | Manually send a raw command to the display and don't wait for an acknowledgement packet |         |
+--------------------------------------------+-----------------------------------------------------------------------------------------+---------+



Please see :ref:`display-printf` for a quick introduction into the ``printf`` formatting rules and
:ref:`display-strftime` for an introduction into the ``strftime`` time formatting.


See Also
--------

- :doc:`index`
- :apiref:`display/nextion.h`
- `Simple Nextion Library <https://github.com/bborncr/nextion>`__ by `Bentley Born <https://github.com/bborncr>`__
- `Official Nextion Library <https://github.com/itead/ITEADLIB_Arduino_Nextion>`__ by `iTead <https://www.itead.cc/>`__
- :ghedit:`Edit`
