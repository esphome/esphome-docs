Generic Sonoff
==============

.. seo::
    :description: Instructions for using generic Sonoff devices with esphomelib.
    :image: sonoff.svg

In principle esphomelib supports all Sonoff devices, but as these devices are quite expensive
and shipping from China takes a long time, I've only set up dedicated guides for the
:doc:`Sonoff S20 <sonoff_s20>` and :doc:`Sonoff 4CH <sonoff_4ch>`.

To use sonoff devices with esphomeyaml, set the ``board`` in the
:doc:`esphomeyaml section </esphomeyaml/components/esphomeyaml>` to ``esp01_1m`` and set
``board_flash_mode`` to ``dout``.

.. code:: yaml

    esphomeyaml:
      name: <NAME_OF_NODE>
      platform: ESP8266
      board: esp01_1m
      board_flash_mode: dout

After that use the following list of pin to function mappings to set up your Sonoff device.
This list has been compiled from the Sonoff Tasmota pin source file which can be found here:
https://github.com/arendst/Sonoff-Tasmota/blob/development/sonoff/sonoff_template.h ❤️

Sonoff RF
---------

.. pintable::

    GPIO0, Button (inverted),
    GPIO12, Relay and Red LED,
    GPIO13, Green LED (inverted),
    GPIO1, UART TX pin (for external sensors)
    GPIO3, UART RX pin (for external sensors)
    GPIO4, Optional sensor
    GPIO14, Optional sensor


Sonoff SV
---------

.. pintable::

    GPIO0, Button (inverted),
    GPIO12, Relay and Red LED,
    GPIO13, Green LED (inverted),
    GPIO17, Analog Input,
    GPIO1, UART TX pin (for external sensors)
    GPIO3, UART RX pin (for external sensors)
    GPIO4, Optional sensor
    GPIO5, Optional sensor
    GPIO14, Optional sensor


Sonoff TH10/TH16
----------------

.. pintable::

    GPIO0, Button (inverted),
    GPIO12, Relay and Red LED,
    GPIO13, Green LED (inverted),
    GPIO1, UART TX pin (for external sensors)
    GPIO3, UART RX pin (for external sensors)
    GPIO4, Optional sensor
    GPIO14, Optional sensor

Sonoff Dual R1
--------------

.. pintable::

    GPIO1, Relay #1,
    GPIO3, Relay #2,
    GPIO13, Blue LED (inverted),
    GPIO4, Optional sensor
    GPIO14, Optional sensor

Sonoff Dual R2
--------------

.. pintable::

    GPIO12, Relay #1,
    GPIO5, Relay #2,
    GPIO10, Button,
    GPIO13, Blue LED (inverted),
    GPIO4, Optional sensor
    GPIO14, Optional sensor

Sonoff Pow R1
-------------

(equivalent to Huafan SS)

.. pintable::

    GPIO0, Button (inverted),
    GPIO12, Relay and Red LED,
    GPIO15, Blue LED,

    GPIO5, HLW8012 SEL Pin
    GPIO13, HLW8012 CF1 Pin
    GPIO14, HLW8012 CF Pin

See :doc:`/esphomeyaml/components/sensor/hlw8012` for measuring power.

Sonoff Pow R2
-------------

(equivalent to Huafan SS)

.. pintable::

    GPIO0, Button (inverted),
    GPIO12, Relay and Red LED,
    GPIO13, Blue LED (inverted),

See :doc:`/esphomeyaml/components/sensor/cse7766` for measuring power.

Sonoff S20, Sonoff S22, Sonoff S26
----------------------------------

See :doc:`sonoff_s20`.

Slampher
--------

.. pintable::

    GPIO0, Button (inverted),
    GPIO3, Relay and Red LED,
    GPIO13, Blue LED (inverted),
    GPIO1, UART TX pin (for external sensors)
    GPIO3, UART RX pin (for external sensors)

Sonoff Touch
------------

.. pintable::

    GPIO0, Button (inverted),
    GPIO12, Relay and Red LED,
    GPIO13, Blue LED (inverted),
    GPIO1, UART TX pin (for external sensors)
    GPIO3, UART RX pin (for external sensors)

