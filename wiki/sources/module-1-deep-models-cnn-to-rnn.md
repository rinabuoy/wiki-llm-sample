---
title: Module 1 - Deep Models CNN to RNN
type: source
tags:
- applied-ai-mastery
- lecture-slides
aliases: []
sources: []
created: '2026-07-21'
updated: '2026-07-21'
---

## Summary

72-slide lecture deck, "Module 1 – Deep Models from Convolutional to Recurrent Neural
Networks", part of the *Applied AI Mastery Program* taught by [[Rina Buoy]] — a
continuation of [[Module 1 - Linear Models]]. It recaps classical ML and shows how
tabular, visual, and textual data all reduce to feature vectors fed through stacked
linear layers `ŷ = f1(f2(f3(x)))`. It then specializes that general architecture in two
directions: **convolutional neural networks (CNNs)** for spatially-structured (image)
data, and **recurrent neural networks (RNNs)** for sequential (text/time-series) data.

## Key takeaways

- Any data modality (tabular, image, text) is ultimately converted to a numeric feature
  vector/matrix and passed through the same stacked-linear-layer architecture; see
  [[Linear Models as Neural Network Layers]] for the underlying single-layer building
  block.
- **CNNs** replace full matrix multiplication with a **convolution operation** (small
  learned filters slid over the input), which is far more parameter-efficient for
  spatially-structured data and preserves local structure — see
  [[Convolutional Neural Networks]].
- Deeper does not automatically mean better: plain stacks of conv layers get *harder to
  optimize* (not just overfit) as they deepen; **ResNet's residual connections** solved
  this and enabled 100+ layer networks. Practical CNN training also depends on
  normalization layers, principled weight initialization, data augmentation, and transfer
  learning — see [[CNN Architectures and Training]].
- CNNs power classification, object detection, semantic segmentation, autoencoders,
  end-to-end autonomous control, and OCR (CNN+RNN hybrids) — see [[CNN Applications]].
- **RNNs** handle sequential data by carrying a hidden state `h_t = f(v_wt, h_{t-1})`
  forward (and optionally backward) through a sequence, which matters because word
  *order* changes meaning (e.g. "good, not bad" vs "bad, not good") — see
  [[Recurrent Neural Networks and Sequence Modeling]].
- Shared training concerns across both architectures — activation functions, loss
  functions, gradient descent, regularization, evaluation metrics — carry over unchanged
  from [[Module 1 - Linear Models]].

## Cited by

- [[Rina Buoy]]
- [[Convolutional Neural Networks]]
- [[CNN Architectures and Training]]
- [[CNN Applications]]
- [[Recurrent Neural Networks and Sequence Modeling]]
