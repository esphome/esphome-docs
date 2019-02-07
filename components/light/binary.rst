Binary Light
============

.. seo::
    :description: Instructions for setting up binary ON/OFF lights in esphomelib.
    :image: lightbulb.png

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
        output: output_component1

Configuration variables:
------------------------

- **name** (**Required**, string): The name of the light.
- **output** (**Required**, :ref:`config-id`): The id of the
  binary :ref:`output` to use for this light.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **effects** (*Optional*, list): A list of :ref:`light effects <light-effects>` to use for this light, though binary lights
  only support very few of them.
- All other options from :ref:`MQTT Component <config-mqtt-component>`.

See Also
--------

- :doc:`/components/output/index`
- :doc:`/components/light/index`
- :doc:`/components/output/gpio`
- :doc:`/components/power_supply`
- :apiref:`light/light_state.h`
- :ghedit:`Edit`

.. disqus::
