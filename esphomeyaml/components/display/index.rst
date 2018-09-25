Display Component
=================

The ``display`` component houses esphomelib's powerful rendering and display
engine. Fundamentally, there are these types of displays:

- Text based displays like :doc:`7-Segment displays <max7219>` or
  :doc:`some LCD displays <lcd_gpio>`.
- Displays like the :doc:`nextion` that have their own processors for rendering.
- Binary displays which can toggle ON/OFF any pixel, like :doc:`E-Paper displays <waveshare_epaper>` or
  :doc:`OLED displays <ssd1306_spi>`.

For the last type, esphomelib and esphomeyaml have a powerful rendering engine that can do
many things like draw some basic shapes, print text with any font you want, or even show images.

To achieve all this flexibility displays tie in directly into esphomeyaml's :ref:`lambda system <config-lambda>`.
So when you want to write some text or sensor values to the screen you will be writing in C++ code
using an API that is designed to

- be simple and to be used without programming experience
- but also be flexible enough to work with more complex tasks like displaying an analog clock.

.. _display-engine:

Display Rendering Engine
------------------------

In this section we will be discussing how to use esphomelib's display rendering engine from esphomeyaml
and some basic commands. Please note that this only applies to displays that can control each pixel
individually.

So, first a few basics: When setting up a display platform in esphomeyaml there will be a configuration
option called ``lambda:`` which will be called every time esphomelib wants to re-render the display.
In there, you can write code like in any :ref:`lambda <config-lambda>` in esphomeyaml. Display
lambdas are additionally passed a variable called ``it`` which represents the rendering engine object.

.. code:: yaml

    display:
      - platform: ...
        # ...
        lambda: |-
          // Write your display rendering code here

          // For example, draw a line from [x=0,y=0] to [x=50,y=50]
          it.line(0, 0, 50, 50);

.. note::

    Lambdas are essentially just a lightly modified version of C++. So don't forget to end each line
    with a semicolon (``;``). Otherwise you will be greeted by a long error message at the compilation stage.

If you compile and upload the configuration above, you should see a black (or white, depending on the display)
line which starts at the top left and goes a few pixels down at a 45° angle. (If it's in another corner, use the
``rotation:`` option to rotate the display to your liking)

This already highlights one of the things you must learn before diving into writing your own custom display code:
The **top left** is always the origin of the pixel coordinate system. Also, all points in this coordinate system
are a pair of integers like ``50, 50`` which represent the shift to the right and shift downwards. So, in other words,
x always represents the horizontal axis (width) and y the vertical axis (height). And the convention in
the rendering engine is always first specify the ``x`` coordinate and then the ``y`` coordinate.

Basic Shapes
************

Now that you know a bit more about esphomelib's coordinate system, let's draw some basic shapes like lines, rectangles
and circles:

.. code:: yaml

    display:
      - platform: ...
        # ...
        lambda: |-
          // Draw a line from [0,0] to [100,50]
          it.line(0, 0, 100, 50);
          // Draw the outline of a rectangle with the top left at [50,60], a width of 30 and a height of 42
          it.rectangle(50, 60, 30, 42);
          // Draw the same rectangle, but this time filled.
          it.filled_rectangle(50, 60, 30, 42);

          // Circles! Let's draw one with the center at [25,25] and a radius of 10
          it.circle(25, 25, 10);
          // ... and the same thing filled again
          it.filled_circle(25, 25, 10);

All the above methods can optionally also be called with an argument at the end which specifies in which
color to draw. Currently, only ``COLOR_ON`` (the default if color is not given) and ``COLOR_OFF`` are supported because
esphomelib only has implemented binary displays.

.. code:: yaml

    display:
      - platform: ...
        # ...
        lambda: |-
          // Turn the whole display on.
          it.fill(COLOR_ON);
          // Turn the whole display off.
          it.fill(COLOR_OFF);

          // Turn a single pixel off at [50,60]
          it.draw_pixel_at(50, 60, COLOR_OFF);

          // Turn off a whole display portion.
          it.rectangle(50, 50, 30, 42, COLOR_OFF);

