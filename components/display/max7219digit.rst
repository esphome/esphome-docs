MAX7219 Digit Display
=====================

.. seo::
    :description: Instructions for setting up MAX7219 Digit displays.
    :image: max7219digit.png

The ``max7219`` display platform allows you to use MAX7219 digit with ESPHome. Please note that this integration is *only* for the digit "matrix" display, the 7 segment display can be used with the other library.

.. figure:: images/max7219digit.png
    :align: center
    :width: 75.0%

    MAX7219 Digit Display.

As the communication with the MAX7219 Digit is done using SPI for this integration, you need
to have an :ref:`SPI bus <spi>` in your configuration with both the **mosi_pin** set (miso_pin is not required).
Connect VCC to 3.3V (the manufacturer recommends 4+ V, but 3.3V seems to work fine), DIN to your ``mosi_pin`` and
CS to your set ``cs_pin`` and finally GND to GND.

You can even daisy-chain multiple MAX7219s by connecting the DOUT of the previous chip in the chain to the
next DIN. With more than ~3 chips the 3.3V will probably not be enough, so then you will have to potentially
use a logic level converted.

.. code-block:: yaml

    # Example configuration entry
    spi:
      clk_pin: D0
      mosi_pin: D1

    display:
      - platform: max7219digit
        cs_pin: D2
        num_chips: 4
        offset: 2
        intensity: 15
        lambda: |-
          it.print(0, 0, id(digit_font), "HELLO!");

Configuration variables:
------------------------

- **cs_pin** (**Required**, :ref:`Pin Schema <config-pin_schema>`): The pin you have the CS line hooked up to.
- **num_chips** (*Optional*, integer): The number of chips you wish to use for daisy chaining. Defaults to
  ``4``.
- **offset** (*Optional*, integer): The number of extra virtual chips to buffer text. (Can be used when scrolling text)
- **intensity** (*Optional*, integer): The intensity with which the MAX7219 should drive the outputs. Range is from
  0 (least intense) to 15 (the default).
- **lambda** (*Optional*, :ref:`lambda <config-lambda>`): The lambda to use for rendering the content on the MAX7219.
  See :ref:`display-max7219digit_lambda` for more information.
- **update_interval** (*Optional*, :ref:`config-time`): The interval to re-draw the screen. Defaults to ``1s``.
- **spi_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the :ref:`SPI Component <spi>` if you want
  to use multiple SPI buses.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.

.. _display-max7219digit_lambda:

Rendering Lambda
----------------

The MAX7219 digit is based on the fully fledged :ref:`display-engine`, as it has a concept of individual pixels 8 X 8 per max7219 chip. 
In the lambda you're passed a variable called ``it``
as with all other displays. Some "Special" commands have been added to the basic display set.

.. code-block:: yaml

    display:
      - platform: max7219digit
        cs_pin: D8
        num_chips: 4
        lambda: |-
          it.strftime(0, 0, id(digit_font), "%H:%M", id(hass_time).now());
          it.image(24, 0, id(my_image));
          it.line(1,8,21,8);
     font:
       - file: "pixelmix.ttf"
         id: digit_font
         size: 6
     time:
       - platform: homeassistant
         id: hass_time
     image:
       - file: "smile.png"
         id: my_image

This is roughly the code used to display the MAX7219 display at the image.

Some special MAX7219 digit code can be added as follows:

.. code-block:: yaml

    display:
      - platform: max7219digit
        # ...
        lambda: |-
          // Print 0 at position 0 (left)
          it.print(0,0, id(digit_font), "Hello!");
          it.scroll_left(1);

The text on the display will scroll left 1 step per update in a contineaous loop. If extra display space is reserved by adding offset = for example 2, "hidden" text will appear in time on more text can be displayed.

.. code-block:: yaml

    display:
      - platform: max7219digit
        # ...
        lambda: |-
          it.invert_on_off(true);
          // Print Hello at position 0 (left)
          it.print(0,0, id(digit_font), "Hello!");
           
The function it.invert_on_off(true); will inverst the display. So background pixels are on and texts pixels are off. it.invert_on_off(false); sets the display back to normal. In case no argument is used: it.inverst_on_off(); the inversion will toggle from on to off or visa versa. This will happen every time the display is updated. So a blinking effect is created.
The background pixels are only set at the next update, the pixels drawn in the various function like print, line, etc. are directly influenced by the invert command.

.. code-block:: yaml

    display:
      - platform: max7219digit
        # ...
        lambda: |-
          // Print Hello at position 0 (left)
          it.print(0,0, id(digit_font), "Hello!");
          it.invert_on_off(true);
          it.line(0,0,32,8);
          it.invert_on_off(false);

This code will only effect the line drawn on the screen. The line will wipe the pixels from top left to right bottom. The background is not effected as the Lambda is closed with an Invert_on_of(false) code.

For a quick display some additional commands are embedded in the code with a related 8 pixel font. Three methods (``printdigit``, ``printfdigit`` and ``strftimedigit``) can be used for diplaying characters. Each 8 X 8 grid is used to display a single character. So not very space efficient. 
The format of the command is: ``it.printdigit("1234");`` or ``it.printfdigit("%S","1234")``;

Please see :ref:`display-printf` for a quick introduction into the ``printf`` formatting rules and
:ref:`display-strftime` for an introduction into the ``strftime`` time formatting.

See Also
--------

- :doc:`index`
- :apiref:`max7219/max7219.h`
- `MAX7219 Library <https://github.com/nickgammon/MAX7219>`__ by `Nick Gammon <https://github.com/nickgammon>`__
- :ghedit:`Edit`
