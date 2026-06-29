import os
import json
import torch
from datasets import load_dataset
try:
    from unsloth import FastLanguageModel
    from trl import SFTTrainer
except ImportError:
    # Handle mock environment where unsloth is missing
    FastLanguageModel = None
    SFTTrainer = None
from transformers import TrainingArguments, TrainerCallback

class TelemetryCallback(TrainerCallback):
    def __init__(self, log_file):
        self.log_file = log_file

    def on_log(self, args, state, control, logs=None, **kwargs):
        if logs is not None:
            with open(self.log_file, "a") as f:
                log_entry = {"step": state.global_step}
                log_entry.update(logs)
                f.write(json.dumps(log_entry) + "\n")

def main():
    # Read config from environment variable
    config_str = os.environ.get("CONFIG_JSON", "{}")
    config = json.loads(config_str)

    job_id = os.environ.get("MTAC_JOB_ID", "local")
    workspace_dir = f"/workspace/{job_id}"
    os.makedirs(workspace_dir, exist_ok=True)

    metrics_file = os.path.join(workspace_dir, "metrics.jsonl")

    model_name = config.get("model", "unsloth/llama-3-8b-bnb-4bit")
    dataset_name = config.get("dataset", "yahma/alpaca-cleaned")
    max_steps = config.get("max_steps", 60)

    print(f"Starting MTaC SFT Training for {job_id}")
    print(f"Model: {model_name}, Dataset: {dataset_name}, Steps: {max_steps}")

    try:
        if FastLanguageModel is None:
            print("Unsloth library not found. Running mock loop.")
            for i in range(max_steps):
                with open(metrics_file, "a") as f:
                    f.write(json.dumps({"step": i, "loss": 2.0 / (i + 1)}) + "\n")
            print("Mock training complete.")
            return

        model, tokenizer = FastLanguageModel.from_pretrained(
            model_name=model_name,
            max_seq_length=2048,
            dtype=None,
            load_in_4bit=True,
        )

        model = FastLanguageModel.get_peft_model(
            model,
            r=16,
            target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
            lora_alpha=16,
            lora_dropout=0,
            bias="none",
            use_gradient_checkpointing=True,
            random_state=3407,
            use_rslora=False,
            loftq_config=None,
        )

        # Note: In production you would format the text column appropriately.
        dataset = load_dataset(dataset_name, split="train[:1000]") # small subset for testing

        trainer = SFTTrainer(
            model=model,
            tokenizer=tokenizer,
            train_dataset=dataset,
            dataset_text_field="text",
            max_seq_length=2048,
            dataset_num_proc=2,
            args=TrainingArguments(
                per_device_train_batch_size=2,
                gradient_accumulation_steps=4,
                warmup_steps=5,
                max_steps=max_steps,
                learning_rate=2e-4,
                fp16=not torch.cuda.is_bf16_supported(),
                bf16=torch.cuda.is_bf16_supported(),
                logging_steps=1,
                optim="adamw_8bit",
                weight_decay=0.01,
                lr_scheduler_type="linear",
                seed=3407,
                output_dir=os.path.join(workspace_dir, "outputs"),
            ),
            callbacks=[TelemetryCallback(metrics_file)]
        )

        trainer_stats = trainer.train()

        print(f"Training completed successfully. Metrics logged to {metrics_file}")

    except Exception as e:
        print(f"Error during training: {e}")
        with open(metrics_file, "a") as f:
            f.write(json.dumps({"error": str(e)}) + "\n")
        raise

if __name__ == "__main__":
    main()
