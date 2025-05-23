#!/usr/bin/env python3
"""
BookFinder AI Discord Bot

A Discord bot that uses AI to help users find books based on descriptions, themes, or partial information.
"""

import asyncio
import logging
from src.bot import main

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run the bot
    asyncio.run(main()) 