ESP-ADF Microphone
==================

.. seo::
    :description: Instructions for settings up ESP-ADF supported board microphones in ESPHome.
    :image: esp-adf.svg

The ``esp_adf`` microphone platform allows automatic configuration of the microphone input
on ESP-ADF supported boards.

.. code-block:: yaml

    microphone:
      - platform: esp_adf

Configuration variables:
------------------------

- **id** (Optional, :ref:`config-id`): Manually specify the ID used for code generation.

See also
--------

- :doc:`ESP-ADF </components/esp_adf>`
- :doc:`ESP-ADF Speaker </components/speaker/esp_adf>`
- :ghedit:`Edit`
