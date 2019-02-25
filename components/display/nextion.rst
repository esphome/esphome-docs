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

As the communication with the MH-Z19 is done using UART, you need to have an :ref:`UART bus <uart>`
in your configuration with ``rx_pin`` both the ``tx_pin`` set to the respective pins on the display.
Additionally, you need to set the baud rate to whatever baud rate you have set on the display. Default is 9600.

.. code-block:: yaml

    # Example configuration entry
    uart:
      rx_pin: D0
      tx_pin: D1
      baud_rate: 9600


    display:
      - platform: nextion
        lambda: |-
          it.set_component_value("gauge", 50);
          it.set_component_text("textview", "Hello World!");

Configuration variables:
------------------------

- **uart_id** (*Optional*, :ref:`config-id`): The ID of the :ref:`UART bus <uart>` you wish to use for this display.
  Use this if you want to use multiple UART buses at once.
- **lambda** (*Optional*, :ref:`lambda <config-lambda>`): The lambda to use for rendering the content on the nextion display.
  See :ref:`display-nextion_lambda` for more information.
- **update_interval** (*Optional*, :ref:`config-time`): The interval to call the lambda to update the display.
  Defaults to ``5s``.
- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.

.. _display-nextion_lambda:

Creating a HMI file
-------------------

First, you need to use the `Nextion Editor <https://nextion.itead.cc/resources/download/nextion-editor/>`__ to
create a display file. When you open up the editor create new project and set your device type (Device model is listed at the back of the display). 

Now in ``Preinitialize Event`` You have to type ``bkcmd=3``

.. figure:: images/nextion-HMI1.jpg
    :align: center
    :width: 75.0%

Then you can add whatever components you want to display.

If you want to enable touch for any component, you must check mark ``Send Component ID`` under the both ``Touch Press Event`` and ``Touch Release Event``. This will let your microcontroller know that this component has been pressed and released. 

.. figure:: images/nextion-HMI2.jpg
    :align: center
    :width: 75.0%

Rendering Lambda
----------------

With Nextion displays, a dedicated chip on the display itself does the whole rendering. ESPHome can only
send *instructions* to the display to tell it *how* to render something and *what* to render.

Then, in the rendering ``lambda``, you have 3 main methods
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


See Also
--------

- :doc:`index`
- :apiref:`display/nextion.h`
- `Simple Nextion Library <https://github.com/bborncr/nextion>`__ by `Bentley Born <https://github.com/bborncr>`__
- `Official Nextion Library <https://github.com/itead/ITEADLIB_Arduino_Nextion>`__ by `iTead <https://www.itead.cc/>`__
- :ghedit:`Edit`

.. disqus::
