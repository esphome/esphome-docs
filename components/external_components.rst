External Components
===================

.. seo::
    :description: Instructions for setting up ESPHome External Components.
    :keywords: External, Custom, Components, ESPHome

You can easily import community or personal components using the external components feature.
Bundled components can be overridden using this feature.

.. code-block:: yaml

    external_components:
      # use rtttl and dfplayer from ESPHome's dev branch in GitHub
      - source:
          type: git
          url: https://github.com/esphome/esphome
          ref: dev
        components: [ rtttl, dfplayer ]

      # equivalent shorthand for GitHub
      - source: github://esphome/esphome@dev
        components: [ rtttl ]

      # use all components from a local folder
      - source:
          type: local
          path: my_components

Configuration variables:

- **source**: The location of the components you want to retrieve. See :ref:`external-components_local`
  and :ref:`external-components_git`.

  - **type** (**Required**): Repository type. One of ``local``, ``git``.

  git options:

  - **url** (**Required**, url): HTTP git repository url. See :ref:`external-components_git`.
  - **ref** (*Optional*, string): Git ref (branch or tag). If not specified the default branch is used.

  local options:

  - **path** (**Required**):  Path to use when using local components. See :ref:`external-components_local`.

- **components** (*Optional*, list): The list of components to use from the external source.
  By default, all available components are used.

- **refresh** (*Optional*, :ref:`time <config-time>`): The interval the source will be checked. Has no
  effect on ``local``. See :ref:`external-components_refresh`. for more info. Defaults to ``1day``.


.. _external-components_local:

Local
-----

You can specify a local path containing external components. This is most useful when developing a
component or if you want to manually control the origin of the files.

.. code-block:: yaml

    external_components:
      - source:
          path: /copied_components

    # shorthand
    external_components:
      - source: my_components


Notice that relative paths are supported, so you can enter ``my_components`` as the source path and then
ESPHome will load components from a ``my_components`` folder in the same folder where your YAML configuration
is.

Example of local components
***************************

Given the above example of ``my_components``, the folder structure must look like:

.. code-block:: text

    <CONFIG_DIR>
    ├── node1.yaml
    ├── node2.yaml
    └── my_components
        ├── my_component1
        │   ├── __init__.py
        │   ├── component1.cpp
        │   ├── component1.h
        │   └── sensor.py
        └── my_component2
            ├── __init__.py
            ├── component2.cpp
            ├── component2.h
            └── switch.py


..   _external-components_git:

Git
---

Retrieving components from git is the easiest way to use components not included in ESPHome by default.
The source components should be inside a ``components`` folder or inside an ``esphome/components``
folder. The latter makes sharing a component from a forked ESPHome repository easier.

Example of git repositories
***************************

For repositories where you share one or a few components:

.. code-block:: text

    components
    ├── my_component1
    │   ├── __init__.py
    │   ├── component1.cpp
    │   ├── component1.h
    │   └── sensor.py
    └── my_component2
        ├── __init__.py
        ├── component2.cpp
        ├── component2.h
        └── switch.py
    example_component1.yaml        <- not required but recommended
    README.md


or, this structure is also supported, which makes handy to share components from a **forked** ESPHome
repository:

.. code-block:: text

    esphome
    ├── components
    │   ├── my_component1
    │   │   ├── __init__.py
    │   │   ├── component1.cpp
    │   │   ├── component1.h
    │   │   └── sensor.py
    │   ├── my_component2
    │   │   ├── __init__.py
    │   │   ├── component2.cpp
    │   │   ├── component2.h
    │   │   └── switch.py
    │  ...
    ...

HTTP git repositories in general are supported with this configuration:

.. code-block:: yaml

    external_components:
      source:
        type: git
        url: http://repository_url/
        ref: branch_or_tag

The source field accepts a short hand **github://** resource:

.. code-block:: yaml

    external_components:
      # shorthand
      source: github://<user or org>/<repository name>[@<branch or tag>]

Under the hood, during validation, ESPHome will clone the git repository into the hidden ``.esphome``
folder and components will then be loaded from this local copy. The local path of the cloned repository
varies per repository name and ref name, so repositories with different refs are considered different
repositories and updated independently.

.. _external-components_refresh:

Refresh
*******

Components are initially cloned into a cache directory, then the repository is checked for updates
(via *git pull*) after the ``refresh:`` time passes since last check.

You can make ESPHome check the repository every time by setting this option to ``0s``, however since
ESPHome is validating the configuration continuously while using the dashboard or the vscode extension,
it is not recommended to set this value to less than a few minutes to avoid validation slow down and
excessive repository checks.

Likewise, you can set this setting to ``never`` and ESPHome will never
**update** the repository, useful e.g. when ``ref`` points to a **tag**.


See Also
--------

- :ghedit:`Edit`
