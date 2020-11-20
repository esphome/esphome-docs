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

+------------------------+---------------------+----------------------+------------------------------------+
| Name                   | Platform name       |  Supports receiver   |                                    |
|                        |                     |                      |                                    |
+========================+=====================+======================+====================================+
| Arduino-HeatpumpIR     | ``heatpumpir``      |                      | :ref:`more info<heatpumpir>`       |
+------------------------+---------------------+----------------------+------------------------------------+
| Coolix                 | ``coolix``          | yes                  |                                    |
+------------------------+---------------------+----------------------+------------------------------------+
| Daikin                 | ``daikin``          | yes                  |                                    |
+------------------------+---------------------+----------------------+------------------------------------+
| Fujitsu General        | ``fujitsu_general`` |                      |                                    |
+------------------------+---------------------+----------------------+------------------------------------+
| Mitsubishi             | ``mitsubishi``      |                      |                                    |
+------------------------+---------------------+----------------------+------------------------------------+
| TCL112, Fuego          | ``tcl112``          | yes                  |                                    |
+------------------------+---------------------+----------------------+------------------------------------+
| Toshiba                | ``toshiba``         | yes                  |                                    |
+------------------------+---------------------+----------------------+------------------------------------+
| Yashima                | ``yashima``         |                      |                                    |
+------------------------+---------------------+----------------------+------------------------------------+
| Whirlpool              | ``whirlpool``       | yes                  | :ref:`more info<model_whirlpool>`  |
+------------------------+---------------------+----------------------+------------------------------------+
| LG                     | ``climate_ir_lg``   | yes                  |                                    |
+------------------------+---------------------+----------------------+------------------------------------+
| Hitachi                | ``hitachi_ac344``   | yes                  |                                    |
+------------------------+---------------------+----------------------+------------------------------------+

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
- **supports_cool** (*Optional*, boolean): Enables setting cooling mode for this climate device. Defaults to ``True``.
- **supports_heat** (*Optional*, boolean): Enables setting heating mode for this climate device. Defaults to ``True``.
- **receiver_id** (*Optional*, :ref:`config-id`): The id of the remote_receiver if this platform supports
  receiver. see: :ref:`ir-receiver_id`.
- All other options from :ref:`Climate <config-climate>`.

Advanced options:

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **transmitter_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the remote transmitter.

.. _heatpumpir:

Arduino-HeatpumpIR
------------------

The ``heatpumpir`` platform supports dozens of manufacturers and hundreds of AC units by utilising the `Arduino-HeatpumpIR library <https://github.com/ToniA/arduino-heatpumpir>`__.

No support can be provided for Arduino-HeatpumpIR, because it is a third party library.

This platform utilises the library's generic one-size-fits-all API, which might not line up perfectly with all of the supported AC units. For example, some AC units have more fan speed options than what the generic API supports.

Additional configuration must be specified for this platform:

- **protocol** (*Required*, string): Choose one of Arduino-HeatpumpIR's supported protcols: ``aux``, ``ballu``, ``carrier_mca``, ``carrier_nqv``, ``daikin_arc417``, ``daikin_arc480``, ``daikin``, ``fuego``, ``fujitsu_awyz``, ``gree``, ``greeya``, ``greeyan``, ``hisense_aud``, ``hitachi``, ``hyundai``, ``ivt``, ``midea``, ``mitsubishi_fa``, ``mitsubishi_fd``, ``mitsubishi_fe``, ``mitsubishi_heavy_fdtc``, ``mitsubishi_heavy_zj``, ``mitsubishi_heavy_zm``, ``mitsubishi_heavy_zmp``, ``mitsubishi_heavy_kj``, ``mitsubishi_msc``, ``mitsubishi_msy``, ``mitsubishi_sez``, ``panasonic_ckp``, ``panasonic_dke``, ``panasonic_jke``, ``panasonic_lke``, ``panasonic_nke``, ``samsung_aqv``, ``samsung_fjm``, ``sharp``, ``toshiba_daiseikai``, ``toshiba``
- **horizontal_default** (*Required*, string): What to default to when the AC unit's horizontal direction is *not* set to swing. Options are: ``left``, ``mleft``, ``middle``, ``mright``, ``right``, ``auto``
- **vertical_default** (*Required*, string): What to default to when the AC unit's vertical direction is *not* set to swing. Options are: ``down``, ``mdown``, ``middle``, ``mup``, ``up``, ``auto``
- **max_temperature** (*Required*, float): The maximum temperature that the AC unit supports being set to.
- **min_temperature** (*Required*, float): The minimum temperature that the AC unit supports being set to.

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
      # high 55% tolerance is recommended for some remote control units
      tolerance: 55%

    climate:
      - platform: coolix
        name: "Living Room AC"
        receiver_id: rcvr

.. _model_whirlpool:

Whirlpool
---------

Additional configuration is available for this model

- **model** (*Optional*, string): There are two valid models

  * ``MODEL_DG11J1_3A``: Temperature range is from 18 to 32 (default)
  * ``MODEL_DG11J1_91``: Temperature range is from 16 to 30


See Also
--------

- :doc:`/components/climate/index`
- :doc:`/components/remote_transmitter`
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
