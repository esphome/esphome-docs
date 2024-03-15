Nextion TFT LCD Display
=======================

.. seo::
    :description: Instructions for setting up Nextion TFT LCD displays
    :image: nextion.jpg

The ``nextion`` display platform allows you to use Nextion LCD displays (`datasheet <https://nextion.itead.cc/resources/datasheets/>`__,
`iTead <https://www.itead.cc/display/nextion.html>`__) with ESPHome.

.. figure:: images/nextion-full.jpg
    :align: center
    :width: 75.0%

    Nextion LCD Display.

As communication with Nextion displays is done via a serial interface, you need to have a :ref:`UART bus <uart>` in
your ESPHome device's configuration with both the ``rx_pin`` and ``tx_pin`` defined. Both lines must also be physically
connected to the respective pins on the Nextion display itself.

.. warning::

    :ref:`uart-hardware_uarts` are **highly** recommended when using Nextion displays. Use of software serial (software
    UARTs) is known to cause problems with Nextion communication, especially at speeds greater than 9600 baud.

Nextion uses a baud rate of 9600 by default. **When** :ref:`uart-hardware_uarts` **are available,** higher speeds may
be configured. To configure a higher speed, in the `Nextion Editor <https://nextion.tech/nextion-editor/>`__, look for
lines in ``program.s`` similar to those shown below and modify them as follows:

.. code-block:: c++

    baud=115200   // Sets the baud rate to 115200
    bkcmd=0       // Tells the Nextion to not send responses on commands. This is the current default but can be set just in case

...and be sure to update your :ref:`UART bus <uart>` in your ESPHome device's configuration to match the new speed!

As an example, the following YAML configures a UART for use with a Nextion display:

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
- **touch_sleep_timeout** (*Optional*, int): Sets internal No-touch-then-sleep timer in seconds.
- **start_up_page** (*Optional*, int): Sets the page to display when ESPHome connects to the Nextion. (Nextion shows page 0 on start-up by default).
- **wake_up_page** (*Optional*, int): Sets the page to display after waking up
- **auto_wake_on_touch** (*Optional*, boolean): Sets if Nextion should auto-wake from sleep when touch press occurs.
- **exit_reparse_on_start** (*Optional*, boolean): Request the Nextion exit Active Reparse Mode before setup of the display. Defaults to ``false``.
- **on_setup** (*Optional*, :ref:`Action <config-action>`): An action to be performed after ESPHome connects to the Nextion. See :ref:`Nextion Automation <nextion-on_setup>`.
- **on_sleep** (*Optional*, :ref:`Action <config-action>`): An action to be performed when the Nextion goes to sleep. See :ref:`Nextion Automation <nextion-on_sleep>`.
- **on_wake** (*Optional*, :ref:`Action <config-action>`): An action to be performed when the Nextion wakes up. See :ref:`Nextion Automation <nextion-on_sleep>`.
- **on_page** (*Optional*, :ref:`Action <config-action>`): An action to be performed after a page change. See :ref:`Nextion Automation <nextion-on_page>`.
- **on_touch** (*Optional*, :ref:`Action <config-action>`): An action to be performed after a touch event (press or release). See :ref:`Nextion Automation <nextion-on_touch>`.
  
.. _display-nextion_lambda:

Rendering Lambda
----------------

Nextion displays have a dedicated processor on the display itself to handle all rendering. ESPHome only sends
*instructions* to the display to update variables in or UI elements on the display.

First, you need to use the `Nextion Editor <https://nextion.tech/nextion-editor/>`__ to create a "TFT" file for your
display. Once created, you'll transfer the TFT file to your Nextion display by either:

- a direct serial connection between the Nextion display and your PC,
- an SD card, or...
- the ``upload_tft`` action in ESPHome

Once the TFT file has been transferred to the Nextion display, you can use various API calls within ESPHome lambdas
to populate data on the display. For example:

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

    Although the ``display`` rendering lambda is most commonly used, updates to the Nextion can be performed by
    :ref:`other Nextion components <nextion_see_also>`, as well.

Please see :ref:`display-printf` for a quick introduction into the ``printf`` formatting rules and
:ref:`display-strftime` for an introduction into the ``strftime`` time formatting.

Lambda Calls
************

Several methods are available for use within :ref:`lambdas <config-lambda>`; these permit advanced functionality beyond simple
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

.. _display-nextion_automation:

Nextion Automation
------------------

With Nextion displays, it's possible to define several automation actions. Depending on your setup, you may or may not need to use some of them.

.. _nextion-on_setup:

``on_setup``
************

