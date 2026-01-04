import httpx
import logging
import os
import json

class PromptImproverTool:
    """A tool to improve user prompts by generating a structured prompt plan.

    This tool uses a multi-step process inspired by Vibe Scaffold to turn a
    rough user idea into a detailed One Pager, Developer Specification, and
    finally a comprehensive Prompt Plan.
    """
    def __init__(self, twin_service):
        self.twin_service = twin_service
        self.name = "prompt_improver"
        self.description = "Converts a rough idea into a structured prompt plan (One Pager -> Dev Spec -> Prompt Plan)."

        # Step 1: One Pager Prompt
        self.step1_prompt = """Here is a description of an app idea:
{user_input}

Please compile this into a clean, comprehensive one-pager. Include the problem, audience, ideal customer, platform, and flow information, such that we could start talking with product & engineering leadership about how this could be built.
"""

        # Step 2: Developer Spec Prompt
        self.step2_prompt = """Using the following One Pager, compile a comprehensive, developer-ready specification. Include all relevant requirements, architecture choices, data handling details, error handling strategies, and a testing plan so a developer can immediately begin implementation.

One Pager:
{one_pager}
"""

        # Step 3: Prompt Plan Prompt
        self.step3_prompt = """Using the following Developer Spec, draft a detailed, step-by-step blueprint for building this project. The blueprint needs to be structured such that we can build components of the app in stages, such that they can be tested and verified manually before moving on to the next component. Then, once you have a solid plan, break it down into small, iterative chunks that build on each other. Look at these chunks and then go another round to break it into small steps. Review the results and make sure that the steps are small enough to be implemented safely with strong testing, but big enough to move the project forward. Iterate until you feel that the steps are right sized for this project.

From here you should have the foundation to provide a series of prompts for a code-generation LLM that will implement each step in a test-driven manner. If manual steps are necessary, note these each as a separate step in the overall series. Prioritize best practices, incremental progress, and early testing, ensuring no big jumps in complexity at any stage. Make sure that each prompt builds on the previous prompts, and ends with wiring things together. There should be no hanging or orphaned code that isn't integrated into a previous step. The prompt plus manual plan should cover the spec entirely, and result in a complete, working MVP.

Make sure and separate each prompt section. Use markdown. Each prompt should be tagged as text using code tags. The goal is to output prompts, but context, etc is important as well.

Include, after each prompt, a set of todo checkboxes that the AI agents can check off, that capture the changes that the prompt contains.

Developer Spec:
{dev_spec}
"""

    async def _discover_llm(self) -> str:
        """Asynchronously discovers the main LLM service via Consul."""
        service_name = os.getenv("PRIMA_API_SERVICE_NAME", "llama-api-main")
        consul_addr = self.twin_service.consul_http_addr
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{consul_addr}/v1/health/service/{service_name}?passing", timeout=5)
                response.raise_for_status()
                services = response.json()
                if services:
                    address = services[0]['Service']['Address']
                    port = services[0]['Service']['Port']
                    return f"http://{address}:{port}/v1"
        except Exception as e:
            logging.error(f"Error discovering LLM service: {e}")
        return ""

    async def _call_llm(self, prompt: str) -> str:
        """Asynchronously calls the LLM."""
        base_url = await self._discover_llm()
        if not base_url:
            return "Error: LLM service not found."

        chat_url = f"{base_url}/chat/completions"
        headers = {"Content-Type": "application/json"}
        model_name = os.getenv("VISION_MODEL_NAME", "llava-llama-3")

        payload = {
            "model": model_name,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 2048,
            "temperature": 0.7
        }

        try:
            async with httpx.AsyncClient(timeout=120) as client:
                response = await client.post(chat_url, headers=headers, json=payload)
                response.raise_for_status()
                return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            logging.error(f"Error calling LLM: {e}")
            return f"Error calling LLM: {e}"

    async def create_prompt_plan(self, user_input: str) -> str:
        """Generates a prompt plan from user input.

        Args:
            user_input (str): The rough idea or description from the user.

        Returns:
            str: The generated Prompt Plan (or error message).
        """

        # Step 1: One Pager
        logging.info("PromptImprover: Generating One Pager...")
        one_pager_prompt = self.step1_prompt.format(user_input=user_input)
        one_pager = await self._call_llm(one_pager_prompt)

        if one_pager.startswith("Error"):
            return f"Failed to generate One Pager: {one_pager}"

        # Step 2: Dev Spec
        logging.info("PromptImprover: Generating Developer Spec...")
        dev_spec_prompt = self.step2_prompt.format(one_pager=one_pager)
        dev_spec = await self._call_llm(dev_spec_prompt)

        if dev_spec.startswith("Error"):
            return f"Failed to generate Developer Spec: {dev_spec}"

        # Step 3: Prompt Plan
        logging.info("PromptImprover: Generating Prompt Plan...")
        prompt_plan_prompt = self.step3_prompt.format(dev_spec=dev_spec)
        prompt_plan = await self._call_llm(prompt_plan_prompt)

        if prompt_plan.startswith("Error"):
            return f"Failed to generate Prompt Plan: {prompt_plan}"

        return prompt_plan
