Over-The-Air Updates
====================

Example Usage
-------------

.. code-block:: cpp

    // Setup basic OTA
    App.init_ota();
    // Enable safe mode.
    App.init_ota()->start_safe_mode();
    // OTA password
    auto *ota = App.init_ota();
    ota->set_auth_plaintext_password("VERY_SECURE");
    ota->start_safe_mode();
    // OTA MD5 password
    auto *ota = App.init_ota();
    ota->start_safe_mode();


API Reference
-------------

.. cpp:namespace:: nullptr

OTAComponent
************

.. doxygenclass:: OTAComponent
    :members:
    :protected-members:
    :undoc-members:
