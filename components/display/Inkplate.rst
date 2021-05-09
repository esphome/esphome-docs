Inkplate 6
==========

.. seo::
    :description: Instructions for setting up Inkplate E-Paper displays in ESPHome.
    :image: Inkplate.jpg

All-in-one e-paper display  ``Inkplate 6``
Inkplate 6 is a powerful, Wi-Fi enabled ESP32 based six-inch e-paper display – recycled from a Kindle e-reader. Its main feature is simplicity.
Learn more at `Inkplate's website <https://inkplate.io/>`__

.. figure:: images/Inkplate.jpg
    :align: center
    :width: 75.0%

    Inkplate 6


.. code-block:: yaml

    # Example minimal configuration entry

    mcp23017:
      - id: mcp23017_hub
        address: 0x20

    display:
    - platform: inkplate6
      id: inkplate_display
      greyscale: false
      partial_updating: false
      update_interval: 60s

      ckv_pin: 32
      sph_pin: 33
      gmod_pin:
        mcp23017: mcp23017_hub
        number: 1
      gpio0_enable_pin:
        mcp23017: mcp23017_hub
        number: 8
      oe_pin:
        mcp23017: mcp23017_hub
        number: 0
      spv_pin:
        mcp23017: mcp23017_hub
        number: 2
      powerup_pin:
        mcp23017: mcp23017_hub
        number: 4
      wakeup_pin:
        mcp23017: mcp23017_hub
        number: 3
      vcom_pin:
        mcp23017: mcp23017_hub
        number: 5

.. warning::

    When using the Inkplate epaper module, the GPIO pin numbers above *cannot be changed* as they are
    hardwired within the module/PCB.

.. warning::

    Inkplate module cannot perform partial update if 3 bit mode is on.
    It just ignores the function call in that case.


Configuration variables
***********************

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **greyscale** (*Optional*, boolean): Makes the screen display 3 bit colors. Defaults to ``False``
- **partial_updating** (*Optional*, boolean): Makes the screen update partially, which is faster, but leaves burnin. Defaults to ``False``
- **full_update_every** (*Optional*, int): When partial updating is enabled, forces a full screen update after chosen number of updates. Defaults to ``10``
- **lambda** (*Optional*, :ref:`lambda <config-lambda>`): The lambda to use for rendering the content on the display.
  See :ref:`display-engine` for more information.
- **update_interval** (*Optional*, :ref:`config-time`): The interval to re-draw the screen. Defaults to ``5s``.
- **pages** (*Optional*, list): Show pages instead of a single lambda. See :ref:`display-pages`.

- **ckv_pin** (**Required**, :ref:`config-pin`): The CKV pin for the Inkplate display.
- **gmod_pin** (**Required**, :ref:`config-pin`): The GMOD pin for the Inkplate display.
- **gpio0_enable_pin** (**Required**, :ref:`config-pin`): The GPIO0 Enable pin for the Inkplate display.
- **oe_pin** (**Required**, :ref:`config-pin`): The OE pin for the Inkplate display.
- **powerup_pin** (**Required**, :ref:`config-pin`): The Powerup pin for the Inkplate display.
- **sph_pin** (**Required**, :ref:`config-pin`): The SPH pin for the Inkplate display.
- **spv_pin** (**Required**, :ref:`config-pin`): The SPV pin for the Inkplate display.
- **vcom_pin** (**Required**, :ref:`config-pin`): The VCOM pin for the Inkplate display.
- **cl_pin** (*Optional*, :ref:`config-pin`): The CL pin for the Inkplate display.
  Defaults to GPIO0.
- **le_pin** (*Optional*, :ref:`config-pin`): The LE pin for the Inkplate display.
  Defaults to GPIO2.

- **display_data_0_pin** (*Optional*, :ref:`config-pin`): The Data 0 pin for the Inkplate display.
  Defaults to GPIO4.
- **display_data_1_pin** (*Optional*, :ref:`config-pin`): The Data 1 pin for the Inkplate display.
  Defaults to GPIO5.
- **display_data_2_pin** (*Optional*, :ref:`config-pin`): The Data 2 pin for the Inkplate display.
  Defaults to GPIO18.
- **display_data_3_pin** (*Optional*, :ref:`config-pin`): The Data 3 pin for the Inkplate display.
  Defaults to GPIO19.
- **display_data_4_pin** (*Optional*, :ref:`config-pin`): The Data 4 pin for the Inkplate display.
  Defaults to GPIO23.
- **display_data_5_pin** (*Optional*, :ref:`config-pin`): The Data 5 pin for the Inkplate display.
  Defaults to GPIO25.
