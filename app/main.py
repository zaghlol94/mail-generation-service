from app.predict import Predictor
from fastapi import FastAPI, HTTPException
import pathlib
import os
import sys

app = FastAPI()
root_dir = pathlib.Path(__file__).resolve().parent.parent
model_dir = os.path.join(root_dir, "model")
predictor = Predictor(model_path=model_dir)


@app.get("/generate")
def generate(prompt: str, n_gen: int, temperature: float = 0.8, top_k: int = 80, top_p: float = 0.8,
            token_count: int = 100):
    """
    <strong>:param prompt</strong>: (str) the initial text that we want to generate some other words after it.<br>
    <strong>:param n_gen </strong>: (int)  Defines how many alternatives will be returned.<br>
    <strong>:param temperature </strong>: (float, default=0.8) The value used to module the next token
        probabilities.<br>
    <strong>:param top_k</strong>: (int, default=20) the top k most likely next words are selected and the entire
        probability mass is shifted to these k words. So instead of increasing the chances of high
        probability words occurring and decreasing the chances of low probability words, we just remove low probability
        words all together We just need to set top_k to however many of the top words we want to consider for our
        conditional probability distribution.<br>
    <strong>:param top_p</strong>: (float, default=0.8)  If set to float < 1, only the most probable tokens with
        probabilities that add up to top_p or higher are kept for generation.<br>
    <strong>:param token_count</strong>:(int) maximum number of words that we want to generate per example.<br>
    <strong>:return</strong>: list of dictionary every item in the list contains one of the generated text. <br>
    """
    try:
        results = predictor.predict(prompt, token_count, n_gen, temperature, top_k, top_p)
        return {
            "status": "success",
            "ai_results": results
        }

    except Exception as error:
        e = sys.exc_info()[1]
        raise HTTPException(status_code=500, detail=str(e))
