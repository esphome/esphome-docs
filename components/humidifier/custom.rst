Custom Humidifier
=================

This integration can be used to create custom humidifier devices in ESPHome
using the C++ (Arduino) API.

Please first read :doc:`/components/sensor/custom` guide,
the same principles apply here.

The example below is an example of a custom humidifier device - all humidifier devices must override
two methods (:apiclass:`Humidifier <humidifier::Humidifier>`):

- ``traits``: This should return a :apiclass:`HumidifierTraits <humidifier::HumidifierTraits>` object
  representing the capabilities of the humidifier device.
- ``control``: This receives a :apiclass:`HumidifierCall <humidifier::HumidifierCall>` object that contains
  the command the user tried to set.

.. code-block:: cpp

    #include "esphome.h"

    class MyCustomHumidifier : public Component, public Humidifier {
     public:
      void setup() override {
        // This will be called by App.setup()
      }
      void control(const HumidifierCall &call) override {
        if (call.get_mode().has_value()) {
          // User requested mode change
          HumidifierMode mode = *call.get_mode();
          // Send mode to hardware
          // ...

          // Publish updated state
          this->mode = mode;
          this->publish_state();
        }
        if (call.get_target_humidity().has_value()) {
          // User requested target humidity change
          float humidity = *call.get_target_humidity();
          // Send target humidity to humidifier
          // ...
        }
      }
      HumidifierTraits traits() override {
        // The capabilities of the humidifier device
        auto traits = humidifier::HumidifierTraits();
        traits.set_supports_current_humidity(true);
        traits.set_supported_modes({humidifier::HUMIDIFIER_MODE_HUMIDIFY_DEHUMIDIFY});
        return traits;
      }
    };

(Store this file in your configuration directory, for example ``my_humidifier.h``)

And in YAML:

.. code-block:: yaml

    # Example configuration entry
    esphome:
      includes:
        - my_humidifier.h

    humidifier:
    - platform: custom
      lambda: |-
        auto my_custom_humidifier = new MyCustomHumidifier();
        App.register_component(my_custom_humidifier);
        return {my_custom_humidifier};

      humidifiers:
        - name: "My Custom Humidifier"

Configuration variables:

- **lambda** (**Required**, :ref:`lambda <config-lambda>`): The lambda to run for instantiating the
  humidifier(s).
- **humidifiers** (**Required**, list): A list of humidifiers to initialize. The length here
  must equal the number of items in the ``return`` statement of the ``lambda``.

  - All options from :ref:`Humidifier <config-humidifier>`.

See :apiclass:`Humidifier <humidifier::Humidifier>`

See Also
--------

- :ghedit:`Edit`
