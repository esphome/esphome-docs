Character-Based LCD Display
===========================

.. seo::
    :description: Instructions for setting up character-based LCD displays.
    :image: lcd.jpg

.. _lcd-pcf8574:

lcd_pcf8574 Component
---------------------

The ``lcd_pcf8574`` display platform allows you to use standard character-based LCD displays like
`this one <https://docs.labs.mediatek.com/resource/linkit7697-arduino/en/tutorial/driving-1602-lcd-with-pcf8574-pcf8574a>`__
with ESPHome. This integration is only for LCD displays that display individual characters on a screen (usually 16-20 columns
and 2-4 rows), and not for LCD displays that can control each pixel individually.

This version of the LCD integration is for LCD displays with a PCF8574 connected to all the data pins. This has
the benefit that you only need to connect two data wires to the ESP instead of the 6 or 10 with the :ref:`lcd-gpio`.
As the communication with the :ref:`I²C Bus <i2c>`, you need to have an ``i2c:`` section in your configuration.

.. figure:: images/lcd-pcf8574.jpg
    :align: center
    :width: 75.0%

    The PCF8574 chip attached to the LCD Display.

.. figure:: images/lcd-hello_world.jpg
    :align: center
    :width: 60.0%

.. code-block:: yaml

    # Example configuration entry
    i2c:
      sda: D0
      scl: D1

    display:
      - platform: lcd_pcf8574
        dimensions: 18x4
        address: 0x3F
        lambda: |-
          it.print("Hello World!");

Configuration variables:
************************

- **dimensions** (**Required**, string): The dimensions of the display with ``COLUMNSxROWS``. If you're not
  sure, power the display up and just count them.
- **address** (*Optional*, int): The :ref:`I²C <i2c>` address of the PCF8574 chip, defaults to ``0x3F``.
- **lambda** (*Optional*, :ref:`lambda <config-lambda>`): The lambda to use for rendering the content on the display.
  See :ref:`display-lcd_lambda` for more information.
- **update_interval** (*Optional*, :ref:`config-time`): The interval to re-draw the screen. Defaults to ``1s``.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.

.. _lcd-gpio:

lcd_gpio Component
------------------

The ``lcd_gpio`` display platform allows you to use standard character-based LCD displays like `this one <https://www.adafruit.com/product/181>`__
with ESPHome. This integration is only for LCD displays that display individual characters on a screen (usually 16-20 columns
and 2-4 rows), and not for LCD displays that can control each pixel individually. Also, this is the GPIO version of the LCD
integration where each of the data pins of the LCD needs a dedicated GPIO pin on the ESP. These LCD displays are also
commonly sold with a PCF8574 chip which only need two lines to the ESP, for that see :ref:`lcd-pcf8574`.

.. figure:: images/lcd-full.jpg
    :align: center
    :width: 75.0%

    LCD Display.

.. code-block:: yaml

    # Example configuration entry
    display:
      - platform: lcd_gpio
        dimensions: 18x4
        data_pins:
          - D0
          - D1
          - D2
          - D3
        enable_pin: D4
        rs_pin: D5
        lambda: |-
          it.print("Hello World!");

Configuration variables:
************************

- **dimensions** (**Required**, string): The dimensions of the display with ``COLUMNSxROWS``. If you're not
  sure, power the display up and just count them.
- **data_pins** (**Required**, list of :ref:`Pin Schemas <config-pin_schema>`): A list of the data pins you
  have hooked up to the LCD. The list can either be 8 items long (when you have connected all 8 data pins), or
  4 items long (if you're operating in 4-bit mode with either the first 4 data pins connected or the last 4 data
  pins connected).
- **enable_pin** (**Required**, :ref:`Pin Schema <config-pin_schema>`): The pin you have ``EN`` hooked up to.
- **rs_pin** (**Required**, :ref:`Pin Schema <config-pin_schema>`): The pin you have ``RS`` hooked up to.
- **rw_pin** (*Optional*, :ref:`Pin Schema <config-pin_schema>`): Optionally set the pin you have ``RW`` hooked up to.
  You can also just permanently connect that pin to GND.
