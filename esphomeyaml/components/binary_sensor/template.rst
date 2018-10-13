Template Binary Sensor
======================

The ``template`` binary sensor platform allows you to define any :ref:`lambda template <config-lambda>`
and construct a binary sensor out if it.

For example, below configuration would turn the state of an ultrasonic sensor into
a binary sensor.

.. code:: yaml

    # Example configuration entry
    binary_sensor:
      - platform: template
        name: "Garage Door Open"
        lambda: >-
          if (isnan(id(ultrasonic_sensor1).value)) {
            // isnan checks if the ultrasonic sensor echo
            // has timed out, resulting in a NaN (not a number) state
            // in that case, return {} to indicate that we don't know.
            return {};
          } else if (id(ultrasonic_sensor1).value > 30) {
            // Garage Door is open.
            return true;
          } else {
            // Garage Door is closed.
            return false;
          }

Possible return values of the lambda:

 - ``return true;`` if the binary sensor should be ON.
 - ``return false;`` if the binary sensor should be OFF.
 - ``return {};`` if the last state should be repeated.

Configuration variables:
------------------------

-  **name** (**Required**, string): The name of the binary sensor.
-  **lambda** (**Required**, :ref:`lambda <config-lambda>`):
   Lambda to be evaluated repeatedly to get the current state of the binary sensor.
   Only state *changes* will be published to MQTT.
-  **id** (*Optional*,
   :ref:`config-id`): Manually specify
   the ID used for code generation.
-  All other options from :ref:`Binary Sensor <config-binary_sensor>`
   and :ref:`MQTT Component <config-mqtt-component>`.

See Also
--------

- :doc:`/esphomeyaml/components/binary_sensor/index`
- :doc:`/esphomeyaml/components/sensor/template`
- :ref:`automation`
- :doc:`API Reference </api/binary_sensor/template>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/binary_sensor/template.rst>`__

.. disqus::
