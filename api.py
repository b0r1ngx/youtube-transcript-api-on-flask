import logging

from flask import request
from youtube_transcript_api import YouTubeTranscriptApi

from flask_app import app, FlaskThread
from constants import *


@app.route("/")
def hello_world():
    return hello()


@app.route(API_START_URL)
def hello_api():
    return hello()


def hello():
    return f'Hello, I\'m ready to {API_STATUS} API!'


@app.route(TRANSCRIPTS, methods=['GET'])
def get_available_transcripts():
    r = request.get_json(force=True)
    logging.info(f'Request: {r}')
    if not r:
        return "Can't force parse json", 400

    video_id = r.get('video_id')
    if not video_id:
        return "video_id parameter not found", 400

    transcripts = YouTubeTranscriptApi.list_transcripts(video_id)

    return {
        'manual': transcripts._get_language_description(
            str(transcript) for transcript in transcripts._manually_created_transcripts.values()
        ),
        'generated': transcripts._get_language_description(
            str(transcript) for transcript in transcripts._generated_transcripts.values()
        ),
        'translation': transcripts._get_language_description(
            '{language_code} ("{language}")'.format(
                language=translation_language['language'],
                language_code=translation_language['language_code'],
            ) for translation_language in transcripts._translation_languages
        )
    }


@app.route(TRANSCRIPT, methods=['GET'])
def get_transcript():
    r = request.get_json(force=True)
    logging.info(f'Request: {r}')
    if not r:
        return "Can't force parse json", 400

    video_id = r.get('video_id')
    if not video_id:
        return "video_id parameter not found", 400
    type = r.get('type')
    language = r.get('language')

    transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
    if type == 'manual':
        transcript = transcripts.find_manually_created_transcript((language,))
    elif type == 'generated':
        transcript = transcripts.find_generated_transcript((language, ))
    elif type == 'translation':
        transcript = transcripts.find_generated_transcript(('en',)).translate(language)
    else:
        return "type parameter not found", 400

    return {'transcript': transcript}


if __name__ == '__main__':
    f = FlaskThread(name='API')
    f.start()