Additionally, you have access to two helper methods which will fetch the width and height of the display:

.. code:: yaml

    display:
      - platform: ...
        # ...
        lambda: |-
          // Draw a circle in the middle of the display
          it.filled_circle(it.get_width() / 2, it.get_height() / 2);


You can view the full API documentation for the rendering engine over at :ref:`display-buffer`.

.. _display-static_text:

Drawing Static Text
*******************

The rendering engine also has a powerful font drawer which integrates seamlessly into esphomeyaml.
Whereas in most arduino display projects you have to use one of a few pre-defined fonts in very
specific sizes, with esphomeyaml you have the option to use **any** truetype (``.ttf``) font file
at **any** size! Granted the reason for it is actually not having to worry about the licensing of font files :)

To use fonts you first have to define a font object in your esphomeyaml configuration file. Just grab
a ``.ttf`` file from somewhere on the Internet and create a ``font:`` section in your configuration:

.. code:: yaml

    font:
      - file: "Comic Sans MS.ttf"
        id: my_font
        size: 20

    display:
      # ...


Configuration variables:

- **file** (**Required**, string): The path (relative to where the .yaml file is) of the truetype font
  file.
- **id** (**Required**, :ref:`config-id`): The ID with which you will be able to reference the font later
  in your display code.
- **size** (*Optional*, int): The size of the font in pt (not pixel!).
  If you want to use the same font in different sizes, create two font objects. Defaults to ``20``.
- **glyphs** (*Optional*, list): A list of characters you plan to use. Only the characters you specify
  here will be compiled into the binary. Adjust this if you need some special characters or want to
  reduce the size of the binary if you don't plan to use some glyphs. The items in the list can also
  be more than one character long if you for example want to use font ligatures. Defaults to
  ``!"%()+,-_.:°0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz``.


.. note::

    To use fonts you will need to have the python ``pillow`` package installed, as esphomeyaml uses that package
    to translate the truetype files into an internal format. If you're running this as a HassIO add-on or with
    the official esphomeyaml docker image, it should already be installed. Otherwise you need to install it using
    ``pip2 installl pillow``.


Then, in your display code just reference the font like so:

.. code:: yaml

    display:
      - platform: ...
        # ...
        lambda: |-
          // Print the string "Hello World!" at [0,10]
          it.print(0, 10, id(my_font), "Hello World!");

By default, esphomelib will *align* the text at the top left. That means if you enter the coordinates
``[0,10]`` for your text, the top left of the text will be at ``[0,10]``. If you want to draw some
text at the right side of the display, it is however sometimes useful to choose a different **text alignment**.
When you enter ``[0,10]`` you're really telling esphomelib that it should position the **anchor point** of the text
at ``[0,10]``. When using a different alignment, like ``TOP_RIGHT``, the text will be positioned left of the anchor
pointed, so that, as the name implies, the anchor point is a the *top right* corner of the text.

.. code:: yaml

    display:
      - platform: ...
        # ...
        lambda: |-
          // Aligned on left by default
          it.print(0, 0, id(my_font), "Left aligned");

          // Aligned on right edge
          it.print(0, it.get_width(), id(my_font), TextAlign::TOP_RIGHT, "Right aligned");

As with basic shapes, you can also specify a color for the text:

.. code:: yaml

    display:
      - platform: ...
        # ...
        lambda: |-
          // Syntax is always: it.print(<x>, <y>, <font>, [color=COLOR_ON], [align=TextAlign::TOP_LEFT], <text>);
          it.print(0, 0, id(my_font), COLOR_ON, "Left aligned");


.. _display-printf:

Formatted Text
**************

Static text by itself is not too impressive. What we really want is to display *dynamic* content like sensor values
on the display!. That's where ``printf`` comes in. ``printf`` is a formatting engine from the C era and esphomelib
chose to use because ... well, I'm too lazy to create a fully-fledged format engine where the existing stuff
is way better documented :)

``printf`` can do way more stuff than you will probably ever need, but it's also quite simple for the basic stuff.
For example, a printf call can look like this:

.. code:: yaml

    sensor:
      - platform: ...
        # ...
        id: my_sensor

    display:
      - platform: ...
        # ...
        lambda: |-
          it.printf(0, 0, id(my_font), "The sensor value is: %.1f", id(my_sensor).value);
          // If the sensor has the value 30.02, the result will be: "The sensor value is: 30.0"

As you can see, when you call ``printf`` most of the string is printed as-is, but when this weird percent sign with some
stuff after it is encountered, it is magically replaced by the argument after the format (here ``id(my_sensor).value``).

Every time you type a percent sign ``%`` in a printf format string, it will treat the following letters as a format tag
until a so-called "specifier" is encountered (in this case ``f``). You can read more about it `here <https://www.tutorialspoint.com/c_standard_library/c_function_printf.htm>`__,
but for esphomelib there are really just a few things you need to know.

Let's break ``%.1f`` down:

- ``%`` - initiate the format string
- ``.1`` - round the decimal number to ``1`` digits after the decimal point.
- ``f`` - the specifier which tells printf the data type of the argument. Here it is a f(loat).

For example, if you would like to print a sensor value with two digits of accuracy, you would write ``%.2f`` and with
zero digits of accuracy (without a decimal) ``%.0f``.

Another interesting format string is ``%7.2f``, which would become the right-justified string
``"  20.51"`` for a value of 20.506.

- ``%`` - initiate the format
- ``7`` - means that the number will be right-justified and be padded on the left by spaces if
  the result would be shorter than 7 characters long.
- ``.1`` - round the decimal number to ``1`` digits after the decimal point.
- ``f`` - specifier: f(loat).

You can even have as many format strings as you want in a single printf call. Just make sure the put the
arguments after the format string in the right order.

.. code:: yaml

    display:
      - platform: ...
        # ...
        lambda: |-
          // %% - literal % sign
          it.printf(0, 0, id(my_font), "Temperature: %.1°C, Humidity: %.1f%%", id(temperature).value, id(humidity).value);


The last printf tip for use in displays I will discuss here is how to display binary sensor values. You
*could* of course just check the state with an ``if`` statement as the first few lines in the example below, but if
you want to be efficient you can use an *inline if* too. With the ``%s`` print specifier you can tell it to
use any string you pass it, like ``"ON"`` or ``"OFF"``.

.. code:: yaml

    binary_sensor:
      - platform: ...
        # ...
        id: my_binary_sensor

    display:
      - platform: ...
        # ...
        lambda: |-
          if (id(my_binary_sensor).value) {
            it.print(0, 0, id(my_font), "state: ON");
          } else {
            it.print(0, 0, id(my_font), "state: OFF");
          }
          // Shorthand:
          it.printf(0, 0, id(my_font), "State: %s", id(my_binary_sensor).value ? "ON" : "OFF");

.. _display-strftime:

Displaying Time
***************

With esphomelib you can also display the current time using the NTP protocol. Please see the example :ref:`here <strftime>`.

Images
^^^^^^

.. code:: yaml

    image:
      - file: "image.png"
        id: my_image
        resize: 100x100

Configuration variables:

- **file** (**Required**, string): The path (relative to where the .yaml file is) of the image file.
- **id** (**Required**, :ref:`config-id`): The ID with which you will be able to reference the font later
  in your display code.
- **resize** (*Optional*, int): If set, this will resize the image to fit inside the given dimensions ``WIDTHxHEIGHT``
  and preserve the aspect ratio.

.. note::

    To use images you will need to have the python ``pillow`` package installed.
    If you're running this as a HassIO add-on or with the official esphomeyaml docker image, it should already be
    installed. Otherwise you need to install it using ``pip2 installl pillow``.

And then later in code:

.. code:: yaml

    display:
      - platform: ...
        # ...
        lambda: |-
          // Draw the image my_image at position [x=0,y=0]
          it.image(0, 0, id(my_image));

See Also
--------

- :doc:`API Reference </api/display/index>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/display/index.rst>`__

.. toctree::
    :maxdepth: 1

    lcd_gpio
    lcd_pcf8574
    max7219
    nextion
    ssd1306_i2c
    ssd1306_spi
    waveshare_epaper
