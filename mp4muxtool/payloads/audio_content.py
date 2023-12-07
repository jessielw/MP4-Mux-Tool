from dataclasses import dataclass
from typing import List, Union


@dataclass
class AudioContentPayload:
    stream_identifier: int
    title: str
    language: str
    other_language: List[str]
    track_id: int
    track_format: str
    track_other_format: List[str]
    track_format_info: str
    commercial_name: str
    channels: int
    duration: int
    other_duration: List[str]
    bit_rate: int
    other_bit_rate: List[str]
    frame_rate: Union[float, int]
    frame_count: int
    bit_depth: int
    sampling_rate: int
    other_sampling_rate: List[str]
    stream_size: int
    other_stream_size: List[str]
    delay: int
    other_delay: List[str]
    compression_mode: str
    default: str
    forced: str
