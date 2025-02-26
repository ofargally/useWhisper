from youtube_transcript_api import YouTubeTranscriptApi

# ID = QOaXm_9S9_0
video_id = 'QOaXm_9S9_0'
# Get the list of ids available
transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
print(transcript_list)
# Retrieve the ids of the available transcripts in the order of priority
# YouTubeTranscriptApi.get_transcript(video_id, languages=['zh', 'en'])
