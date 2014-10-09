django-snappy-vumi-bouncer
==========================

A Django app that bounces messages from Vumi to Snappy and back


Overview
-------------------------

    +---------------------------------------+            +----------------------+         +------------------+
    |             Vumi Go                   |            |     Django Proj      |         |    Snappy        |
    |                                       |            |                      |         |                  |
    | +------------+         +-----------+  |            |   +--------------+   |         |                  |
    | | Vumi       |         | Vumi      |  |  HTTP      |   |              |   | HTTP    |                  |
    | | Transport  +-------> | Sandbox   |  +----------> |   |  Snappy      |   +-------> | 1. Create ticket |
    | | (e.g. SMS) |         | App       |  |  POST      |   |  Bouncer     |   | POST    |                  |
    | |            |         |           |  |            |   |              |   |         |                  |
    | |            |         +-----------+  |            |   |  1. Store    |   |         | 2. Ticket        |
    | |            |                        |            |   |  2. Forward  |   |         |    response      |
    | |            |         +-----------+  |            |   |  3. Listen   |   |         |                  |
    | |            |         | Vumi      |  |   HTTP     |   |  4. Respond  |   |         |                  |
    | |            | <-------+ HTTP      |  | <----------+   |              |   | <-------+ 3. Hook fires    |
    | |            |         | API       |  |   POST     |   +--------------+   | Webhook |                  |
    | |            |         |           |  |            |                      |         |                  |
    | +------------+         +-----------+  |            |                      |         |                  |
    |                                       |            |                      |         |                  |
    +---------------------------------------+            +----------------------+         +------------------+
