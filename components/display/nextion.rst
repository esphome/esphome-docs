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
The Nextion uses a baud rate of 9600 by default. It may be configured to use a faster speed by adding (for
example) 

.. code-block:: c++

    baud=115200   // Sets the baud rate to 115200
    bkcmd=0       // Tells the Nextion to not send responses on commands. This is the current default but can be set just in case

 
  
to the ``program.s`` source file (in the Nextion Editor) before the ``page`` line.
This permits faster communication with the Nextion display and it is highly recommended when using :ref:`uart-hardware_uarts`. Without a hardware uart make sure to set the baud rate to 9600.


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
  See :ref:`display-nextion_lambda` for more information. This is typically empty. The individual components for the Nextion will handle almost all features needed for updating
- **update_interval** (*Optional*, :ref:`config-time`): The interval to call the lambda to update the display.
  Defaults to ``5s``.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **tft_url** (*Optional*, string): The URL to download the TFT file from for updates. See :ref:`Nextion Upload <nextion_upload_tft>`.
- **on_sleep** (*Optional*, :ref:`Action <config-action>`): An automation to perform when the Nextion goes to sleep.
- **on_wake** (*Optional*, :ref:`Action <config-action>`): An automation to perform when the Nextion wakes up.
- **touch_sleep_timeout** (*Optional*, int): Sets internal No-touch-then-sleep timer in seconds.
- **wake_up_page** (*Optional*, int): Sets the page to display after waking up
- **auto_wake_on_touch** (*Optional*, boolean): Sets if Nextion should auto-wake from sleep when touch press occurs.
  

.. _display-nextion_lambda:
Rendering Lambda
----------------

With Nextion displays, a dedicated chip on the display itself does the whole rendering. ESPHome can only
send *instructions* to the display to tell it *how* to render something and *what* to render.

First, you need to use the `Nextion Editor <https://nextion.itead.cc/resources/download/nextion-editor/>`__ to
create a display file and insert it using the SD card slot. Then, in the rendering ``lambda``, you can use the various API calls
to populate data on the display:

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

.. note::

    Although you can use the rendering lambda most, if not all, updates to the Nextion can be handled by the individual Nextion components. **See Below**

Please see :ref:`display-printf` for a quick introduction into the ``printf`` formatting rules and
:ref:`display-strftime` for an introduction into the ``strftime`` time formatting.

Lambda Calls
************

Several methods are available for use within :ref:`lambdas <config-lambda>` ; these permit advanced functionality beyond simple
display updates. See the full :apiref:`nextion/nextion.h` for more info. 

.. _nextion_upload_tft:

- ``upload_tft``: Start the upload process. See :ref:`nextion_upload_tft_file`

The developer tools in Home Assistant can be used to trigger the update. The below code block is an example on how to set this up.
  .. code-block:: yaml

      api:
        services:
          - service: update_nextion
            then:
              - lambda: 'id(nextion1)->upload_tft();' 

.. _nextion_update_all_components:

- ``update_all_components()``: All the components will publish their states.

  .. code-block:: c++

      id(nextion1).update_all_components();

.. _update_components_by_prefix:

- ``update_components_by_prefix(std::string page)``: This will send the current state of any **component_name** matching the prefix. Some settings like background color need to be resent on page change. This is a good hook for that.

  .. code-block:: c++

      id(nextion1).update_components_by_prefix("page0.");

.. _set_nextion_sensor_state:

- ``set_nextion_sensor_state(NextionQueueType queue_type, std::string name, float state);`` : Sets the sensor state. See :ref:`Queue Types <nextion_queue_types>`
- ``set_nextion_sensor_state(int queue_type, std::string name, float state);`` : Sets the sensor state. See :ref:`Queue Types <nextion_queue_types>`

- ``set_nextion_text_state(std::string name, std::string state);`` : Sets the text sensor state

.. note::

    Below is a method for HASS to send updates to the Nextion by code.

    .. code-block:: yaml

        # Enable Home Assistant API
        api:
          services:
            - service: set_nextion_sensor
              variables:
                nextion_type: int
                name: string
                state: float
              then:
                - lambda: |-
                    id(nextion1).set_nextion_sensor_state(nextion_type,name,state);
            - service: set_nextion_text
              variables:
                name: string
                state: string
              then:
                - lambda: |-
                    id(nextion1).set_nextion_text_state(name,state);

.. _nextion_queue_types:

 Queue Types: 
  - SENSOR            0
  - BINARY_SENSOR     1
  - SWITCH            2
  - TEXT_SENSOR       3
  - WAVEFORM_SENSOR   4
  - NO_RESULT         5

.. _nextion_upload_tft_file:

Uploading A TFT File
--------------------
This will download the file from the tft_url and will transfer it over the UART to the Nextion.
Once completed both the ESP and Nextion will reboot. During the upload process esphome will be 
unresponsive and no logging will take place. This uses the same protocol as the Nextion editor and
only updates the changes of the TFT file. If HTTPS/SSL is enabled it will be about 1kB/sec.

.. warning::

    If :ref:`uart-hardware_uarts` are not available then inconsistent results WILL occur. Lowering the speed to 9600 baud may help.


To host the TFT file you can use Home Assistant itself or any other web server. HTTPS, while always recommended on any network, will greatly reduce the upload speed.

Home Assistant
**************
To host the TFT file from Home Assistant, create a www directory if it doesn't exist in your config 
directory. You can create a subdirectory for those files as well.

For example if the file is located
under your configuration directory ``www/tft/default.tft`` the URL to access it will be
``http(s)://your_home_assistant_url:port/local/tft/default.tft``

NGINX
*****

`NGINX <https://www.nginx.com/>`__

The below NGINX example configuration will serve files out of the /var/www/nextion directory.

.. code-block:: nginx

    server {
      listen 80;    
      access_log  /var/log/nginx/nextion_access.log;    
      error_log  /var/log/nginx/nextion_error.log;
      root /var/www/nextion;
    }



Components
----------
This library supports a few different components allowing communication back and forth from HA <-> MCU <-> Nextion.

.. note::

    If the Nextion is sleeping or if the component was set to be hidden, it will not update its components even if updates are sent.
    After the Nextion wakes up, all components will send their states to the Nextion to get around this.

With the exception of the :doc:`../binary_sensor/nextion` that has the ``page_id``/``component_id`` options configured, the example below illustrates:
 - Polling the Nextion for updates
 - Dynamic updates sent from the Nextion to the ESP device

 .. code-block:: yaml

     sensor:
       - platform: nextion
         nextion_id: nextion1
         name: "n0"
         component_name: n0
       - platform: nextion
         id: current_page
         name: "current_page"
         variable_name: dp
         update_interval: 1s


Note that the first one requires a custom protocol to be included in the Nextion display's code/configuration. See the individual components for more detail.

See Also
--------

- :doc:`index`
- :doc:`../binary_sensor/nextion`
- :doc:`../sensor/nextion`
- :doc:`../switch/nextion`
- :doc:`../text_sensor/nextion`
- :doc:`../uart`
- :apiref:`nextion/nextion.h`
- `Simple Nextion Library <https://github.com/bborncr/nextion>`__ by `Bentley Born <https://github.com/bborncr>`__
- `Official Nextion Library <https://github.com/itead/ITEADLIB_Arduino_Nextion>`__ by `iTead <https://www.itead.cc/>`__
- :ghedit:`Edit`