Sonoff LED
----------

.. pintable::

    GPIO0, Button (inverted),
    GPIO13, Blue LED (inverted),
    GPIO5, Red Channel
    GPIO4, Green Channel
    GPIO15, Blue Channel
    GPIO12, Cold White Channel
    GPIO14, Warm White Channel

See :doc:`/esphomeyaml/components/light/rgbww` for controlling the lights together with
:doc:`/esphomeyaml/components/output/esp8266_pwm`.

ElectroDragon
-------------

.. pintable::

    GPIO2, Button 1 (inverted),
    GPIO0, Button 2 (inverted),
    GPIO13, Relay 1 and Red LED,
    GPIO12, Relay 2 and Red LED,
    GPIO16, Green/Blue LED
    GPIO17, Analog Input


Sonoff SC
---------

.. pintable::

    GPIO12, Light,
    GPIO13, Red LED (inverted)

See :doc:`/esphomeyaml/components/light/monochromatic` and :doc:`/esphomeyaml/components/output/esp8266_pwm`
for controlling the light pin.

Sonoff 4CH Pro
--------------

Same configuration as the :doc:`Sonoff 4CH <sonoff_4ch>`.


Sonoff B1, Ai-Thinker AiLight
-----------------------------

See :doc:`/esphomeyaml/components/my9231`.

Sonoff T1 1CH, 2CH, 3CH
-----------------------

.. pintable::

    GPIO0, Button 1 (inverted),
    GPIO12, Relay 1 and Blue LED,
    GPIO9, Button 2 (inverted),
    GPIO5, Relay 2 and Blue LED,
    GPIO10, Button 3 (inverted),
    GPIO4, Relay 3 and Blue LED,
    GPIO1, UART TX pin (for external sensors)
    GPIO3, UART RX pin (for external sensors)

Arilux LC10, Magic Home
-----------------------

.. pintable::

    GPIO2, Blue LED,
    GPIO14, Red Channel,
    GPIO5, Green Channel,
    GPIO12, Blue Channel,
    GPIO13, White Channel,

    GPIO1, UART TX pin (for external sensors)
    GPIO3, UART RX pin (for external sensors)

See :doc:`/esphomeyaml/components/light/rgbw` for controlling the lights together with
:doc:`/esphomeyaml/components/output/esp8266_pwm`.

Arilux LC01
-----------

.. pintable::

    GPIO0, Button (inverted),
    GPIO2, Blue LED,
    GPIO5, Red Channel,
    GPIO12, Green Channel,
    GPIO13, Blue Channel,
    GPIO14, White Channel,

    GPIO1, UART TX pin (for external sensors)
    GPIO3, UART RX pin (for external sensors)

See :doc:`/esphomeyaml/components/light/rgbw` for controlling the lights together with
:doc:`/esphomeyaml/components/output/esp8266_pwm`.

Arilux LC11
-----------

.. pintable::

    GPIO0, Button (inverted),
    GPIO2, Blue LED,
    GPIO5, Red Channel,
    GPIO4, Green Channel,
    GPIO14, Blue Channel,
    GPIO13, Cold White Channel,
    GPIO12, Warm White Channel,

    GPIO1, UART TX pin (for external sensors)
    GPIO3, UART RX pin (for external sensors)

See :doc:`/esphomeyaml/components/light/rgbww` for controlling the lights together with
:doc:`/esphomeyaml/components/output/esp8266_pwm`.

Sonoff S31
----------

.. pintable::

    GPIO0, Button (inverted),
    GPIO12, Relay and Red LED,
    GPIO13, Green LED (inverteD),

See :doc:`/esphomeyaml/components/sensor/cse7766` for measuring power

Shelly 1
--------

.. pintable::

    GPIO4, Relay,
    GPIO5, SW Input,

See Also
--------

- :doc:`sonoff_s20`
- :doc:`sonoff_4ch`
- :doc:`sonoff_basic`
- :doc:`esp8266`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/devices/sonoff.rst>`__

.. disqus::
