.. audio_clips_for_i2s:

CREATE AUDIO CLIP FILES FOR USE WITH I2S SPEAKERS
=================================================

It is possible to create sound clips to include in your build to use with i2s speakers. No need for a media player component!  

- Using `Audacity<https://github.com/audacity/audacity>`, convert audio to WAV, mono, 16kHz, Unsigned 8bit PCM

.. image:: /images/save_as_wav.png
    :alt: Audacity export dialog
    :height: 200

- Convert again, this time with `SOX<https://github.com/chirlu/sox>`.

.. code-block:: console

    sox startup.wav --bits 8 --encoding signed-integer --endian little startup_again.raw

- Now convert it into a hexadecimal string using xxd into a C++ file.

.. code-block:: console

    xxd -i startup_again.raw startup.c

- The resulting file needs a modification in the start line:
  Open in an editor and change ``unsigned char startup_again_raw[] = {…[SNIP]…}`` to ``std::vector<unsigned char> startup_raw = {…[SNIP]…}``

Now you can rename the file to startup.h, put it inside the esphome configuration directory and put it in a include in your device config like this:

.. code-block:: yaml

    esphome:
      includes:
        - startup.h

Now you can define using the audio clip using the following:

.. code-block:: yaml

    - speaker.play:
        id: speaker
        data: !lambda return startup_raw;

Enjoy!

HowTo by [NUT].
