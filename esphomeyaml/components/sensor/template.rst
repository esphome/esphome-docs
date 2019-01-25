Template Sensor
===============

.. seo::
    :description: Instructions for setting up template sensors with esphomelib.
    :image: description.png

The ``template`` sensor platform allows you to create a sensor with templated values
using :ref:`lambdas <config-lambda>`.

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: template
        name: "Template Sensor"
        lambda: |-
          if (id(some_binary_sensor).state) {
            return 42.0;
          } else {
            return 0.0;
          }
        update_interval: 60s


Possible return values for the lambda:

 - ``return <FLOATING_POINT_NUMBER>;`` the new value for the sensor.
 - ``return NAN;`` if the state should be considered invalid to indicate an error (advanced).
 - ``return {};`` if you don't want to publish a new state (advanced).

Configuration variables:
------------------------

- **name** (**Required**, string): The name of the sensor.
- **lambda** (*Optional*, :ref:`lambda <config-lambda>`):
  Lambda to be evaluated every update interval to get the new value of the sensor
- **update_interval** (*Optional*, :ref:`config-time`): The interval to check the
  sensor. Defaults to ``60s``.
- **id** (*Optional*,:ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Sensor <config-sensor>` and :ref:`MQTT Component <config-mqtt-component>`.

.. note::

    You can use the ``publish_state()`` method to set the value of a template
    sensor from other automations:

    .. code-block:: cpp

        id(my_sensor).publish_state(42.0);

See Also
--------

- :ref:`sensor-filters`
- :ref:`automation`
- :doc:`API Reference </api/sensor/template>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/sensor/template.rst>`__

.. disqus::
