Voice Assistant
===============

.. seo::
    :description: Instructions for setting up a Voice Assistant in ESPHome.
    :image: voice-assistant.svg

ESPHome devices with a microphone are able to stream the audio to Home Assistant and be processed there by `assist <https://www.home-assistant.io/docs/assist/>`__.

.. note::

    Voice Assistant requires Home Assistant 2023.5 or later.

Configuration:
--------------

.. code-block::yaml

    microphone:
      - platform: ...
        id: mic_id

    voice_assistant:
      microphone: mic_id

- **microphone** (**Required**, :ref:`config-id`): The microphone to use for input.


.. _voice_assistant-actions:

Voice Assistant Actions
-----------------------

The following actions are available for use in automations:

``voice_assistant.start`` - Start listening for voice commands.
``voice_assistant.stop`` - Stop listening for voice commands.


Push to Talk
------------

Here is an example offering Push to Talk with a :doc:`/components/binary_sensor/index`.

.. code-block::yaml

    voice_assistant:
      microphone: mic_id

    binary_sensor:
      - platform: gpio
        pin: ...
        on_press:
          - voice_assistant.start:
        on_release:
          - voice_assistant.stop:


See Also
--------

- :doc:`microphone/index`
- :apiref:`voice_assistant/voice_assistant.h`
- :ghedit:`Edit`
