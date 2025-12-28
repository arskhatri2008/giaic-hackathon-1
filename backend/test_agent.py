#!/usr/bin/env python3
"""Test script to verify agent functionality"""

import asyncio
from agent import ask_question

async def test():
    print("Testing agent with query: 'What is ROS 2?'")
    result = await ask_question('What is ROS 2?')
    print('Agent response:')
    print(result)
    return result

if __name__ == "__main__":
    asyncio.run(test())