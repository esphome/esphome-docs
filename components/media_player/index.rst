Media Player Components
=======================

.. seo::
    :description: Instructions for setting up generic media players in ESPHome.
    :image: folder-open.svg

The ``media_player`` domain includes all platforms that implement media player
functionality.

.. note::

    ESPHome media players require Home Assistant 2022.6 or newer.

.. _config-media_player:

Base Media Player Configuration
-------------------------------

.. code-block:: yaml

    media_player:
      - platform: ...
        name: "Media Player Name"

Configuration variables:

- **name** (**Required**, string): The name of the media player.
- **icon** (*Optional*, icon): Manually set the icon to use for the
  media player in the frontend.
- **internal** (*Optional*, boolean): Mark this component as internal. Internal components will
  not be exposed to the frontend (like Home Assistant). Only specifying an ``id`` without
  a ``name`` will implicitly set this to true.
- **disabled_by_default** (*Optional*, boolean): If true, then this entity should not be added to any client's frontend,
  (usually Home Assistant) without the user manually enabling it (via the Home Assistant UI).
  Defaults to ``false``.
- **entity_category** (*Optional*, string): The category of the entity.
  See https://developers.home-assistant.io/docs/core/entity/#generic-properties
  for a list of available options. Set to ``""`` to remove the default entity category.

.. _media_player-play:

``media_player.play`` Action
----------------------------

This action will resume playing the media player.
A future change will allow specifying the ``media_url`` for starting
a new stream.

.. _media_player-pause:

``media_player.pause`` Action
-----------------------------

This action pauses the current playback.

.. _media_player-stop:

``media_player.stop`` Action
----------------------------

This action stops the current playback.

.. _media_player-toggle:

``media_player.toggle`` Action
------------------------------

This action will pause or resume the current playback.


See Also
--------

.. toctree::
    :maxdepth: 1
    :glob:

    *

- :ghedit:`Edit`
