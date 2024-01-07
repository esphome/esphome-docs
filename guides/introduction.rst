Introduction
============

.. seo::
    :description: Introduction and getting started guide for using ESPHome

ESPHome is a tool for generating customized firmware for embedded CPUs, originally only ones from Espressiv,
but now it's available for more.  How to install ESPHome is explained in other guides, this one is about how
to get started with creating configurations and then on to how to extend it with your own components.

ESPHome takes a configuration file written in YAML and generates a ``main.cpp`` file and collects the various
component source files together.  This code then gets compiled into a firmware binary file that can be installed
to the device.  Only the source files needed for this specific configuration are included, so the resulting
firmware file is as small as possible.

YAML
----

`YAML <https://yaml.org/>`__ is the language used for describing the requested configuration.  It has a
structured syntax with significant whitespace.  Indents matter!  You can use spaces or tabs, but if you value
your sanity, only use spaces.  It is a collection of keys and values separated by colons.  e.g. ``key: value``
Comments can be included by putting a ``#`` character.  Anything following it will be ignored by the parser.
Comments can put almost anywhere in a file, but not inside a ``lambda`` (described later).

Keys
****

Keys are strings without spaces.

.. code-block:: yaml

    key:
    entry200:
    a_long_extended_key:

Value: number
************

Numbers can be integers (``500``), floats (``1.23``), hexadecimal (``0x80``), and possibly others.

.. code-block:: yaml

    integer: 500
    float: 1.23
    hex: 0x80

Value: boolean
**************

Boolean values can be, `true`, `false`, `yes`, `no`, `on`, `off`.

.. code-block:: yaml

    have_keys: false
    start_car: no
    lights: on

Value: string
*************

String values can be quoted with ``''`` or ``""`` or left unquoted.  However, if there are YAML special characters
in the string, such as ``:``, it must be quoted.

.. code-block:: yaml

    simple_string: this is a string
    has_colon: "must: be quoted"

Value: dictionary
*****************

A "dictionary" is a collection of key/value pairs.  Notice the indenting.

.. code-block:: yaml

    dictionary_key:
      integer: 500
      start_car: no
      lights: on

Value: list/array
*****************

A list (or array) can be represented in two ways, as comma-separated items inside square brackets (``[]``), or as
separate lines started with a hyphen (``-``).  If you use the hyphen option, you don't need to indent, but it can
still be better for readability.

.. code-block:: yaml

    array_key:
      - item1
      - 2

    array_key2:
    - item1
    - 2

Combining
*********

As you can see from the examples, the different values can be combined in various ways.  The top-level items
in the yaml file are part of the main dictionary, so have to be key/value pairs.  Here are some examples of
what can be done.

.. code-block:: yaml

    simple_key: value
    array_of_dict:
      - key1: value1
        key2: 2
      - key1: value2
        key3: 1.2
    dict_of_dict:
      key1:
        level2: stuff
      key2:
        more: values
        here: again

Note that you can only have one type of value per key, so these examples are invalid:

.. code-block:: yaml

    array_of_dict: value  # can't have a simple value here with an array following
      - key1: value1
        key2: 2
      key1: value2  # dictionary key in the array
    dict_of_dict: "can't have something here"  # can't have a value with a dictionary following
      key1: this_is_bad  # same as here
        level2: stuff
      key2:
        more: values
        here: again

Other things
************

There are a few other YAML syntax features that won't be described here.  There are special commands you can
use that start with ``!``, for example ``!secret`` and ``!lambda`` that will be explained in separate sections
later.  There are also "includes" that are described in the configuration types guide and "anchors" that are
mentioned in the interlock section of GPIO switches.

Creating an ESPHome config
--------------------------

Now that you understand the basics of YAML, you can create an ESPHome config.  Each possible section is described
in detail in the documentation.  The first section you need is the `esphome </components/esphome.html>`__ section.
The most important parameter here is the ``name:`` which is how your device is identified.  You can add an optional
"friendly name" which will be shown in the dashboard and HA will add it to the name of each entity that your
config publishes.

.. code-block:: yaml

    esphome:
      name: tutorial
      friendly_name: Tutorial ESP  #optional

Next, you need to define the platform, that is which type of CPU you're making this firmware for.  The
current options are `ESP8266 </components/esp8266.html>`__, `ESP32 </components/esp32.html>`__ (which also
includes the ESP32S2, ESP32S3, ESP32C3, etc.), and `RP2040 </components/rp2040.html>`__.  More platforms will
likely be added over time.  In this section you need to specify which board you are using from the platformio
list.  See the documentation for each platform for more information.

.. code-block:: yaml

    esp8266:
      board: nodemcuv2

    esp32:
      board: esp32dev


WiFi
----

You most likely want this device to connect to your network, so you need to add the `WiFi </components/wifi.html>`__
section.  Here you can specify the SSID and password it needs to connect with.  It is possible to give it several
networks that it can try and it will connect to the first one it finds.  This and other advanced options can
be found in the docs.

