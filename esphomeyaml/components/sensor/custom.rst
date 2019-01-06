Custom Sensor Component
=======================

.. seo::
    :description: Instructions for setting up Custom C++ sensors with esphomelib.
    :image: language-cpp.png
    :keywords: C++, Custom

.. warning::

    While I do try to keep the esphomeyaml configuration options as stable as possible
    and back-port them, the esphomelib API is less stable. If something in the APIs needs
    to be changed in order for something else to work, I will do so.

So, you just set up esphomelib for your ESP32/ESP8266, but sadly esphomelib is missing a sensor integration
you'd really like to have 😕. It's pretty much impossible to support every single sensor, as there are simply too many.
That's why esphomelib has a really simple API for you to create your own **custom sensors** 🎉

In this guide, we will go through creating a custom sensor component for the
`BMP180 <https://www.adafruit.com/product/1603>`__ pressure sensor (we will only do the pressure part,
temperature is more or less the same). During this guide, you will learn how to 1. define a custom sensor
esphomelib can use 2. go over how to register the sensor so that it will be shown inside Home Assistant and
3. leverage an existing arduino library for the BMP180 with esphomelib.

.. note::

    Since the creation of this guide, the BMP180 has been officially supported by the :doc:`BMP085 component
    <bmp085>`. The code still applies though.

This guide will require at least a bit of knowledge of C++, so be prepared for that. If you've already written
code for an Arduino, you have already written C++ code :) (Arduino uses a slightly customized version of C++).
If you have any problems, I'm here to help: https://discord.gg/KhAMKrd

Step 1: Custom Sensor Definition
--------------------------------

To create your own custom sensor, you just have to create your own C++ class. If you've never heard of that
before, don't worry, at the end of this guide you can just copy the example source code and modify it to your needs
- learning the intricacies of C++ classes won't be required.

Before you can create your own custom sensors, let's first take a look at the basics: How sensors (and components)
are structured in the esphomelib ecosystem.

In esphomelib, a **sensor** is some hardware device (like a BMP180) that periodically
sends out numbers, for example a temperature sensor that periodically publishes its temperature **state**.

Another important abstraction in esphomelib is the concept of a **component**. In esphomelib,
a **component** is an object with a *lifecycle* managed by the :cpp:class:`Application` class.
What does this mean? Well if you've coded in Arduino before you might know the two special methods
``setup()`` and ``loop()``. ``setup()`` is called one time when the node boots up and ``loop()`` is called
very often and this is where you can do things like read out sensors etc.

Components have something similar to that: They also have ``setup()`` and ``loop()`` methods which will be
called by the application kind of like the arduino functions.

So, let's now take a look at some code: This is an example of a custom component class (called ``MyCustomSensor`` here):

.. code-block:: cpp

    #include "esphomelib.h"

    using namespace esphomelib;

    class MyCustomSensor : public Component, public sensor::Sensor {
     public:
      void setup() override {
        // This will be called by App.setup()
      }
      void loop() override {
        // This will be called by App.loop()
      }
    };

In the first two lines, we're importing esphomelib so you can use the APIs and telling the compiler that
we want to use the esphomelib "namespace" (you don't need to know what this is now, it's basically just
there to have a clean, well-structured codebase).

Let's now also take a closer look at this line, which you might not be too used to when writing Arduino code:

.. code-block:: cpp

    class MyCustomSensor : public Component, public sensor::Sensor {

What this line is essentially saying is that we're defining our own class that's called ``MyCustomSensor``
which is also a subclass of :cpp:class:`Component` and :cpp:class:`sensor::Sensor`
(in the namespace ``sensor::``). As described before, these two "parent" classes have
special semantics that we will make use of.

We *could* go implement our own sensor code now by replacing the contents of ``setup()`` and ``loop()``.
In ``setup()`` we would initialize the sensor and in ``loop()`` we would read out the sensor and publish
the latest values.

However, there's a small problem with that approach: ``loop()`` gets called very often (about 60 times per second).
If we would publish a new state each time that method is called we would quickly make the node unresponsive
since the MQTT protocol wasn't really designed for 60 messages per second.

So this fix this, we will use an alternative class to :cpp:class:`Component`: :cpp:class`PollingComponent`.
This class is for situations where you have something that should get called repeatedly with some **update interval**.
In the code above, we can simply replace :cpp:class:`Component` by :cpp:class:`PollingComponent` and
``loop()`` by a special method ``update()`` which will be called with an interval we can specify.

.. code-block:: cpp

    class MyCustomSensor : public PollingComponent, public sensor::Sensor {
     public:
      // constructor
      MyCustomSensor() : PollingComponent(15000) {}

      void setup() override {
        // This will be called by App.setup()
      }
      void update() override {
        // This will be called every "update_interval" milliseconds.
      }
    };


Our code has slightly changed, as explained above we're now inheriting from :cpp:class:`PollingComponent` instead of
just :cpp:class:`Component`. Additionally, we now have a new line: the constructor. You also don't really need to
know much about constructors here, so to simplify let's just say this is where we "initialize" the custom sensor.

In this constructor we're telling the compiler that we want :cpp:class:`PollingComponent` to be instantiated with an
*update interval* of 15s, or 15000 milliseconds (esphomelib uses milliseconds internally).

Let's also now make our sensor actually publish values in the ``update()`` method:

.. code-block:: cpp

    // class MyCustomSensor ...
      // ... previous code
      void update() override {
        publish_state(42.0);
      }
    };

