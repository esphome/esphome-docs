Template Number
===============

.. seo::
    :description: Instructions for setting up template numbers with ESPHome.
    :image: description.png

The ``template`` number platform allows you to create a number with templated values
using :ref:`lambdas <config-lambda>`.

.. code-block:: yaml

    # Example configuration entry
    number:
      - platform: template
        name: "Template number"
        update_interval: never

Configuration variables:
------------------------

- **name** (**Required**, string): The name of the number.
- **lambda** (*Optional*, :ref:`lambda <config-lambda>`):
  Lambda to be evaluated every update interval to get the new value of the number
- **update_interval** (*Optional*, :ref:`config-time`): The interval to check the
  number. Defaults to ``60s``.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Sensor <config-number>`.

``number.set`` Action
----------------------------------

You can also publish a state to a template number from elsewhere in your YAML file
with the :ref:`number-set_action`.

See Also
--------

- :ref:`automation`
- :apiref:`template/number/template_number.h`
- :ghedit:`Edit`
