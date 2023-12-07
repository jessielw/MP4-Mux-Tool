from pathlib import Path
from typing import Union

from pymediainfo import MediaInfo

from mp4muxtool.backend.backend_base import BackendBase
from mp4muxtool.exceptions import TrackError, MissingTrackError
from mp4muxtool.payloads.audio_content import AudioContentPayload


class AudioContentBackEnd(BackendBase):
    def __init__(self):
        super().__init__()

    def get_payload(self, file_input: Union[str, Path]):
        self.parsed_file = MediaInfo.parse(file_input)
        try:
            track = self.parsed_file.audio_tracks[0]
            payload = AudioContentPayload(
                stream_identifier=track.stream_identifier,
                title=track.title,
                language=track.language,
                other_language=track.other_language,
                track_id=track.track_id,
                track_format=track.format,
                track_other_format=track.track_other_format,
                track_format_info=track.track_format_info,
                commercial_name=track.commercial_name,
                channels=track.channel_s,
                duration=track.duration,
                other_duration=track.other_duration,
                bit_rate=track.bit_rate,
                other_bit_rate=track.other_bit_rate,
                frame_rate=track.frame_rate,
                frame_count=track.frame_count,
                bit_depth=track.bit_depth,
                sampling_rate=track.sampling_rate,
                other_sampling_rate=track.other_sampling_rate,
                stream_size=track.stream_size,
                other_stream_size=track.other_stream_size,
                delay=self._parse_delay(track),
                other_delay=track.other_delay,
                compression_mode=track.compression_mode,
                default=track.default,
                forced=track.forced,
            )
            return payload
        except IndexError:
            raise MissingTrackError(
                f"Input file '{self.file_input.name}' has no audio track"
            )
        except Exception as e:
            raise TrackError(f"Error opening input file '{self.file_input.name}': {e}")

    @staticmethod
    def _parse_delay(track):
        # TODO: parse file name for delay
        if track.delay:
            return int(track.delay)
        elif track.source_delay:
            return int(track.source_delay)
        else:
            return None
