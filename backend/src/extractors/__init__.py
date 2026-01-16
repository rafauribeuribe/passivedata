"""
Extractors Package - Extractores de metadata
"""
from .email_extractor import EmailExtractor
from .calendar_extractor import CalendarExtractor
from .teams_extractor import TeamsExtractor

__all__ = ["EmailExtractor", "CalendarExtractor", "TeamsExtractor"]
