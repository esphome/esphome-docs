Micro Wake Word
================

.. seo::
    :description: Instructions for creating a custom wake word using microWakeWord.
    :image: voice-assistant.svg

ESPHome implements an on-device wake word detection framework from `microWakeWord <https://github.com/kahrendt/microWakeWord>`__.
This repository/library allows you to create a custom wake word for your ESPHome device.

The training process is described on the `microWakeWord GitHub repository <https://github.com/kahrendt/microWakeWord>`__.

The ``micro_wake_word`` component requires an **ESP32-S3 with PSRAM** to function.

.. code-block:: yaml

    # Shorthand name
    micro_wake_word:
      model: okay_nabu

    # Github shorthand URL
    micro_wake_word:
      model: github://esphome/micro-wake-word-models/models/okay_nabu.json

Configuration variables:
------------------------

- **model** (**Required**, string): The model to use. This can be one of:

  - A simple name of a model that exists in the official `ESPHome Models repository <https://github.com/esphome/micro-wake-word-models>`__.
    e.g. ``okay_nabu``.
  - A github shorthand URL to a model JSON file.
    e.g. ``github://esphome/micro-wake-word-models/models/okay_nabu.json@main``.
  - A full URL to a model JSON file.
    e.g. ``https://github.com/esphome/micro-wake-word-models/raw/main/models/okay_nabu.json``.

- **on_wake_word_detected** (*Optional*, Automation): An automation to perform when the wake word is detected.
  The ``wake_word`` phrase from the model manifest is provided as a ``std::string`` to any actions in this automation.

The below two options are provided by the JSON file, but can be overridden in YAML.

- **probability_cutoff** (*Optional*, percentage): The probability cutoff for the wake word detection.
  If the probability of the wake word is below this value, the wake word is not detected.
  A larger value reduces the number of false accepts but increases the number of false rejections.
- **sliding_window_average_size** (*Optional*, int): The size of the sliding window average for the wake word detection. A small value lowers latency but may increase the number of false accepts.

Model JSON
----------

.. code-block:: json

    {
      "type": "micro",
      "wake_word": "okay nabu",
      "author": "Kevin Ahrendt",
      "website": "https://www.kevinahrendt.com/",
      "model": "./okay_nabu.tflite",
      "version": 1,
      "micro": {
        "probability_cutoff": 0.5,
        "sliding_window_average_size": 10
      }
    }

The model JSON file contains the following fields that are all **required** unless otherwise specified:

- **type** (string): The type of the model. This should always be ``micro``.
- **wake_word** (string): The wake word that the model is trained to detect.
- **author** (string): The name of the author that trained the model.
- **website** (string): The website of the author.
- **model** (string): The relative or absolute path or URL to the TFLite trained model file.
- **version** (int): The version of the JSON schema. Currently only version ``1`` exists.
- **micro** (object): The microWakeWord specific configuration.

  - **probability_cutoff** (float): The probability cutoff for the wake word detection.
    If the probability of the wake word is below this value, the wake word is not detected.
  - **sliding_window_average_size** (int): The size of the sliding window average for the wake word detection.
  - **minimum_esphome_version** (*Optional* version): The minimum ESPHome version required to use this model.


Automations
-----------

``micro_wake_word.start`` Action
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Starts the wake word detection.

``micro_wake_word.stop`` Action
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Stops the wake word detection.

Example usage
-------------

.. code-block:: yaml

    micro_wake_word:
      model: okay_nabu
      on_wake_word_detected:
        then:
          - voice_assistant.start:
              wake_word: !lambda return wake_word;


See Also
--------

- :doc:`voice_assistant`
- :apiref:`micro_wake_word/micro_wake_word.h`
- :ghedit:`Edit`
