ESP-ADF Speaker
===============

.. seo::
    :description: Instructions for settings up ESP-ADF supported board speakers in ESPHome.
    :image: esp-adf.svg

The ``esp_adf`` speaker platform allows automatic configuration of the speaker output
on :ref:`ESP-ADF supported boards <esp_adf-boards>`.

.. code-block:: yaml

    speaker:
      - platform: esp_adf

Configuration variables:
------------------------

- **id** (Optional, :ref:`config-id`): Manually specify the ID used for code generation.

See also
--------

- :doc:`ESP-ADF </components/esp_adf>`
- :doc:`ESP-ADF Microphone </components/microphone/esp_adf>`
- :ghedit:`Edit`
