Sensor Component
================

esphomelib has support for many different sensors. Each of them is a
platform of the ``sensor`` domain and each sensor has several base
configuration options.

.. _config-sensor:

Base Sensor Configuration
-------------------------

All sensors in esphomeyaml/esphomelib have a name and some other
optional configuration options. By default, the sensor platform will
chose appropriate values for all of these by default, but you can always
override them if you want to.

.. code:: yaml

    # Example sensor configuration
    name: Livingroom Temperature

    # Optional variables:
    unit_of_measurement: "°C"
    icon: "mdi:water-percent"
    accuracy_decimals: 1
    expire_after: 30s
    filters:
      - sliding_window_moving_average:
          window_size: 15
          send_every: 15

Configuration variables:

- **name** (**Required**, string): The name for the sensor.
- **unit_of_measurement** (*Optional*, string): Manually set the unit
  of measurement the sensor should advertise its values with. This does
  not actually do any maths (conversion between units).
- **icon** (*Optional*, icon): Manually set the icon to use for the sensor in the frontend.
- **accuracy_decimals** (*Optional*, int): Manually set the accuracy of decimals to use when reporting values.
- **expire_after** (*Optional*, :ref:`config-time`): Manually set the time in which
  the sensor values should be marked as “expired”/“unknown”. Not providing any value means no expiry.
- **filters** (*Optional*): Specify filters to use for some basic
  transforming of values. Defaults to a basic sliding window moving
  average over the last few values. See :ref:`Sensor Filters <sensor-filters>` for more information.

Automations:

- **on_value** (*Optional*, :ref:`Automation <automation>`): An automation to perform
  when a new value is published. See :ref:`sensor-on_value`.
- **on_value_range** (*Optional*, :ref:`Automation <automation>`): An automation to perform
  when a published value transition from outside to a range to inside. See :ref:`sensor-on_value_range`.
- **on_raw_value** (*Optional*, :ref:`Automation <automation>`): An automation to perform
  when a raw value is received that hasn't passed through any filters. See :ref:`sensor-on_raw_value`.
- All other options from :ref:`MQTT Component <config-mqtt-component>`.


.. note::

    If you're trying to setup filters for a sensor that has multiple outputs - for example a DHT22 which
    reports temperature *and* humidity - put the ``filters`` option into each sensor output like this:

    .. code:: yaml

        sensor:
          - platform: dht
            # ...
            temperature:
              filters:
                # ...
            humidity:
              filters:
                # ...

.. _sensor-filters:

Sensor Filters
--------------

esphomeyaml/esphomelib allow you to do some basic preprocessing of
sensor values before they’re sent to Home Assistant. This is for example
useful if you want to apply some average over the last few values to
relief Home Assistant’s state machine and keep the history graphs in the
front-end a bit more clean. More sophisticated filters should be done
with Home Assistant `filter
sensor <https://www.home-assistant.io/components/sensor.filter/>`__.

.. code:: yaml

    # Example filters:
    filters:
      - offset: 2.0
      - multiply: 1.2
      - filter_out: 42.0
      - filter_nan:
      - sliding_window_moving_average:
          window_size: 15
          send_every: 15
      - exponential_moving_average:
          alpha: 0.1
          send_every: 15
      - throttle: 1s
      - heartbeat: 5s
      - debounce: 0.1s
      - delta: 5.0
      - unique:
      - or:
        - throttle: 1s
        - delta: 5.0
      - lambda: return x * (9.0/5.0) + 32.0;

Above example configuration entry is probably a bit useless, but shows
every filter there is currently:

-  **offset**: Add an offset to every sensor value.
-  **multiply**: Multiply each sensor value by this number.
-  **filter_out**: Remove every sensor value that equals this number.
-  **filter_nan**: Remove every value that is considered ``NAN`` (not a
   number) in C.
-  **sliding_window_moving_average**: A `simple moving
   average <https://en.wikipedia.org/wiki/Moving_average#Simple_moving_average>`__
   over the last few values.

   -  **window_size**: The number of values over which to perform an
      average when pushing out a value.
   -  **send_every**: How often a sensor value should be pushed out. For
      example, in above configuration the weighted average is only
      pushed out on every 15th received sensor value.

-  **exponential_moving_average**: A simple `exponential moving
   average <https://en.wikipedia.org/wiki/Moving_average#Exponential_moving_average>`__
   over the last few values.

   -  **alpha**: The forget factor/alpha value of the filter.
   -  **send_every**: How often a sensor value should be pushed out.

-  **throttle**: Throttle the incoming values. When this filter gets an incoming value,
   it checks if the last incoming value is at least ``specified time period`` old.
   If it is not older than the configured value, the value is not passed forward.

-  **heartbeat**: Send the last value that this sensor in the specified time interval.
   So a value of ``10s`` will cause the filter to output values every 10s regardless
   of the input values.

-  **debounce**: Only send values if the last incoming value is at least ``specified time period``
   old. For example if two values come in at almost the same time, this filter will only output
   the last value and only after the specified time period has passed without any new incoming
   values.

-  **delta**: This filter stores the last value passed through this filter and only
   passes incoming values through if the absolute difference is greater than the configured
   value. For example if a value of 1.0 first comes in, it's passed on. If the delta filter
   is configured with a value of 5, it will now not pass on an incoming value of 2.0, only values
   that are at least 6.0 big or -4.0.

