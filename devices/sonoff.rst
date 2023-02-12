Generic Sonoff
==============

.. seo::
    :description: Instructions for using generic Sonoff devices with ESPHome.
    :image: sonoff.svg

ESPHome supports Sonoff devices with ESP based chips inside, but as these devices are quite cheap
and shipping from China takes a long time, I've only set up dedicated guides for the
:doc:`Sonoff S20 <sonoff_s20>` and :doc:`Sonoff 4CH <sonoff_4ch>`.

.. code-block:: yaml

    esphome:
      name: <NAME_OF_NODE>

    esp8266:
      board: esp8285

After that use the following list of pin to function mappings to set up your Sonoff device.
This list has been compiled from the Sonoff Tasmota pin source file which can be found `here <https://github.com/arendst/Tasmota/blob/development/tasmota/tasmota_template.h>`__.


.. note::

    SAFETY HAZARD: Some devices such as Sonoff POWs/Shelly/etc, have the digital GND connected directly to mains voltage so **the GPIOs become LIVE during normal operation**. Our advice is to mark these boards to prevent any use of the dangerous digital pins.

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
    GPIO2, Optional Pin EXP-LOG (TH16 Ver 2.1 2019)

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

Sonoff Dual R2 v1.4
-------------------

.. pintable::

    GPIO00, Button #0(inside header board v1.4),
    GPIO09, Button #1(inside header board v1.4),
    GPIO12, Relay #1,
    GPIO5, Relay #2,
    GPIO10, Button on the case,
    GPIO13, Blue LED (inverted)

Sonoff Dual R3 v1.x, v2.x
-------------------------

.. pintable::

    GPIO27, Relay #1,
    GPIO14, Relay #2,
    GPIO0, Button,
    GPIO13, Blue LED (inverted),
    GPIO32, SW Input #1 (inverted),
    GPIO33, SW Input #2 (inverted),
    GPIO25, UART TX pin (for power sensor)
    GPIO26, UART RX pin (for power sensor)

For power measuring see :doc:`/components/sensor/cse7761` (v1.x) or :doc:`/components/sensor/bl0939` (v2.x)

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

See :doc:`/components/sensor/hlw8012` for measuring power.

Sonoff Pow R2
-------------

(equivalent to Huafan SS)

.. pintable::

    GPIO0, Button (inverted),
    GPIO12, Relay and Red LED,
    GPIO13, Blue LED (inverted),

See :doc:`/components/sensor/cse7766` for measuring power.

Sonoff S20, Sonoff S22, Sonoff S26
----------------------------------

See :doc:`sonoff_s20`.

Slampher
--------

.. pintable::

    GPIO0, Button (inverted),
    GPIO12, Relay and Red LED,
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

See :doc:`/components/light/rgbww` for controlling the lights together with
:doc:`/components/output/esp8266_pwm`.

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

See :doc:`/components/light/monochromatic` and :doc:`/components/output/esp8266_pwm`
for controlling the light pin.

Sonoff 4CH Pro
--------------

Same configuration as the :doc:`Sonoff 4CH <sonoff_4ch>`.


Sonoff B1, Ai-Thinker AiLight
-----------------------------

See :doc:`/components/output/my9231`.

Sonoff T1, Sonoff T3 (1CH, 2CH, 3CH)
------------------------------------

.. pintable::

    GPIO0, Button 1 (inverted),
    GPIO12, Relay 1 and Blue LED,
    GPIO9, Button 2 (inverted),
    GPIO5, Relay 2 and Blue LED,
    GPIO10, Button 3 (inverted),
    GPIO4, Relay 3 and Blue LED,
    GPIO13, Blue LED (inverted),

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

See :doc:`/components/light/rgbw` for controlling the lights together with
:doc:`/components/output/esp8266_pwm`.

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

See :doc:`/components/light/rgbw` for controlling the lights together with
:doc:`/components/output/esp8266_pwm`.

Arilux LC02
-----------

