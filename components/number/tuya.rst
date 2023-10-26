Tuya Number
===========

.. seo::
    :description: Instructions for setting up a Tuya device integer or enum datapoint..
    :image: upload.svg

The ``tuya`` number platform allows you to create a number that controls
a tuya serial component. This platform requires :doc:`/components/tuya` to be configured.

When :doc:`/components/tuya` has been properly configured, it will output a list of
valid data points to the log after start-up.

.. code-block:: text

    [21:37:14][C][tuya:028]: Tuya:
    [21:37:14][C][tuya:045]:   Datapoint 101: enum (value: 4)
    [21:37:14][C][tuya:045]:   Datapoint 102: enum (value: 1)
    [21:37:14][C][tuya:041]:   Datapoint 103: int value (value: 5)
    [21:37:14][C][tuya:039]:   Datapoint 104: switch (value: OFF)
    [21:37:14][C][tuya:041]:   Datapoint 105: int value (value: 229)
    [21:37:14][C][tuya:041]:   Datapoint 106: int value (value: 37)
    [21:37:14][C][tuya:041]:   Datapoint 107: int value (value: 10)
    [21:37:14][C][tuya:041]:   Datapoint 108: int value (value: 35)
    [21:37:14][C][tuya:041]:   Datapoint 109: int value (value: 30)
    [21:37:14][C][tuya:041]:   Datapoint 110: int value (value: 80)
    [21:37:14][C][tuya:039]:   Datapoint 112: switch (value: OFF)
    [21:37:14][C][tuya:039]:   Datapoint 113: switch (value: OFF)
    [21:37:14][C][tuya:039]:   Datapoint 114: switch (value: OFF)
    [21:37:14][C][tuya:045]:   Datapoint 115: enum (value: 4)
    [21:37:14][C][tuya:045]:   Datapoint 116: enum (value: 2)
    [21:37:14][C][tuya:055]:   Product: '{"p":"ymf4oruxqx0xlogp","v":"1.0.3","m":0}'

The example output above from a Tuya Siren with temperature and humidity sensors. The
``tuya`` number platform can be used to control all of the integer and enum datapoints.

On this device, datapoint 116 represents the volume control, with valid values being
0=High, 1=Medium, 2=Low.

Based on this, you can create a number as follows:

.. code-block:: yaml

    - platform: "tuya"
      name: "Volume"
      number_datapoint: 116
      min_value: 0
      max_value: 2
      step: 1

The value for ``multiply`` is used as the scaling factor for the Number. All numbers in Tuya are integers, so a scaling factor is sometimes needed to convert the Tuya reported value into floating point.

For instance, assume we have a pH sensor that reads from 0.00 to 15.00 with a scaling of 0.01. By setting ``multiply`` to 100, on the Tuya side (not visible to the user) the number will be reported as an integer from 0 to 1500. The following configuration could be used:

.. code-block:: yaml

    - platform: "tuya"
      name: "pH Sensor"
      number_datapoint: 106
      min_value: 0.00
      max_value: 15.00
      multiply: 100

Configuration variables:
------------------------

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **name** (**Required**, string): The name of the switch.
- **number_datapoint** (**Required**, int): The datapoint id number of the number.
- **min_value** (**Required**, float): The minimum value this number can be.
- **max_value** (**Required**, float): The maximum value this number can be.
- **step** (*Optional*, float): The granularity with which the number can be set. Defaults to 1.
- **multiply** (*Optional*, float): multiply the new value with this factor before sending the requests.

- All other options from :ref:`Number <config-number>`.

See Also
--------

- :doc:`/components/number/index`
- :apiref:`tuya/number/tuya_number.h`
- :ghedit:`Edit`
