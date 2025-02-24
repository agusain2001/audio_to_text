from google.cloud import aiplatform
import logging
from config import PROJECT_ID, LOCATION, GEMINI_ENDPOINT_ID

def call_vertex_gemini(prompt, task_type="summarization"):
    """
    Calls the deployed Gemini model on Vertex AI with the provided prompt and task type.
    The task_type can be "summarization", "rewriting", or "keywords".
    """
    try:
        client = aiplatform.gapic.PredictionServiceClient()
    except Exception as e:
        logging.error("Failed to create Vertex AI PredictionServiceClient.")
        raise e

    endpoint = client.endpoint_path(project=PROJECT_ID, location=LOCATION, endpoint=GEMINI_ENDPOINT_ID)
    instance = {"prompt": prompt, "task": task_type}
    instances = [instance]
    parameters = {"temperature": 0.7, "max_output_tokens": 256}

    try:
        response = client.predict(endpoint=endpoint, instances=instances, parameters=parameters)
    except Exception as e:
        logging.error("Error during Vertex AI prediction.")
        raise e

    predictions = response.predictions
    if predictions:
        # Assuming the model returns a dictionary with key 'generated_text'
        return predictions[0].get("generated_text", "")
    else:
        raise Exception("No predictions returned from Vertex AI.")

def summarize_text(text):
    """
    Uses Vertex AI to generate a summary of the transcript.
    """
    prompt = f"Summarize the following transcript:\n{text}"
    return call_vertex_gemini(prompt, task_type="summarization")

def rewrite_text(text, variant=1):
    """
    Uses Vertex AI to produce an alternative version of the transcript.
    The 'variant' parameter adjusts the style or tone.
    """
    prompt = f"Rewrite the following text in variant {variant} style:\n{text}"
    return call_vertex_gemini(prompt, task_type="rewriting")

def generate_keywords(text, num_keywords=5):
    """
    Uses Vertex AI to extract keywords from the transcript.
    """
    prompt = f"Extract the top {num_keywords} keywords from the following text:\n{text}"
    keywords_text = call_vertex_gemini(prompt, task_type="keywords")
    # Assuming a comma-separated list is returned
    keywords = [kw.strip() for kw in keywords_text.split(",")]
    return keywords
