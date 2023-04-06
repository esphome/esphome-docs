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

    esp8266:
      board: nodemcuv2

    wifi:
      ssid: !secret wifi_ssid
      password: !secret wifi_password

    api:

    # Enable logging
    logger:

    ota:

    sensor:
      - platform: dht
        pin: D7
        temperature:
          name: "Multisensor Temperature"
        humidity:
          name: "Multisensor Humidity"
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
