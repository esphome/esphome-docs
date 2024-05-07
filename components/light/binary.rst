Binary Light
============

.. seo::
    :description: Instructions for setting up binary ON/OFF lights in ESPHome.
    :image: lightbulb.svg

The ``binary`` light platform creates a simple ON/OFF-only light from a
:ref:`binary output component <output>`.

.. figure:: images/binary-ui.png
    :align: center
    :width: 40.0%

.. code-block:: yaml

    # Example configuration entry
    light:
      - platform: binary
        name: "Desk Lamp"
        output: light_output


Configuration variables:
------------------------

- **name** (**Required**, string): The name of the light.
- **output** (**Required**, :ref:`config-id`): The id of the
  binary :ref:`output` to use for this light.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **effects** (*Optional*, list): A list of :ref:`light effects <light-effects>` to use for this light, though binary lights
  only support very few of them.
- All other options from :ref:`Light <config-light>`.

See Also
--------

- :doc:`/components/output/index`
- :doc:`/components/light/index`
- :doc:`/components/output/gpio`
- :doc:`/components/power_supply`
- :apiref:`binary/light/binary_light_output.h`
- :ghedit:`Edit`
