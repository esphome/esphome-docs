Custom Output
=============

This integration can be used to create custom binary and float :doc:`outputs </esphomeyaml/components/output/index>`
in esphomelib using the C++ (Arduino) API.

Please first read :doc:`/esphomeyaml/components/sensor/custom` guide, the same principles apply here.

The example below is an example of a custom float output; this custom output is essentially the
same as the :doc:`ESP8266 software PWM output </esphomeyaml/components/output/esp8266_pwm>`.

.. code-block:: cpp

    #include "esphomelib.h"
    using namespace esphomelib;

    class MyCustomFloatOutput : public Component, public output::FloatOutput {
     public:
      void setup() override {
        // This will be called by App.setup()
        pinMode(5, OUTPUT);
      }

      void write_state(float state) override {
        // state is the amount this output should be on, from 0.0 to 1.0
        // we need to convert it to an integer first
        int value = state * 1024;
        analogWrite(5, value);
      }
    };

    // Custom binary output, for exposing binary states
    class MyCustomBinaryOutput : public Component, public output::BinaryOutput {
     public:
      void setup() override {
        // This will be called by App.setup()
        pinMode(5, OUTPUT);
      }

      void write_state(bool state) override {
        digitalWrite(5, state);
      }
    };

(Store this file in your configuration directory, for example ``my_output.h``)

And in YAML:

.. code-block:: yaml

    # Example configuration entry
    esphomeyaml:
      includes:
        - my_output.h

    output:
    - platform: custom
      type: float
      lambda: |-
        auto my_custom_float_output = new MyCustomFloatOutput();
        App.register_component(my_custom_float_output);
        return {my_custom_float_output};

      outputs:
        id: custom_float

    - platform: custom
      type: binary
      lambda: |-
        auto my_custom_binary_output = new MyCustomBinaryOutput();
        App.register_component(my_custom_binary_output);
        return {my_custom_binary_output};

      outputs:
        id: custom_binary

Configuration variables:

- **type** (**Required**, string): The type of output. One of ``binary`` and ``float``.
- **lambda** (**Required**, :ref:`lambda <config-lambda>`): The lambda to run for instantiating the
  output(s).
- **outputs** (**Required**, list): A list of outputs to initialize. The length here
  must equal the number of items in the ``return`` statement of the ``lambda``.

    - All options from :ref:`Output <config-output>`.

See :cpp:class:`output::BinaryOutput` and :cpp:class`output::FloatOutput`.

See Also
--------

- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/output/custom.rst>`__

.. disqus::
