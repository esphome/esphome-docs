EasyScale Light
=================

.. seo::
    :description: Instructions for setting up EasyScale brightness-only lights in ESPHome.
    :image: lightbulb.svg

The ``easyscale`` light platform creates a a simple brightness-only light using a supported Texas Instruments device.

.. note:: 
    
    Tested devices: TPS61165

.. code-block:: yaml

    # Example configuration entry
    light:
      - platform: easyscale
        name: "Desk Lamp"
        pin: 32

Configuration variables:
------------------------

- **name** (**Required**, string): The name of the light.
- **pin** (**Required**, :ref:`Pin Schema <config-pin_schema>`): The pin the Easyscale device is connected to.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- All other options from :ref:`Light <config-light>`.

See Also
--------

- :doc:`/components/light/index`
- :doc:`/components/power_supply`
- :apiref:`easyscale/easyscale.h`
- :ghedit:`Edit`
