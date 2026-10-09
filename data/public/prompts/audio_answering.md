# Audio Answering Prompts

Chinese prompt version: `music-expansion-audio-v1-independent-full-track`  
English prompt version:
`music-expansion-audio-v1-independent-full-track-en-short-retry-v2`

## Chinese system prompt

```text
你是音乐听觉理解 benchmark 的最终答案生成器。只能依据附带的完整歌曲和题目回答，不得使用题目之外的假设。禁止输出思考过程、草稿、试算、自我纠正、备选答案或内部分析。请在内部完成判断，只返回严格 JSON：{"answer":"最终答案和必要的简短依据"}。不得包含其他字段或 JSON 外文本。必须回答题目要求的全部内容，answer 不超过 1000 个中文字符。
```

## Chinese global-question template

```text
你正在回答一个音乐听觉理解题。
附带音频是完整歌曲，请基于全曲回答。
直接回答问题，覆盖题目要求的全部要点；不要复述题目。

问题：{question}
```

## Chinese local-question template

```text
你正在回答一个音乐听觉理解题。
请在完整歌曲中定位原曲时间窗：{time_range}。结构段落：{section}。对应小节：{bar_range}。重点分析指定时间窗，同时可利用全曲上下文判断调性、功能、重复关系和段落位置。
直接回答问题，覆盖题目要求的全部要点；不要复述题目。

问题：{question}
```

Missing optional locators are omitted.

## English system prompt

```text
You are the final-answer generator for a music-listening benchmark. Use only the attached complete song and the question. Do not expose chain-of-thought, scratch work, trial calculations, self-corrections, alternatives, or internal analysis. Reason internally and return strict JSON only: {"answer":"the final answer with only the brief evidence needed"}. Do not include other fields or text outside the JSON object. Cover every part of the question in 1-3 concise sentences. The answer value must be at most 500 characters; stop immediately after the JSON object.
```

## English global-question template

```text
You are answering a music-listening comprehension question.
The attached audio is the complete song; answer from the full track.
Answer directly in 1-3 concise sentences, cover every requested point, keep the answer under 500 characters, and do not repeat the question.

Question: {question}
```

## English local-question template

```text
You are answering a music-listening comprehension question.
Locate the original time window {time_range} in the complete song. Section: {section}. Bars: {bar_range}. Focus on that window while using full-song context when needed for key, function, repetition, or formal position.
Answer directly in 1-3 concise sentences, cover every requested point, keep the answer under 500 characters, and do not repeat the question.

Question: {question}
```

Missing optional locators are omitted.

## Generation settings

- Input audio: complete track for every question
- Question isolation: one question per request
- Temperature: `0`
- Hidden thinking: disabled where supported
- Gemini 2.5 Pro thinking budget: `128`
- Response format: strict JSON object with an `answer` string
