Sonoff D1 Dimmer
================

.. seo::
    :description: Instructions for setting up a Sonoff D1 dimmer switch.
    :image: brightness-medium.svg

The ``sonoff_d1`` light platform creates a simple brightness-only light for the
hardware found in `Sonoff D1 dimmer <https://itead.cc/product/sonoff-d1-smart-dimmer-switch/>`__. Installations with Sonoff RM433 433MHz radio
remotes are also supported. Use this component to integrate Sonoff D1 dimmer into
ESPHome / Home Assistant ecosystem.

.. figure:: images/sonoff_d1.jpg
    :align: center
    :width: 100.0%

    Sonoff D1 dimmer front and back view. Image by `ITEAD <https://itead.cc/product/sonoff-d1-smart-dimmer-switch/>`__.

Sonoff D1 uses another MCU for light dimming and handling of radio commands.
It's hooked up to ESP8266 via UART bus with default RX / TX pins being used on
ESP8266 side. Bi-directional symmetric request / response protocol is implemented
between ESP8266 and MCU. ``sonoff_d1`` component implements this protocol and
translates between HA light commands and serial messages.

To replace the stock firmware with ESPHome you will need to locate GPIO0 pin and serial port. Photos below should help.

.. figure:: images/sonoff_d1_gpio0.jpg
    :align: center
    :width: 100.0%

    Photo of GPIO 0, images by `klotzma <https://github.com/arendst/Tasmota/issues/7598#issuecomment-578433417>`__.
.. figure:: images/sonoff_d1_serial.jpg
    :align: center
    :width: 100.0%

    Photo of serial port pins, images by  `klotzma <https://github.com/arendst/Tasmota/issues/7598#issuecomment-578433417>`__.

Before using this components make sure:

- board is configured to ``esp8285``
- :ref:`UART bus <uart>` is configured with default RX / TX pins and 9600 baud rate
- :doc:`logger </components/logger>` to the serial port is disabled by setting ``baud_rate`` to ``0``
- in case you need light state restoration on power up, make sure ``restore_from_flash`` is set to ``true`` in the :doc:`ESP8266 platform </components/esp8266>`


This component is useless for devices other than Sonoff D1 dimmer.

.. code-block:: yaml


    # Example configuration entry
    esphome:
      name: my-d1-dimmer

    # Restore from flash if you want to keep the last state at power up
    esp8266:
      board: esp8285
      restore_from_flash: true

    # Make sure your WiFi will connect
    wifi:
      ssid: "ssid"
      password: "password"

    # Make sure logging is not using the serial port
    logger:
      baud_rate: 0

    # Enable Home Assistant API
    api:

    # Make sure you can upload new firmware OTA
    ota:
      platform: esphome

    # D1 dimmer uses hardware serial port on the default pins @ 9600 bps
    uart:
      rx_pin: RX
      tx_pin: TX
      baud_rate: 9600

    # And finally the light component
    # gamma correction equal to zero gives linear scale,
    # exactly what's needed for this device
    light:
      - platform: sonoff_d1
        use_rm433_remote: False
        name: Sonoff D1 Dimmer
        restore_mode: RESTORE_DEFAULT_OFF
        gamma_correct: 0.0
        default_transition_length: 1s


Configuration variables:
------------------------

- **use_rm433_remote** (*Optional*, boolean): Set to ``True`` if your setup uses Sonoff RM433
  or any other radio remote control. Properly setting this parameter allows the platform to
  identify what to do with incoming UART commands. RF chip is known to catch random commands
  if not paired with a real remote (so called ghost commands). This problem is observed even
  with the stock firmware and most probably is a bug in the MCU firmware or in the RF chip
  firmware. Setting this to ``False`` instructs the platform to properly ignore such commands
  and thus prevent unexpected switches or light intensity changes.
- **min_value** (*Optional*, int): The lowest dimmer value allowed. Acceptable value for your
  setup will depend on actual light bulbs installed and number of them. Start with the default
  value and check what will be the minimal brightness bulbs can render. Pay attention that for
  some dimmable LED lamps minimal turn-on brightness will be higher that the minimal achievable
  brightness if you just decrease it when lamp is already turned on. Defaults to 0.
- **max_value** (*Optional*, int): The highest dimmer value allowed. Use this to hard-limit light
  intensity for your setup. For some bulbs this parameter might be also useful to prevent
  flickering at high brightness values. Defaults to 100.
- All other options from :ref:`Light <config-light>`.


See Also
--------

- :doc:`/components/light/index`
- :doc:`/components/uart`
- :doc:`/components/logger`
- :doc:`/components/esp8266`
- :ghedit:`Edit`
