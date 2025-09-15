"""
Core module containing the foundation architecture components.

This module provides the enterprise-level patterns and abstractions
that form the backbone of the CoachPro application.
"""

__version__ = "1.0.0"
__author__ = "CoachPro Team"

from .container import DIContainer, inject, Injectable
from .events import EventBus, Event, EventHandler
from .exceptions import CoachProException, ValidationError, BusinessRuleError

__all__ = [
    # Dependency Injection
    "DIContainer",
    "inject",
    "Injectable",

    # Event System
    "EventBus",
    "Event",
    "EventHandler",

    # Exceptions
    "CoachProException",
    "ValidationError",
    "BusinessRuleError",
]