- **lambda** (*Optional*, :ref:`lambda <config-lambda>`): The lambda to use for rendering the content on the display.
  See :ref:`display-lcd_lambda` for more information.
- **update_interval** (*Optional*, :ref:`config-time`): The interval to re-draw the screen. Defaults to ``1s``.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.

.. _display-lcd_lambda:

Rendering Lambda
----------------

The LCD displays has a similar API to the fully fledged :ref:`display-engine`, but it's only a subset as LCD displays
don't have a concept of individual pixels. In the lambda you're passed a variable called ``it``
as with all other displays. In this case however, ``it`` is an instance of either ``GPIOLCDDisplay`` or ``PCF8574LCDDisplay``.

The most basic operation with LCD Displays is writing static text to the screen as in the configuration example
at the top of this page.

Each of the three methods (``print``, ``printf`` and ``strftime``) all optionally take a column and row arguments at the
beginning which can be used to print the text at a specific position. These arguments are set to ``0`` (column) and ``0`` (row)
by default which means the character at the top left.

.. code-block:: yaml

    display:
      - platform: lcd_gpio # or lcd_pcf8574
        # ...
        lambda: |-
          // Print 0 at the top left
          it.print("0");

          // Print 1 at the second row and second column.
          it.print(1, 1, "1");

          // Let's write a sensor value (let's assume it's 42.1)
          it.printf("%.1f", id(my_sensor).state);
          // Result: "42.1" (the dot will appear on the "2" segment)

          // Print a right-padded sensor value with 0 digits after the decimal
          it.printf("Sensor value: %8.0f", id(my_sensor).state);
          // Result: "Sensor value:       42"

          // Print the current time
          it.strftime("It is %H:%M on %d.%m.%Y", id(my_time).now());
          // Result for 10:06 on august 21st 2018 -> "It is 10:06 on 21.08.2018"

    # (Optional) For displaying time:
    time:
    - platform: sntp
      id: my_time

.. note::

    If you're not seeing anything on the display, make sure you try turning the contrast potentiometer around.

Please see :ref:`display-printf` for a quick introduction into the ``printf`` formatting rules and
:ref:`display-strftime` for an introduction into the ``strftime`` time formatting.

Backlight Control
-----------------

For the GPIO based display, the backlight is lit by applying Vcc to the A pin and K connected to ground.
The backlight can draw more power than the microcontroller output pins can supply, so it is advisable to use
a transistor as a switch to control the power for the backlight pins.

With the ``lcd_pcf8574`` the backlight can be turned on by ``it.backlight()`` and off by ``it.no_backlight()`` in the
display lambda definition. The jumper on the PCF8574 board needs to be closed for the backlight control to work.
Keep in mind that the display lambda runs for every ``update_interval``, so if the backlight is turned on/off there,
it cannot be overridden from other parts.

Here is one solution for a typical use-case where the backlight is turned on after a motion sensor activates and
turns off 90 seconds after the last activation of the sensor.

.. code-block:: yaml

    display:
      - platform: lcd_pcf8574
        id: mydisplay
        # ...

    binary_sensor:
      - platform: gpio
        # ...
        on_press:
          then:
            - binary_sensor.template.publish:
                id: backlight
                state: ON
            - binary_sensor.template.publish:
                id: backlight
                state: OFF
      - platform: template
        id: backlight
        filters:
          - delayed_off: 90s
        on_press:
          then:
            - lambda: |-
                id(mydisplay).backlight();
        on_release:
          then:
            - lambda: |-
                id(mydisplay).no_backlight();

See Also
--------

- :doc:`index`
- :doc:`/components/switch/gpio`
- :doc:`/components/binary_sensor/gpio`
- :doc:`/components/pcf8574`
- :apiref:`lcd_base/lcd_display.h`
- `Arduino LiquidCrystal Library <https://www.arduino.cc/en/Reference/LiquidCrystal>`__
- :ghedit:`Edit`
