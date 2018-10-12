Binary Light
============

The ``binary`` light platform creates a simple ON/OFF-only light from a
:ref:`binary output component <output>`.

.. figure:: images/binary-ui.png
    :align: center
    :width: 40.0%

.. code:: yaml

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

- :doc:`/esphomeyaml/components/output/index`
- :doc:`/esphomeyaml/components/light/index`
- :doc:`/esphomeyaml/components/output/gpio`
- :doc:`/esphomeyaml/components/power_supply`
- :doc:`API Reference </api/light/index>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/light/binary.rst>`__

.. disqus::
