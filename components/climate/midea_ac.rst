Midea Air Conditioner
=====================

.. seo::
    :description: Instructions for setting up a Midea climate device
    :image: air-conditioner.png

The ``midea_ac`` component creates a Midea air conditioner climate device.

This component requires a :doc:`/components/midea_dongle` to be configured.

.. note::

    This protocol also used by some vendors:

        - `Electrolux <https://www.electrolux.ru/>`_
        - `Qlima <https://www.qlima.com/>`_
        - `Artel <https://www.artelgroup.com/>`_
        - `Carrier <https://www.carrier.com/>`_
        - `Comfee <http://www.comfee-russia.ru/>`_
        - `Inventor <https://www.inventorairconditioner.com/>`_
        - and maybe others

    Example of hardware implementation is `Midea Open Dongle <https://github.com/dudanov/midea-open-dongle>`_ in free `KiCad <https://kicad-pcb.org>`_ format.

.. code-block:: yaml

    # Example configuration entry
    # Disable logging over UART
    logger:
      baud_rate: 0

    uart:
      tx_pin: 1
      rx_pin: 3
      baud_rate: 9600

    midea_dongle:

    midea_ac:
      name: "Midea AC"
      outdoor_temperature:
        name: "outdoor"
      beeper: true

Configuration variables:
------------------------

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **midea_dongle_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the :doc:`/components/midea_dongle` if you want to use multiple devices.
- **name** (**Required**, string): The name of the climate device.
- **outdoor_temperature** (*Optional*): The information for the outdoor temperature
  sensor.

  - **name** (**Required**, string): The name of the sensor.
  - **id** (*Optional*, :ref:`config-id`): Set the ID of this sensor for use in lambdas.
  - All other options from :ref:`Sensor <config-sensor>`.
- **beeper** (*Optional*, bool, default: **false**): Beeper feedback on command.
- All other options from :ref:`Climate <config-climate>`.

Acknowledgments:
----------------

Thanks to the following people for their contributions to reverse engineering the UART protocol and source code in the following repositories:

* `Mac Zhou <https://github.com/mac-zhou/midea-msmart>`_
* `NeoAcheron <https://github.com/NeoAcheron/midea-ac-py>`_
* `Rene Klootwijk <https://github.com/reneklootwijk/node-mideahvac>`_

See Also
--------

- :doc:`/components/midea_dongle`
- :doc:`/components/climate/index`
- :apiref:`climate/midea_ac.h`
- :ghedit:`Edit`
