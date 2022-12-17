Kamstrup MULTICAL 40x
=====================

.. figure:: images/kamstrup_mc40x.jpg
    :scale: 75%

    Kamstrup MULTICAL 403 heat meter

The Kamstrup MULTICAL 40x is a meter used by some energy companies in 
The Netherlands to measure delivered heat by a district heating 
network (in Dutch: stadsverwarming). 

Heat is transported using warm water to the consumer. The meter measures
the temperature of the water delivered and returned as well as the water
flow. This is used to calculate the consumed energy, typically in giga 
joule (GJ).

The Kamstrup Multical has an optical interface just above the display.
This component can be used to request measurements from the meter using
this optical interface.

Configuration
-------------

.. code-block:: yaml

    # Example configuration entry
    uart:
      baud_rate: 1200
      stop_bits: 2
      tx_pin: GPIO15
      rx_pin: GPIO13

    sensor:
      - platform: kamstrup_mc40x
        heat_energy:
          name: 'Heat Energy'
        power:
          name: 'Heat Power'
        temp_diff:
          name: 'Heat Temperature Difference'
        flow:
          name: 'Heat Flow'
        update_interval: 60s

Configuration variables:

- **heat_energy** (*Optional*): Heat energy delivered.

  - **name** (**Required**, string): The name for the heat_energy sensor.
  - All other options from :ref:`Sensor <config-sensor>`.

- **power** (*Optional*): Current power delivered.

  - **name** (**Required**, string): The name for the power sensor.
  - All other options from :ref:`Sensor <config-sensor>`.

- **temp1** (*Optional*): Temperatue of sensor 1.

  - **name** (**Required**, string): The name for the temp1 sensor.
  - All other options from :ref:`Sensor <config-sensor>`.

- **temp2** (*Optional*): Temperatue of sensor 2.

  - **name** (**Required**, string): The name for the temp2 sensor.
  - All other options from :ref:`Sensor <config-sensor>`.

- **temp_diff** (*Optional*): Temperature difference between the 2 sensors.

  - **name** (**Required**, string): The name for the temp_diff sensor.
  - All other options from :ref:`Sensor <config-sensor>`.

- **flow** (*Optional*): Water flow.

  - **name** (**Required**, string): The name for the flow sensor.
  - All other options from :ref:`Sensor <config-sensor>`.

- **volume** (*Optional*): Volume.

  - **name** (**Required**, string): The name for the volume sensor.
  - All other options from :ref:`Sensor <config-sensor>`.

- **update_interval** (*Optional*): The polling interval.
  When not provided a default value of 60 seconds is used.

.. note:: 
  
    - The uart baudrate has to be set to 1200 baud and the stop bits to 2. 
      It is recommended to use pins associated with a hardware UART.
      For more information regarding uart configuration, refer to :ref:`UART <uart>`.
    - Only the provided sensors will appear as sensor, and only those are  read from 
      the meter.
    - Keep in mind that the meter is battery operated. The more sensors read and the 
      lower the update interval, the faster the battery will drain.

Hardware
--------

The Kamstrup meter uses an optical interface, just above the display. The required 
optical transceiver can be made using the schematic below. Connect the RX and TX 
lines to the pins configured under the uart section in the config file. In the 
configuration example above, this would be GPIO pin pin 13 and 15 respectively.

.. figure:: images/kamstrup_mc40x_sch.svg
    :scale: 200%

    Optical reader schematic

To safe energy, the optical interface of the Kamstrup meter is not active by default.
To activate the interface, press a button on the device. The interface will now be
available for a few minutes. To keep the interface alive, magnets must be placed 
around the LED / photo cell. The image below shows the arrangement. The green 
circles are the LED and photo diode, which must be places exactly on top of the 
optical interface window of the meter. The red circles indicate 6mm neodymium 
magnets.

.. figure:: images/kamstrup_mc40x_holder.svg

    Magnet arrangement
