"""
Configuration management for the CoachPro application.

Handles environment variables, settings validation, and configuration
loading with proper defaults and type safety.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional


@dataclass
class DatabaseSettings:
    """Database configuration settings."""

    path: str = "coach.db"
    backup_enabled: bool = True
    backup_interval: int = 3600  # seconds
    pool_size: int = 5
    timeout: int = 30  # seconds


@dataclass
class UISettings:
    """User interface configuration settings."""

    theme: str = "dark"
    window_size: str = "1280x800"
    fullscreen: bool = False
    font_size: int = 12


@dataclass
class LoggingSettings:
    """Logging configuration settings."""

    level: str = "INFO"
    file: str = "coach.log"
    debug_sql: bool = False
    max_file_size: int = 10485760  # 10MB
    backup_count: int = 5


@dataclass
class PerformanceSettings:
    """Performance configuration settings."""

    cache_size: int = 100  # MB
    async_enabled: bool = False
    lazy_loading: bool = True
    prefetch_enabled: bool = True


@dataclass
class Settings:
    """Main application settings."""

    database: DatabaseSettings = field(default_factory=DatabaseSettings)
    ui: UISettings = field(default_factory=UISettings)
    logging: LoggingSettings = field(default_factory=LoggingSettings)
    performance: PerformanceSettings = field(default_factory=PerformanceSettings)

    environment: str = "development"
    debug: bool = False


class ConfigurationManager:
    """
    Configuration manager for loading and validating application settings.

    Supports multiple configuration sources:
    - Environment variables
    - Configuration files
    - Default values
    """

    def __init__(self, config_file: Optional[Path] = None):
        self._config_file = config_file
        self._settings: Optional[Settings] = None

    def load_settings(self) -> Settings:
        """Load settings from environment and configuration files."""
        if self._settings is None:
            self._settings = self._create_settings()
        return self._settings

    def _create_settings(self) -> Settings:
        """Create settings from environment variables."""
        return Settings(
            database=DatabaseSettings(
                path=os.getenv("COACH_DB_PATH", "coach.db"),
                backup_enabled=self._get_bool_env("COACH_DB_BACKUP_ENABLED", True),
                backup_interval=self._get_int_env("COACH_DB_BACKUP_INTERVAL", 3600),
                pool_size=self._get_int_env("COACH_DB_POOL_SIZE", 5),
                timeout=self._get_int_env("COACH_DB_TIMEOUT", 30),
            ),
            ui=UISettings(
                theme=os.getenv("COACH_THEME", "dark"),
                window_size=os.getenv("COACH_WINDOW_SIZE", "1280x800"),
                fullscreen=self._get_bool_env("COACH_FULLSCREEN", False),
                font_size=self._get_int_env("COACH_FONT_SIZE", 12),
            ),
            logging=LoggingSettings(
                level=os.getenv("COACH_LOG_LEVEL", "INFO"),
                file=os.getenv("COACH_LOG_FILE", "coach.log"),
                debug_sql=self._get_bool_env("COACH_DEBUG_SQL", False),
                max_file_size=self._get_int_env("COACH_LOG_MAX_SIZE", 10485760),
                backup_count=self._get_int_env("COACH_LOG_BACKUP_COUNT", 5),
            ),
            performance=PerformanceSettings(
                cache_size=self._get_int_env("COACH_CACHE_SIZE", 100),
                async_enabled=self._get_bool_env("COACH_ASYNC_ENABLED", False),
                lazy_loading=self._get_bool_env("COACH_LAZY_LOADING", True),
                prefetch_enabled=self._get_bool_env("COACH_PREFETCH_ENABLED", True),
            ),
            environment=os.getenv("COACH_ENV", "development"),
            debug=self._get_bool_env("COACH_DEBUG", False),
        )

    def _get_bool_env(self, key: str, default: bool) -> bool:
        """Get boolean environment variable."""
        value = os.getenv(key, "").lower()
        if value in ("true", "1", "yes", "on"):
            return True
        elif value in ("false", "0", "no", "off"):
            return False
        return default

    def _get_int_env(self, key: str, default: int) -> int:
        """Get integer environment variable."""
        try:
            return int(os.getenv(key, str(default)))
        except ValueError:
            return default

    def update_setting(self, key: str, value: Any) -> None:
        """Update a setting value."""
        if self._settings is None:
            self._settings = self.load_settings()

        # Simple dot notation support
        parts = key.split(".")
        current = self._settings

        for part in parts[:-1]:
            current = getattr(current, part)

        setattr(current, parts[-1], value)

    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a setting value."""
        if self._settings is None:
            self._settings = self.load_settings()

        # Simple dot notation support
        parts = key.split(".")
        current = self._settings

        try:
            for part in parts:
                current = getattr(current, part)
            return current
        except AttributeError:
            return default


# Global configuration manager instance
config_manager = ConfigurationManager()


def get_settings() -> Settings:
    """Get application settings."""
    return config_manager.load_settings()


def get_database_url() -> str:
    """Get database URL."""
    settings = get_settings()
    return f"sqlite:///{settings.database.path}"


def is_debug_mode() -> bool:
    """Check if debug mode is enabled."""
    return get_settings().debug


def is_development() -> bool:
    """Check if running in development environment."""
    return get_settings().environment == "development"


def is_production() -> bool:
    """Check if running in production environment."""
    return get_settings().environment == "production"