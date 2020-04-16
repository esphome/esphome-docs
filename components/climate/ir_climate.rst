IR Remote Climate
=================

.. seo::
    :description: Controls a variety of compatible Climate via IR
    :image: air-conditioner-ir.png

The climate component allows you to control a variety of compatible AC units by sending IR signals
as your remote unit would do.

.. figure:: images/climate-ui.png
    :align: center
    :width: 60.0%

There is a growing list of compatible units. If your unit is not listed below you can fill a feature
request so it will be added (see FAQ).

+------------------------+---------------------+----------------------+
| Name                   | Platform name       |  Supports receiver   |
|                        |                     |                      +
+========================+=====================+======================+
| Coolix                 | ``coolix``          | yes                  |
+------------------------+---------------------+----------------------+
| Daikin                 | ``daikin``          | yes                  |
+------------------------+---------------------+----------------------+
| Fujitsu General        | ``fujitsu_general`` | no                   |
+------------------------+---------------------+----------------------+
| Mitsubishi             | ``mitsubishi``      | no                   |
+------------------------+---------------------+----------------------+
| TCL112, Fuego          | ``tcl112``          | yes                  |
+------------------------+---------------------+----------------------+
| Yashima                | ``yashima``         | no                   |
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
      - platform: coolix       # adjust to match your AC unit!
        name: "Living Room AC"

Configuration variables:
------------------------

- **name** (**Required**, string): The name for the climate device.
- **sensor** (*Optional*, :ref:`config-id`): The sensor that is used to measure the ambient
  temperature. This is only for reporting the current temperature in the frontend.
- **supports_cool** (*Optional*, boolean): Enables setting cooling mode for this climate device. Defaults to ``True``.
- **supports_heat** (*Optional*, boolean): Enables setting heating mode for this climate device. Defaults to ``True``.
- **receiver_id** (*Optional*, :ref:`config-id`): The id of the remote_receiver if this platform supports
  receiver. see: :ref:`ir-receiver_id`.
- All other options from :ref:`Climate <config-climate>`.

Advanced options:

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **transmitter_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the remote transmitter.

.. _ir-receiver_id:

Using a Receiver
----------------

.. note::

    This is only supported with select climate devices, see "Supports receiver" in the table at the top of the page.

Optionally, some platforms can listen to data the climate device sends over infrared to update their state (
for example what mode the device is in). By setting up a :doc:`remote_receiver </components/remote_receiver>`
and passing its ID to the climate platform you can enable this mode.

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
- :apiref:`coolix.h <coolix/coolix.h>`,
  :apiref:`daikin.h <daikin/daikin.h>`
  :apiref:`fujitsu_general.h <fujitsu_general/fujitsu_general.h>`,
  :apiref:`mitsubishi.h <mitsubishi/mitsubishi.h>`,
  :apiref:`tcl112.h <tcl112/tcl112.h>`,
  :apiref:`yashima.h <yashima/yashima.h>`
- :ghedit:`Edit`
