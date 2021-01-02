Nextion TFT LCD Display
=======================

.. seo::
    :description: Instructions for setting up Nextion TFT LCD displays
    :image: nextion.jpg

The ``nextion`` display platform allows you to use Nextion LCD displays (`datasheet <https://nextion.itead.cc/resources/datasheets/>`__,
`iTead <https://www.itead.cc/display/nextion.html>`__)
with ESPHome.

.. figure:: images/nextion-full.jpg
    :align: center
    :width: 75.0%

    Nextion LCD Display.

As the communication with the Nextion LCD display is done using UART, you need to have an :ref:`UART bus <uart>`
in your configuration with ``rx_pin`` both the ``tx_pin`` set to the respective pins on the display.
By default the baud rate is 9600. To change that to something else (115200) add ``baud=115200``
in your program.s before the page line. This will set the nextion to listen on 115200 which is highly recommended.

The below example configures a UART for the Nextion display to use

.. code-block:: yaml

    # Example configuration entry
    uart:
      id: uart_2
      rx_pin: GPIO16
      tx_pin: GPIO17
      baud_rate: 115200


    display:
      - platform: nextion
        id: nextion1
        uart_id: uart_2      
        lambda: |-
          it.set_component_value("gauge", 50);
          it.set_component_text("textview", "Hello World!");

Configuration variables:
------------------------

- **uart_id** (*Optional*, :ref:`config-id`): The ID of the :ref:`UART bus <uart>` you wish to use for this display.
  Use this if you want to use multiple UART buses at once.
- **brightness** (*Optional*, percentage): Set display brightness in %. Defaults to ``100%``
- **lambda** (*Optional*, :ref:`lambda <config-lambda>`): The lambda to use for rendering the content on the nextion display.
  See :ref:`display-nextion_lambda` for more information.
- **update_interval** (*Optional*, :ref:`config-time`): The interval to call the lambda to update the display.
  Defaults to ``5s``.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **tft_url** (*Optional*, string): The URL to download the TFT file from for updates. See :ref:`nextion_upload_tft`.
- **on_sleep** (*Optional*, :ref:`Action <config-action>`): An automation to perform
  when the Nextion goes to sleep. See :ref:`nextion_on_sleep_on_wake`.
- **on_wake** (*Optional*, :ref:`Action <config-action>`): An automation to perform
  when the Nextion wakes up. See :ref:`nextion_on_sleep_on_wake`.

.. _display-nextion_lambda:
 
Rendering Lambda
----------------

With Nextion displays, a dedicated chip on the display itself does the whole rendering. ESPHome can only
send *instructions* to the display to tell it *how* to render something and *what* to render.

First, you need to use the `Nextion Editor <https://nextion.tech/nextion-editor/>`__ to
create a display file and insert it using the SD card slot. Then, in the rendering ``lambda``, you have 3 main methods
you can call to populate data on the display:

.. code-block:: yaml

    display:
      - platform: nextion
        # ...
        lambda: |-
          // set the "value" of a component - value is always an integer
          // for example gauges represent their status using integers from 0 to 100
          it.set_component_value("gauge", 50);

          // set the text of a component
          it.set_component_text("textview", "Hello World!");

          // set the text of a component with formatting
          it.set_component_text_printf("textview", "The uptime is: %.1f", id(uptime_sensor).state);


Please see :ref:`display-printf` for a quick introduction into the ``printf`` formatting rules and
:ref:`display-strftime` for an introduction into the ``strftime`` time formatting.

lambda calls
************

From :ref:`lambdas <config-lambda>`, you can call several methods do some
advanced stuff (see the full API Reference for more info).

.. _nextion_upload_tft:

- ``upload_tft``: Start the upload process. This will download the file from
              the tft_url and will transfer it over the UART to the Nextion
              Once completed both the MCU and Nextion will reboot.
              During this process esphome will be unresponsive and no logging
              will take place. This is slow on an ESP32 @115200 baud expect around
              10kB/sec

  .. code-block:: yaml

      // Template switch. When turned on it will start the upload proccess
      - platform: template
        name: "Upgrade TFT File"
        turn_on_action:
          - lambda: |-
            id(n1)->upload_tft();      

.. _nextion_on_sleep_on_wake:

- ``on_sleep``/``on_wake``: Retrieve the current state of the switch.

  .. code-block:: yaml

      // Within lambda
      on_sleep:
        then:
          lambda: 'ESP_LOGD("display","Display went to sleep");'
      on_wake:
        then:
          lambda: 'ESP_LOGD("display","Display woke up");'

Components
----------
This library supports a few different components allowing communication back and forth from HA <-> MCU <-> Nextion.
Except for the - :doc:`../binary_sensor/nextion` the below handles polling data from the Nextion as well as the Nextion
sending updates via the - :doc:`../binary_sensor/nextion` or from a custom protocol that needs to be added to the Nextion
components. Refer to the below for more information.

- :doc:`../binary_sensor/nextion`
- :ref:`nextion_sensor`

See Also
--------

- :doc:`index`
- :doc:`/components/binary_sensor/nextion`.
- :doc:`/components/sensor/nextion`.
- :apiref:`nextion/nextion.h`
- `Simple Nextion Library <https://github.com/bborncr/nextion>`__ by `Bentley Born <https://github.com/bborncr>`__
- `Official Nextion Library <https://github.com/itead/ITEADLIB_Arduino_Nextion>`__ by `iTead <https://www.itead.cc/>`__
- :ghedit:`Edit`
