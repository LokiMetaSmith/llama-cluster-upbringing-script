// sandbox.ts

// This script executes Python code in a secure, isolated environment
// using Pyodide, which runs Python in WebAssembly. It's designed to be
// called from another process (like our Python tool), which passes the
// code to be executed via standard input.

// @deno-types="https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.d.ts"
import { loadPyodide } from "https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.mjs";

async function main() {
  // 1. Read the Python code from standard input.
  const pythonCode = new TextDecoder().decode(await Deno.readAll(Deno.stdin));

  if (!pythonCode) {
    console.error("Error: No Python code was provided to the sandbox via stdin.");
    Deno.exit(1);
  }

  // 2. Initialize the Pyodide runtime.
  // On its first run, Deno will download and cache the Pyodide assets.
  const pyodide = await loadPyodide();

  // 3. Redirect Python's stdout and stderr to capture all output.
  let stdout = "";
  pyodide.setStdout({
    batched: (str: string) => {
      stdout += str + "\n";
    },
  });
  let stderr = "";
  pyodide.setStderr({
    batched: (str: string) => {
      stderr += str + "\n";
    },
  });

  try {
    // 4. If the code uses 'micropip' to install packages, load it first.
    if (pythonCode.includes("micropip")) {
      await pyodide.loadPackage("micropip");
    }

    // 5. Execute the user's Python code.
    const result = await pyodide.runPythonAsync(pythonCode);

    // 6. Print the captured output and the final result to stdout/stderr.
    if (stdout) console.log(stdout.trim());
    if (stderr) console.error(stderr.trim());

    if (result !== undefined) {
      console.log(result);
    }

  } catch (error) {
    // If an error occurs during Python execution, print it to stderr.
    console.error(`Python execution failed: ${error.message}`);
    Deno.exit(1);
  }
}

main();
