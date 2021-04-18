External Components
===================

.. seo::
    :description: Instructions for setting up ESPHome External Components.
    :keywords: External, Custom, Components, ESPHome

You can easily import community components using the external components feature. Bundled components
can be overriden using this feature.

.. code-block:: yaml

    external_components:
      # use rtttl from ESPHome's dev branch in GitHub
      - source:
          type: git
          url: https://github.com/esphome/esphome
          ref: dev
        components: [ rtttl ]

      # equivalent shorthand for GitHub
      - source: github://esphome/esphome@dev
        components: [ rtttl ]

Configuration variables:

- **source**: The location of the components you want to retrieve. See :ref:`external-components_local`
  and :ref:`external-components_git`.

  - **type** (**Required**): Repository type. One of ``local``, ``git``.

  git options:

  - **url** (**Required**, url): Http git repository url. See :ref:`external-components_git`.
  - **ref** (*Optional*, string): Git ref (branch or tag). If not specified the default branch is used.

  local options:

  - **path** (**Required**):  Path to use when using local components. See :ref:`external-components_local`.

- **components** (*Optional*, list): The list of compoments to retrieve from the external source.
  Defaults to ``all``.

- **refresh** (*Optional*, :ref:`time <config-time>`): The interval the source will be checked. Has no
  effect on ``local``. See :ref:`external-components_refresh`. for more info. Defaults to ``1day``.


.. _external-components_local:

Local
-----

You can specify a local path for the external components, this is most useful if you want to manually
control the origin of the files.

.. code-block:: yaml

    external_components:
      source:
        path: /copied_components

    # shrothand
    external_components:
      source: my_components


Notice that relative paths are supported, so you can enter ``my_components`` as the source path and then
ESPHome will load components from a ``my_components`` folder in the same folder where your YAML configuration
is.


.. _external-components_git:

Git
---

Retrieving components from git is the easiest way to use components not included in ESPHome by default.
The source components should be inside a ``components`` folder or inside a ``esphome/components``
folder. The later makes sharing a component from a forked ESPHome repository easier.

.. code-block:: yaml

    external_components:
      source:
        type: git
        url: http://repository_url/
        ref: branch_or_tag

The source fields accepts a short hand **github://** resource:

.. code-block:: yaml

    external_components:
      # shorthand
      source: github://<user or org>/<repository name>[@<branch or tag>]

Under the hood, during validation, ESPHome will copy or clone the files into the hidden ``.esphome``
folder and components will then be loaded from this local cache.

.. _external-components_refresh:

Refresh
*******

Components are initially cloned into a cache directory, then the repository is checked for updates
(via *git pull*) after the ``refresh:`` time passes since last check. You can make ESPHome check the
repository every time by setting this option to ``0s``, however since ESPHome is validating the
configuration continuously while using the dashboard or the vscode extension, it is not recommended
to set this value to less than a few minutes to avoid validation slow down and excesive repository checks.
Likewise, you can set this setting to ``never`` and ESPHome will never **update** the repository.

See Also
--------

- :ghedit:`Edit`
