Custom Climate
==============

.. esphome:component-definition::
   :alias: custom
   :category: climate-components
   :friendly_name: Custom Climate Component
   :toc_group: Climate Components
   :toc_image: language-cpp.svg

This integration can be used to create custom climate devices in ESPHome
using the C++ (Arduino) API.

Please first read :doc:`/components/sensor/custom` guide,
the same principles apply here.

The example below is an example of a custom climate device - all climate devices must override
two methods (:apiclass:`Climate <climate::Climate>`):

- ``traits``: This should return a :apiclass:`ClimateTraits <climate::ClimateTraits>` object
  representing the capabilities of the climate device.
- ``control``: This receives a :apiclass:`ClimateCall <climate::ClimateCall>` object that contains
  the command the user tried to set.

.. code-block:: cpp

    #include "esphome.h"

    class MyCustomClimate : public Component, public Climate {
     public:
      void setup() override {
        // This will be called by App.setup()
      }
      void control(const ClimateCall &call) override {
        if (call.get_mode().has_value()) {
          // User requested mode change
          ClimateMode mode = *call.get_mode();
          // Send mode to hardware
          // ...

          // Publish updated state
          this->mode = mode;
          this->publish_state();
        }
        if (call.get_target_temperature().has_value()) {
          // User requested target temperature change
          float temp = *call.get_target_temperature();
          // Send target temp to climate
          // ...
        }
      }
      ClimateTraits traits() override {
        // The capabilities of the climate device
        auto traits = climate::ClimateTraits();
        traits.set_supports_current_temperature(true);
        traits.set_supported_modes({climate::CLIMATE_MODE_HEAT_COOL});
        return traits;
      }
    };

(Store this file in your configuration directory, for example ``my_climate.h``)

And in YAML:

.. code-block:: yaml

    # Example configuration entry
    esphome:
      includes:
        - my_climate.h

    climate:
    - platform: custom
      lambda: |-
        auto my_custom_climate = new MyCustomClimate();
        App.register_component(my_custom_climate);
        return {my_custom_climate};

      climates:
        - name: "My Custom Climate"

Configuration variables:

- **lambda** (**Required**, :ref:`lambda <config-lambda>`): The lambda to run for instantiating the
  climate(s).
- **climates** (**Required**, list): A list of climates to initialize. The length here
  must equal the number of items in the ``return`` statement of the ``lambda``.

  - All options from :ref:`Climate <config-climate>`.

See :apiclass:`Climate <climate::Climate>`

See Also
--------

- :ghedit:`Edit`
