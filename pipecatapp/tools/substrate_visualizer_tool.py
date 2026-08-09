import os
import json
import logging
from typing import Any, Optional

logger = logging.getLogger("SubstrateVisualizerTool")

class SubstrateVisualizerTool:
    """
    Renders a visual representation of a holographic activation matrix.
    Generates an HTML file that visually represents the 'branched flow' of light
    through the simulated disordered potential (programmable matter).
    """

    name = "substrate_visualizer"
    description = "Generates a visual representation (HTML/SVG) of a holographic activation matrix, allowing the agent and user to see the emulated 'branched flow' paths and correlation lengths of the substrate."

    input_schema = {
        "type": "object",
        "properties": {
            "matrix_data": {
                "type": "object",
                "description": "The activation matrix data to visualize."
            },
            "output_filename": {
                "type": "string",
                "description": "The name of the HTML file to output (e.g., 'visualization.html')."
            }
        },
        "required": ["matrix_data"]
    }

    def __init__(self, output_dir: str = "visualizations"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)

    def _generate_html(self, correlation_length: float, branches: int, state: str) -> str:
        # A simple visual representation of branched flow
        # Higher correlation length = straighter lines
        # More branches = more diverging lines

        # We'll use SVG to draw the substrate
        lines_html = ""
        center_x = 250

        # Calculate divergence based on state and correlation length
        divergence = 100 if state == "scattered" else 20
        divergence = int(divergence / correlation_length)

        for i in range(branches):
            # Calculate a pseudo-random path for each branch
            offset = (i - (branches / 2)) * divergence
            lines_html += f'<path d="M 250 0 Q {center_x + offset} 250, {center_x + (offset * 1.5)} 500" stroke="cyan" stroke-width="2" fill="none" opacity="0.6" />\n'

        color = "#001a1a" if state == "focused" else "#1a0000"

        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Glitter UI: Substrate Visualization</title>
            <style>
                body {{ background-color: #0a0a0a; color: #00ffff; font-family: monospace; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0; }}
                .glass-panel {{ background: {color}; border: 1px solid #00ffff; border-radius: 8px; padding: 20px; box-shadow: 0 0 15px rgba(0, 255, 255, 0.2); }}
                svg {{ border: 1px solid rgba(0, 255, 255, 0.3); background-color: #000; }}
            </style>
        </head>
        <body>
            <div class="glass-panel">
                <h2>Holographic Memory Substrate</h2>
                <p>State: <strong>{state.upper()}</strong> | Correlation Length: <strong>{correlation_length}</strong> | Branches: <strong>{branches}</strong></p>
                <svg width="500" height="500">
                    <!-- Disordered potential background representation -->
                    <rect width="500" height="500" fill="url(#noise)" opacity="0.1" />
                    {lines_html}
                </svg>
            </div>
        </body>
        </html>
        """
        return html_template

    def run(self, matrix_data: dict, output_filename: str = "visualization.html") -> Any:
        try:
            correlation_length = matrix_data.get("correlation_length", 0.5)
            branches = matrix_data.get("branches", 15)
            state = matrix_data.get("substrate_state", "scattered")

            html_content = self._generate_html(correlation_length, branches, state)

            # Prevent directory traversal
            safe_filename = os.path.basename(output_filename)
            if not safe_filename.endswith(".html"):
                safe_filename += ".html"

            file_path = os.path.join(self.output_dir, safe_filename)

            with open(file_path, "w") as f:
                f.write(html_content)

            logger.info(f"Substrate visualization saved to {file_path}")
            return f"Successfully generated substrate visualization at: {file_path}"

        except Exception as e:
            logger.error(f"Error generating visualization: {e}")
            return f"Error generating visualization: {str(e)}"
