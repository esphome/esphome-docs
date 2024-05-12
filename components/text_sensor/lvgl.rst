.. _lvgl-txs:

LVGL Text Sensor
================

.. seo::
    :description: Instructions for setting up an LVGL Text Sensor.
    :image: ../images/lvgl_c_txt.png

The ``lvgl`` text platform creates a Text Sensor from an LVGL textual widget
and requires :ref:`LVGL <lvgl-main>` to be configured.

Supported widgets are :ref:`lvgl-wgt-lbl` and :ref:`lvgl-wgt-txt`. A single text sensor supports only a single widget; in other words, it's not possible to have multiple widgets associated with a single ESPHome text sensor component.

Configuration variables:
------------------------

- **widget** (**Required**): The ID of a ``textarea`` widget configured in LVGL, which will reflect the state of the text sensor.
- All other variables from :ref:`Text Sensor <config-text_sensor>`.

Example:

.. code-block:: yaml

    text_sensor:
      - platform: lvgl
        widget: textarea_id
        name: "Textarea 1 text"

.. note::

    Widget-specific actions (``lvgl.label.update``, ``lvgl.textarea.update``) will trigger correspponding component updates to be sent to Home Assistant.

See Also
--------
- :ref:`LVGL Main component <lvgl-main>`
- :ref:`Label widget <lvgl-wgt-lbl>`
- :ref:`Textarea widget <lvgl-wgt-txt>`
- :doc:`/components/binary_sensor/lvgl`
- :doc:`/components/sensor/lvgl`
- :doc:`/components/number/lvgl`
- :doc:`/components/switch/lvgl`
- :doc:`/components/light/lvgl`
- :doc:`/components/select/lvgl`
- :doc:`/components/text/lvgl`
- :ghedit:`Edit`
