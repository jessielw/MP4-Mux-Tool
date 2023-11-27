from dataclasses import dataclass
from typing import List, Union


@dataclass
class VideoContentPayload:
    stream_identifier: int
    title: str
    track_id: int
    track_format: str
    track_other_format: List[str]
    track_format_info: str
    commercial_name: str
    format_profile: str
    duration: int
    other_duration: List[str]
    bit_rate: int
    other_bit_rate: List[str]
    max_bit_rate: int
    other_max_bit_rate: List[str]
    width: int
    height: int
    pixel_aspect_ratio: float
    display_aspect_ratio: float
    frame_rate_mode: str
    frame_rate: Union[float, int]
    bit_depth: int
    stream_size: int
    other_stream_size: List[str]
