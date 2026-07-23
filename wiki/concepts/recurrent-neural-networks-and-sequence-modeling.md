---
title: Recurrent Neural Networks and Sequence Modeling
type: concept
tags:
- neural-networks
- rnn
- nlp
aliases:
- RNN
sources:
- sources/module-1-deep-models-cnn-to-rnn.md
created: '2026-07-21'
updated: '2026-07-21'
---

## Definition

Recurrent neural networks model sequential data (text, time series) by carrying a hidden
state forward through the sequence: `h_t = f(v_wt, h_{t-1})`, where `v_wt` is the
(embedded) input at step `t` and `h_{t-1}` is the hidden state from the previous step.

## Discussion

- **Why order matters**: "The movie was good, not bad" and "The movie was bad, not
  good" contain the same bag of words but opposite sentiment — a model that just
  averages word vectors (ignoring order) can't distinguish them; a model that processes
  words *in sequence*, carrying state forward, can.
- **Words as vectors**:
  - *One-hot encoding*: each vocabulary word is a sparse indicator vector (1 at its own
    index, 0 elsewhere).
  - *Embeddings*: a learned linear layer `W_emb Xᵀ` maps one-hot vectors to dense,
    lower-dimensional vectors (`v_word = f(x_word)`) — this embedding layer is trained
    jointly with the rest of the model.
- **RNN recurrence variants**:
  - *Forward RNN*: processes the sequence left-to-right, `h_1 = f(v_w1, h_0)`, …,
    `h_T = f(v_wT, h_{T-1})`.
  - *Backward RNN*: same recurrence, processed right-to-left.
  - *Bidirectional RNN*: runs forward and backward RNNs in parallel and concatenates
    their hidden states at each position, `[h_t^forward, h_t^backward]` — gives each
    position context from both directions.
  - *Deep RNN*: stacks multiple RNN layers, each layer's hidden-state sequence feeding
    the next layer as input.
  - Whether to use `h_1`, `h_t`, or `h_T` as the feature passed to a downstream classifier
    depends on the task (e.g. `h_T`, the final hidden state, commonly summarizes the
    whole sequence for classification).
- **Task types**:
  - *Sentiment classification* (sequence → single output): input a sequence of words,
    output one probability (e.g. positive sentiment) — a many-to-one task, trained with
    softmax cross-entropy.
  - *Sequence labelling* (sequence → sequence, aligned): classical NLP tasks like
    part-of-speech tagging, named-entity recognition, word segmentation — one output
    per input position, many-to-many.
  - *Language modelling* (predict next token): given "The food was great.", predict each
    next word from the previous ones — the classic autoregressive pretraining objective.
- **Applications**: RNNs are used across stock price series, video, DNA sequences, ECG
  signals, sports/motion data, and time-series like ozone measurements — any data with a
  meaningful temporal or sequential order.
- Relationship to [[CNN Applications]]: CRNN architectures (e.g. for OCR) combine a CNN
  feature extractor with an RNN sequence model, showing the two architectures compose
  rather than compete.

## Related

- [[Module 1 - Deep Models CNN to RNN]]
- [[Linear Models as Neural Network Layers]]
- [[CNN Applications]]