.. pintable::

    GPIO0, Button (inverted),
    GPIO2, Blue LED,
    GPIO5, Red Channel,
    GPIO14, Green Channel,
    GPIO12, Blue Channel,
    GPIO13, White Channel,

    GPIO1, UART TX pin (for external sensors)
    GPIO3, UART RX pin (for external sensors)

See :doc:`/components/light/rgbw` for controlling the lights together with
:doc:`/components/output/esp8266_pwm`.

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

See :doc:`/components/light/rgbww` for controlling the lights together with
:doc:`/components/output/esp8266_pwm`.

Sonoff S31
----------

.. pintable::

    GPIO0, Button (inverted),
    GPIO12, Relay and Red LED,
    GPIO13, Green LED (inverted),

See :doc:`/components/sensor/cse7766` for measuring power

Sonoff S55
----------

.. pintable::

    GPIO0, Button (inverted),
    GPIO12, Relay and Red LED,
    GPIO13, Blue LED (inverted),
    GPIO1, UART TX pin (for external sensors)
    GPIO3, UART RX pin (for external sensors)


Sonoff Mini
-----------

.. pintable::

    GPIO0, Button (inverted),
    GPIO4, SW Input (inverted),
    GPIO12, Relay and Red LED,
    GPIO13, Blue LED (inverted),
    GPIO16, Optional sensor


Sonoff THR316D
--------------

.. pintable::

    GPIO0, Button,
    GPIO21, Relay 1,
    GPIO4, Relay 2,
    GPIO27, Optionnal sensor power ON/OFF,
    GPIO25, sensor,
    GPIO16, Power LED,
    GPIO15, Wifi LED (inverted),
    GPIO13, Cycle LED (inverted),
    GPIO23, Display Read,
    GPIO18, Display Write,
    GPIO5, Display Data,
    GPIO17, Display CS,
    
    GPIO1, UART TX pin (for log)
    GPIO3, UART RX pin (for log)


Shelly 1
--------

.. pintable::

    GPIO4, Relay,
    GPIO5, SW Input,

Shelly 2
--------

.. pintable::

    GPIO4, Relay #1,
    GPIO5, Relay #2,
    GPIO12, SW Input #1,
    GPIO14, SW Input #2,

Teckin
------

.. pintable::

    GPIO1, Button (inverted),
    GPIO3, Blue LED (inverted),
    GPIO13, Red LED (inverted),
    GPIO14, Relay,

    GPIO12, HLW8012 SEL Pin (inverted),
    GPIO4, HLW8012 CF Pin,
    GPIO5, HLW8012 CF1 Pin,

See :doc:`/components/sensor/hlw8012` for measuring power.
Example config: `teckin.yaml <https://github.com/esphome/esphome-docs/blob/current/devices/teckin.yaml>`__

Teckin SP20 (US)
----------------

.. pintable::

    GPIO13, Button,
    GPIO2, Blue LED (inverted),
    GPIO0, Red LED (inverted),
    GPIO4, Relay,

    GPIO12, HLW8012 SEL Pin (inverted),
    GPIO5, HLW8012 CF Pin,
    GPIO14, HLW8012 CF1 Pin,

See :doc:`/components/sensor/hlw8012` for measuring power.
Example config: `teckin_sp20_us.yaml <https://github.com/esphome/esphome-docs/blob/current/devices/teckin_sp20_us.yaml>`__

TorchStar LED Controller (Nov 2018)
-----------------------------------

.. pintable::

    GPIO13, Button (inverted),
    GPIO16, Blue LED (inverted),
    GPIO4, Red LED (inverted),
    GPIO14, Red Channel,
    GPIO12, Green Channel,
    GPIO5, Blue Channel,
    GPIO15, White Channel,

See Also
--------

- :doc:`sonoff_s20`
- :doc:`sonoff_4ch`
- :doc:`sonoff_basic`
- :doc:`/components/esp8266`
- :ghedit:`Edit`
