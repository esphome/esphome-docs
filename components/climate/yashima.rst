Yashima Remote Climate
======================

.. seo::
    :description: Controls a Yashima compatible Climate via IR
    :image: air-conditioner.png

The ``yashima`` climate platform allows you to control a Yashima compatible AC unit by sending IR signals
as your remote unit would do.

This component requires that you have setup a :doc:`/components/remote_transmitter`.

Due to the unidirectional nature of IR remote controllers, this component cannot determine the
actual state of the device, and will assume the state of the device is the latest state requested.

.. figure:: images/climate-ui.png
    :align: center
    :width: 60.0%

.. code-block:: yaml

    # Example configuration entry
    remote_transmitter:
      pin: GPIO32
      carrier_duty_percent: 50%

    climate:
      - platform: yashima
        name: "Living Room AC"

Configuration variables:
------------------------

- **name** (**Required**, string): The name for the climate.
- **supports_cool** (*Optional*, boolean): Enables setting cool mode for this climate device. Defaults to ``True``.
- **supports_heat** (*Optional*, boolean): Enables setting cool heat for this climate device. Defaults to ``True``.
- **sensor** (*Optional*, :ref:`config-id`): The sensor that is used to measure the ambient
  temperature. This is only for reporting the current temperature in the frontend.
- All other options from :ref:`Climate <config-climate>`.

Advanced options:

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **transmitter_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the remote transmitter.

See Also
--------

- :doc:`/components/climate/index`
- :doc:`/components/remote_transmitter`
- :apiref:`yashima/yashima.h`
- :ghedit:`Edit`