.. code-block:: yaml

    wifi:
      ssid: MyHomeNetwork
      password: VerySafePassword

But wait!  What if you want to share your ESPHome config or ask for help?  You might not want to have your
SSID and password visible for everyone to see.  That's where "secrets" come in.

Secrets
-------

There's a special file called ``secrets.yaml`` that holds values that you don't want generally visible or
that you want to be able to share between config files.  Then you can change the value in one place and
all the configs that use it will automatically get the new value.  If you use the dashboard, this file
will be automatically created, but if you're using the cli method, you will need to create it yourself.
The content of the secrets file is a simple yaml key/value dictionary.

.. code-block:: yaml

    wifi_ssid: MyHomeNetwork
    wifi_password: VerySafePassword

And then your wifi block looks like this instead:

.. code-block:: yaml

    wifi:
      ssid: !secret wifi_ssid
      password: !secret wifi_password


Remote Access
-------------

If you can't contact the device to get its information or update the firmware, it won't be very useful.
The next sections you'll add are the `logger </components/logger.html>`__, which provides information on
what the devices is doing, the `api </components/api.html>`__, which allows you to view those logs and
lets HA connect to collect sensor values, and `ota </components/ota.html>`__, which lets you upload new
firmware OTA (Over The Air).  You can add passwords or encryption keys to these services, but that
isn't required.  See the docs for details.

.. code-block:: yaml

    logger:

    api:

    ota:

Sensors
-------

You now have a functional config that you could compile and upload to your device, but it doesn't
actually do anything other than connect to the wifi.  So let's add something.  For many sections, there
is the top-level general type and then a "platform" to specify what exactly you're using.  For example,
if you want to measure a voltage, you would use an ADC sensor, so the component "type" is ``sensor`` and the
"platform" is ``adc``.  First, let's add an `uptime </components/sensor/uptime.html>`__ sensor.  This
sensor tracks how long it has been since the device last rebooted.

.. code-block:: yaml

    sensor:
      platform: uptime
      name: Uptime

.. note::

   Components that can be published can have a ``name:`` or an ``id:`` or both.  If it doesn't have a
   name, then it is "internal" and won't get published to HA or the web server (by default).  You can
   also make it internal with the ``internal: true`` option.

Now, if you upload this config, HA will show a sensor called "Uptime" with a timer that will update every
60 seconds with the running time of this device.  But that form of the config is not the best.  What
happens if you want to add another sensor?  You can't add another ``sensor:`` block (you can't have
duplicate keys in a dictionary) and you can't just add another platform (again, duplicate keys), so
you need to make an array as described earlier in the YAML introduction.  Let's add an
`adc </components/sensor/adc.html>`__ sensor to the config.

.. code-block:: yaml

    sensor:
      - platform: uptime
        name: Uptime
      - platform: adc
        pin: A0
        name: Voltage

Almost all top-level components and sections let you add multiple items like this.

Switch
------

A `switch </#switch-components>`__ is something that has controllable on and off states.
Let's use the on-board LED, which is usually on GPIO2, to demonstrate.

.. code-block:: yaml

    switch:
      - platform: gpio
        name: LED
        pin: 2


This will give you a switch that you can click to toggle the LED on and off.  This component is
commonly used for controlling relays.

Light
_____

But you probably don't want an LED to look like a switch since it's a light.  So first, we nned
to create an `output </#output-components>`__.  An output is a component that can be set to a
value between 0 and 1.  There are binary outputs which are only 0 or 1, and there are float
outputs that can be any value from 0 to 1.  A `gpio output </components/output/gpio.html>`__
is binary, so we will use a `binary light </components/light/binary.html>`__ to control it.
Remove the ``switch`` config from above and add the following instead:

.. code-block:: yaml

    output:
      - platform: gpio
        id: led_output
        pin: 2

    light:
      - platform: binary
        name: LED
        output: led_output

Now you will have a light you can turn on and off.  This is also the first example of how
you can chain components using the ``id``.  An output doesn't have a name and doesn't
create an entity in HA.  It can only be used by other components.

On and off works, but what about changing the brightness.  For this, we use PWM.  Each platform
has it's own component for that.  For ESP8266, it's
`esp8266_pwm </components/output/esp8266_pwm.html>`__ and for ESP32, it's
`ledc </components/output/ledc.html>`__.  These components are float outputs, so now we'll
use the `monochromatic light </components/light/monochromatic.html>`__.  Replace the
``output`` and ``light`` with the following (use a different output platform if you're not
working with an ESP8266):

.. code-block:: yaml

    output:
      - platform: esp8266_pwm
        id: led_output
        pin: 2

    light:
      - platform: monochromatic
        name: LED
        output: led_output

Now you have a light that you can turn on and off as well as change the brightness.

Automation
----------

Now that you understand how basic esphome configuration works, the next step is
`automations </guides/automations.html>`__, doing actions based on various conditions.

