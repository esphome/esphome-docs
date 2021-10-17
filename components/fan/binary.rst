Binary Fan
==========

.. seo::
    :description: Instructions for setting up binary fans.
    :image: fan.png

The ``binary`` fan platform lets you represent any binary :ref:`output` as a fan.

.. figure:: images/fan-ui.png
    :align: center
    :width: 80.0%

.. code-block:: yaml

    # Example configuration entry
    fan:
      - platform: binary
        output: my_output_1
        name: "Living Room Fan"

Configuration variables:
------------------------

- **output** (**Required**, :ref:`config-id`): The id of the
  binary output component to use for this fan.
- **name** (**Required**, string): The name for this fan.
- **oscillation_output** (*Optional*, :ref:`config-id`): The id of the
  :ref:`output <output>` to use for the oscillation state of this fan. Default is empty.
- **direction_output** (*Optional*, :ref:`config-id`): The id of the
  :ref:`output <output>` to use for the direction state of the fan. Default is empty.
- **id** (*Optional*, :ref:`config-id`): Manually specify
  the ID used for code generation.
- All other options from :ref:`Fan Component <config-fan>`.

See Also
--------

- :doc:`/components/output/index`
- :doc:`/components/output/gpio`
- :doc:`/components/fan/index`
- :apiref:`fan/fan_state.h`
- :ghedit:`Edit`
