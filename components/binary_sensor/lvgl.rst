.. _lvgl-bse:

LVGL Binary Sensor
==================

.. seo::
    :description: Instructions for setting up an LVGL widget binary sensor.
    :image: ../images/lvgl_c_bns.png

The ``lvgl`` binary sensor platform creates a binary sensor from an LVGL widget
and requires :ref:`LVGL <lvgl-main>` to be configured.

Supported widget is :ref:`lvgl-wgt-btn`. A single binary sensor supports
only a single widget; it is not possible to have a single binary sensor respond to multiple widgets.

Configuration options:
----------------------

- **widget** (**Required**): The ID of a supported widget configured in LVGL, which will reflect the state of the binary sensor.
- All other options from :ref:`Binary Sensor <config-binary_sensor>`.

Example:

.. code-block:: yaml

    binary_sensor:
      - platform: lvgl
        widget: btn_id
        name: LVGL push button

See Also
--------
- :ref:`LVGL Main component <lvgl-main>`
- :ref:`Button widget <lvgl-wgt-btn>`
- :doc:`/components/sensor/lvgl`
- :doc:`/components/number/lvgl`
- :doc:`/components/switch/lvgl`
- :doc:`/components/select/lvgl`
- :doc:`/components/light/lvgl`
- :doc:`/components/text/lvgl`
- :doc:`/components/text_sensor/lvgl`
- :ghedit:`Edit`
