# IVR Demo (Python)
Simple Interactive Voice Response (IVR) demo built on Call Control in python using Telnyx API.

## Prerequisites

Before you get started, you’ll need to complete these steps:

1. Create a Telnyx account [here](https://telnyx.com/sign-up)
2. Buy a Telnyx number on Mission Portal, that you can learn how to do [here](https://developers.telnyx.com/docs/v1/numbers/quickstarts/portal-setup)
3. Create a new Connection as Call Control on Mission Portal, that you can learn how to do [here](https://developers.telnyx.com/docs/v1/numbers/quickstarts/portal-setup)

              - Creating Connection through Mission Portal is easier than using API endpoint
4. You’ll need to have the following to continue:

              - Python [here](https://www.python.org/downloads/)
                  - Check whether you already have python using the below command

                   ```shell
                    $ python -V
                   ```
              - Flask [here](https://flask.palletsprojects.com/en/1.1.x/installation/#install-flask)
              - Requests [here](https://realpython.com/python-requests/)
              - Ngrok [here](https://ngrok.com/download)
                  - Exposes local server to internet to listen for incoming webhooks

                   ```shell
                    $ ./ngrok http 5000
                   ```

## Telnyx Call Control Basics

For the Call Control application you’ll need to get a set of basic functions to perform Telnyx Call Control Commands. This tutorial will be using the following subset of Telnyx Call Control Commands:

- [Call Control Transfer](https://developers.telnyx.com/docs/api/v1/call-control/Call-Commands#CallControlTransfer)
- [Call Control Answer](https://developers.telnyx.com/docs/api/v1/call-control/Call-Commands#CallControlAnswer)
- [Call Control Speak](https://developers.telnyx.com/docs/api/v1/call-control/Call-Commands#CallControlSpeak)
- [Call Control Gather Using Speak](https://developers.telnyx.com/docs/api/v1/call-control/Call-Commands#CallControlSpeak)
- [Call Control Hangup](https://developers.telnyx.com/docs/api/v1/call-control/Call-Commands#CallControlHangup)

You can get the full set of available Telnyx Call Control Commands [here](https://developers.telnyx.com/docs/api/v1/call-control/).

## Telnyx Message

Implement text message feature within call control application:

- [Setup Message](https://developers.telnyx.com/docs/v2/messaging/quickstarts/portal-setup)
- [Enable Number Pooling for text message](https://support.telnyx.com/en/articles/3154822-number-pooling)
- [Send Message](https://developers.telnyx.com/docs/api/v1/messaging/Messages)

## Voice IVR Flow

<p align="center">
    <img src="https://raw.githubusercontent.com/team-telnyx/demo-ivr-node/master/examples/ivr_flow_example.png" width="90%" height="90%" title="sms_otp_example">
</p>



