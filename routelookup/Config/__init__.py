"""
Configuration Control for the application
"""
# imports
from .config import DevelopmentConfig, ProductionConfig

# Config Decider
development = False # Change to False when in production mode else True

if development:
    config = DevelopmentConfig()
else:
    config = ProductionConfig()

# __all__
__all__ = [
    "config"
]