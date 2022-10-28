VBUS Component
==============

.. seo::
    :description: Instructions for integrating a solar energy collector controller using VBUS protocol in ESPHome.
    :image: resol_deltasol_bs_plus.jpg
    :keywords: VBUS RESOL SOLAR

The ``VBUS`` Component provides status reading connectivity to solar heat energy collector controllers using VBUS 
protocol. These devices are mainly produced by Resol, often also found under different brand names like Viessmann, 
Kioto, Wagner etc. The component currently supports natively Resol Deltasol C, DeltaSol CS2 and DeltaSol BS Plus 
but any device can be added via lambda by knowing `its packet structure <https://danielwippermann.github.io/resol-vbus>`__. 

.. figure:: images/resol_deltasol_bs_plus.jpg
    :align: center

The device must be connected via a :doc:`UART bus </components/uart>` supporting the receiving line only. The UART bus 
must be configured at the same speed of the module which is by default 9600bps. The controller outputs data every second. 

.. warning::

    If you are using the :doc:`logger` make sure you are not using the same pins for it or otherwise disable the UART 
    logging with the ``baud_rate: 0`` option.

To connect to this and read data from the bus a level shifting is needed as the voltage is around 8V (direct connection
would damage the MCU). Although this is a symmetric connection supporting long wires, for our read-only purposes it's 
enough to adapt the level appropriately to 3.3V using a circuit like below:

.. figure:: images/resol_vbus_adapter_schematic.png
    :align: center

Another approach, with PCB design ready to be manufactured `can be found here <https://github.com/FatBeard/vbus-arduino-library/tree/master/pcb>`__.

.. note::

    Do not connect the GND pin of your module with the ground of Resol unit as that may damage the output port of it. 
    The output of the device is symmetric, meaning that the signal is not referenced to the ground, but rather it's a 
    differential signal between the two wires. However, the MCU references the signal against the ground, so the two
    grounds are not supposed to be connected to each other as can be seen in the circuit depicted above.


Component
---------

.. code-block:: yaml

    # Example configuration entry
    uart:
      id: resol
      rx_pin: GPIO3
      baud_rate: 9600

    vbus:
      uart_id: resol

    logger:
      baud_rate: 0 # disable uart logger on ESP8266

Configuration variables:

- **uart_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the UART hub used to connect to the device.

.. note::

    Functionality of the sensors are depending on the type of the device and the the scheme arrangement of the hydraulic 
    system it controls. Please check the user manual and assess your arrangement to determine the functionality of each 
    sensor. 


Sensor
------

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: vbus
        model: deltasol_bs_plus
        temperature_1:
          name: Temperature 1
        temperature_2:
          name: Temperature 2
        temperature_3:
          name: Temperature 3
        temperature_4:
          name: Temperature 4
        pump_speed_1:
          name: Pump Speed 1
        pump_speed_2:
          name: Pump Speed 2
        operating_hours_1:
          name: Operating Hours 1
        operating_hours_2:
          name: Operating Hours 2
        heat_quantity:
          name: Heat Quantity

Configuration variables:

- **model** (*Mandatory*): Specify the model of the connected controller. Currently supported models are: ``deltasol_bs_plus``, ``deltasol_c``, ``deltasol_cs2``, ``custom``.  


Supported sensors:

- for **deltasol_bs_plus**: ``temperature_1``,  ``temperature_2``, ``temperature_3``, ``temperature_4``, ``pump_speed_1``, ``pump_speed_2``, ``operating_hours_1``, ``operating_hours_2``, ``heat_quantity``.  
- for **deltasol_c**: ``temperature_1``,  ``temperature_2``, ``temperature_3``, ``temperature_4``, ``pump_speed_1``, ``pump_speed_2``, ``operating_hours_1``, ``operating_hours_2``, ``heat_quantity``.  
- for **deltasol_cs2**: ``temperature_1``,  ``temperature_2``, ``temperature_3``, ``temperature_4``, ``temperature_5``, ``pump_speed``, ``operating_hours``, ``heat_quantity``.  


All sensors are *Optional* and support all other options from :ref:`Sensor <config-sensor>`.


Binary Sensor
-------------

.. code-block:: yaml

    binary_sensor:
      - platform: vbus
        model: deltasol_bs_plus
        relay_1:
          name: Pump
        relay_2:
          name: 3-way Valve

Configuration variables:

- **model** (*Mandatory*): Specify the model of the connected controller. Currently supported models are: ``deltasol_bs_plus``, ``deltasol_c``, ``deltasol_cs2``, ``custom``.

Supported sensors:

- for **deltasol_bs_plus**: ``relay_1``,  ``relay_2``, ``a``, ``b``, ````, ``c``,  ``d``, ``e``, ``f``, ``g``.  
- for **deltasol_c**: ``a``, ``b``, ````, ``c``,  ``d``, ``e``, ``f``, ``g``.  
- for **deltasol_cs2**: ``a``, ``b``, ````, ``c``,  ``d``, ``e``, ``f``, ``g``.  


All sensors are *Optional* and support all other options from :ref:`Binary Sensor <config-binary_sensor>`.


Lambda definition for ``custom`` VBUS sensor
--------------------------------------------

Devices on a VBUS bus are identified with a source address. There can be multiple devices on the same bus, 
each device type has a different address. The address code can be identified from the 
`protocol description <https://danielwippermann.github.io/resol-vbus>`__. To decode some of the sensors 
of DeltaSol BS Plus follow the example below:

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: vbus
        model: custom
        command: 0x100
        source: 0x1234
        dest: 0x10
        lambda: |-
          // the data is in `x`
        temperature_1:
          name: Temperature 1

    binary_sensor:
      - platform: vbus
        model: custom
        command: 0x100
        source: 0x1234
        dest: 0x10
        lambda: |-
          // the data is in `x`
        relay_1:
          name: Pump

See Also
--------

- :doc:`/components/uart`
- `VBUS protocol <https://danielwippermann.github.io/resol-vbus>`
- `Resol manuals <https://www.resol.de/en/dokumente>`
- :ghedit:`Edit`
