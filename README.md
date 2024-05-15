## Installation and Usage

0. Create a virtual environment (if needed):

```bash
conda create -n llm-personality python=3.12
```

and activate it:

```bash
conda activate llm-personality
```

1. Copy `.env.example` and rename it to `.env`. Follow instructions
   on [this page](https://platform.openai.com/docs/api-reference/authentication) to obtain your own OpenAI API key and
   on [this page](https://huggingface.co/docs/hub/security-tokens) for HuggingFace authentication token. You may also
   need to follow instructions on [this page](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf) to access Llama 2
   models.
2. Install the requirements:

```bash
pip install -r requirements.txt
```

3Run the script:

```bash
python main.py
```

Options for the main program are

- `-m`, `--model`: model to use. Possible
  values: `"gpt-4o-2024-05-13", "gpt-4-turbo-2024-04-09", "gpt-4-0613", "gpt-3.5-turbo-0125"`
- `-p`, `--personality`: personality type. Possible
  values: `"no_personality", "agreeableness", "conscientiousness", "extraversion", "neuroticism", "openness"`
    - `-i`, `--interaction`: interaction type. Possible
      values: `"all_at_once", "one_at_a_time_same_context", "one_at_a_time_new_context"`
