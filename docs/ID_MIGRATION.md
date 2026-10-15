# Updating identifiers from the original release

The audio naming update replaces category-bearing names with neutral IDs.
The separate mapping records which original question ID, track name, and audio
path corresponds to each updated neutral ID.

If you already have model outputs using the original IDs, use
[`id_mapping.json`](../data/public/audio/assets/id_mapping.json) to update
their IDs before joining them to the new questions or answers. The `questions`
array maps `old_id` to `id`; the `tracks` array maps original track names and
paths to their neutral replacements. Question and answer text and MP3 bytes
are unchanged.

New users downloading the updated packages do not need this mapping.
It is a separate compatibility file, not part of the benchmark ZIPs.
