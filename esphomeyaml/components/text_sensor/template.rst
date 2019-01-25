Template Text Sensor
====================

.. seo::
    :description: Instructions for setting up template text sensors in esphomelib
    :image: description.png

The ``template`` text sensor platform allows you to create a text sensor with templated values
using :ref:`lambdas <config-lambda>`.

.. code-block:: yaml

    # Example configuration entry
    text_sensor:
      - platform: template
        name: "Template Text Sensor"
        lambda: |-
          return {"Hello World"};
        update_interval: 60s


Possible return values for the lambda:

 - ``return {"STRING LITERAL"};`` the new value for the sensor of type ``std::string``. **Has to be** in
   brackets ``{}``!
 - ``return {};`` if you don't want to publish a new state (advanced).

Configuration variables:
------------------------

- **name** (**Required**, string): The name of the text sensor.
- **lambda** (*Optional*, :ref:`lambda <config-lambda>`):
  Lambda to be evaluated every update interval to get the new value of the text sensor
- **update_interval** (*Optional*, :ref:`config-time`): The interval to check the
  text sensor. Defaults to ``60s``.
- **id** (*Optional*,:ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Text Sensor <config-text_sensor>` and :ref:`MQTT Component <config-mqtt-component>`.

See Also
--------

- :ref:`automation`
- :doc:`API Reference </api/text_sensor/template>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/text_sensor/template.rst>`__

.. disqus::
