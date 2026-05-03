use extism_pdk::*;
use serde::{Deserialize, Serialize};

#[derive(Deserialize)]
struct InputData {
    text: String,
    action: String,
}

#[derive(Serialize)]
struct OutputData {
    result: String,
}

#[plugin_fn]
pub fn process_text(input: String) -> FnResult<String> {
    let data: InputData = serde_json::from_str(&input)?;

    let result = match data.action.as_str() {
        "uppercase" => data.text.to_uppercase(),
        "lowercase" => data.text.to_lowercase(),
        "reverse" => data.text.chars().rev().collect(),
        _ => format!("Unknown action: {}", data.action),
    };

    let output = OutputData { result };
    let json_output = serde_json::to_string(&output)?;

    Ok(json_output)
}
