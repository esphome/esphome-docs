AHT10 Temperature+Humidity Sensor
=================================

.. seo::
    :description: Instructions for setting up AHT10 temperature and humidity sensors
    :image: aht10.jpg
    :keywords: aht10 aht20 dht20 aht30

The ``aht10`` Temperature+Humidity sensor allows you to use your AHT10
(`datasheet <http://www.aosong.com/userfiles/files/media/aht10%E8%A7%84%E6%A0%BC%E4%B9%A6v1_1%EF%BC%8820191015%EF%BC%89.pdf>`__), AHT20 (`datasheet <https://cdn-learn.adafruit.com/assets/assets/000/091/676/original/AHT20-datasheet-2020-4-16.pdf?1591047915>`__) or AHT30 (`datasheet <https://eleparts.co.kr/data/goods_attach/202306/good-pdf-12751003-1.pdf>`__) :ref:`I²C <i2c>`-based sensor with ESPHome.

The DHT20 (`datasheet <https://cdn.sparkfun.com/assets/8/a/1/5/0/DHT20.pdf>`__) sensor has the packaging of the :doc:`dht` series, but has the AHT20 inside and is speaking :ref:`I²C <i2c>` as well.

.. figure:: images/aht10-full.jpg
    :align: center
    :width: 50.0%

    AHT10 Temperature & Humidity Sensor.

.. figure:: images/temperature-humidity.png
    :align: center
    :width: 80.0%

.. note::

    When configured for humidity, the log *'Components should block for at most 20-30ms in loop().'* will be generated in verbose mode. This is due to technical specs of the sensor and can not be avoided.

.. code-block:: yaml

    # Example configuration entry
    sensor:
      - platform: aht10
        variant: AHT10
        temperature:
          name: "Living Room Temperature"
        humidity:
          name: "Living Room Humidity"
        update_interval: 60s

Configuration variables:
------------------------

- **variant** (*Optional*, enum): Set the variant of the device in use. Defaults to ``AHT10``.

  - ``AHT10`` - For AHT10 devices.
  - ``AHT20`` - For AHT20 and AHT30 devices.

- **temperature** (**Required**): The information for the temperature sensor.

  - All options from :ref:`Sensor <config-sensor>`.

- **humidity** (**Required**): The information for the humidity sensor

  - All options from :ref:`Sensor <config-sensor>`.

- **update_interval** (*Optional*, :ref:`config-time`): The interval to check the sensor. Defaults to ``60s``.


See Also
--------

- :ref:`sensor-filters`
- :doc:`absolute_humidity`
- :apiref:`aht10/aht10.h`
- `AHT10 Library <https://github.com/Thinary/AHT10>`__  by `Thinary Electronic <https://github.com/Thinary>`__
- `Unofficial Translated AHT10 Datasheet (en) <https://wiki.liutyi.info/download/attachments/30507639/Aosong_AHT10_en_draft_0c.pdf>`__
- :ghedit:`Edit`
