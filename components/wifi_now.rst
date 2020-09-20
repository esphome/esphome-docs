WiFi Now Component
==================

.. seo::
    :description: Instructions for setting up the WiFi Now (an ESP-Now implementation) configuration for your ESP nodes in ESPHome.
    :image: wifi_now.png
    :keywords: Wifi-Now, ESP-Now, WiFi, ESP8266, ESP32

The ``wifi_now`` component allows you to directly communicate between your ESP devices.
This means you'll no longer need an access point for your ESPhome units to start communicating
and doing work.

Also, battery powered devices can save power compared to when using always on Wifi because there is
no delay when connecting to an access point after startup.

.. note::

    Currently, this component is not safe for any application that is security critical as it does not
    include authentication.
    An example would be for the use in door locks, or other entry systems.
    A future release will mitigate this.

.. note::

    This is the very first implementation, this version is ment to be used for simple applications.
    In future releases basic stuff like longer packets and security features, and some kind
    of a stream mode is planned do a "proxy" ap (need to add a port number for the api in the home
    assistant code) and "proxy" ota.

**Restrictions (by ESP-Now)**:

- Maximum of 20 un-encrypted peers (a hard limit by ESP-Now)
- Maximum of 6 different cryptographic keys (a hard limit by ESP-Now) (will be mitigated in a
  future release)
- Maximum payload size is currently 242 bytes (250 - 8 byte service key) (will be mitigated in a
  future release)
- Encrypts the data on Unicast, but received data is not authenticated, the data is 
  authenticated by WPA when sent encrypted but the ``wifi_now`` component can not determine
  if the data was send encrypted or not. (will be mitigated in a future release)
- Multicasts are always un-encrypted (will be mitigated in a future release)
- Wifi channel of WLAN connected devices must be fixed to a specific channel (will be mitigated
  in a future release)
- Each peer must be defined locally, this is only when Multicasting, not during a Broadcast.

Configuration examples
----------------------

Use a tool to get the BSSID aka **station** MAC from devices that should be able to talk together.
BSSID is the only address needed for a peer used by ``wifi_now``, there is no translation from a name
except the local id provided in the peer entry. Optionally, create a 16 byte master key or
password. Optionally, for each device, a communication key or password.

For more details see see :ref:`Configuration Variables <wifi-now_configuration_variables>`.

Example configuration for three devices:

.. code-block:: yaml

    # Device A
    wifi_now:
      channel: 2
      password: "<master password>"
      peers:
        - id: device_b
          bssid: <Mac ID Device B>
          password: "<communication A between B password>"
        - id: device_c
          bssid: <Mac ID Device C>
          password: "<communication A between C password>"

.. code-block:: yaml

    # Device B
    wifi_now:
      channel: 2
      password: "<master password>"
      peers:
        - id: device_a
          bssid: <Mac ID Device A>
          password: "<communication A between B password>"
        - id: device_c
          bssid: <Mac ID Device C>
          password: "<communication B between C password>"

.. code-block:: yaml

    # Device C
    wifi_now:
      channel: 2
      password: "<master password>"
      peers:
        - id: device_a
          bssid: <Mac ID Device A>
          password: "<communication A between C password>"
        - id: device_b
          bssid: <Mac ID Device B>
          password: "<communication B between C password>"

To accomplish basic communication, add an `on_receive` event on the receiving device, 
see :ref:`on_receive <wifi-now_on_receive>` for details:

.. code-block:: yaml

    # Device A
    wifi_now:
    ...
      on_receive:
        - service: "Boolean Sensor A"
          payloads:
            - bool: sensor_a_payload
          then:
            - boolean_sensor.template.publish:
              id: sensor_a
              state: !lambda 'return id(sensor_a_payload)->get_value();'

On the sending device, add a wifi_now.send action to send the data to the receiving device:

.. code-block:: yaml

    # Device B
    wifi_now:
    ...

    binary_sensor:
      ...
      - platform: gpio
        id: pin0
        pin:
          number: 0
          mode: INPUT_PULLUP
          inverted: True
        filters:
          - delayed_on: 10ms
          - delayed_off: 10ms
        on_state:
          then:
          - wifi_now.send:
            peerid: device_a
            service: "Boolean Sensor A"
            payloads:
            - bool: !lambda return x

