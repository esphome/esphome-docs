ESPHome IR HiFi amplifier control
=================================

.. seo::
    :description: The goal is to remote control the volume, a standard knob managing a potentiometer, and also switch the HiFi amplifier on and off.
    :image: ESPHome-IR-amplifier-control.jpg
    :keywords: IR servo mqtt ESPHome

The goal is to remote control the volume, a standard knob managing a potentiometer, and also switch the HiFi amplifier on and off.

The project is based on an ESP32 and ESPHome, to receive and decode the IR from a remote control. It can use any remote with a few minor adjustements.

For the ON/OFF the project uses a Shelly Plug S managed via web from Node-RED. One of the keys of the remote is decoded and triggers a MQTT message that Node-RED can capture and convert to a relay toggle order for the Shelly Plug. Of course any other smart plug can be used if it accepts commands via web.

.. figure:: images/ESPHome-IR-amplifier-control.jpg
    :align: center
    :width: 90.0%

The servo and the board are fixed with double sided tape, so everything is removable.

.. figure:: images/apple_remote.jpg
    :align: center
    :width: 20.0%

The remote used

.. figure:: images/servo_pulley.jpg
    :align: center
    :width: 10.0%

and the servo pulley (`servo_pulley.stl <https://github.com/deltazerorsan/ESPHome-IR-HiFi-amplifier-control/blob/master/ESPHome_yaml/irreceiver.yaml>`__)

So, the project needs:

- TSOP38238 to receive infrared signals
- ESP-WROOM-32 module (or any board with similar module)
- 360 degrees small servo (not a standard one, but 360 degrees)
- Appropriate belt
- some 3.3 power source
  - 5 volts to 3.3 converter (it can be onboard)
  - Wall 5 volts power supply (or something equivalent)
- Any smart plug like Shelly Plug S or similar

Infrastructure:

- WiFi network
- ESPHome running (in my case Hassio version)
- Node-RED running (in my case Hassio version) (`Download node here in JSON to import to Node-RED <https://github.com/deltazerorsan/ESPHome-IR-HiFi-amplifier-control/blob/master/ESPHome_yaml/ir_amplifier_control.ndr>`__)


This is the yaml code: (`Download irreceiver.yaml from here <https://github.com/deltazerorsan/ESPHome-IR-HiFi-amplifier-control/blob/master/ESPHome_yaml/irreceiver.yaml>`__)

.. code-block:: yaml

    substitutions:
      devicename: irreceiver
      uper_devicename: IR Receiver
      device_ip: 192.168.1.33            # use your own
    
    esphome:
      name: $devicename
      platform: ESP32
      board: esp-wrover-kit
    
      on_boot:
        priority: -10
        then:
          - servo.write:
              id: my_servo
              level: 0                   # put the servo in neutral (stoped)
          - delay: 100ms
          - servo.detach: my_servo       # always detach the servo to ensure it stops completely
          - lambda: 'id(my_global_timer) = millis();'
    
      on_loop:
        then:
          - if:
              condition:                 # this stops de servo after 300ms from a received order
                lambda: |-
                  if ((millis() > (id(my_global_timer) + 300)) and (id(my_global_attach))) {
                    id(my_global_attach) = false;
                    return true;
                  } else {
                    return false;
                  }
              then:
                - servo.write:
                    id: my_servo
                    level: 0
                - delay: 100ms
                - servo.detach: my_servo
                - lambda: 'ESP_LOGD("main", "Dettached");' # just to see in the logs that the timeout is working as expected
    
    globals:
      - id: my_global_level                                # the value to pass to the servo
        type: float
        restore_value: no
        initial_value: '0'
      - id: my_global_timer                                # the time to control de 300ms timeout
        type: ulong
        restore_value: no
        initial_value: '1000000'
      - id: my_global_attach                               # just to know inside the on_loop if the servo is attached
        type: boolean
        restore_value: no
        initial_value: 'false'
    
    wifi:
      networks:
        - ssid: !secret wifi2_ssid
          password: !secret wifi_pass
        - ssid: !secret wifi_ssid
          password: !secret wifi_pass
        - ssid: !secret wifi3_ssid
          password: !secret wifi_pass
      manual_ip:
        static_ip: $device_ip
        gateway: 192.168.1.1
        subnet: 255.255.255.0
        dns1: !secret dns1
        dns2: !secret dns2
    
    # Enable logging
    logger:
    
    # Enable Home Assistant API
    api:
      password: !secret api_pass
      
    ota:
      password: !secret ota_pass
    
    mqtt:
      broker: !secret broker_ip
    
    remote_receiver:
      pin:
        number: 32
        inverted: true
      dump: lg                         # you can comment this line out when every keys is known
      
     on_lg:
    #                                  0.15 slow ccw rotation to lower the volume
    #                                     1 fast ccw rotation to fast lower the volume
    #                                 -0.15 slow cw rotation to raise the volume
    #                                     0 for later use to send mqtt message 
        then:
          - lambda: 'id(my_global_timer) = millis();'
          - lambda: 'id(my_global_attach) = true;'
          - servo.write:
              id: my_servo
              level: !lambda |-
                switch (x.data) {
                  case 2011279369:
                    id(my_global_level) = 0.15;
                    return id(my_global_level);
                  case 2011242505:
                    id(my_global_level) = 1;
                    return id(my_global_level);
                  case 2011287561:
                    id(my_global_level) = -0.15;
                    return id(my_global_level);
                  case 2011250697:
                    id(my_global_level) = 0;
                    return id(my_global_level);
                  default:
                    id(my_global_level) = 1;
                    return 0;
                }
          - lambda: 'ESP_LOGD("main", "x = %d", x.data);'                             # show the code of the remote key pressed
          - lambda: 'ESP_LOGD("main", "my_global_level = %f", id(my_global_level));'  # show the value passed to the servo
          - if:
              condition:                                                              # uses the 0 value to trigger the mqtt message
                lambda: |-
                  if (id(my_global_level) == 0) {
                    return true;
                  } else {
                    return false;
                  }
              then:
                - mqtt.publish:
                    topic: Amplificador/SW1                                           # this topic is the one used in Node-RED
                    payload: "SW"
                - lambda: 'ESP_LOGD("main", "SW = %f", id(my_global_level));'

    servo:
      - id: my_servo
        output: pwm_output
        idle_level: 7.40%     # those three values depend on your servo
        min_level: 6%         # you must adjust it by trial and error
        max_level: 9.5%       # until the servo stops BEFORE the detach
    
    output:
      - platform: ledc
        id: pwm_output
        pin: 12               # adapt to your needs
        frequency: 50 Hz

See Also
--------

- :doc:`/components/remote_receiver`
- :doc:`/components/servo`
- :doc:`/components/mqtt`
- :ghedit:`Edit`
