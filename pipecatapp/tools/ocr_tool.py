import os
import torch
import tempfile
from pydantic import BaseModel, Field

class OCRToolInput(BaseModel):
    file_path: str = Field(description="The path to the image (.jpg, .png) or PDF (.pdf) file to process with OCR.")
    prompt: str = Field(default="<image>document parsing.", description="The prompt to guide the OCR extraction. Defaults to generic document parsing.")

class OCRTool:
    """A tool to extract text from an image or PDF using the baidu/Unlimited-OCR model."""
    name = "ocr_tool"
    description = "Use this tool to extract text, tables, and parse contents from an image or PDF file using a powerful OCR model. Provide the absolute file_path."
    input_schema = {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The path to the image (.jpg, .png) or PDF (.pdf) file to process with OCR."
            },
            "prompt": {
                "type": "string",
                "default": "<image>document parsing.",
                "description": "The prompt to guide the OCR extraction. Defaults to generic document parsing."
            }
        },
        "required": ["file_path"]
    }

    def __init__(self):
        # We don't initialize the model here to save memory.
        # It's loaded on-demand when the tool is run.
        self.model_name = "baidu/Unlimited-OCR"
        self.model_path = "/opt/nomad/models/vision/Unlimited-OCR"

        # Check if the model exists locally in the cluster cache, otherwise use HF repo
        if not os.path.exists(self.model_path):
            self.model_path = self.model_name

        self._model = None
        self._tokenizer = None

    def _load_model(self):
        if self._model is None or self._tokenizer is None:
            from transformers import AutoModel, AutoTokenizer
            print(f"Loading OCR model from {self.model_path}...")

            # Check for CUDA availability
            device = "cuda" if torch.cuda.is_available() else "cpu"
            dtype = torch.bfloat16 if torch.cuda.is_available() and torch.cuda.is_bf16_supported() else torch.float32

            self._tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            self._model = AutoModel.from_pretrained(
                self.model_path,
                use_safetensors=True,
                torch_dtype=dtype,
            )
            self._model = self._model.eval().to(device)
            print("OCR model loaded successfully.")

    def _pdf_to_images(self, pdf_path, dpi=300):
        import fitz # PyMuPDF
        doc = fitz.open(pdf_path)
        tmp_dir = tempfile.mkdtemp(prefix='pdf_ocr_')
        mat = fitz.Matrix(dpi / 72, dpi / 72)
        paths = []
        for i, page in enumerate(doc):
            out = os.path.join(tmp_dir, f'page_{i+1:04d}.png')
            page.get_pixmap(matrix=mat).save(out)
            paths.append(out)
        doc.close()
        return paths, tmp_dir

    def run(self, **kwargs):
        file_path = kwargs.get("file_path")
        prompt = kwargs.get("prompt", "<image>document parsing.")

        if not file_path or not os.path.exists(file_path):
            return f"Error: File not found at path '{file_path}'"

        try:
            self._load_model()

            # Temporary directory for outputs
            tmp_out_dir = tempfile.mkdtemp(prefix='ocr_out_')
            result_text = ""

            if file_path.lower().endswith('.pdf'):
                # Handle PDF
                print(f"Processing PDF: {file_path}")
                image_paths, tmp_img_dir = self._pdf_to_images(file_path)

                if not image_paths:
                     return "Error: Could not extract any images from the PDF."

                # model.infer_multi is intended for multi-page parsing
                self._model.infer_multi(
                    self._tokenizer,
                    prompt=prompt,
                    image_files=image_paths,
                    output_path=tmp_out_dir,
                    image_size=1024,
                    max_length=32768,
                    no_repeat_ngram_size=35, ngram_window=1024,
                    save_results=True,
                )

                # Check for output result
                # Based on the model API, check what it saves or if infer_multi returns the text directly
                # In many transformers OCR recipes, the infer method might save a json or txt to the output_path.
                # Assuming it returns text directly or we can read it from the output dir.

                # Actually, according to the Unlimited-OCR README:
                # `model.infer_multi(...)` does the inference. Let's see if we can capture the output.
                # The README uses save_results=True, which saves to output_path. Let's read from it.

                for file_name in sorted(os.listdir(tmp_out_dir)):
                     if file_name.endswith('.txt'):
                         with open(os.path.join(tmp_out_dir, file_name), 'r') as f:
                             result_text += f.read() + "\n\n"

                # Cleanup temp images
                import shutil
                shutil.rmtree(tmp_img_dir, ignore_errors=True)

            else:
                # Handle Image
                print(f"Processing Image: {file_path}")
                self._model.infer(
                    self._tokenizer,
                    prompt=prompt,
                    image_file=file_path,
                    output_path=tmp_out_dir,
                    base_size=1024, image_size=640, crop_mode=True,
                    max_length=32768,
                    no_repeat_ngram_size=35, ngram_window=128,
                    save_results=True,
                )

                for file_name in sorted(os.listdir(tmp_out_dir)):
                     if file_name.endswith('.txt'):
                         with open(os.path.join(tmp_out_dir, file_name), 'r') as f:
                             result_text += f.read() + "\n\n"

            import shutil
            shutil.rmtree(tmp_out_dir, ignore_errors=True)

            if not result_text.strip():
                 return "OCR completed, but no text was extracted or found in the output directory."

            return f"OCR Extraction Results:\n{result_text}"

        except Exception as e:
            return f"Error during OCR extraction: {str(e)}"
