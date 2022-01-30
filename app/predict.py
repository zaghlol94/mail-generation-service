from transformers import GPT2LMHeadModel, GPT2Tokenizer


class Predictor:
    def __init__(self, model_path):
        self.model_path = model_path
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        self.model = GPT2LMHeadModel.from_pretrained(model_path)

    def predict(self, prompt, max_length, n_gen, temperature=0.8, top_k=50, top_p=0.8):
        '''
        :param prompt: (str) the initial text that we want to generate some other words after it.
        :param max_length: (int) maximum number of words that we want to generate per example.
        :param n_gen: (int) Defines how many alternatives will be returned.
        :param temperature: (float, default=0.8) The value used to module the next token probabilities.
        :param top_k: (int, default=50) the top k most likely next words are selected and the entire probability mass is
        shifted to these k words. So instead of increasing the chances of high probability words occurring and
        decreasing the chances of low probability words, we just remove low probability words all together We just need
         to set top_k to however many of the top words we want to consider for our conditional probability distribution.
        :param top_p: (float, default=0.8)  If set to float < 1, only the most probable tokens with probabilities that
        add up to top_p or higher are kept for generation.
        :return:
            list of dictionary every item in the list contains one of the generated text.
        '''
        results = []
        input_ids = self.tokenizer.encode(prompt, return_tensors='pt')
        output = self.model.generate(input_ids, max_length=max_length, do_sample=True, num_return_sequences=n_gen,
                                     temperature=temperature, top_k=top_k, top_p=top_p)
        for email in output:
            sample = self.tokenizer.decode(email, skip_special_tokens=True)
            results.append({"generated_text": sample, "text_length": len(sample)})
        return results