Every time ``update`` is called we will now **publish** a new value to the frontend.
The rest of esphomelib will then take care of processing this value and ultimately publishing it
to the outside world (for example using MQTT).

Step 2: Registering the custom sensor
-------------------------------------

Now we have our Custom Sensor set up, but unfortunately it doesn't do much right now.
Actually ... it does nothing because it's never included nor instantiated.
First, create a new file called ``my_custom_sensor.h`` in your configuration directory and copy the source code
from above into that file.

Then in the YAML config, *include* that file in the top-level ``esphomeyaml`` section like this:

.. code-block:: yaml

    esphomeyaml:
      # ... [Other options]
      includes:
        - my_custom_sensor.h

Next, create a new ``custom`` sensor platform entry like this:

.. code-block:: yaml

    # Example configuration entry
    sensor:
    - platform: custom
      lambda: |-
        auto my_sensor = new MyCustomSensor();
        App.register_component(my_sensor);
        return {my_sensor};

      sensors:
        name: "My Custom Sensor"

Let's break this down:

- First, we specify a :ref:`lambda <config-lambda>` that will be used to **instantiate** our sensor class. This will
  be called on boot to register our sensor in esphomelib.
- In this lambda, we're first creating a new instance of our custom class (``new MyCustomSensor()``) and then
  assigning it to a variable called ``my_sensor``. Note: This uses a feature in the C++ standard, ``auto``, to make our
  lives easier. We could also have written ``MyCustomSensor *my_sensor = new MyCustomSensor()``
- Next, as our custom class inherits from Component, we need to **register** it - otherwise esphomelib will not know
  about it and won't call our ``setup()`` and ``update`` methods!
- Finally, we ``return`` the custom sensor - don't worry about the curly braces ``{}``, we'll cover that later.
- After that, we just let *esphomeyaml* know about our newly created sensor too using the ``sensors:`` block. Additionally,
  here we're also assigning the sensor a name.

Now all that's left to do is upload the code and let it run :)

If you have Home Assistant MQTT discovery setup, it will even automatically show up in the frontend 🎉

.. figure:: images/custom-ui.png
    :align: center
    :width: 60%

Step 3: BMP180 support
----------------------

Let's finally make this custom sensor useful by adding the BMP180 aspect into it! Sure, printing ``42`` is a nice number
but it won't help with home automation :D

A great feature of esphomelib is that you don't need to code everything yourself. You can use any existing arduino
library to do the work for you! Now for this example we'll
use the `Adafruit BMP085 Library <https://platformio.org/lib/show/525/Adafruit%20BMP085%20Library>`__
library to implement support for the BMP085 sensor. But you can find other libraries too on the
`platformio library index <https://platformio.org/lib>`__

First we'll need to add the library to our project dependencies. To do so, put ``Adafruit BMP085 Library``
in your global ``libraries``:

.. code-block:: yaml

    esphomeyaml:
      includes:
        - my_custom_sensor.h
      libraries:
        - "Adafruit BMP085 Library"

Next, include the library at the top of your custom sensor file you created previously:

.. code-block:: cpp

    #include "esphomelib.h"
    #include "Adafruit_BMP085.h"

    using namespace esphomelib;

    // ...

Then update the sensor for BMP180 support:

