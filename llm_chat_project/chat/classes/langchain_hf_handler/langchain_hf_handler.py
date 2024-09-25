from langchain.llms.huggingface_pipeline import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, TextStreamer
from langchain_core.prompts import PromptTemplate


class LangchainHFHandler:
    def __init__(self, init=False):
        self.model_id = ""
        self.tokenizer = None
        self.streamer = None
        self.model = None
        self.chain = None
        self.chain_output = ""

        self.prompt = ""

        if init:
            self.init_pipeline()

    def init_pipeline(self):
        if self.model_id == "":
            self.model_id = "gpt2"

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        self.streamer = TextStreamer(self.tokenizer, skip_prompt=True)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_id)

        pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            # streamer=self.streamer,
            repetition_penalty=1.1,
            temperature=0.7,
            top_p=0.95,
            top_k=40,
            max_new_tokens=500,
            do_sample=True
        )

        hf = HuggingFacePipeline(pipeline=pipe)
        template = """ """

        prompt = PromptTemplate.from_template(template)

        self.chain = prompt | hf

    def invoke_prompt(self):
        self.chain_output = self.chain.invoke({ "prompt": self.prompt })
