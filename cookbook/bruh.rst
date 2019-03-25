BRUH Multisensor
================

.. seo::
    :description: Instructions for re-creating a BRUH multisensor using ESPHome.
    :image: bruh.png

The BRUH Multisensor is a great introductory project into Home Automation with an
amazing setup tutorial. And fortunately ESPHome has complete support for all the
stuff used by the Multisensor 🎉

.. raw:: html

    <iframe width="560" height="315" src="https://www.youtube.com/embed/jpjfVc-9IrQ" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>

Thank you very much to `@jackjohnsonuk <https://github.com/jackjohnsonuk>`__ for providing this
configuration file 😀

.. code-block:: yaml

    esphome:
      name: <NODE_NAME>
      platform: ESP8266
      board: nodemcuv2

    wifi:
      ssid: <SSID>
      password: <PASSWORD>

    api:

    # Enable logging
    logger:

    ota:

    sensor:
      - platform: dht
        pin: D7
        temperature:
          name: "Multisensor Temperature"
          id: dht_temprature
        humidity:
          name: "Multisensor Humidity"
          id: dht_humidity
      - platform: template
        name: "Multisensor Feels Like"
        lambda: |-
          return (((-42.379 + (2.04901523*((id(dht_temprature).state*1.8)+32)) + (10.14333127*id(dht_humidity).state) - (0.22475541*((id(dht_temprature).state*1.8)+32)*id(dht_humidity).state) - (6.83783 * pow(10,(-3))*pow(((id(dht_temprature).state*1.8)+32),2)) - (5.481717 * pow(10,(-2))*pow(id(dht_humidity).state,2)) + (1.22874 * pow(10,(-3))*(pow(((id(dht_temprature).state*1.8)+32),2)*id(dht_humidity).state)) + (8.5282 * pow(10,(-4))*((id(dht_temprature).state*1.8)+32)*pow(id(dht_humidity).state,2)) - (1.99 * pow(10,(-6))*pow((id(dht_temprature).state*1.8)+32),2)*pow(id(dht_humidity).state,2)))-32)/1.8);
          update_interval: 60s
          accuracy_decimals: 1
          unit_of_measurement: "°C"
          icon: "mdi:thermometer"
      - platform: adc
        pin: A0
        name: "Multisensor Brightness"
        unit_of_measurement: lux
        filters:
          - lambda: |-
              return (x / 10000.0) * 2000000.0;

    binary_sensor:
      - platform: gpio
        pin: D5
        name: "Multisensor Motion"
        device_class: motion

    output:
      - platform: esp8266_pwm
        pin: D1
        id: redgpio
      - platform: esp8266_pwm
        pin: D2
        id: greengpio
      - platform: esp8266_pwm
        pin: D3
        id: bluegpio

    light:
      - platform: rgb
        name: "Multisensor Light"
        red: redgpio
        green: greengpio
        blue: bluegpio


See Also
--------

- :doc:`/devices/nodemcu_esp8266`
- :doc:`pir`
- :doc:`temt6000`
- :doc:`/components/light/rgb`
- :doc:`/components/output/esp8266_pwm`
- :doc:`/components/sensor/dht`
- :doc:`/components/sensor/adc`
- :doc:`/components/binary_sensor/gpio`
- :ghedit:`Edit`

.. disqus::
