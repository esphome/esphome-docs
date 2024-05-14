Uponor Smatrix Base Pulse Underfloor Heating
============================================

.. seo::
    :description: Instructions for setting up an Uponor Smatrix Base Pulse underfloor heating control system in ESPHome.
    :keywords: Uponor Smatrix, HCS, Thermostat

The Uponor Smatrix component allows you to integrate an Uponor Smatrix Base Pulse underfloor heating control system in ESPHome without the need for an Smatrix Pulse Com R-208 communication module.
It directly communicates with the controller and thermostats via the RS485 thermostat bus.

Connecting to the bus
---------------------

This component is able to communicate directly with the RS485 thermostat bus. For that, you will need to connect an RS485 to TTL converter to a UART bus of your ESPHome device.

The RS485 side of the converter can either be connected to one of the A/B terminals on the controller or on one of the thermostats.
The +/- terminals provide 5 volts and can be used to power your ESPHome device.

The :ref:`UART Component <uart>` must be configured with a baud rate of 19200, 8 data bits, no parity, 1 stop bit.

.. _uponor-gettingstarted:

Getting started
---------------

The controller and the thermostats have unique addresses used for communication that are not displayed anywhere but can only be found when scanning the bus.
Start with a basic configuration that just contains the UART and Uponor hub components. Make sure that the UART pins are configured according to your wiring and the baud rate is set to 19200.

.. code-block:: yaml

    uponor_smatrix:

When you upload this configuration to your ESPHome device and connect it to the Uponor Smatrix bus, it will print a list of detected addresses to the log output.

.. code-block:: text

    [00:00:00][C][uponor_smatrix:019]: Uponor Smatrix
    [00:00:00][C][uponor_smatrix:020]:   System address: 0x110B
    [00:00:00][C][uponor_smatrix:031]:   Detected unknown device addresses:
    [00:00:00][C][uponor_smatrix:033]:     0xDE62
    [00:00:00][C][uponor_smatrix:033]:     0xDDFF
    [00:00:00][C][uponor_smatrix:033]:     0xDE72
    [00:00:00][C][uponor_smatrix:033]:     0xDE4A
    [00:00:00][C][uponor_smatrix:033]:     0xDE13

With that you can then add ``climate`` or ``sensor`` components for the detected devices. Optionally, you can also statically add the detected system address to your ``uponor_smatrix`` configuration.

.. code-block:: yaml

    uponor_smatrix:
      address: 0x110B
  
    climate:
      - platform: uponor_smatrix
        address: 0xDE13
        name: Thermostat Living Room


Controller/Hub component
------------------------

The main ``uponor_smatrix`` component is responsible for the communication with the controller and thermostats and distributes data to the climate and sensor components described below.

It is also able to synchronize the date and time of the thermostats with a time source in case your system has thermostats that can be programmed with a time schedule.

.. code-block:: yaml

    uponor_smatrix:
      address: 0x110B
      uart_id: my_uart
      time_id: my_time

Configuration variables:
~~~~~~~~~~~~~~~~~~~~~~~~

- **address** (*Optional*, int): The 16 bit system/controller address. This will be automatically detected from the bus if not specified. See :ref:`uponor-gettingstarted` on how to find the address.
- **uart_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the :ref:`UART Component <uart>` if you want to use multiple UART buses.
- **time_id** (*Optional*, :ref:`config-id`): Specify the ID of the :doc:`Time Component <time/index>` to use as the time source if you want ESPHome to automatically synchronize the date and time of the thermostats.
- **time_device_address** (*Optional*, int): The 16 bit device address of the thermostat that keeps the system time. This will be automatically detected from the bus if not specified.
  It needs to be the device address of the first thermostat that was paired to the controller, and the one where you can manually change the date and time via the buttons on the thermostat.

.. note::

    The system address and the address of the thermostat keeping the time will be automatically detected from the bus if not specified in the configuration!
    You can safely leave out those parameters in almost all cases.

Climate component
------------------

.. code-block:: yaml

    climate:
      - platform: uponor_smatrix
        address: 0xDE13
        name: Thermostat Living Room

Configuration variables:
~~~~~~~~~~~~~~~~~~~~~~~~

- **address** (*Required*, int): The 16 bit device address of the thermostat. See :ref:`uponor-gettingstarted` on how to find the address.
- **uponor_smatrix_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the ``uponor_smatrix`` hub component if you want to use multiple hub components on one ESPHome device.
- All options from :ref:`Climate <config-climate>`.

Sensor component
----------------

.. code-block:: yaml

    sensor:
      - platform: uponor_smatrix
        address: 0xDE13
        humidity:
          name: Humidity Living Room
        temperature:
          name: Temperature Living Room
        external_temperature:
          name: Floor Temperature Living Room

Configuration variables:
~~~~~~~~~~~~~~~~~~~~~~~~

- **address** (*Required*, int): The 16 bit device address of the thermostat. See :ref:`uponor-gettingstarted` on how to find the address.
- **uponor_smatrix_id** (*Optional*, :ref:`config-id`): Manually specify the ID of the ``uponor_smatrix`` hub component if you want to use multiple hub components on one ESPHome device.
- **humidity** (*Optional*): A sensor reading the current humidity the thermostat reports.
  All options from :ref:`Sensor <config-sensor>`.
- **temperature** (*Optional*): A sensor reading the current temperature the thermostat reports.
  All options from :ref:`Sensor <config-sensor>`.
- **external_temperature** (*Optional*): A sensor reading the current external temperature the thermostat reports.
  This comes from an optionally attached external temperature sensor that can measure the floor or outdoor temperature.
  All options from :ref:`Sensor <config-sensor>`.


See Also
--------

- `Protocol Analysis <https://github.com/kroimon/uponor-smatrix-analysis>`__
- :apiref:`uponor_smatrix/uponor_smatrix.h`
- :ghedit:`Edit`
