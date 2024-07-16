Modem Component
===============

.. seo::
    :description: Instructions for setting up the Ethernet configuration for your ESP32 node in ESPHome.
    :image: ethernet.svg
    :keywords: Network, Modem

This ESPHome component enables cellular modem TCP/IP connections for ESP32s.

Only ESP32 with IDF framework is supported.

As the device IP will be on a foreign private network, :doc:`/components/mqtt` should be used, or :doc:`/components/api` with :doc:`/components/wireguard`. 

This component can't be used with the :doc:`/components/wifi` or the :doc:`/components/ethernet`, even if other are physically available.

.. code-block:: yaml

    modem:
      id: atmodem
      rx_pin: 26
      tx_pin: 27
      model: SIM7600  
      apn: orange
      pin_code: "0000"


Configuration variables:
------------------------

- **model** (**Required**, string): The type of the modem.

  Supported modems are:

  - ``BG96``
  - ``SIM800``
  - ``SIM7000``
  - ``SIM7600``

- **rx_pin** (**Required**, integer): The pin number of the ``RX`` on the esp side (connected to the ``TX`` pin on the modem side).
- **tx_pin** (**Required**, integer): The pin number of the ``TX`` on the esp side (connected to the ``RX`` pin on the modem side).
- **apn** (**Required**, string): Operator apn.
- **pin_code** (*Optional*, string): The pin code of the sim card.
- **init_at** (*Optional*, list): A list of ``AT`` commands that will be sent to the modem after the connection
- **on_not_responding** (*Optional*, :ref:`Automation <automation>`): An action to be performed when the modem doesn't respond.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.


.. note::

  This component doesn't poweron the modem. If the modem doesn't respond, the ``on_not_responding`` action will be called to let you powercycle the modem.
  For example the following code try to powercycle the modem, assuming that ``modem_power`` is a gpio switch connected to the modem powerkey.

.. note::

  Most modems consume too much current to be powered directly by the ESP32. An external power supply is often required.

.. note::

  Internally, the modem component use the CMUX protocol to comminicate with the modem. 
  This create two virtual channels: one for ``AT`` commands, and one for data.
  As the data channel is used for ``PPPoS``, It's not possible to create another data channel, for example for NMEA GNSS frames. 
  (For GNSS, a workaround is to use ``AT+CGNSSINFO``, that doesn't produce NMEA frames).



Configuration examples
----------------------

.. code-block:: yaml

  modem:
    id: atmodem
    rx_pin: 26
    tx_pin: 27
    model: SIM7600  
    apn: orange
    pin_code: "0000"
    init_at:
      # enable GNSS
      - AT+CGNSSMODE=15,1 # GNSS all navigation systems
      - AT+CGPS=1 # GPS on
    on_not_responding:
      # Triggered if the modem is not responding.
      # assuming tha the gpio switch 'modem_power' is connected to the modem pwrkey, we will powercycle the modem 
      - logger.log: modem powercyle
      - switch.turn_off: modem_power
      - delay: 15s
      - switch.turn_on: modem_power
      - delay: 15s

Lambda calls
------------

From :ref:`lambdas <config-lambda>`, you can call several methods to do some advanced stuff.

- ``->dce``: The DCE object from the underlying `esp_modem`_ library. Most of the `DCE methods <https://docs.espressif.com/projects/esp-protocols/esp_modem/docs/latest/internal_docs.html#_CPPv4N9esp_modem3DCEE>`_ are available.

For example, to send an ``AT`` command, and get the result:

.. code-block:: cpp

  std::string gnss_info;
  esp_modem::command_result err;
  err = id(atmodem)->dce->at("AT+CGNSSINFO", gnss_info, 3000);
  if (err != esp_modem::command_result::OK) {
    ESP_LOGE("", "Error while executing AT command");
  } else {
    ESP_LOGI("", "Result: %s", gnss_info.c_str());
  }


See Also
--------

- :doc:`network`
- :doc:`/components/mqtt`
- :doc:`/components/wireguard`
- `SIM7600 AT command list <https://simcom.ee/documents/SIM7600C/SIM7500_SIM7600%20Series_AT%20Command%20Manual_V1.01.pdf>`__
- `SIM7600 Hardware design <https://simcom.ee/documents/SIM7600E/SIM7600%20Series%20Hardware%20Design_V1.03.pdf>`__
- :ghedit:`Edit`


.. _esp_modem: https://docs.espressif.com/projects/esp-protocols/esp_modem/docs/latest/