This is just a basic example, in the case of a binary sensor use the 
`wifi_now.inject action < _wifi-now_inject_action>`
to trigger an event to avoid issues with timing and packet loss.

.. _wifi-now_configuration_variables:

Configuration variables
-----------------------

- **channel** (*optional*, integer from 1 to 12):
  Channel set on startup.
  The ``wifi_now`` component will never adjust the channel when other components like when Wifi changes
  the channel (current version). if not set, ``wifi_now`` depends on other the component to set the channel.

- **password** (*optional*, string):
  This is the master password. ``wifi_now`` derives the master aes key by using the first 16 bytes of the md5sum
  of the password.

- **aeskey** (*optional*, 16 bytes in the form xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx):
  This is the master aes key, needs to be the same an all devices.
  Password and aeskey are exclusive.
  If not set by aeskey or password the ESP-Now default key is used.

- **peers** (*required*, list of peer):
  A list of all peers this device can communicate with.
  
  - **id** (*required*, identifier):
    Local id of the peer, this is used as a reference in the wifi_now.send action.

  - **bssid** (*required*, mac address 6 bytes in the form xx:xx:xx:xx:xx:xx)
    Basic Service Set Identification aka. Station Mac Address of the peer

  - **password** (*optional*, string):
    This is the communication password, ``wifi_now`` derives the communication aes key by using the first 
    16 bytes of the md5sum.

  - **aeskey** (*optional*, 16 bytes in the form xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx):
    This is the communication aes key. It needs to be the same on the peer devices.
    Password and aeskey are exclusive.
    If not set by aeskey or password communication will not be encrypted.
    You can use 6 different aes keys on a device, behavior is undefined if more than 6 keys are used.

Automations
-----------

.. _wifi-now_on_receive:

``on_receive``
**************

This automation is triggered when a packet is received by ``wifi_now``.

Configuration Variables:

- **peerid** (*optional*, identifier):
  If set, the automation is only executed when the packet is sent from this peer.

- **service** (*optional*, string): service name,
  If set the automation is only executed when the packet contains the service key.
  wifi-now derives the service by using the first 8 Bytes of the service name md5sum.

- **servicekey** (*optional*, 8 bytes in the form XX:XX:XX:XX:XX:XX:XX:XX):
  Service key, if set the automation is only executed when the packet contains the
  service key.
  
- **payloads** (*optional*, list of payload type and name)

  - **<payload type>**: id

<payload type> can be one of, see :ref:`wifi_now.send action <wifi-now_sent_action>`
for details:

- bool: boolean (32 Bit)

- float: float (ieee ???)

- int: integer (32 Bit)

- string: variable length string (std::string)

- vector: variable length binary (std:vector)

- binary_sensor_event: special value for 
  :ref:`wifi_now.inject action <wifi-now_inject_action>`

Example:

.. code-block:: yaml

    ...
    on_receive:
      - peerid: device_a
      - service: Binary Sensor 1
        payloads:
          - bool: BinarySensor1Value
        then:
          - binary_sensor_template.publish:
              id: binarysenosor1
              state !lambda return BinarySensor1Value->get_value();
    ...

Automation Actions:
-------------------

.. _wifi-now_sent_action:

``wifi_now.send``
*****************

An automation action to send a packet to a peer or all peers.

Like the if action, this action as two flow branches called on_fail and on_success.

Configuration Variables:

- **peerid** (*optional*, identifier): Id of the destination peer
  If set the payload is send only to this peer otherwise to all configured peers.

- **service** (*optional*, string): Service name.
  ``wifi_now`` derives the service by using the first 8 Bytes of the service name md5sum.

- **servicekey** (*optional*, 8 bytes in the form XX:XX:XX:XX:XX:XX:XX:XX):
  if set the packet is filtered by the service key.
  `service` and `servicekey` are exclusive.

- **payloads** (*optional*, list of payload type and name)

  - **<payload type>**: value
    Value for the payload, see list below.

<payload type> can be one off:

- bool: boolean (boolean lambda or boolean value)
  transfers a 32 bit unsigned integer with the value 0 if lamba returns 0 and 1 on
  all values > 0 when received this value can be used with the wifi_now.inject
  action to set the sensor state instead executing an automation.

- float: float (float lambda or float value)

- int: integer (integer lambda or integer value)

- string: variable length string (std::string lambda or string)

- vector: variable length binary (std:vector lambda)

- binary_sensor_event: special value for 
  :ref:`wifi_now.inject action <wifi-now_inject_action>`

.. note::

    combined payload must be below 242 char otherwise the send will fail, on an esp32 
    this means a restart!

Example:

.. code-block:: yaml

    ...
    - on_state
      - then
        ...
        - wifi_now.send:
            peerid: device_b
            service: Binary Sensor 1
            payloads:
              - bool: !lambda x
            on_fail:
              - wifi_now.retry_send:
              - wifi_now.abort:
            on_success:
              - logger.log: Success
        ...

``wifi_now.retry``
******************

An automation action retry sending a packet.

**This action can only be used in the `on_fail` branch of the send action**!

This action changes the flow of the automation back to the send action.

If max retries is reached the next action is executed.

Configuration Variables:

- **max_retries** (*optional*, unsigned integer, default 2): maximum number of retries to perform

Example: 

.. code-block:: yaml

    ...
    - on_state
      - then
        ...
        - wifi_now.send:
            peerid: device_b
            service: Binary Sensor 1
            payloads:
              - bool: !lambda x
            on_fail:
              - wifi_now.retry_send:
              # this is only executed after 2 retries!
              - wifi_now.abort:
        ...

``wifi_now.abort``
******************

An automation action to abort (or stop) the current automation.

**This action can only be used in the on_fail or on_success branch of the send action**!

Example:

.. code-block:: yaml

    - on_state
      - then
        ...
        - wifi_now.send:
            peerid: device_b
            service: Binary Sensor 1
            payloads:
              - bool: !lambda x
            on_fail:
              - wifi_now.retry_send:
              # this aborts the automation after 2 retrys!
              - wifi_now.abort:
        - logger.log this is only executed on success
        ...


.. _wifi-now_inject_action:

``wifi_now.inject``
*******************

An automation to inject an event into a binary_sensor, calls the automation trigger of a
binary_sensor.

This automation was created to avoid problems with timing of the multi click handling and to
mitigates problems with lost packets.

Configuration Variables:

- **sensor_id** (*required*, id): id of the binary sensor

- **payload_id** (*required*, id): id of payload setter

Values of the payload setter and the execution:

+--------+---------------+-----------------------------------------------------+
| binary | enumeration   | performed action                                    |
+========+===============+=====================================================+
| 0      | SWITCH_OFF    | calls set_state(true) on the sensor                 |
+--------+---------------+-----------------------------------------------------+
| 1      | SWITCH_ON     | calls set_state(false) on the sensor                |
+--------+---------------+-----------------------------------------------------+
| 2      | PRESS         | starts the on_press automation of the sensor        |
+--------+---------------+-----------------------------------------------------+
| 3      | RELEASE       | starts the on_release automation of the sensor      |
+--------+---------------+-----------------------------------------------------+
| 4      | CLICK         | starts the on_click automation of the sensor        |
+--------+---------------+-----------------------------------------------------+
| 5      | DOUBLE_CLICK  | starts the on_double_click automation of the sensor |
+--------+---------------+-----------------------------------------------------+
| 6      | MULTI_CLICK1  | starts the on_multi_click/n-th timing automation    |
+--------+---------------+ of the sensor                                       |
| 7      | MULTI_CLICK2  |                                                     |
+--------+---------------+                                                     |
| 8      | MULTI_CLICK3  |                                                     |
+--------+---------------+                                                     |
| 9      | MULTI_CLICK4  |                                                     |
+--------+---------------+                                                     |
| 10     | MULTI_CLICK5  |                                                     |
+--------+---------------+                                                     |
| 11     | MULTI_CLICK6  |                                                     |
+--------+---------------+                                                     |
| 12     | MULTI_CLICK7  |                                                     |
+--------+---------------+                                                     |
| 13     | MULTI_CLICK8  |                                                     |
+--------+---------------+                                                     |
| 14     | MULTI_CLICK9  |                                                     |
+--------+---------------+                                                     |
| 15     | MULTI_CLICK10 |                                                     |
+--------+---------------+                                                     |
| 16     | MULTI_CLICK11 |                                                     |
+--------+---------------+                                                     |
| 17     | MULTI_CLICK12 |                                                     |
+--------+---------------+                                                     |
| 18     | MULTI_CLICK13 |                                                     |
+--------+---------------+                                                     |
| 19     | MULTI_CLICK14 |                                                     |
+--------+---------------+                                                     |
| 20     | MULTI_CLICK15 |                                                     |
+--------+---------------+                                                     |
| 21     | MULTI_CLICK16 |                                                     |
+--------+---------------+                                                     |
| 22     | MULTI_CLICK17 |                                                     |
+--------+---------------+                                                     |
| 23     | MULTI_CLICK18 |                                                     |
+--------+---------------+                                                     |
| 24     | MULTI_CLICK19 |                                                     |
+--------+---------------+                                                     |
| 25     | MULTI_CLICK20 |                                                     |
+--------+---------------+-----------------------------------------------------+
  
