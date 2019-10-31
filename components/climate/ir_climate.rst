IR Remote Climate
=================

.. seo::
    :description: Controls a variety of compatible Climate via IR
    :image: air-conditioner.png

The climate component allows you to control a variety of compatible AC units by sending IR signals
as your remote unit would do.

.. figure:: images/climate-ui.png
    :align: center
    :width: 60.0%

There is a growing list of compatible units. If your unit is not listed below you can fill a feature
request so it will be added.

+------------------------+---------------------+----------------------+
| Name                   | Platform name       |  Supports receiver   |
|                        |                     |                      +
+========================+=====================+======================+
| Coolix                 | ``coolix``          | yes                  |
+------------------------+---------------------+----------------------+
| Fujitsu General        | ``fujitsu_general`` |                      |
+------------------------+---------------------+----------------------+
| Mitsubishi             | ``mitsubishi``      |                      |
+------------------------+---------------------+----------------------+
| TCL112, Fuego          | ``tcl112``          | yes                  |
+------------------------+---------------------+----------------------+
| Yashima                | ``yashima``         |                      |
+------------------------+---------------------+----------------------+

This component requires that you have setup a :doc:`/components/remote_transmitter`.

Due to the unidirectional nature of IR remote controllers, this component cannot determine the
actual state of the device, and will assume the state of the device is the latest state requested.

However, when receiver is supported, you can optionally you can add a
:doc:`/components/remote_receiver` component so the climate state will be tracked when it is operated
with the original remote controller unit.

.. code-block:: yaml

    # Example configuration entry
    remote_transmitter:
      pin: GPIO32
      carrier_duty_percent: 50%

    climate:
      - platform: coolix #  change here the platform name for your AC model
        name: "Living Room AC"

Configuration variables:
------------------------

- **name** (**Required**, string): The name for the climate.
- **supports_cool** (*Optional*, boolean): Enables setting cool mode for this climate device. Defaults to ``True``.
- **supports_heat** (*Optional*, boolean): Enables setting heat mode for this climate device. Defaults to ``True``.
- **sensor** (*Optional*, :ref:`config-id`): The sensor that is used to measure the ambient
  temperature. This is only for reporting the current temperature in the frontend.
- **receiver_id** (*Optional*, :ref:`config-id`): The remote_receiver id, see: :ref:`coolix-receiver_id`.
- All other options from :ref:`Climate <config-climate>`.

Advanced options:

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **transmitter_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the remote transmitter.

.. _coolix-receiver_id:

Using a receiver
----------------

When using a receiver it is recommended to put the IR receiver as close as possible to the equipment's
IR receiver.

.. code-block:: yaml

    # Example configuration entry
    remote_receiver:
      id: rcvr
      pin:
        number: GPIO14
        inverted: True
        mode: INPUT_PULLUP
      tolerance: 55%  # high 55% tolerance is recommended for some remote control units

    climate:
      - platform: coolix
        name: "Living Room AC"
        receiver_id: rcvr

See Also
--------

- :doc:`/components/climate/index`
- :doc:`/components/remote_transmitter`
- :apiref:`coolix/coolix.h`
- :ghedit:`Edit`
