.. seo::
    :description: EasyPower DIY power meter utility with ESPHome
    :image: easypower.jpg
    :keywords: power meter ina219 esp8266 esphome current voltage

EasyPower - simple power meter
------------------------------

EasyPower is a simple power meter powered by ESPHome.

Check source code at GitHub: `ohdarling/EasyPower <https://github.com/ohdarling/EasyPower>`__

.. figure:: images/easypower.jpg
    :align: center
    :width: 50%

Features
--------

- **Measure the voltage and current of the load device**
- **Calculate the power of the load device in mW**
- **Cumulative power consumption in mWh**
- **Cumulative operating time to evaluate battery usage**

Hardware
--------

- ESP8266 dev board, such as NodeMCU
- INA219 module
- 128x64 OLED module, with I2C pins

That's all!

Wiring
------

.. figure:: images/easypower_wiring.jpg
    :align: center
    :width: 50%

Firmware
--------

With the power of ESPHome, we can build and upload firmware to mcu with just one line of command:

.. code-block:: bash

    esphome upload easypower.yaml

If you need monitor the data trends, you should set Wi-Fi and MQTT broker information first in secrets.yaml:

.. code-block:: yaml

    wifi_ssid: ""
    wifi_password: ""
    mqtt_broker: ""

Usage
-----

Finally, you can connect the load device which want to be measured, for example a NodeMCU:

- Connect power 5V to VIN+
- Connect VIN- to V5 on NodeMCU
- Connect power GND to NodeMCU GND
- Connect power GND to INA219 GND

.. figure:: images/easypower_demo.jpg
    :align: center
    :width: 50%

Monitor
-------

You can use MQTT Explorer to monitor data trends across measurements, just selecting the topic easypower/metrics, then using "Add to chart panel" in the Value panel, aha, a data trend chart apperaed:

.. figure:: images/easypower_monitor.jpg
    :align: center
    :width: 50%

Source
------

GitHub: `ohdarling/EasyPower <https://github.com/ohdarling/EasyPower>`__

See Also
--------

- :doc:`/devices/nodemcu_esp8266`
- :doc:`/components/sensor/ina219`
- :doc:`/components/display/ssd1306`
- :doc:`/components/mqtt`
- :ghedit:`Edit`
