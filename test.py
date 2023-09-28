from youtube_transcript_api import YouTubeTranscriptApi

video_id = "NFHDHcs4BvQ"
video_id_w_languages = "74ijsBhbxSQ"
# transcript = YouTubeTranscriptApi.get_transcript(video_id_w_languages)
# print(transcript)

# retrieve the available transcripts
transcripts = YouTubeTranscriptApi.list_transcripts(video_id_w_languages)
# transcript = transcripts.find_manually_created_transcript(('en-GB',)).fetch()
transcript = transcripts.find_generated_transcript(('en', ))
# transcript = transcripts.find_transcript(['en-GB']).translate('ar').fetch()
print(type(transcript))
print(transcript)