Custom Binary Sensor
====================

This integration can be used to create custom binary sensors in esphomelib
using the C++ (Arduino) API.

Please first read :doc:`/esphomeyaml/components/sensor/custom` guide,
the same principles apply here and binary sensors are very similar
to sensors internally.

The example below is an example of a custom binary sensor; this custom sensor is essentially the
same as the gpio binary sensor.

.. code-block:: cpp

    #include "esphomelib.h"
    using namespace esphomelib;

    class MyCustomBinarySensor : public PollingComponent, public binary_sensor::BinarySensor {
     public:
      // constructor
      MyCustomBinarySensor() : PollingComponent(15000) {}

      void setup() override {
        // This will be called by App.setup()
        pinMode(5, INPUT);
      }
      void update() override {
        // This will be called every "update_interval" milliseconds.

        // Publish an OFF state
        bool state = digitalRead(5)
        publish_state(state);
      }
    };

(Store this file in your configuration directory, for example ``my_binary_sensor.h``)

And in YAML:

.. code-block:: yaml

    # Example configuration entry
    esphomeyaml:
      includes:
        - my_binary_sensor.h

    binary_sensor:
    - platform: custom
      lambda: |-
        auto my_custom_sensor = new MyCustomBinarySensor();
        App.register_component(my_custom_sensor);
        return {my_custom_sensor};

      binary_sensors:
        name: "My Custom Binary Sensor"

Configuration variables:

- **lambda** (**Required**, :ref:`lambda <config-lambda>`): The lambda to run for instantiating the
  binary sensor(s).
- **binary_sensors** (**Required**, list): A list of binary sensors to initialize. The length here
  must equal the number of items in the ``return`` statement of the ``lambda``.

    - All options from :ref:`Binary Sensor <config-binary_sensor>` and :ref:`MQTT Component <config-mqtt-component>`.

See :cpp:class:`binary_sensor::BinarySensor`

See Also
--------

- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/binary_sensor/custom.rst>`__

.. disqus::