This automation will be triggered once ESP establishes a connection with Nextion. This happens after a boot up and may take some
noticeable time (e.g. hundreds of milliseconds) to establish a connection over UART. Typical use scenario for this automation is choosing of the initial
page to display depending on some runtime conditions or simply showing a page with a non-zero index (Nextion shows page 0 by default and ESPHome will
use ``start_up_page`` on connection, if set).

.. code-block:: yaml

    wifi:
      ap: {} # This spawns an AP with the device name and mac address with no password.

    captive_portal:

    display:
      - platform: nextion
        id: disp
        on_setup:
          then:
            lambda: |-
              // Check if WiFi hot-spot is configured
              if (wifi::global_wifi_component->has_sta()) {
                // Show the main page
                id(disp).goto_page("main_page");
              } else {
                // Show WiFi Access Point QR code for captive portal, see https://qifi.org/
                id(disp).goto_page("wifi_qr_page");
              }

.. _nextion-on_sleep:

``on_sleep / on_wake``
**********************

The action is called before and after Nextion goes to sleep mode. Nextion is not responsive while in sleep mode. Use these triggers to prepare your code
for that and :ref:`force-update <nextion_update_all_components>` the on-screen content once it's back.

.. _nextion-on_page:

``on_page``
***********

This automation is triggered when a page is changed on the Nextion display. This includes both ESP and Nextion initiated page changes.
ESP initiates a page change by calling ``goto_page("page_name")`` or ``goto_page(page_id)`` function. Nextion can change pages as a reaction to user's activity (e.g. clicks) or using a timer.
In either case, this automation can be helpful to update on-screen controls for the newly displayed page.

If you fully own your Nextoin HMI design and follow the best practice of setting the components' vscope to global in the Nextion Editor, you'll probably never need this trigger.
However, if this is not the case and all / some of your UI components have local visibility scope, ``on_page`` will be your remedy. Here you can initiate updates of the relevant components.

Before actually updating components, you need to understand which page Nextion was switched to. ``x`` argument will contain a page id integer.
Once you know the page id, it's time to update the components. Two strategies would be possible. The first one is to use :ref:`Nextion Sensors <nextion_sensor>` for every UI field and use one of the
:ref:`update functions <nextion_update_all_components>`. The second is to manually set component text or value for each field:

.. code-block:: yaml

    on_page:
      then:
        lambda: |-
          switch (x) {
            case 0x02: // wifi_qr_page
              // Manually trigger update for controls on page 0x02 here
              id(disp).set_component_text_printf("qr_wifi", "WIFI:T:nopass;S:%s;P:;;", wifi::global_wifi_component->get_ap().get_ssid().c_str());
              break;
          }

.. _nextion-on_touch:

``on_touch``
************

This automation is triggered when a component is pressed or released on the Nextion display.

The following arguments will be available:

  - ``page_id``: Contains the id (integer) of the page where the touch happened.

  - ``component_id``: Contains the id (integer) of the component touched. It's required that the component have "Send Component ID" enabled either for "Touch Press Event" and/or "Touch Release Event".

  - ``touch_event``: It will be ``true`` for a "press" event, or ``false`` for a "release" event.

.. code-block:: yaml

    on_touch:
      then:
        lambda: |-
          ESP_LOGD("nextion.on_touch", "Nextion touch event detected!");
          ESP_LOGD("nextion.on_touch", "Page Id: %i", page_id);
          ESP_LOGD("nextion.on_touch", "Component Id: %i", component_id);
          ESP_LOGD("nextion.on_touch", "Event type: %s", touch_event ? "Press" : "Release");

.. _nextion_upload_tft_file:

Uploading A TFT File
--------------------

ESPHome can download a file from ``tft_url`` and transfer it to the Nextion via its serial interface. Note that, during
the upload process, ESPHome will be unresponsive and only limited logging will take place.

ESPHome uses the same protocol as the `Nextion Editor <https://nextion.tech/nextion-editor/>`__ and only transfers
required portions of the TFT file so as to minimize the time required to update the Nextion display.

.. note::

    The upload engine uses insecure connections over HTTPS. You can host the file in a local web server
    to avoid insecure transfers over the public Internet.

Any modern web server--including Home Assistant itself--can host the TFT file.

Home Assistant
**************

To host the TFT file from Home Assistant, create a www directory if it doesn't exist in your config 
directory. You can create a subdirectory for those files as well.

For example if the file is located
under your configuration directory ``www/tft/default.tft`` the URL to access it will be
``http(s)://your_home_assistant_url:port/local/tft/default.tft``

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

.. _nextion_see_also:

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
