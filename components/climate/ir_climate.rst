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

+---------------------------------------+---------------------+----------------------+
| Name                                  | Platform name       |  Supports receiver   |
|                                       |                     |                      |
+=======================================+=====================+======================+
| Ballu                                 | ``ballu``           | yes                  |
+---------------------------------------+---------------------+----------------------+
| Coolix                                | ``coolix``          | yes                  |
+---------------------------------------+---------------------+----------------------+
| Daikin                                | ``daikin``          | yes                  |
+---------------------------------------+---------------------+----------------------+
| Fujitsu General                       | ``fujitsu_general`` | yes                  |
+---------------------------------------+---------------------+----------------------+
| Mitsubishi                            | ``mitsubishi``      |                      |
+---------------------------------------+---------------------+----------------------+
| TCL112, Fuego                         | ``tcl112``          | yes                  |
+---------------------------------------+---------------------+----------------------+
| Toshiba                               | ``toshiba``         | yes                  |
+---------------------------------------+---------------------+----------------------+
| Yashima                               | ``yashima``         |                      |
+---------------------------------------+---------------------+----------------------+
| :ref:`Whirlpool<climate_ir_whirlpool>`| ``whirlpool``       | yes                  |
+---------------------------------------+---------------------+----------------------+
| :ref:`LG<climate_ir_lg>`              | ``climate_ir_lg``   | yes                  |
+---------------------------------------+---------------------+----------------------+
| Hitachi                               | ``hitachi_ac344,    | yes                  |
|                                       |   hitachi_ac424``   |                      |
+---------------------------------------+---------------------+----------------------+

This component requires that you have setup a :doc:`/components/remote_transmitter`.

Due to the unidirectional nature of IR remote controllers, this component cannot determine the
actual state of the device, and will assume the state of the device is the latest state requested.

However, when receiver is supported, you can optionally add a :doc:`/components/remote_receiver`
component so the climate state will be tracked when it is operated with the original remote
controller unit.

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
- **supports_cool** (*Optional*, boolean): Enables setting cooling mode for this climate device. Defaults to ``true``.
- **supports_heat** (*Optional*, boolean): Enables setting heating mode for this climate device. Defaults to ``true``.
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
        inverted: true
        mode: INPUT_PULLUP
      # high 55% tolerance is recommended for some remote control units
      tolerance: 55%

    climate:
      - platform: coolix
        name: "Living Room AC"
        receiver_id: rcvr

.. _climate_ir_whirlpool:

``whirlpool`` Climate
---------------------

Additional configuration is available for this model


Configuration variables:

- **model** (*Optional*, string): There are two valid models

 -* ``DG11J1-3A``: Temperature range is from 18 to 32 (default)
 -* ``DG11J1-91``: Temperature range is from 16 to 30


.. _climate_ir_lg:

``climate_ir_lg`` Climate
-------------------------

Additional configuration is available for this platform


Configuration variables:

- **header_high** (*Optional*, :ref:`config-time`): time for the high part of the header for the LG protocol. Defaults to ``8000us``
- **header_low** (*Optional*, :ref:`config-time`): time for the low part of the header for the LG protocol. Defaults to ``4000us``
- **bit_high** (*Optional*, :ref:`config-time`): time for the high part of any bit in the LG protocol. Defaults to ``600us``
- **bit_one_low** (*Optional*, :ref:`config-time`): time for the low part of a '1' bit in the LG protocol. Defaults to ``1600us``
- **bit_zero_low** (*Optional*, :ref:`config-time`): time for the low part of a '0' bit in the LG protocol. Defaults to ``550us``

.. code-block:: yaml

    # Example configuration entry
    climate:
      - platform: climate_ir_lg
        name: "AC"
        sensor: room_temperature
        header_high: 3265us # AC Units from LG in Brazil, for example use these timings
        header_low: 9856us

See Also
--------

- :doc:`/components/climate/index`
- :doc:`/components/remote_transmitter`
- :apiref:`ballu.h <ballu/ballu.h>`,
- :apiref:`coolix.h <coolix/coolix.h>`,
  :apiref:`daikin.h <daikin/daikin.h>`
  :apiref:`fujitsu_general.h <fujitsu_general/fujitsu_general.h>`,
  :apiref:`hitachi_ac344.h <hitachi_ac344/hitachi_ac344.h>`,
  :apiref:`mitsubishi.h <mitsubishi/mitsubishi.h>`,
  :apiref:`tcl112.h <tcl112/tcl112.h>`,
  :apiref:`yashima.h <yashima/yashima.h>`
  :apiref:`whirlpool.h <whirlpool/whirlpool.h>`
  :apiref:`climate_ir_lg.h <climate_ir_lg/climate_ir_lg.h>`
- :ghedit:`Edit`
