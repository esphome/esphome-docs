Jablotron Info
====================

.. seo::
    :description: Instructions for setting up a jablotron_info text sensor.

The `jablotron_info` text sensor platform creates a sensor reporting the Jablotron
JA-121T gateway version. The text sensor requires 
:doc:`Jablotron Component </components/jablotron>` to be configured.

The sensor reports a string like this:

  ``JA-121T, SN:12101234, SWV:NN6021.05.0, HWV:1``

Configuration variables:
------------------------
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **name** (*Required*, string): The name of the sensor.

All other options from :ref:`Text Sensor component <config-text_sensor>`.

Example

.. code-block:: yaml

    uart:
      # ...
    jablotron:
      # ...
    text_sensor:
      - platform: jablotron_info
        name: Jablotron Info


See Also
--------
- :apiclass:`:jablotron_info::InfoSensor`
- :doc:`/components/jablotron`
- :doc:`/components/uart`
- `JA-121 RS-485 Interface <https://jablotron.com.hk/image/data/pdf/manuel/JA-121T.pdf>`__
- :ghedit:`Edit`
