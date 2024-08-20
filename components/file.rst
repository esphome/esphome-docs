File
====

.. seo::
    :description: Instructions to import binary files into ESPHome

This component allows importing binary files into ESPHome.
The files are imported as a "progmem" data array which can then be referenced by
automations etc.

.. code-block:: yaml

    file:
      - id: my_file
        file: "bloop.wav"
      - id: my_remote_file
        file: "https://example.com/bloop.wav"

Configuration variables:

- **id** (**Required**, :ref:`config-id`): The ID with which you will be able to reference the file later
  in your configuration.
- **file** (**Required**): The shorthand relative path or a web URL of the file. Or a dictionary for one
  of the following:

    Local:

    - **path** (**Required**, string): The path to the file to import. This path is relative to the
      folder where the configuration file is located.
    - **type** (**Required**, string): Must be ``local``.

    Remote:

    - **url** (**Required**, string): The URL of the file to import. Must be a web URL.
    - **type** (**Required**, string): Must be ``remote``.

- **format** (*Optional*, string): The format of the file.

  - ``raw``:   The file is imported as is with no pre-processing.
  - ``wav``: The file is imported as a WAV file. This will convert the WAV file to a raw PCM format
    and remove the WAV header.

Example
-------

.. code-block:: yaml

    speaker:
      - platform: ...
        id: my_speaker
        ...

    file:
      - id: my_bloop
        file: bloop.wav

    button:
      - platform: template
        name: Play the bloop
        on_press:
          - lambda: id(my_speaker).play(id(my_bloop), sizeof(id(my_bloop)));

See Also
--------

- :doc:`/components/speaker/index`

- :ghedit:`Edit`
