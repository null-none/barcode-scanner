Reading information from Dymo USB scale.


=======
Install
=======

.. code-block:: bash

    # sudo apt-get install python libusb-1.0-0

.. code-block:: bash

    pip install barcode-scanner

=======
Example
=======

.. code-block:: python

  from barcode import scanner

  usb = scanner.USB(vendor_id=0x0922, product_id=0x8003)
  print scanner.get_code()


=======
Donation
=======

.. image:: https://img.shields.io/badge/Donate-PayPal-green.svg
  :target: https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=YYZQ6ZRZ3EW5C
