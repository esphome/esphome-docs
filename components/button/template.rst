Template Button
===============

.. seo::
    :description: Instructions for setting up template buttons that can execute arbitrary actions when pressed.
    :image: description.svg

The ``template`` button platform allows you to create simple buttons out of just actions. Once defined,
it will automatically appear in Home Assistant as a button and can be controlled through the frontend.

.. code-block:: yaml

    # Example configuration entry
    button:
      - platform: template
        name: "Template Button"
        on_press:
          - logger.log: Button Pressed

Configuration variables:
------------------------

- **name** (**Required**, string): The name of the switch.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Button <config-button>`.

See Also
--------

- :doc:`/guides/automations`
- :doc:`/components/button/index`
- :ghedit:`Edit`
