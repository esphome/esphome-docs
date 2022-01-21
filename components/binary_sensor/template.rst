Template Binary Sensor
======================

.. seo::
    :description: Instructions for setting up template binary sensors.
    :image: description.svg

The ``template`` binary sensor platform allows you to define any :ref:`lambda template <config-lambda>`
and construct a binary sensor out if it. The lambda will run continuously; it isn't possible to specify
an interval at which the lambda runs.

For example, below configuration would turn the state of an ultrasonic sensor into
a binary sensor.

.. code-block:: yaml

    # Example configuration entry
    binary_sensor:
      - platform: template
        name: "Garage Door Open"
        lambda: |-
          if (id(ultrasonic_sensor1).state > 30) {
            // Garage Door is open.
            return true;
          } else {
            // Garage Door is closed.
            return false;
          }

Possible return values of the lambda:

 - ``return true;`` if the binary sensor should be ON.
 - ``return false;`` if the binary sensor should be OFF.
 - ``return {};`` if the state is not known (use last known state)

Configuration variables:
------------------------

-  **name** (**Required**, string): The name of the binary sensor.
-  **lambda** (*Optional*, :ref:`lambda <config-lambda>`):
   Lambda to be evaluated repeatedly to get the current state of the binary sensor.
-  **id** (*Optional*,
   :ref:`config-id`): Manually specify
   the ID used for code generation.
-  All other options from :ref:`Binary Sensor <config-binary_sensor>`.

.. _binary_sensor-template-publish_action:

``binary_sensor.template.publish`` Action
-----------------------------------------

You can also publish a state to a template binary sensor from elsewhere in your YAML file
with the ``binary_sensor.template.publish`` action.

.. code-block:: yaml

    # Example configuration entry
    binary_sensor:
      - platform: template
        name: "Garage Door Open"
        id: template_bin

    # in some trigger
    on_...:
      - binary_sensor.template.publish:
          id: template_bin
          state: ON

      # Templated
      - binary_sensor.template.publish:
          id: template_bin
          state: !lambda 'return id(some_sensor).state > 30;'

Configuration options:

- **id** (**Required**, :ref:`config-id`): The ID of the template binary sensor.
- **state** (**Required**, boolean, :ref:`templatable <config-templatable>`):
  The state to publish.

.. note::

    This action can also be written in lambdas:

    .. code-block:: cpp

        id(template_bin).publish_state(true);

See Also
--------

- :doc:`/components/binary_sensor/index`
- :doc:`/components/sensor/template`
- :ref:`automation`
- :apiref:`template/binary_sensor/template_binary_sensor.h`
- :ghedit:`Edit`
