Speaker Components
==================

.. seo::
    :description: Instructions for setting up speakers in ESPHome.
    :image: speaker.svg

The ``speaker`` domain contains common functionality shared across the
speaker platforms.

.. _config-speaker:

Base Speaker Configuration
--------------------------

No configuration variables

.. _speaker-actions:

Speaker Actions
------------------

All ``speaker`` actions can be used without specifying an ``id`` if you have only one ``speaker`` in
your configuration YAML.

Configuration variables:

**id** (*Optional*, :ref:`config-id`): The speaker to control. Defaults to the only one in YAML.


.. _speaker-play:

``speaker.play`` Action
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This action will start playing raw audio data from the speaker.

.. code-block:: yaml

    on_...:
      # Static raw audio data
      - speaker.play: [...]

      # Templated, return type is std::vector<uint8_t>
      - speaker.play: !lambda return {...};

      # in case you need to specify the speaker id
      - speaker.play:
          id: my_speaker
          data: [...]

Configuration variables:

**id** (*Optional*, :ref:`config-id`): The speaker to control. Defaults to the only one in YAML.
**data** (*Required*, :ref:`config-raw-data`): The raw audio data to play.

.. _speaker-stop:

``speaker.stop`` Action
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This action will stop playing audio data from the speaker and discard the unplayed data.

.. _speaker-conditions:

Speaker Conditions
---------------------

All ``speaker`` conditions can be used without specifying an ``id`` if you have only one ``speaker`` in
your configuration YAML.

Configuration variables:

**id** (*Optional*, :ref:`config-id`): The speaker to check. Defaults to the only one in YAML.

.. _speaker-is_playing:

``speaker.is_playing`` Condition
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This condition will check if the speaker is currently playing audio data.


Platforms
---------

.. toctree::
    :maxdepth: 1
    :glob:

    *

See Also
--------

- :ghedit:`Edit`