- **display_data_6_pin** (*Optional*, :ref:`config-pin`): The Data 6 pin for the Inkplate display.
  Defaults to GPIO26.
- **display_data_7_pin** (*Optional*, :ref:`config-pin`): The Data 7 pin for the Inkplate display.
  Defaults to GPIO27.


Complete example
****************

The following is a complete example YAML configuration that does a few things beyond the usual
Wi-Fi, API, and OTA configuration.

.. code-block:: yaml

    # Example configuration entry
    esphome:
      name: inkplate
      platform: ESP32
      board: esp-wrover-kit

    logger:

    wifi:
      ssid: <YOUR WIFI SSID>
      password: <YOUR WIFI PASSWORD>
      ap:
        ssid: Inkplate-AP
        password: '12345678'

    captive_portal:

    ota:

    api:

    switch:
      - platform: restart
        name: "Inkplate Reboot"
        id: reboot

      - platform: gpio
        id: battery_read_mosfet
        pin:
          mcp23017: mcp23017_hub
          number: 9
          inverted: true

      - platform: template
        name: "Inkplate Greyscale mode"
        lambda: return id(inkplate_display).get_greyscale();
        turn_on_action:
          - lambda: id(inkplate_display).set_greyscale(true);
        turn_off_action:
          - lambda: id(inkplate_display).set_greyscale(false);

      - platform: template
        name: "Inkplate Partial Updating"
        lambda: return id(inkplate_display).get_partial_updating();
        turn_on_action:
          - lambda: id(inkplate_display).set_partial_updating(true);
        turn_off_action:
          - lambda: id(inkplate_display).set_partial_updating(false);

    sensor:
      - platform: adc
        id: battery_voltage
        update_interval: never
        attenuation: 11db
        pin: 35
      - platform: template
        name: "Inkplate Battery Voltage"
        lambda: |-
          id(battery_read_mosfet).turn_on();
          delay(1);
          float adc = id(battery_voltage).sample();
          id(battery_read_mosfet).turn_off();
          return adc;
        filters:
          - multiply: 2

    i2c:

    mcp23017:
      - id: mcp23017_hub
        address: 0x20

    binary_sensor:
      - platform: status
        name: "Inkplate Status"
        id: system_status

      - platform: gpio
        name: "Inkplate Touch Pad 1"
        pin:
          mcp23017: mcp23017_hub
          number: 10
      - platform: gpio
        name: "Inkplate Touch Pad 2"
        pin:
          mcp23017: mcp23017_hub
          number: 11
      - platform: gpio
        name: "Inkplate Touch Pad 3"
        pin:
          mcp23017: mcp23017_hub
          number: 12

    time:
      - platform: sntp
        id: esptime

    font:
      - file: "Helvetica.ttf"
        id: helvetica_96
        size: 96
      - file: "Helvetica.ttf"
        id: helvetica_48
        size: 48


    display:
    - platform: inkplate6
      id: inkplate_display
      greyscale: false
      partial_updating: false
      update_interval: 60s

      ckv_pin: 32
      sph_pin: 33
      gmod_pin:
        mcp23017: mcp23017_hub
        number: 1
      gpio0_enable_pin:
        mcp23017: mcp23017_hub
        number: 8
      oe_pin:
        mcp23017: mcp23017_hub
        number: 0
      spv_pin:
        mcp23017: mcp23017_hub
        number: 2
      powerup_pin:
        mcp23017: mcp23017_hub
        number: 4
      wakeup_pin:
        mcp23017: mcp23017_hub
        number: 3
      vcom_pin:
        mcp23017: mcp23017_hub
        number: 5

      lambda: |-
        it.fill(COLOR_ON);

        it.print(100, 100, id(helvetica_48), COLOR_OFF, TextAlign::TOP_LEFT, "ESPHome");

        it.strftime(400, 300, id(helvetica_48), COLOR_OFF, TextAlign::CENTER, "%Y-%m-%d", id(esptime).now());
        it.strftime(400, 400, id(helvetica_96), COLOR_OFF, TextAlign::CENTER, "%H:%M", id(esptime).now());

        if (id(system_status).state) {
          it.print(700, 100, id(helvetica_48), COLOR_OFF, TextAlign::TOP_RIGHT, "Online");
        } else {
          it.print(700, 100, id(helvetica_48), COLOR_OFF, TextAlign::TOP_RIGHT, "Offline");
        }


See Also
--------

- :doc:`index`
- `Arduino Inkplate 6 library <https://github.com/e-radionicacom/Inkplate-6-Arduino-library>`__ by `E-radionica.com <https://e-radionica.com/>`__
- :ghedit:`Edit`
