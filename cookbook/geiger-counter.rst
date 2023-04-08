Geiger counter RadiationD v1.1 (CAJOE)
======================================

.. seo::
    :description: Instructions for setting up RadiationD v1.1(CAJOE) sensor in ESPHome and calculate the current radation level.
    :image: radiationD-v1-1-cajoe_small.jpg
    :keywords: Radiation Geiger counter

With the help of :doc:`/components/sensor/pulse_counter` and the RadiationD v1.1(CAJOE) you can make your own Geiger counter, which will give you 
a more or less precise messurement of the current radation level. But it should be good enough to warn you about critical events.  


Assembly:
---------

.. figure:: images/radiationD-v1-1-cajoe_small.jpg
    :align: center
    :width: 100.0%

The first step is to connect the sensor.

You just need to connect the +5V, the ground and a GPIO pin to the ESP.
In my case I used the pin 34 for the signal. (The print on the PCB is wrong VIN is the signal.)
This setup should give you the pulse of each messurement or count. For more information check the Video of `Andreas Spiess <https://www.youtube.com/watch?v=K28Az3-gV7E>`__.

Housing:
********
I just 3D printed an small housing the avoid touching the high voltage Geiger Mueller tube.
`Counter Tube Case <https://www.thingiverse.com/thing:5425224>`__
(The tube should not be in direct sunlight. So maybe you will need another case.)


Configuration:
--------------

The block :doc:`/components/sensor/pulse_counter` will count the radation events per minute. 
With the found specs of the tube you will be able to calculate the radiation in μSv/h.

It's just the counts per minute (CPM) times the factor of your Geiger Mueller tube you're using. It should be the J305ß, which comes with the PCB.
(To make sure - check your printing on the tube)

μSv/h = (CPM - Tube noise) * Factor
According to the video of `Andreas Spiess <https://www.youtube.com/watch?v=K28Az3-gV7E>`__ the tube should have about 12 CPM as background noise.

.. note::

    The current version of the pack comes with the J305ß Geiger tube which detectes Beta and Gamma radiation. Specifications:     
    Manufacturer: North Optic     Radiation Detection: β, γ     Length: 111mm     Diameter: 11mm     Recommended Voltage: 350V     Plateau Voltage: 360-440V     
    Sensitivy γ (60Co): 65cps/(μR/s)     
    Sensitivy γ (equivalent Sievert): 108cpm / (μSv/h)     
    Max cpm: 30000     
    cps/mR/h: 18     
    cpm/m/h: 1080     
    cpm/μSv/h: 123.147092360319     
    Factor: 0.00812037037037


`Source: opengeiger.de/LibeliumDoku.pdf <http://www.opengeiger.de/LibeliumDoku.pdf>`__.


.. code-block:: yaml

    sensor:
      - platform: pulse_counter
        pin: 34
        name: "Radiation"
        unit_of_measurement: 'μSv/h'
        count_mode:
         rising_edge: DISABLE
         falling_edge: INCREMENT
        filters:
          - offset: -12.0 # J305ß Geiger Mueller tube background noise 0.2 pulses / sec x 60 sec = 12 CPM (Counts per Minute)
          - multiply: 0.00812037037037 # Factor: 0.00812037037037


See Also
--------

- :doc:`/components/sensor/pulse_counter`
- :ghedit:`Edit`


Geiger counter GGreg20_V3 with pulse output
===========================================

.. seo::
    :description: Instructions for setting up IoT-devices GGreg20_V3 sensor in ESPHome and calculate the current radiation level.
    :image: ggreg20_v3-geiger-counter_.jpg
    :keywords: Radiation Geiger counter pulse output

With the help of :doc:`/components/sensor/pulse_counter` and the GGreg20_V3 module with SBM20 or J305 GM tube and pulse output you can make your own 
Geiger counter, which will give you measurement of the current ionizing radiation level. It is useful to build a pocket or stationary device.  


Connection:
-----------

.. figure:: images/ggreg20_v3-geiger-counter.jpg
    :align: center
    :width: 40.0%

The first step is to connect the sensor to the MCU.

You just need to connect the power ('-Bat+' JST connector) and the ('Out' JST connector) to the ground and a GPIO pin of the MCU (ESP32, ESP8266, RPi).
In our example we use the ESP32 GPIO23 pin as a pulse input signal.