`enumeration` is one of the WifiNowBinarySensorEvent values

Example:

.. code-block:: yaml

    # device A
    wifi_now:
      ...
      on_receive:
      - service: Binary Sensor 1
        payloads:
          - binary_sensor_event: BinarySensor1EventValue
        then:
          - logger.log: revieved for BinarySensor1
          - wifi_now.inject:
              sensor_id: BinarySensor1
              payload_id: BinarySensor1EventValue
    ...
    binary_sensor:
    ...
    - platform: gpio
      id: BinarySensor1
      name: Some fancy name
      pin: 2
      on_multi_click:
        - timing:
            - ON for at most 2s
          then:
            - logger.log: Multi click 1
        - timing:
            - ON for at most 4s
          then:
            - logger.log: Multi click 2
        - timing:
            - ON for at most 6s
          then:
            - logger.log: Multi click 3
        - timing:
            - ON for at most 8s
          then:
            - logger.log: Multi click 4
    ...

.. code-block:: yaml

    # device B
    binary_sensor:
    ...
    - platform: gpio
      id: BinarySensor1
      name: Some fancy name
      pin: 2
      on_multi_click:
        - timing:
            - ON for at most 1s
          then:
            - wifi_now.send:
                peerid: device_a
                service: Binary Sensor 1
                payloads:
                  - binary_sensor_event: !lambda wifi_now::WifiNowBinarySensorEvent::MULTI_CLICK1
        - timing:
            - ON for at most 2s
          then:
            - wifi_now.send:
                peerid: device_a
                service: Binary Sensor 1
                payloads:
                  - binary_sensor_event: !lambda wifi_now::WifiNowBinarySensorEvent::MULTI_CLICK2
        - timing:
            - ON for at most 3s
          then:
            - wifi_now.send:
                peerid: device_a
                service: Binary Sensor 1
                payloads:
                  - binary_sensor_event: !lambda wifi_now::WifiNowBinarySensorEvent::MULTI_CLICK3
        - timing:
            - ON for at most 4s
          then:
            - wifi_now.send:
                peerid: device_a
                service: Binary Sensor 1
                payloads:
                  - binary_sensor_event: !lambda wifi_now::WifiNowBinarySensorEvent::MULTI_CLICK4
    ...

The example maps the multiclick Events of abinary sensor on device_b to a binary sensor on device_a:

Note that the devices use different timings for the sensor.


See Also
--------

- :apiref:`esp_now/component.h`
- `Esspresif Esp-Now Userguide (ESP8266) <https://www.espressif.com/sites/default/files/documentation/esp-now_user_guide_en.pdf>`__.
- `Esspresif Esp Non-OS SDK (ESP8266) <https://www.espressif.com/sites/default/files/documentation/2c-esp8266_non_os_sdk_api_reference_en.pdf>`__.
- `Esspresif Esp-Now API (ESP32) <https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/network/esp_now.html>`__.
- :ghedit:`Edit`

.. toctree::
    :maxdepth: 1
    :glob:

    
