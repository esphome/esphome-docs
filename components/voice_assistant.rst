Voice Assistant
===============

.. seo::
    :description: Instructions for setting up a Voice Assistant in ESPHome.
    :image: voice-assistant.svg

ESPHome devices with a microphone are able to stream the audio to Home Assistant and be processed there by `assist <https://www.home-assistant.io/voice_control/>`__.

.. note::

    Voice Assistant requires Home Assistant 2023.5 or later.

Configuration:
--------------

.. code-block:: yaml

    microphone:
      - platform: ...
        id: mic_id

    voice_assistant:
      microphone: mic_id

- **microphone** (**Required**, :ref:`config-id`): The :doc:`microphone </components/microphone/index>` to use for input.
- **speaker** (*Optional*, :ref:`config-id`): The :doc:`speaker </components/speaker/index>` to use to output the response.
- **on_start** (*Optional*, :ref:`Automation <automation>`): An automation to
  perform when the voice assistant starts listening.
- **on_end** (*Optional*, :ref:`Automation <automation>`): An automation to perform
  when the voice assistant is finished all tasks.
- **on_stt_end** (*Optional*, :ref:`Automation <automation>`): An automation to perform
  when the voice assistant has finished speech-to-text. The resulting text is
  available to automations as the variable ``x``.
- **on_tts_start** (*Optional*, :ref:`Automation <automation>`): An automation to perform
  when the voice assistant has started text-to-speech. The text to be spoken is
  available to automations as the variable ``x``.
- **on_tts_end** (*Optional*, :ref:`Automation <automation>`): An automation to perform
  when the voice assistant has finished text-to-speech. A URL containing the audio response
  is available to automations as the variable ``x``.
- **on_error** (*Optional*, :ref:`Automation <automation>`): An automation to perform
  when the voice assistant has encountered an error. The error code and message are available to
  automations as the variables ``code`` and ``message``.

.. _voice_assistant-actions:

Voice Assistant Actions
-----------------------

The following actions are available for use in automations:

- ``voice_assistant.start`` - Start listening for voice commands.
- ``voice_assistant.stop`` - Stop listening for voice commands.


Push to Talk
------------

Here is an example offering Push to Talk with a :doc:`/components/binary_sensor/index`.

.. code-block:: yaml

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