-  **unique**: This filter has no parameter and does one very simple thing: It only passes
   forward values if they are different from the last one that got through the pipeline.

-  **or**: Pass forward a value with the first child filter that returns. Above example
   will only pass forward values that are *either* at least 1s old or are if the absolute
   difference is at least 5.0.

-  **lambda**: Perform a simple mathematical operation over the sensor
   values. The input value is ``x`` and the result of the lambda is used
   as output. Each floating point operation should have ``.0`` attached
   as in above configuration. This will be copied over to the C++ code
   as a raw string.

Example: Converting Celsius to Fahrenheit
-----------------------------------------

While I personally don’t like the Fahrenheit temperature scale, I do
understand that having temperature values appear in the fahrenheit unit
is quite useful to some users. esphomelib uses the celsius temperature
unit internally, and I’m not planning on making converting between the
two simple (😉), but you can use this filter to convert celsius values to
fahrenheit.

.. code:: yaml

    filters:
      - lambda: return x * (9.0/5.0) + 32.0;
    unit_of_measurement: "°F"

.. _sensor-default_filter:

``update_interval`` gotchas
---------------------------

By default, esphomelib takes an average over the last 15 values before publishing updates.
This was done in order to automatically decrease sensor noise.
Therefore if you have an ``update_interval`` of 15 seconds, you will only see the values
every 3 and a half minutes or so. To disable the default filter and publish all raw values
directly, put an empty ``filters:`` block in your configuration:

.. code:: yaml

    sensor:
      - platform: ...
        filters:

Sensor Automation
-----------------

You can access the most recent state of the sensor in :ref:`lambdas <config-lambda>` using
``id(sensor_id).value`` and the most recent raw state using ``id(sensor_id).raw_value``.

.. _sensor-on_value:

``on_value``
************

This automation will be triggered when a new value that has passed through all filters
is published. In :ref:`Lambdas <config-lambda>` you can get the value from the trigger
with ``x``.

.. code:: yaml

    sensor:
      - platform: dallas
        # ...
        on_value:
          then:
            - light.turn_on:
                id: light_1
                red: !lambda "return x/255;"

Configuration variables: See :ref:`Automation <automation>`.

.. _sensor-on_value_range:

``on_value_range``
******************

With this automation you can observe if a sensor value passes from outside
a defined range of values to inside a range. For example you can have an
automation that triggers when a humidity crosses a threshold, and then turns on a dehumidifier.
This trigger will only trigger when the new value is inside the range and the previous value
was outside the range. It will also trigger on startup if the first value received is inside the range.

Define the range with ``above`` and ``below``. If only one of them is defined, the interval is half-open.
So for example ``above: 5`` with no below would mean the range from 5 to positive infinity.

.. code:: yaml

    sensor:
      - platform: dallas
        # ...
        on_value_range:
          above: 5
          below: 10
          then:
            - switch.turn_on:
                id: relay_1

Configuration variables:

- **above** (*Optional*, float): The minimum for the trigger.
- **below** (*Optional*, float): The maximum for the trigger.
- See :ref:`Automation <automation>`.

.. _sensor-on_raw_value:

``on_raw_value``
****************

This automation will be triggered when a new value that has passed through all filters
is published. In :ref:`Lambdas <config-lambda>` you can get the value from the trigger
with ``x``.

.. code:: yaml

    sensor:
      - platform: dallas
        # ...
        on_value:
          then:
            - light.turn_on:
                id: light_1
                red: !lambda "return x/255;"

Configuration variables: See :ref:`Automation <automation>`.

lambda calls
************

From :ref:`lambdas <config-lambda>`, you can call several methods on all sensors to do some
advanced stuff (see the full :doc:`API Reference </api/sensor/index>` for more info).

- ``push_new_value()``: Manually cause the sensor to push out a value. It will then
  be processed by the sensor filters, and once done be published to MQTT.

  .. code:: yaml

      // Within lambda, push a value of 42.0
      id(my_sensor).push_new_value(42.0);

- ``value``: Retrieve the current value of the sensor that has passed through all sensor filters.
  Is ``NAN`` if no value has gotten through all filters yet.

  .. code:: yaml

      // For example, create a custom log message when a value is received:
      ESP_LOGI("main", "Value of my sensor: %f", id(my_sensor).value);

- ``raw_value``: Retrieve the current value of the sensor that has not passed through any filters
  Is ``NAN`` if no value if no value has been pushed by the sensor itself yet.

  .. code:: yaml

      // For example, create a custom log message when a value is received:
      ESP_LOGI("main", "Raw Value of my sensor: %f", id(my_sensor).value);


See Also
********

- :doc:`API Reference </api/sensor/index>`
- `Edit this page on GitHub <https://github.com/OttoWinter/esphomedocs/blob/current/esphomeyaml/components/sensor/index.rst>`__

.. toctree::
    :maxdepth: 1

    adc
    ads1115
    bh1750
    ble_rssi
    bme280
    bme680
    bmp085
    bmp280
    custom
    dallas
    dht
    dht12
    duty_cycle
    esp32_hall
    hdc1080
    hlw8012
    hmc5883l
    htu21d
    hx711
    ina219
    ina3221
    max6675
    mhz19
    mpu6050
    ms5611
    pulse_counter
    rotary_encoder
    sht3xd
    tcs34725
    template
    tsl2561
    ultrasonic
    uptime
    wifi_signal
    xiaomi_miflora
    xiaomi_mijia

.. disqus::
