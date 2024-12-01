Copyshopdenbosch.nl
===================

This repository contains the source code of Copyshopdenbosch.nl, a web
application created by [Return to the Source](https://rtts.eu/),
provided here for everyone to use under the [GPLv3](LICENSE) license
as part of our free and open source philosophy.

**This source code is provided as-is, without any support or
  warranties**


Installation
------------

Make sure that Python is installed, then run the following commands:

    git clone https://github.com/rtts/copyshopdenbosch.nl
    cd copyshopdenbosch.nl
    pip install -r requirements.txt
    ./manage.py migrate
    ./manage.py createsuperuser
    ./manage.py runserver


Usage
-----

Visit http://localhost:8000/admin/ to login. Then, visit
http://localhost:8000/edit/ to edit the homepage. You can add various
types of sections and click the save icon. These sections can then be
edited by clicking their edit icons.
