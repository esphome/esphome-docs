PipSolar PV Inverter
========================

.. seo::
    :description: Instructions for setting up PipSolar Compatible PV Inverter in ESPHome.
    :image: pipsolar.jpg

The PipSolar component allows you to integrate PIP-compatible Inverters in ESPHome. 
It uses :ref:`UART <uart>` for communication.

Once configured, you can use sensors, binary sensors, switches and outputs as described below for your projects.

.. warning::

    All functionality is working fine on esp8266 and esp32 chips. 
    If you configure a lot of the possible sensors etc. from below it could be that you run out of memory (on esp8266).
    If you configure more than one if this devices with nearly all sensors etc. you run in a stack-size issue. In this case you have to increase stack size.

.. figure:: images/pipsolar.jpg
    :align: center
    :width: 50.0%

    pip4048 compatible PV Inverter.

Overview
--------

You can connect a wide variety of PV Inverters as long as they provide a serial interface and talk the commands used (at least those you want to use).
A documentation about the communication protocol mostly supported can be found |here|_.

This component will poll the needed polling commands in a loop. If there is a command to send for controlling the inverter this command will be queued and fired as next after the current polling command ends.
There is a buffer to buffer up to 10 commands.

.. |here| replace:: ``here``
.. _here: https://github.com/jblance/mpp-solar/raw/master/docs/PI30_PIP-GK_MK-Protocol.pdf

.. code-block:: yaml

    # Example configuration entry
    uart:
      - id: uart_bus
        tx_pin: GPIO18
        rx_pin: GPIO19
        # most devices use 2400 as baud_rate
        baud_rate: 2400

    pipsolar:
      - uart_id: uart_bus
        id: inverter0

Configuration variables:
~~~~~~~~~~~~~~~~~~~~~~~~

- **id** (**Required**, :ref:`config-id`): The id to use for this pipsolar component.
- **uart_id** (*Optional*): The uart Bus ID

Sensors
--------
.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: pipsolar
        pipsolar_id: inverter0
        grid_rating_voltage:
          id: inverter0_grid_rating_voltage
          name: inverter0_grid_rating_voltage
        grid_rating_current:
          id: inverter0_grid_rating_current
          name: inverter0_grid_rating_current
        ac_output_apparent_power:
          id: inverter0_ac_output_apparent_power
          name: inverter0_ac_output_apparent_power
        ac_output_active_power:
          id: inverter0_ac_output_active_power
          name: inverter0_ac_output_active_power

Configuration variables:
~~~~~~~~~~~~~~~~~~~~~~~~

all sensors are normal sensors... so all sensor variables are working to.

- **uart_id** (*Optional*): The uart Bus ID

See Also
--------

- :ref:`uart`
- :ghedit:`Edit`
