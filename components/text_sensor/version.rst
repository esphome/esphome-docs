Version Text Sensor
===================

.. seo::
    :description: Instructions for setting up version text sensors.
    :image: new-box.svg

The ``version`` text sensor platform exposes the ESPHome version the firmware
was compiled against as a text sensor.

.. figure:: images/version-ui.png
    :align: center

.. code-block:: yaml

    # Example configuration entry
    text_sensor:
      - platform: version
        name: "ESPHome Version"

Configuration variables:
------------------------

- **hide_timestamp** (*Optional*, boolean): Allows you to hide the compilation timestamp from the version string. Defaults to ``false``.
- All other options from :ref:`Text Sensor <config-text_sensor>`.

Disabling the compilation timestamp:
------------------------------------

.. code-block:: yaml

    # Example configuration entry
    text_sensor:
      - platform: version
        name: "ESPHome Version"
        hide_timestamp: true

This will, for example, change the output of the sensor from:

``2024.6.0-dev May 30 2024, 09:07:35`` to just ``2024.6.0-dev``


See Also
--------

- :apiref:`version/version_text_sensor.h`
- :ghedit:`Edit`
