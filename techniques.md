# Techniques

## Tree of Thoughts

The **Tree of Thoughts (ToT)** is a reasoning framework designed to enhance the problem-solving capabilities of large language models (LLMs). Instead of generating a single linear sequence of thoughts, the model explores multiple reasoning paths, evaluates them, and selects the most promising one. This approach mimics human problem-solving by considering various possibilities before committing to a final decision.

Some documentation on implementing ToT can be found at the following links:

- [**Tree of Thoughts: Deliberate Problem Solving with Large Language Models** by Shunyu Yao et al. (2023)](https://arxiv.org/abs/2305.10601)
- [**Langchain Expiremental Docs for ToT**](https://python.langchain.com/v0.2/api_reference/experimental/tot.html)
- [**Implementing the Tree of Thoughts in LangChain’s Chain** by AstroPomeAI](https://medium.com/@astropomeai/implementing-the-tree-of-thoughts-in-langchains-chain-f2ebc5864fac)

## Chain of Thought

The **Chain of Thought (CoT)** is a reasoning technique that enables large language models (LLMs) to break down complex problems into intermediate steps. Instead of directly predicting the final answer, the model generates a sequence of reasoning steps, allowing it to handle tasks that require multi-step reasoning. This method improves the model's ability to solve problems by making its thought process explicit, which can be particularly useful for tasks involving arithmetic, logic, or commonsense reasoning.

This approach is particularly effective in tasks where intermediate reasoning steps are crucial for arriving at the correct solution.

Chain of thought langchain documentation can be found under Langchain ToT documentation. See below:

- [**SampleCoTStrategy**](https://api.python.langchain.com/en/latest/experimental/tot/langchain_experimental.tot.thought_generation.SampleCoTStrategy.html#langchain_experimental.tot.thought_generation.SampleCoTStrategy)
- [**get_cot_prompt**](https://api.python.langchain.com/en/latest/experimental/tot/langchain_experimental.tot.prompts.get_cot_prompt.html#langchain_experimental.tot.prompts.get_cot_prompt)