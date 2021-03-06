About hopper.pw
===============

hopper.pw is the idea of a really simple single purpose dynamic dns service.
Unlike other dynamic dns services its intention is that you do not
have to click a link every 30 days to keep your domain enabled or other jokes
like this.
The basic software was originally developed during DjangoDash 2013 by Arne
Schauf, Fabian Faessler and Thomas Waldmann. Hopper.pw was a fork after the dash
to continue developing and add new features.

Like nsupdate.info, hopper.pw is is intended to be self hostable,
but there is a free service on http://www.hopper.pw/ where you can add your own domains.


Features (Frontend)
===================

* Dynamic DNS updates via URL with Basic Http-Auth
* Multiple Hosts for each user
* Custom comment for each host
* Manual IP updates via webinterface
* Show time since last update via api
* Add own domains (public or only for yourself) - you will need an nsupdate-capable dns-server for that


Features (Backend)
==================

* Use of awesome django framework
* Nameserver updates via RFC2136
* Nameserver to update configurable via DB for each domain


Installation
============

If you haven't already done create and change to a virtualenv for the
installation (here with virtualenvwrapper)::

    mkvirtualenv hopper.pw
    workon hopper.pw


Clone the repo and cd into::

    git clone git@github.com:asmaps/hopper.pw.git hopper.pw
    cd hopper.pw


Then install the requirements::

    # for production
    pip install -r requirements.d/prod.txt
    # for dev
    pip install -r requirements.d/dev.txt

From time to time execute this again to install the newest dependencies.

For production environments I prefer gunicorn with nginx and postgresql as DB.
For the moment please use google for instructions how to set it up.

