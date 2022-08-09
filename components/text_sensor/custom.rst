Custom Text Sensor
==================

.. esphome:component-definition::
   :alias: custom
   :category: text-sensor-components
   :friendly_name: Custom Text Sensor
   :toc_group: Text Sensor Components
   :toc_image: language-cpp.svg

This integration can be used to create custom text sensors in ESPHome
using the C++ (Arduino) API.

Please first read :doc:`/components/sensor/custom` guide,
the same principles apply here and text sensors are very similar
to sensors internally.

The example below is an example of a custom text sensor which constantly publishes
the message "Hello World!".

.. code-block:: cpp

    #include "esphome.h"

    class MyCustomTextSensor : public PollingComponent, public TextSensor {
     public:
      // constructor
      MyCustomTextSensor() : PollingComponent(15000) {}

      void setup() override {
        // This will be called by App.setup()
      }
      void update() override {
        // This will be called every "update_interval" milliseconds.
        // Publish state
        publish_state("Hello World!");
      }
    };

(Store this file in your configuration directory, for example ``my_text_sensor.h``)

And in YAML:

.. code-block:: yaml

    # Example configuration entry
    esphome:
      includes:
        - my_text_sensor.h

    text_sensor:
    - platform: custom
      lambda: |-
        auto my_custom_sensor = new MyCustomTextSensor();
        App.register_component(my_custom_sensor);
        return {my_custom_sensor};

      text_sensors:
        name: "My Custom Text Sensor"

Configuration variables:

- **lambda** (**Required**, :ref:`lambda <config-lambda>`): The lambda to run for instantiating the
  text sensor(s).
- **text_sensors** (**Required**, list): A list of text sensors to initialize. The length here
  must equal the number of items in the ``return`` statement of the ``lambda``.

    - All options from :ref:`Text Sensor <config-text_sensor>`.

See Also
--------

- :doc:`/components/text_sensor/index`
- :apiclass:`API Reference <text_sensor::TextSensor>`
- :ghedit:`Edit`
