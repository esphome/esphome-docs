Switch Component
================

The ``switch`` domain includes all platforms that should show up like a
switch and can only be turned ON or OFF.

.. _config-switch:

Base Switch Configuration
-------------------------

.. code:: yaml

    switch:
      - platform: ...
        name: "Switch Name"
        icon: "mdi:restart"

Configuration variables:

-  **name** (**Required**, string): The name of the switch.
-  **icon** (*Optional*, icon): Manually set the icon to use for the
   sensor in the frontend.
-  **inverted** (*Optional*, boolean): Whether to invert the binary
   state, i.e. report ON states as OFF and vice versa. Defaults
   to ``False``.
-  All other options from :ref:`MQTT Component <config-mqtt-component>`.

.. _switch-toggle_action:

``switch.toggle`` Action
^^^^^^^^^^^^^^^^^^^^^^^^

This action toggles a switch with the given ID when executed.

.. code:: yaml

    on_...:
      then:
        - switch.toggle:
            id: relay_1

.. _switch-turn_on_action:

``switch.turn_on`` Action
^^^^^^^^^^^^^^^^^^^^^^^^^

This action turns a switch with the given ID on when executed.

.. code:: yaml

    on_...:
      then:
        - switch.turn_on:
            id: relay_1

.. _switch-turn_off_action:

``switch.turn_off`` Action
^^^^^^^^^^^^^^^^^^^^^^^^^^

This action turns a switch with the given ID off when executed.

.. code:: yaml

    on_...:
      then:
        - switch.turn_off:
            id: relay_1

See Also
^^^^^^^^

- :doc:`API Reference </api/switch/index>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/master/esphomeyaml/components/switch/index.rst>`__

.. toctree::
    :maxdepth: 1

    gpio.rst
    shutdown.rst
    output.rst
    ir_transmitter.rst
    restart.rst
    template.rst
