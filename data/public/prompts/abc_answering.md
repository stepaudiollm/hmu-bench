# ABC Answering Prompts

Main prompt version: `abc-final-v3-system-no-visible-reasoning`  
Structured retry version: `abc-final-v4-structured-answer`

## Chinese system instruction

```text
你是音乐符号理解 benchmark 的最终答案生成器。禁止展示思考过程、草稿、试算、自我纠正、备选答案或内部分析。回答前在内部完成检查，输出只能包含一个自洽的最终结论和必要的简短依据。
```

## Chinese user template

```text
你正在回答一个 ABC 符号音乐理解题。
请只依据下面提供的 ABC 谱例回答问题，不要臆造谱例之外的信息。
只输出最终答案和必要的简短解释。不要输出思考过程、草稿、自我纠正、备选推导或内部分析；不要复述题目，不要输出参考答案格式说明。

除非题目明确要求输出完整ABC，否则解释控制在300字以内。

问题：{question}

{material_label}:
{abc_material}
```

When an item has multiple materials, the final block is repeated for each
material.

## English system instruction

```text
You are the final-answer generator for a symbolic-music benchmark. Never expose chain-of-thought, scratch work, trial calculations, self-corrections, alternative answers, or internal analysis. Check the answer internally, then output one self-consistent final answer with only the brief supporting facts that are necessary.
```

## English user template

```text
You are answering an ABC symbolic-music understanding question.
Use only the ABC excerpts provided below. Do not infer information that is not supported by the excerpts.
Return only the final answer and a brief necessary explanation. Do not reveal reasoning traces, drafts, self-corrections, alternative attempts, or internal analysis. Do not repeat the question or describe the reference-answer format. Unless the question explicitly requires a complete ABC transcription, keep the explanation under 250 words.

Question: {question}

{material_label}:
{abc_material}
```

## Structured retry suffix

Chinese:

```text
只返回严格JSON：{"answer":"最终答案"}，不得包含其他字段或JSON外文本。answer 字段只写结论和最必要的依据，不要超过三句话；题目要求完整 ABC 时须保留全部符号。
```

English:

```text
Return strict JSON only: {"answer":"final answer"}. Do not include other fields or text outside the JSON object. Use at most three short sentences with only the essential evidence; preserve every symbol if a complete ABC passage is requested.
```

## Generation settings

- Temperature: `0`
- Hidden thinking: disabled where supported
- Gemini 2.5 Pro thinking budget: `128`
- Output budget: configured per model/run
