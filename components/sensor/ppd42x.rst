PPD42X Particulate Matter Sensor
================================

.. seo::
    :description: Instructions for setting up PPD42X Particulate matter sensors
    :image: ppd42x.jpg
    :keywords: PPD42X

The ``PPD42X`` sensor platform allows you to use PPD42X particulate matter sensors
(`datasheet <https://www.researchgate.net>`__) with ESPHome.
NB: This sensor use counting method to test dust concentration but not
weight method, and the unit is pcs/L or pcs/0.01cf

.. figure:: images/ppd42-full.jpg
    :align: center
    :width: 50.0%

    PPD42X Particulate Matter Sensor
Wiring:
-------

==================== ===================== =====================
**Pin**               **Function**           **Wire color**
-------------------- --------------------- ---------------------
``1``                 ``Ground``             ``Green``
-------------------- --------------------- ---------------------
``2``                 ``P2 (output)``        ``White``
-------------------- --------------------- ---------------------
``3``                 ``5V``                 ``Yellow``
-------------------- --------------------- ---------------------
``4``                 ``P1 (output)``        ``Black``
-------------------- --------------------- ---------------------
``5``                 ``Threshold V for P2    ``Red``(*) 
==================== ===================== =====================

(*) (not yet implemented)


Pin 5 is closest to the corner of the board (and there is a 5 printed on both sides of the board near pin 5).
Note the colors in the photo above are different from the wire colors available from other sources (like Grove).

The P1 output is used to measure particles between 1um and 10um.
The P2 output (with the threshold pin unconnected) is used to measure particles between 2.5um and 10um.
To read the sensor, the total time that the P1 or P2 signal is low (measured in microsends) is used to determine particle concentrations.

.. code-block:: yaml

    # Example configuration entry

    sensor:
      - platform: ppd42x
        pm_2_5:
          pin: GPIO32
          name: "Particulate Matter <2.5µm Concentration"
        pm_10_0:
          pin: GPIO35
          name: "Particulate Matter <10.0µm Concentration"
        update_interval: 5min
        time_out: 30000

With ``update_interval``, the working period of the PPD42X device will be changed. If ``update_interval`` is
equal to ``0min``, the PPD42X will be set to continuous measurement and will report wrong measurement values
approximately every second: the update_interval must be > time_out

If ``update_interval`` is between 1-30 minutes, the PPD42X periodically turns on for 30s before each measurement.

Configuration variables:
------------------------

- **pm_2_5** (*Optional*): Use the concentration of particulates of size less than 2.5µm in µg per cubic meter.
  All options from :ref:`Sensor <config-sensor>`.

- **pm_10_0** (*Optional*): Use the concentration of particulates of size less than 10.0µm in µg per cubic meter.
  All options from :ref:`Sensor <config-sensor>`.

- **update_interval** (*Optional*, :ref:`config-time`): The interval to check the sensor in minutes.
  This affects the working period of the PPD42X sensor. Defaults to ``5min``.

- **time_out** (*Optional*, :ref:`config-time`): The interval to check the P1 and P2 pins in micro-seconds.
  This affects the working period of the PPD42X sensor. Defaults to ``30000``.

See Also
--------

- :doc:`/components/sensor/pmsx003`, `/components/sensor/sds011`
- :ref:`sensor-filters`
- `Laser Dust Sensor Control Protocol <https://nettigo.pl/attachments/415>`__
- :apiref:`sensor/ppd42x_component.h`
- :ghedit:`Edit`
