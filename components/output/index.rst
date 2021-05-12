.. _output:

Output Component
================

.. seo::
    :description: Instructions for setting up generic outputs in ESPHome
    :image: folder-open.png

Each platform of the ``output`` domain exposes some output to
ESPHome. These are grouped into two categories: ``binary`` outputs
(that can only be ON/OFF) and ``float`` outputs (like PWM, can output
any rational value between 0 and 1).

.. _config-output:

Base Output Configuration
-------------------------

Each output platform extends this configuration schema.

.. code-block:: yaml

    # Example configuration entry
    output:
      - platform: ...
        id: my_output_id
        power_supply: power_supply_id
        inverted: False
        min_power: 0.01
        max_power: 0.75

Configuration variables:

- **id** (**Required**, :ref:`config-id`): The id to use for this output component.
- **power_supply** (*Optional*, :ref:`config-id`): The :doc:`power
  supply </components/power_supply>` to connect to
  this output. When the output is enabled, the power supply will
  automatically be switched on too.
- **inverted** (*Optional*, boolean): If the output should be treated
  as inverted. Defaults to ``False``.

Float outputs only:

- **min_power** (*Optional*, float): Sets the minimum output value of this output platform.
  Must be in range from 0 to max_power. Defaults to ``0``.
- **max_power** (*Optional*, float): Sets the maximum output value of this output platform.
  Must be in range from min_power to 1. Defaults to ``1``.


.. _output-turn_on_action:

``output.turn_on`` Action
*************************

This action turns the output with the given ID on when executed.

.. code-block:: yaml

    on_...:
      then:
        - output.turn_on: relay_1

.. note::

    This action can also be expressed in :ref:`lambdas <config-lambda>`:

    .. code-block:: cpp

        id(relay_1).turn_on();

.. _output-turn_off_action:

``output.turn_off`` Action
**************************

This action turns the output with the given ID off when executed.

.. code-block:: yaml

    on_...:
      then:
        - output.turn_off: relay_1

.. note::

    This action can also be expressed in :ref:`lambdas <config-lambda>`:

    .. code-block:: cpp

        id(relay_1).turn_off();

.. _output-set_level_action:

``output.set_level`` Action
***************************

This action sets the float output to the given level when executed. Note: This only
works with floating point outputs like ESP8266 PWM or LEDC.

.. code-block:: yaml

    on_...:
      then:
        - output.set_level:
            id: output_1
            level: 50%

.. note::

    This action can also be expressed in :ref:`lambdas <config-lambda>`:

    .. code-block:: cpp

        // range is 0.0 (off) to 1.0 (on)
        id(relay_1).set_level(0.5);

Full Output Index
-----------------

- :doc:`/components/switch/output`
- :doc:`/components/power_supply`
- :doc:`/components/light/binary`
- :doc:`/components/light/monochromatic`
- :doc:`/components/light/rgb`
- :doc:`/components/fan/binary`
- :doc:`/components/fan/speed`
- :apiref:`binary_output.h <output/binary_output.h>`,
  :apiref:`float_output.h <output/float_output.h>`
- :ghedit:`Edit`

.. toctree::
    :maxdepth: 1
    :glob:

    *
