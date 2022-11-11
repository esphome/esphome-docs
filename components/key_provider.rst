Key provider
============

.. seo::
    :description: Key provider component to pass on pressed keys to other components
    :image: description.svg

The ``key_provider`` is an internal component required by any component that can provide 
key presses for the ``key_collect`` component. 
Currently supported components are ``matrix_keypad`` and ``wiegand``.

.. code-block:: yaml

    # Example configuration entry
    key_provider:


Configuration variables:

This component has no configuration variables.

See Also
--------

- :ghedit:`Edit`
- :doc:`/components/matrix_keypad`
- :doc:`/components/viegand`
- :doc:`/components/key_collect`

