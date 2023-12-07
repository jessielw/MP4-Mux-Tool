from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union, List

from iso639 import iter_langs, Lang as ISOLang
from iso639.exceptions import InvalidLanguageValue


class BackendBase(ABC):
    def __init__(self):
        self.file_input = None
        self.parsed_file = None

    @abstractmethod
    def get_payload(self, file_input: Union[str, Path]) -> object:
        """
        Override this method with a similar implementation below.

        self.parsed_file = MediaInfo.parse(file_input)
        try:
            track = self.parsed_file.video_tracks[0]
            payload = VideoContentPayload(
                stream_identifier=track.stream_identifier,
                title=track.title,
                ... (etc)
            )
            return payload
        except IndexError:
            raise MissingTrackError(
                f"Input file '{self.file_input.name}' has no video track"
            )
        except Exception as e:
            raise TrackError(f"Error opening input file '{self.file_input.name}': {e}")
        """

    def get_language_object(self) -> List[object]:
        """Returns a list of objects if lg.pt1 has data"""
        return [lg for lg in iter_langs() if lg.pt1 != ""]

    def get_language_list(self) -> List[str]:
        """Returns a list of strings sorted with common languages in the start of the list"""
        languages = ["", "English", "French", "Japanese", "Spanish"]
        for lang in self.get_language_object():
            if lang.name not in languages:
                languages.append(lang.name)
        return languages

    def find_language(self, language: str) -> str:
        """Returns a the official ISO language name if it exists, else return an empty string"""
        try:
            return ISOLang(language).name
        except InvalidLanguageValue:
            return ""
