Binary Sensor Map
=================

.. seo::
    :description: Instructions for setting up a Binary Sensor Map
    :image: binary_sensor_map.png

The ``binary_sensor_map`` sensor platform allows you to map your ``binary_sensors`` as ``channels`` into a ``binary_sensor_map``.
This sensor is mostly used for touch devices but could be used for any ``binary_sensor`` that publishes its ``ON`` or ``OFF`` state.

Add your ``binary_sensors`` as ``channels`` to the ``binary_sensor_map``. The ``binary_sensor_map`` then publishes a value depending
 on the type of the ``binary_sensor_map`` and the values specified with each channel.

This platform will support three sensor types, which you need to specify using the ``type:`` configuration
value:

- ``GROUP`` Each channel has its own value. The sensor publishes the average value for all active binary_sensors.
- ``SLIDER`` This type is not implemented yet.
- ``WHEEL`` This type is not implemented yet.

.. code-block:: yaml

    # Example configuration entry
    mpr121:
      id: mpr121_first
      address: 0x5A

	binary_sensor:
	  - platform: mpr121
	    channel: 0
	    id: touchkey0
	  - platform: mpr121
	    channel: 1
	    id: touchkey1
	  - platform: mpr121
	    channel: 2
	    id: touchkey2
	  - platform: mpr121
	    channel: 3
	    id: touchkey3

	sensor:
	  - platform: binary_sensor_map
	    id: group_0
	    name: 'Group Map 0'
	    type: GROUP
	    channels:
	      - channel: touchkey0
	        value: 0
	      - channel: touchkey1
	        value: 10
	      - channel: touchkey2
	        value: 20
	      - channel: touchkey3
	        value: 30

Configuration variables:
------------------------

- **name** (**Required**, string): The name for the binary sensor.
- **type** (**Optional**, string): The sensor type. Should be one of: ``GROUP``, ``SLIDER``, ``WHEEL``. defaults to ``GROUP``
- **channels** (**Required**): A list of channels that are mapped to certain values.
  - **channel** (**Required**): The id of the ``binary_sensor`` to add as a channel for this sensor.
  - **value** (**Optional**): The value this channel shoul report when its binary_sensor is active. This option is only used for the ``GROUP`` type sensor.
- All other options from :ref:`Binary Sensor <config-binary_sensor>`.


See Also
--------

- :doc:`/components/binary_sensor/mpr121`
- :ref:`sensor-filters`
- :apiref:`sensor/binary_sensor_map.h`
- :ghedit:`Edit`

.. disqus::