.. code-block:: cpp

    // ...

    class MyCustomSensor : public PollingComponent, public sensor::Sensor {
     public:
      Adafruit_BMP085 bmp;

      MyCustomSensor() : PollingComponent(15000) { }

      void setup() override {
        bmp.begin();
      }

      void update() override {
        int pressure = bmp.readPressure(); // library returns value in in Pa, which equals 1/100 hPa
        publish_state(pressure / 100.0); // convert to hPa
      }
    };

    // ...

There's not too much going on there. First, we define the variable ``bmp`` of type ``Adafruit_BMP085``
inside our class as a class member. This is the object the adafruit library exposes and through which
we will communicate with the sensor.

In our custom ``setup()`` function we're *initializing* the library (using ``.begin()``) and in
``update()`` we're reading the pressure and publishing it using ``publish_state``.

For esphomeyaml we can use the previous YAML. So now if you upload the firmware, you'll see the sensor
reporting actual pressure values! Hooray 🎉!

Step 4: Additional Overrides
----------------------------

There's a slight problem with our code: It does print the values fine, **but** if you look in Home Assistant
you'll see a) the value has no **unit** attached to it and b) the value will be rounded to the next integer.
This is because esphomelib doesn't know these infos, it's only passed a floating point value after all.

We *could* fix that in our custom sensor class (by overriding the ``unit_of_measurement`` and ``accuracy_decimals``
methods), but here we have the full power of esphomeyaml, so let's use that:

.. code-block:: yaml

    # Example configuration entry
    sensor:
    - platform: custom
      lambda: |-
        auto my_sensor = new MyCustomSensor();
        App.register_component(my_sensor);
        return {my_sensor};

      sensors:
        name: "My Custom Sensor"
        unit_of_measurement: hPa
        accuracy_decimals: 2


Bonus: Sensors With Multiple Output Values
------------------------------------------

The ``Sensor`` class doesn't fit every use-case. Sometimes, (as with the BMP180),
a sensor can expose multiple values (temperature *and* pressure, for example).

Doing so in esphomelib is a bit more difficult. Basically, we will have to change our sensor
model to have a **component** that reads out the values and then multiple **sensors** that represent
the individual sensor measurements.

Let's look at what that could look like in code:

.. code-block:: cpp

    class MyCustomSensor : public PollingComponent {
     public:
      Adafruit_BMP085 bmp;
      sensor::Sensor *temperature_sensor = new sensor::Sensor();
      sensor::Sensor *pressure_sensor = new sensor::Sensor();

      MyCustomSensor() : PollingComponent(15000) { }

      void setup() override {
        bmp.begin();
      }

      void update() override {
        // This is the actual sensor reading logic.
        float temperature = bmp.readTemperature();
        temperature_sensor->publish_state(temperature);

        int pressure = bmp.readPressure();
        pressure_sensor->publish_state(pressure / 100.0);
      }
    };

The code here has changed a bit:

- Because the values are no longer published by our custom class, ``MyCustomSensor`` no longer inherits
  from ``Sensor``.
- The class has two new members: ``temperature_sensor`` and ``pressure_sensor``. These will be used to
  publish the values.
- In our ``update()`` method we're now reading out the temperature *and* pressure. These values are then
  published with the temperature and pressure sensor instances we declared before.


Our YAML configuration needs an update too:

.. code-block:: yaml

    # Example configuration entry
    sensor:
    - platform: custom
      lambda: |-
        auto my_sensor = new MyCustomSensor();
        App.register_component(my_sensor);
        return {my_sensor->temperature_sensor, my_sensor->pressure_sensor};

      sensors:
      - name: "My Custom Temperature Sensor"
        unit_of_measurement: °C
        accuracy_decimals: 1
      - name: "My Custom Pressure Sensor"
        unit_of_measurement: hPa
        accuracy_decimals: 2

In ``lambda`` the return statement has changed: Because we have *two* sensors now we must tell esphomeyaml
about both of them. We do this by returning them as an array of values in the curly braces.

``sensors:`` has also changed a bit: Now that we have multiple sensors, each of them needs an entry here.

Note that the number of arguments you put in the curly braces *must* match the number of sensors you define in the YAML
``sensors:`` block - *and* they must be in the same order.

Configuration variables:

- **lambda** (**Required**, :ref:`lambda <config-lambda>`): The lambda to run for instantiating the
  sensor(s).
- **sensors** (**Required**, list): A list of sensors to initialize. The length here
  must equal the number of items in the ``return`` statement of the ``lambda``.

  - All options from :ref:`Sensor <config-sensor>` and :ref:`MQTT Component <config-mqtt-component>`.

See Also
--------

- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/sensor/custom.rst>`__

.. disqus::
