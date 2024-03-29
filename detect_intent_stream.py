import qi


def detect_intent_stream(project_id, session_id, audio_file_path, language_code, ip):
    """Returns the result of detect intent with streaming audio as input.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    import dialogflow_v2 as dialogflow

    session_client = dialogflow.SessionsClient()

    # Note: hard coding audio_encoding and sample_rate_hertz for simplicity.
    audio_encoding = dialogflow.enums.AudioEncoding.AUDIO_ENCODING_LINEAR_16
    sample_rate_hertz = 48000

    session_path = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session_path))

    def request_generator(audio_config, audio_file_path):
        query_input = dialogflow.types.QueryInput(audio_config=audio_config)

        # The first request contains the configuration.
        yield dialogflow.types.StreamingDetectIntentRequest(
            session=session_path, query_input=query_input
        )

        # Here we are reading small chunks of audio data from a local
        # audio file.  In practice these chunks should come from
        # an audio input device.
        while True:
            chunk = audio_file_path.read(4096)
            if not chunk:
                break
            # The later requests contains audio data.
            yield dialogflow.types.StreamingDetectIntentRequest(input_audio=chunk)

    audio_config = dialogflow.types.InputAudioConfig(
        audio_encoding=audio_encoding,
        language_code=language_code,
        sample_rate_hertz=sample_rate_hertz,
    )

    requests = request_generator(audio_config, audio_file_path)
    responses = session_client.streaming_detect_intent(requests=requests)

    print("=" * 20)
    for response in responses:
        print(
            'Intermediate transcript: "{}".'.format(
                response.recognition_result.transcript
            )
        )

    # Note: The result from the last response is the final transcript along
    # with the detected content.
    query_result = response.query_result

    print("=" * 20)
    print("Query text: {}".format(query_result.query_text))
    print(
        "Detected intent: {} (confidence: {})\n".format(
            query_result.intent.display_name, query_result.intent_detection_confidence
        )
    )
    print("Fulfillment text: {}\n".format(query_result.fulfillment_text))

    if query_result.intent_detection_confidence > 0.5:
        session = qi.Session()
        try:
            session.connect("tcp://{}:{}".format(ip, 9559))
            if query_result.action.lower() == "say":
                tts = session.service("ALTextToSpeech")
                tts.say(query_result.fulfillment_text)
            # elif query_result.action.lower() == "dialog":
            #     do_dialog(query_result, session)
            elif query_result.action.lower() == "behavior":
                behaviorName = query_result.fulfillment_text
                bm = session.service("ALBehaviorManager")
                try:
                    bm.stopBehavior(behaviorName)
                except:
                    pass
                bm.runBehavior(behaviorName)
            # elif query_result.action.lower() == "url":
            #     do_tablet(query_result, session)
            else:
                tts = session.service("ALAnimatedSpeech")
                # anim_player = session.service("ALAnimationPlayer")
                if query_result.action == 'input.welcome':
                    # print('no error')
                    # anim_player.run('animations/Stand/Gestures/Hey_3')
                    tts.say('^start(animations/Stand/Gestures/Hey_6)'+query_result.fulfillment_text)
                    # tts.say(query_result.fulfillment_text)
                elif query_result.action == 'smalltalk.agent.acquaintance':
                    tts.say('^start(animations/Stand/Gestures/Me_7)'+query_result.fulfillment_text)
                elif query_result.action == 'smalltalk.appraisal.bad' or query_result.action == 'smalltalk.agent.bad':
                    tts.say('^start(nimations/Stand/Emotions/Positive/Embarrassed_1)'+query_result.fulfillment_text)
                else:
                    tts.say(query_result.fulfillment_text)
        except:
            # traceback.print_exc()
            raise "session.connect failed."
        finally:
            session.close()
