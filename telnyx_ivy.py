""" Interactive Voice Response (IVR) """
import os
from flask import json
from flask import request
from flask import Flask, jsonify
import datetime, requests, base64
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

# download ngrok to expose localhost to external

#end-poitnt
telnyx_api_url = 'https://api.telnyx.com/calls/{}/actions/'
# Application:
g_appName = "demo-telnyx-ivr"

#  TTS Options
g_ivr_voice = 'female'
g_ivr_language = 'en-GB'

# IVR Redirect Options
g_account_exec = os.getenv('ACCOUNT_EXECUTIVE')
g_sales_eng = os.getenv('SALES_ENGINEER')


# Telnyx Account Details
g_telnyx_key = os.getenv('API_KEY')
g_telnyx_secret = os.getenv('SECRET_KEY')
g_profile_id = os.getenv('PROFILE_ID')



# =========================================== TELNYX SEND SMS  ============================================

def send_sms(m_dest):
    """ Sends a message by submitting an outbound message request """

    print("-"*100)
    print("SEND MESSAGE")
    print("-"*100)


    headers = {
               'Content-Type': 'application/json',
               'Accept': 'application/json',
               'x-profile-secret': g_profile_id
            }
    payload = {
                "body": 'Thanks for calling Telnyx! 😀',
                "to": m_dest
                }

    url = 'https://sms.telnyx.com/messages'

    try:
        response = requests.post(url, json=payload, headers=headers).json()
    except Exception as e:
        print("-"*100)
        print("[{}] DEBUG - Command Executed [{}]".format(datetime.datetime.now(), "Text Message"))
        print(e)
        print("-"*100)

    return response



# =========================================== TELNYX CALL CONTROL COMMANDS  ============================================


# Telnyx Call Control - Transfer
def call_control_transfer(f_call_control_id, f_dest, f_orig):
    """
    Transfer a call to a new destination. If the transfer is unsuccessful, a 'call_hangup' webhook will be sent indicating that the transfer could not be completed.
    The original call will remain active and may be issued additional commands, potentially transfering the call to an alternate destination.
    """
    print("-"*100)
    print("CALL CONTROL TRANSFER")
    print("-"*100)

    cc_action = 'transfer'
    url = telnyx_api_url.format(f_call_control_id) + cc_action

    payload = {
                "to": f_dest,
                "from": f_orig
            }
    try:
        response = requests.post(url, data=payload, auth=HTTPBasicAuth(g_telnyx_key, g_telnyx_secret)).json()
        print('RESPONSE', response)
    except Exception as e:
        print("-"*100)
        print("[{}] DEBUG - Command Executed [{}]".format(datetime.datetime.now(), cc_action))
        print(e)
        print("-"*100)

    return response

# Telnyx Call Control - Answer Call
def call_control_answer_call(f_call_control_id, f_client_state_s):
    """
    Answer an incoming call.
    """
    print("-"*100)
    print("CALL CONTROL ANSWER")
    print("-"*100)

    l_cc_action = 'answer'
    l_client_state_64 = None

    if f_client_state_s:
        # base64 encode
        l_client_state_64 = base64.b64encode(f_client_state_s.encode())

    url = telnyx_api_url.format(f_call_control_id) + l_cc_action

    payload = {
                "client_state": l_client_state_64 #optional
            }

    try:
        response = requests.post(url, data=payload, auth=HTTPBasicAuth(g_telnyx_key, g_telnyx_secret)).json()
    except Exception as e:
        print("-"*100)
        print("[{}] DEBUG - Command Executed [{}]".format(datetime.datetime.now(), cc_action))
        print(e)
        print("-"*100)

    return response

# Telnyx Call Control - Speak
def call_control_speak(f_call_control_id, f_tts_text):
    """
    Convert text to speech and play it back on the call. If multiple speak text commands are issued consecutively,
    the audio files will be placed in a queue awaiting playback.
    """

    print("-"*100)
    print("CALL CONTROL SPEAK")
    print("-"*100)

    cc_action = 'speak'

    url = telnyx_api_url.format(f_call_control_id) + cc_action

    payload = {
                "payload": f_tts_text,
                "voice":  g_ivr_voice,
                "language": g_ivr_language
            }

    try:
        response = requests.post(url, data=payload, auth=HTTPBasicAuth(g_telnyx_key, g_telnyx_secret)).json()
    except Exception as e:
        print("-"*100)
        print("[{}] DEBUG - Command Executed [{}]".format(datetime.datetime.now(), cc_action))
        print(e)
        print("-"*100)

    return response

