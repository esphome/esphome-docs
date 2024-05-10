.. _lvgl-txt:

LVGL Text
=========

.. seo::
    :description: Instructions for setting up an LVGL textarea Text component.
    :image: ../images/lvgl_c_txt.png

The ``lvgl`` text platform creates an editable text component from an LVGL textarea widget
and requires :ref:`LVGL <lvgl-main>` to be configured.

Supported widget is :ref:`lvgl-wgt-txt`. A single text component supports
a single widget, thus you need to choose among which one's state you want to use.


Configuration options:
----------------------

- **id** (*Optional*, :ref:`config-id`): Manually specify the ID used for code generation.
- **name** (**Required**, string): The name of the text component.
- **widget** (**Required**): The ID of a ``textarea`` widget configured in LVGL, which will reflect the state of the text component.
- All other options from :ref:`Text <config-text>`.

Example:

.. code-block:: yaml

    text:
      - platform: lvgl
        widget: textarea_id
        name: "Textarea 1 text"

See Also
--------
- :ref:`LVGL Main component <lvgl-main>`
- :ref:`Textarea widget <lvgl-wgt-txt>`
- :doc:`/components/binary_sensor/lvgl`
- :doc:`/components/sensor/lvgl`
- :doc:`/components/number/lvgl`
- :doc:`/components/switch/lvgl`
- :doc:`/components/light/lvgl`
- :doc:`/components/select/lvgl`
- :doc:`/components/text_sensor/lvgl`
- :ghedit:`Edit`
