Switch Component
================

.. seo::
    :description: Instructions for setting up generic switches in esphomelib.
    :image: folder-open.png

The ``switch`` domain includes all platforms that should show up like a
switch and can only be turned ON or OFF.

.. _config-switch:

Base Switch Configuration
-------------------------

.. code-block:: yaml

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
************************

This action toggles a switch with the given ID when executed.

.. code-block:: yaml

    on_...:
      then:
        - switch.toggle: relay_1

.. _switch-turn_on_action:

``switch.turn_on`` Action
*************************

This action turns a switch with the given ID on when executed.

.. code-block:: yaml

    on_...:
      then:
        - switch.turn_on: relay_1

.. _switch-turn_off_action:

``switch.turn_off`` Action
**************************

This action turns a switch with the given ID off when executed.

.. code-block:: yaml

    on_...:
      then:
        - switch.turn_off: relay_1

.. _switch-is_on_condition:
.. _switch-is_off_condition:

``switch.is_on`` / ``switch.is_off`` Condition
**********************************************

This :ref:`Condition <config-condition>` checks if the given switch is ON (or OFF).

.. code-block:: yaml

    # In some trigger:
    on_...:
      if:
        condition:
          # Same syntax for is_off
          switch.is_on: my_switch

lambda calls
************

From :ref:`lambdas <config-lambda>`, you can call several methods on all covers to do some
advanced stuff (see the full :doc:`API Reference </api/cover/index>` for more info).

- ``publish_state()``: Manually cause the switch to publish a new state and store it internally.
  If it's different from the last internal state, it's additionally published to the frontend.

  .. code-block:: yaml

      // Within lambda, make the switch report a specific state
      id(my_switch).publish_state(false);
      id(my_switch).publish_state(true);

- ``state``: Retrieve the current state of the switch.

  .. code-block:: yaml

      // Within lambda, get the switch state and conditionally do something
      if (id(my_switch).state) {
        // Switch is ON, do something here
      } else {
        // Switch is OFF, do something else here
      }

- ``turn_off()``/``turn_on``: Manually turn the switch ON/OFF from code.
  Similar to the ``switch.turn_on`` and ``switch.turn_off`` actions,
  but can be used in complex lambda expressions.

  .. code-block:: yaml

      id(my_switch).turn_off();
      id(my_switch).turn_on(true);
      // Toggle the switch
      id(my_switch).toggle();

.. _switch-is_on_off_condition:

``switch.is_on`` / ``switch.is_off Condition
********************************************

This :ref:`condition <config-condition>` passes if the given switch is on/off.

.. code-block:: yaml

    # in a trigger:
    on_...:
      if:
        condition:
          switch.is_on: my_switch
          # same goes for is_off
        then:
        - script.execute: my_script

See Also
--------

- :doc:`API Reference </api/switch/index>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/switch/index.rst>`__

.. toctree::
    :maxdepth: 1
    :glob:

    *

.. disqus::