# Telnyx Call Control - Gather Using Speak
def call_control_gather_using_speak(f_call_control_id, f_tts_text, f_gather_digits, f_gather_max, f_client_state_s):
    """
    Convert text to speech and play it on the call until the required Dual-tone multifrequency (DTMF) signals are gathered to build interactive menus.
    """

    print("-"*100)
    print("CALL CONTROL GATHER USING SPEAK")
    print("-"*100)

    l_cc_action = 'gather_using_speak'
    l_client_state_64 = None

    if f_client_state_s:
        # base64 encode
        l_client_state_64 = base64.b64encode(f_client_state_s.encode())


    url = telnyx_api_url.format(f_call_control_id) + l_cc_action

    payload = {
                "payload": f_tts_text,
                "voice":  g_ivr_voice,
                "language": g_ivr_language,
                "valid_digits": f_gather_digits, #optional
                "max": f_gather_max, #optional
                "client_state": l_client_state_64 #optional
            }

    try:
        response = requests.post(url, data=payload, auth=HTTPBasicAuth(g_telnyx_key, g_telnyx_secret)).json()
    except Exception as e:
        print("-"*100)
        print("[{}] DEBUG - Command Executed [{}]".format(datetime.datetime.now(), l_cc_action))
        print(e)
        print("-"*100)

    return response


# Call Control - Hangup
def call_control_hangup(f_call_control_id):
    """
    Hang up call
    """
    print("-"*100)
    print("IN HANG-UP")
    print("-"*100)

    l_cc_action = 'hangup'

    url = telnyx_api_url.format(f_call_control_id) + l_cc_action

    try:
        response = requests.post(url, data=payload, auth=HTTPBasicAuth(g_telnyx_key, g_telnyx_secret)).json()
    except Exception as e:
        print("-"*100)
        print("[{}] DEBUG - Command Executed [{}]".format(datetime.datetime.now(), l_cc_action))
        print(e)
        print("-"*100)

    return response

@app.route('/')
def api_root():
    return ' Welcome To Telnyx IVR'

@app.route(f'/{g_appName}', methods=['POST'])
def api_webhooks():
    data = request.get_json(force=True, silent=True).copy()

    try:
        l_hook_event_type = data.get('event_type')
        l_call_control_id = data.get('payload').get('call_control_id')
        l_client_state_64 = data.get('payload').get('client_state')
        l_call_from_number = data.get('payload').get('from')
    except Exception as e:
        print("[{}] LOG - Invalid Webhook received!".format(datetime.datetime.now()))

    print("[{}] LOG - Webhook received - call_control_id [{}]".format(datetime.datetime.now(), l_call_control_id))
    print("[{}] DEBUG - Webhook received - complete payload: [{}]".format(datetime.datetime.now(), data))

    if l_hook_event_type == 'call_initiated':
        if data.get('payload').get('direction') == 'incoming':
            return jsonify(call_control_answer_call(l_call_control_id, None))
        else:
            #f_client_state_s == 'stage-outgoing'
            return jsonify(call_control_answer_call(l_call_control_id, 'stage-outgoing'))
    elif l_hook_event_type == 'call_answered':
        if not l_client_state_64:
            """  No State >> Incoming >> Gather Input """
            return jsonify(call_control_gather_using_speak(l_call_control_id,
                'Welcome to this Telnyx IVR Demo,' +
                'To contact sales please press 1,' +
                'To contact operations, please press 2.',
                '12', '1', None))
        """ State >> Outbound >> Do Nothing """
        return '', 204
    elif l_hook_event_type == 'speak_ended':
        """ Speach Ended >> Do Nothing """
        return '', 204
    elif l_hook_event_type == 'call_hangup':
        """ Call Hangup """
        return jsonify(send_sms(l_call_from_number))
    elif l_hook_event_type == 'call_bridged':
        """ Call Bridged >> Do Nothing """
        return '', 204
    elif l_hook_event_type == 'gather_ended':
        """ Gather Ended >> Proccess DTMF Input """
        # Receive DTMF Option
        l_ivr_option = data.get('payload').get("digits")
        print("[{}] DEBUG - RECEIVED DTMF [{}]".format(datetime.datetime.now(), l_ivr_option))

        """ Check Current IVR Level """
        if not l_client_state_64:
            """ IVR Lobby """
            if l_ivr_option == '1':
                """ Sales """
                # Speak Text
                return jsonify(call_control_gather_using_speak(l_call_control_id,
                    'You reached the sales support channel,' +
                    'To contact an Account Executive please press 1,' +
                    'To contact a Sales Engineer, please press 2,',
                    '12', '1', 'stage-sales'))
            elif l_ivr_option == '2':
                return jsonify(call_control_speak(l_call_control_id,
                    'You reached the operations support channel,' +
                    'no operations staff is available at the moment,' +
                    'please try again later'))
        else:
            """  Beyond Lobby Level """

            # Set Client State
            l_client_state_buff = base64.b64decode(l_client_state_64)
            l_client_state_s  = l_client_state_buff.decode("utf-8")

            # Selected Sales >> Choose Destinatio
            if l_client_state_s == "stage-sales":
                #  Select Destination
                if l_ivr_option == '1':
                    # Dial Account Executive
                    return jsonify(call_control_transfer(l_call_control_id, g_account_exec, data.get('payload').get('from')))
                elif l_ivr_option == '2':
                    return jsonify(call_control_transfer(l_call_control_id, g_sales_eng, data.get('payload').get('from')))

        return '', 204



if __name__ == '__main__':
    app.run(debug=True)