This basic setup makes the output pulses count by the MCU possible. For more information see our detailed config example at `GitHub repo <https://github.com/iotdevicesdev/GGreg20_V3-ESP32-HomeAssistant-ESPHome>`__.

Housing:
********
We recommend using a protective 3d-printed plastic case with the module to avoid accidental electric shocks when working with the GGreg20_V3.
`Sefety Case <https://sketchfab.com/iot-devices/collections/ggreg20_v3-case-d7fb99552f054ad5a7960c43e66bae18>`__
(The J305 tube also should not be in direct sunlight.)


Configuration:
--------------

The block :doc:`/components/sensor/pulse_counter` will count the radation events per minute. 
With the found specs of the tube you will be able to calculate the absorbed radiation equivalent dose by human body in μSv/h.

J305 GM tube factor for the human body phantom model is: 
********************************************************
* If datasheet specifies that "Sensitivy γ (60Co): 65 cps/(µR/s)" then: 0.00812 µSv/h per 1 CPM (or 123,1470924 CPM per 1 µSv/h)

* But if it specifies that sensitivy γ (60Co): 44 cps/(mR/h) then: 0,00332 µSv per CPM (or 301,0262258 CPM per 1 µSv/h)


SBM20 GM tube factor for the human body phantom model is: 
*********************************************************
* Magic factor from the internet forums: 0.0057 µSv/h per 1 CPM or 175,4385964 CPM per 1 µSv/h

* If datasheet specifies γ sensitivy 240-280 CPS/(µR/second) at Cs-137 source, then: 0.00812 µSv/h per 1 CPM or 123,1470924 CPM per 1 µSv/h (our calculation for a soviet-made tubes for the human body phantom model)

* But if it specifies that γ sensitivy is 78 imp/mR, then: 0.00664 µSv/h per 1 CPM or 150,5131129 CPM per 1 µSv/h (our calculation against a modern datasheet for the human body phantom model)

It's just the counts per minute (CPM) times the factor of your Geiger Mueller tube you're using.

So, absorbed equivalent dose for human body model formula is: 
***************************************************************
*μSv/h = (CPM - Tube noise) * Factor*

Tube noise values:
******************

* SBM20 datasheet states that tube-to-tube measurement error may vary +-20%. So it means near +-4 Counts per minute at normal background.

* J305 datasheet states that internal tube noise is 0.2 counts per second (i.e. 12 Counts per minute at normal background).


.. note::

    The current version of the pack GGreg20_V3 comes both with the J305ß tube or SBM20 tube as user options. Both GM-tubes detect Beta and Gamma radiation. 

Full code example for both SBM20 or J305 tubes
***********************************************
.. code-block:: yaml

    sensor:
    - platform: pulse_counter
      pin: GPIO23
      unit_of_measurement: 'CPM'
      name: 'Ionizing Radiation Power CPM'
      count_mode: 
        rising_edge: DISABLE
        falling_edge: INCREMENT # GGreg20_V3 uses Active-Low logic
    # It seems that only one instance of pulse counter internal filters can be set
    # So here no any debounce filters for CPM value 
    #  use_pcnt: False
    #  internal_filter: 190us
      update_interval: 60s
      accuracy_decimals: 0
      id: my_cpm_meter

    - platform: pulse_counter
      pin: GPIO23
      unit_of_measurement: 'μSv/Hour'
      name: 'Ionizing Radiation Power'
      count_mode: 
        rising_edge: DISABLE
        falling_edge: INCREMENT
      # Hardware counter alows only 13us debounce, so we set it OFF:
      use_pcnt: False
      # When hw counter is OFF then we may set our filter time to SBM20 190 us Deadtime value or any other (also in microseconds):
      internal_filter: 190us
      update_interval: 60s
      accuracy_decimals: 3
      id: my_dose_meter
      filters:
        - sliding_window_moving_average: # 5-minutes moving average (MA5) here
            window_size: 5
            send_every: 5      
      # Use this with SBM20 tube:
        - offset: -4.0 # SBM20 GM-tube internal measurement error at background 20 CPM (Counts per Minute)
        - multiply: 0.00812 # SBM20 tube conversion factor of pulses into uSv/Hour 
      # Use this with J305 tube:
      # - offset: -12.0 # J305 GM-tube internal background noise 0.2 pulses / sec x 60 sec = 12 CPM (Counts per Minute)
      # - multiply: 0.00332 # J305 Factor: 0.00332

See Also
--------

- :doc:`/components/sensor/pulse_counter`
- :ghedit:`Edit`
