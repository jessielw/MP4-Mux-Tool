from pathlib import Path
from typing import Union
from pymediainfo import MediaInfo

from mp4muxtool.exceptions import TrackError, VideoTrackError
from mp4muxtool.payloads.video_content import VideoContentPayload


class VideoContentBackEnd:
    def __init__(self, file_input: Union[str, Path]):
        self.file_input = Path(file_input)
        self.parsed_file = MediaInfo.parse(file_input)

    def get_payload(self):
        try:
            track = self.parsed_file.video_tracks[0]
            payload = VideoContentPayload(
                stream_identifier=track.stream_identifier,
                title=track.title,
                track_id=track.track_id,
                track_format=track.format,
                track_other_format=track.other_format,
                track_format_info=track.format_info,
                commercial_name=track.commercial_name,
                format_profile=track.format_profile,
                duration=track.duration,
                other_duration=track.other_duration,
                bit_rate=track.bit_rate,
                other_bit_rate=track.other_bit_rate,
                max_bit_rate=track.maximum_bit_rate,
                other_max_bit_rate=track.other_maximum_bit_rate,
                width=track.width,
                height=track.height,
                pixel_aspect_ratio=track.pixel_aspect_ratio,
                display_aspect_ratio=track.display_aspect_ratio,
                frame_rate_mode=track.frame_rate_mode,
                frame_rate=track.frame_rate,
                bit_depth=track.bit_depth,
                stream_size=track.stream_size,
                other_stream_size=track.other_stream_size,
            )
            return payload
        except IndexError:
            raise VideoTrackError(
                f"Input file '{self.file_input.name}' has no video track"
            )
        except Exception as e:
            raise TrackError(f"Error opening input file '{self.file_input.name}': {e}")
