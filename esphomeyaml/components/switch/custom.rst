Custom Switch
=============

This integration can be used to create custom switches in esphomelib
using the C++ (Arduino) API.

Please first read :doc:`/esphomeyaml/components/sensor/custom` guide,
the same principles apply here.

The example below is an example of a custom switch; this custom switch is essentially the
same as the gpio switch implementation.

.. code-block:: cpp

    #include "esphomelib.h"
    using namespace esphomelib;

    // namespace is called 'switch_' because 'switch' is a reserved keyword
    class MyCustomSwitch : public Component, public switch_::Switch {
     public:
      void setup() override {
        // This will be called by App.setup()
        pinMode(5, INPUT);
      }
      void write_state(bool state) override {
        // This will be called every time the user requests a state change.

        digitalWrite(5, state);

        // Acknowledge new state by publishing it
        publish_state(state);
      }
    };

(Store this file in your configuration directory, for example ``my_switch.h``)

And in YAML:

.. code-block:: yaml

    # Example configuration entry
    esphomeyaml:
      includes:
        - my_switch.h

    switch:
    - platform: custom
      lambda: |-
        auto my_custom_switch = new MyCustomSwitch();
        App.register_component(my_custom_switch);
        return {my_custom_switch};

      switches:
        name: "My Custom Switches"

Configuration variables:

- **lambda** (**Required**, :ref:`lambda <config-lambda>`): The lambda to run for instantiating the
  switch(es).
- **switches** (**Required**, list): A list of switches to initialize. The length here
  must equal the number of items in the ``return`` statement of the ``lambda``.

  - All options from :ref:`Switch <config-switch>` and :ref:`MQTT Component <config-mqtt-component>`.

See :cpp:class:`switch_::Switch`

See Also
--------

- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/switch/custom.rst>`__

.. disqus::
