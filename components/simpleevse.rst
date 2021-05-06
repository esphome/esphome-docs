SimpleEVSE
==========

.. seo::
    :description: Instructions for setting up SimpleEVSE component in ESPHome.

SimplEVSE is a popular DIY EV charger solution which can be connected to ESPHome using the :ref:`UART bus <uart>`.

.. _simpleevse-label:

SimplEVSE Component
-------------------

The SimplEVSE must be connected to an UART of the ESPHome and switched to modbus mode (`manual <http://evracing.cz/evse/evse-wallbox/evse-wb-din_20210202.pdf>`__).

+----------------------------+---------+
| Pin SimpleEVSE PROG (5pin) | ESPHome |
+----------------------------+---------+
| 4 TX                       | rx_pin  |
+----------------------------+---------+
| 5 RX                       | tx_pin  |
+----------------------------+---------+

.. warning::

    The SimplEVSE seems to provide a 5V level uart while the ESPHome is working with 3.3V. A level shifter is therefore strongly recommended.


.. code-block:: yaml

    # Example config.yaml
    uart:
      baud_rate: 9600
      rx_pin: GPIO16
      tx_pin: GPIO17

    simpleevse:
      web_config: enable

    sensor:
      - platform: simpleevse
        connected:
          name: "Connected"
        set_charge_current:
          name: "Set Charge Current"
        actual_charge_current:
          name: "Actual Charge Current"
        vehicle_state:
          name: "Vehicle State"
        max_current_limit:
          name: "Max. Current Limit"
        firmware_revision:
          name: "Firmware Revision"
        evse_state:
          name: "EVSE State"

    switch:
      - platform: simpleevse
        name: "Charge Enable"

Simpleevse Configuration Variables:
***********************************
- **update_interval** (*Optional*, :ref:`config-time`): The interval to poll the status. Defaults to 5s.
- **uart_id** (*Optional*, :ref:`config-id`): Manually specifiy which uart to use.
- **web_config** (*Optional*, bool): Determines if the web configuration should be enabled. Defaults to disable. The page can opened at the url path `/simpleevse`.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **on_unplugged** (*Optional*, :ref:`Automation <automation>`): An automation to perform if a vehicle was unplugged.
- **on_plugged** (*Optional*, :ref:`Automation <automation>`): An automation to perform if a vehicle was plugged in.

Sensor Configuration Variables:
*******************************
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **simpleevse_id** (*Optiona*, :ref:`config-id`): Manually specifiy which simpleevse to use. 
- **connected** (*Optional*): All options from :ref:`Binary Sensor <config-binary_sensor>`.
- **set_charge_current** (*Optional*): All options from :ref:`Sensor <config-sensor>`.
- **actual_charge_current** (*Optional*): All options from :ref:`Sensor <config-sensor>`.
- **max_current_limit** (*Optional*): All options from :ref:`Sensor <config-sensor>`.
- **firmware_revision** (*Optional*): All options from :ref:`Sensor <config-sensor>`.
- **vehicle_state** (*Optional*): All options from :ref:`Text Sensor <config-text_sensor>`.
- **evse_state** (*Optional*): All options from :ref:`Text Sensor <config-text_sensor>`.

Switch Configuration Variables:
*******************************
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **simpleevse_id** (*Optiona*, :ref:`config-id`): Manually specifiy which simpleevse to use. 
- All other options from :ref:`Switch <config-switch>`.

``is_plugged`` / ``is_unplugged`` Conditions
--------------------------------------------

This :ref:`Condition <config-condition>` checks if a vehicle is plugged in or not.

.. code-block:: yaml

    # In some trigger:
    on_...:
      if:
        condition:
          # Same syntax for is_unplugged
          simpleevse.is_plugged

``simplevse.set_charging_current`` Action
-----------------------------------------

Sets the charging current to the given value.

.. code-block:: yaml

    on_...:
      then:
        - simpleevse.set_charge_current:
            current: 16

Configuration options:

- **current** (**Required**, int): The new charging current. 


``simplevse.set_charging_enabled`` Action
-----------------------------------------

Enables or disables charging.

.. code-block:: yaml

    on_...:
      then:
        - simpleevse.set_charging_enabled:
            enable: true

Configuration options:

- **enable** (**Required**, bool): Enables (``true``) or disables charging (``false``).

Advanced Usages
---------------

Home Assistant service integration
**********************************

To adjust the charging current within Home Assistant, the ``simpleevse_set_charging_current`` action can be provided to HA as service:

.. code-block:: yaml

    api:
      services:
        - service: simpleevse_current
          variables:
            new_current: int
          then:
            - if:
                condition:
                  switch.is_off: charge_override
                then:
                  - simplevse.set_charging_current:
                      current: !lambda 'return new_current;'

Disable charging as soon as the vehicle is unplugged
****************************************************

The following configuration disables charging if the vehicle was unplugged. It must be enabled again manually (for example using the switch).

.. code-block:: yaml

    simpleevse:
      on_unplugged:
        - simplevse.set_charging_enabled: 
            enable: false


See Also
--------

- :ref:`uart`
- :apiref:`API Reference (SimpleEVSE) <simpleevse/simpleevse.h>`
- :ghedit:`Edit`
