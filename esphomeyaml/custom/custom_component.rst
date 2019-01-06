Generic Custom Component
========================

This integration can be used to create generic custom components in esphomelib
using the C++ (Arduino) API. This integration should be used in cases where
none of esphomelib's abstraction layers (for example the "sensor", "binary sensor",
"switch", etc concepts) work well for your integration.

Please first read :doc:`/esphomeyaml/components/sensor/custom` guide, the same principles apply here.

The example below is an example of a custom component that can do anything you want really.

.. code-block:: cpp

    #include "esphomelib.h"
    using namespace esphomelib;

    class MyCustomComponent : public Component {
     public:
      void setup() override {
        // This will be called once to set up the component
        // think of it as the setup() call in Arduino
        pinMode(5, INPUT);
        pinMode(6, OUTPUT);
      }
      void loop() override {
        // This will be called very often after setup time.
        // think of it as the loop() call in Arduino
        if (digitalRead(5)) {
          digitalWrite(6, HIGH);

          // You can also log messages
          ESP_LOGD("custom", "The GPIO pin 5 is HIGH!");
        }
      }
    };

In many cases however components should communicate with other appliances using the network.
That's why there is :cpp:class:`mqtt::CustomMQTTDevice`. It is a helper class to create
custom components that communicate using MQTT.

.. code-block:: cpp

    #include "esphomelib.h"
    using namespace esphomelib;

    class MyCustomComponent : public Component, public mqtt::CustomMQTTDevice {
     public:
      void setup() override {
        // This will be called once to set up the component
        // think of it as the setup() call in Arduino
        pinMode(6, OUTPUT);

        subscribe("the/topic", &MyCustomComponent::on_message);

        // also supports JSON messages
        subscribe_json("the/json/topic", &MyCustomComponent::on_json_message);
      }
      void on_message(const std::string &payload) {
        if (payload == "ON") {
          digitalWrite(6, HIGH);
          publish("the/other/topic", "Hello World!");
        } else {
          digitalWrite(6, LOW);
          publish("the/other/topic", 42);
        }
      }
      void on_json_message(JsonObject &root) {
        if (!root.containsKey("key"))
          return;

        int value = root["key"];
        // do something with Json Object

        // publish JSON using lambda syntax
        publish_json("the/other/json/topic", [=](JsonObject &root2) {
          root2["key"] = "Hello World";
        });
      }
    };

(Store this file in your configuration directory, for example ``my_custom_component.h``)

And in YAML:

.. code-block:: yaml

    # Example configuration entry
    esphomeyaml:
      includes:
        - my_custom_component.h

    custom_component:
    - lambda: |-
        auto my_custom = new MyCustomComponent();
        return {my_custom};

Configuration variables:

- **lambda** (**Required**, :ref:`lambda <config-lambda>`): The lambda to run for instantiating the
  binary sensor(s).

See :cpp:class:`Component` and :cpp:class:`mqtt::CustomMQTTDevice`.

See Also
--------

- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/custom/custom_component.rst>`__

.. disqus::
