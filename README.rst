django-snappy-vumi-bouncer
==============================

A Django app that bounces messages from Vumi to Snappy and back


Overview
------------------------------

::

    +-------------------------------+        +----------------+         +------------------+
    |            Vumi Go            |        |  Django Proj   |         |    Snappy        |
    |                               |        |                |         |                  |
    | +------------+    +---------+ |        | +------------+ |         |                  |
    | | Vumi       |    | Vumi    | | HTTP   | |            | | HTTP    |                  |
    | | Transport  +--> | Sandbox | +------> | | Snappy     | +-------> | 1. Create ticket |
    | | (e.g. SMS) |    | App     | | POST   | | Bouncer    | | POST    |                  |
    | |            |    |         | |        | |            | |         |                  |
    | |            |    +---------+ |        | | 1. Store   | |         | 2. Ticket        |
    | |            |                |        | | 2. Forward | |         |    response      |
    | |            |    +---------+ |        | | 3. Listen  | |         |                  |
    | |            |    | Vumi    | |   HTTP | | 4. Respond | |         |                  |
    | |            | <--+ HTTP    | | <------+ |            | | <-------+ 3. Hook fires    |
    | |            |    | API     | |   POST | +------------+ | Webhook |                  |
    | |            |    |         | |        |                |         |                  |
    | +------------+    +---------+ |        |                |         |                  |
    |                               |        |                |         |                  |
    +-------------------------------+        +----------------+         +------------------+


Configuration
-------------------------

The following configuration (with dummy values replaced by real ones) needs to
be added to ``settings.py`` to configure this app::

    SNAPPY_API_KEY = 'keyfromsettings'
    SNAPPY_BASE_URL = 'https://app.besnappy.com/api/v1'
    SNAPPY_EMAIL = 'sharedmailbox@example.com'
    SNAPPY_EXTRAS = ["extra1", "extra2"]
    SNAPPY_MAILBOX_ID = 0
    SNAPPY_STAFF_ID = 0
    VUMI_GO_ACCOUNT_KEY = "key"
    VUMI_GO_CONVERSATION_TOKEN = "token"
    VUMI_GO_API_TOKEN = "token"
    VUMI_GO_API_URL = "http://go.vumi.org/api/v1/go"
    VUMI_GO_BASE_URL = VUMI_GO_API_URL + "/http_api_nostream"
    VUMI_GO_CONVERSATION_KEY = "convokey"
