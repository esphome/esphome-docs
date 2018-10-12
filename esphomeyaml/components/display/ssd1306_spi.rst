SSD1306 OLED Display over SPI
=============================

The ``ssd1306_spi`` display platform allows you to use
SSD1306 (`datasheet <https://cdn-shop.adafruit.com/datasheets/SSD1306.pdf>`__, `Adafruit <https://www.adafruit.com/product/326>`__)
and SH1106 (`datasheet <https://www.elecrow.com/download/SH1106%20datasheet.pdf>`__, `electrodragon <https://www.electrodragon.com/product/1-3-12864-blue-oled-display-iicspi/>`__)
displays with esphomelib. Note that this component is for displays that are connected via the 4-Wire :ref:`SPI bus <spi>`.
If your SSD1306 or SH1106 is connected via the :ref:`I²C Bus <i2c>`, see :doc:`ssd1306_i2c`.

.. figure:: images/ssd1306-full.jpg
    :align: center
    :width: 75.0%

    SSD1306 OLED Display

Connect D0 to the CLK pin you chose for the :ref:`SPI bus <spi>`, connect D1 to the MOSI pin and ``DC`` and ``CS``
to some GPIO pins on the ESP. For power, connect
VCC to 3.3V and GND to GND. Optionally you can also connect the ``RESET`` pin to a pin on the ESP which may
improve reliability.

.. code:: yaml

    # Example configuration entry
    spi:
      clk_pin: D0
      mosi_pin: D1

    display:
      - platform: ssd1306_spi
        model: "SSD1306 128x64"
        cs_pin: D2
        dc_pin: D3
        reset_pin: D4
        lambda: |-
          it.print(0, 0, id(font), "Hello World!");

Configuration variables:
------------------------

- **model** (**Required**): The model of the display. Options are:

  - ``SSD1306 128x32`` (SSD1306 with 128 columns and 32 rows)
  - ``SSD1306 128x64``
  - ``SSD1306 96x16``
  - ``SSD1306 64x48``
  - ``SH1106 128x32``
  - ``SH1106 128x64``
  - ``SH1106 96x16``
  - ``SH1106 64x48``

- **cs_pin** (**Required**, :ref:`Pin Schema <config-pin_schema>`): The Chip Select (CS) pin.
- **dc_pin** (**Required**, :ref:`Pin Schema <config-pin_schema>`): The DC pin.
- **reset_pin** (*Optional*, :ref:`Pin Schema <config-pin_schema>`): The RESET pin. Defaults to not connected.
- **rotation** (*Optional*): Set the rotation of the display. Everything you draw in ``lambda:`` will be rotated
  by this option. One of ``0°`` (default), ``90°``, ``180°``, ``270°``.
- **external_vcc** (*Optional*, boolean): Set this to true if you have the VCC pin connected to an external power supply.
  Defaults to ``false``.
- **lambda** (*Optional*, :ref:`lambda <config-lambda>`): The lambda to use for rendering the content on the display.
  See :ref:`display-engine` for more information.
- **update_interval** (*Optional*, :ref:`config-time`): The interval to re-draw the screen. Defaults to ``5s``.
- **spi_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the :ref:`SPI Component <spi>` if you want
  to use multiple SPI buses.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.

See Also
--------

- :doc:`index`
- :doc:`API Reference </api/display/ssd1306>`
- `SSD1306 Library <https://github.com/adafruit/Adafruit_SSD1306>`__ by `Adafruit <http://adafruit.com/>`__
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/display/ssd1306_spi.rst>`__

.. disqus::
