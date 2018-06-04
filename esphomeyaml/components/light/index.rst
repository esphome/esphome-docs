Light Component
===============

The ``light`` domain in esphomeyaml lets you create lights that will
automatically be shown in Home Assistant’s frontend and have many
features such as RGB colors, transitions, flashing and effects.

.. _light-toggle_action:

``light.toggle`` Action
^^^^^^^^^^^^^^^^^^^^^^^

This action toggles a light with the given ID when executed.

.. code:: yaml

    on_...:
      then:
        - light.toggle:
            id: light_1

Configuration options:

- **id** (**Required**, :ref:`config-id`): The ID of the light.
- **transition_length** (*Optional*, :ref:`config-time`, :ref:`templatable <config-templatable>`): The length of the transition
  if the light supports it.

.. _light-turn_on_action:

``light.turn_on`` Action
^^^^^^^^^^^^^^^^^^^^^^^^

This action turns a light with the given ID on when executed.

.. code:: yaml

    on_...:
      then:
        - light.turn_on:
            id: light_1
            brightness: 100%
            red: 100%
            green: 100%
            blue: 1.0

        # Templated
        - light.turn_on:
            id: light_1
            brightness: !lambda >-
              // output value must be in range 0 - 1.0
              return id(some_sensor).value / 100.0;

Configuration options:

- **id** (**Required**, :ref:`config-id`): The ID of the light.
- **transition_length** (*Optional*, :ref:`config-time`, :ref:`templatable <config-templatable>`): The length of the transition
  if the light supports it.
- **brightness** (*Optional*, percentage, :ref:`templatable <config-templatable>`): The brightness of the light. Must be in range
  ``0%`` to ``100%`` or ``0.0`` to ``1.0``. Defaults to not changing brightness.
- **red** (*Optional*, percentage, :ref:`templatable <config-templatable>`): The red channel of the light. Must be in range
  ``0%`` to ``100%`` or ``0.0`` to ``1.0``. Defaults to not changing red.
- **green** (*Optional*, percentage, :ref:`templatable <config-templatable>`): The green channel of the light. Must be in range
  ``0%`` to ``100%`` or ``0.0`` to ``1.0``. Defaults to not changing green channel.
- **blue** (*Optional*, percentage, :ref:`templatable <config-templatable>`): The blue channel of the light. Must be in range
  ``0%`` to ``100%`` or ``0.0`` to ``1.0``. Defaults to not changing blue channel.
- **white** (*Optional*, percentage, :ref:`templatable <config-templatable>`): The white channel value of RGBW lights. Must be in range
  ``0%`` to ``100%`` or ``0.0`` to ``1.0``. Defaults to not changing white value.
- **flash_length** (*Optional*, :ref:`config-time`, :ref:`templatable <config-templatable>`): If set, will flash the given color
  for this period of time and then go back to the previous state.
- **effect** (*Optional*, string, :ref:`templatable <config-templatable>`): If set, will attempt to
  start an effect with the given name.

.. _light-turn_off_action:

``light.turn_off`` Action
^^^^^^^^^^^^^^^^^^^^^^^^^

This action turns a light with the given ID off when executed.

.. code:: yaml

    on_...:
      then:
        - light.turn_off:
            id: light_1

Configuration options:

- **id** (**Required**, :ref:`config-id`): The ID of the light.
- **transition_length** (*Optional*, :ref:`config-time`, :ref:`templatable <config-templatable>`): The length of the transition
  if the light supports it.

This action turns a switch with the given ID off when executed.

See Also
^^^^^^^^

- :doc:`API Reference </api/light/index>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/light/index.rst>`__

.. toctree::
    :maxdepth: 1

    binary.rst
    monochromatic.rst
    rgb.rst
    rgbw.rst
    fastled_clockless.rst
    fastled_spi.rst
