import asyncio
from pipecatapp.tools.autoresearch_tool import AutoresearchTool

class MockLLM:
    def generate(self, prompt):
        return "<final_code>\ndef test():\n    print('Hello')\n</final_code>"

async def main():
    tool = AutoresearchTool(llm_client=MockLLM())
    print("tool initialized")

asyncio.run(main())
