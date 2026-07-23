---
title: CNN Architectures and Training
type: concept
tags:
- neural-networks
- cnn
- training
aliases: []
sources:
- sources/module-1-deep-models-cnn-to-rnn.md
created: '2026-07-21'
updated: '2026-07-21'
---

## Definition

Practical concerns in designing and training [[Convolutional Neural Networks|CNNs]]:
architecture choices that made networks deeper and more accurate over time, and the
recipes needed to actually train them well.

## Discussion

**Architecture evolution (ImageNet ILSVRC winners)**: error rates dropped from 28.2%
(2010, shallow) to 2.3% (2017, 152 layers) as architectures got deeper —
AlexNet (8 layers) → VGG (19 layers) → GoogLeNet (22 layers) → ResNet/SENet (152 layers).

- **VGG-Net**: uses small 3×3 filters exclusively. A stack of three 3×3 convs has the
  same effective receptive field as one 7×7 conv, but is deeper (more non-linearities)
  and has fewer parameters (`3×(3²C²)` vs `7²C²` for C channels per layer).
- **Going deeper is not automatically better**: a plain 56-layer CNN has *higher* training
  AND test error than a 20-layer one — this is an optimization problem, not overfitting.
  **ResNet** fixes this with residual connections: each block computes `F(x) + x` (adding
  the block's input back to its output via an identity shortcut) before the ReLU,
  letting very deep networks (152 layers) train successfully — ILSVRC'15 winner at 3.57%
  top-5 error.
- **Kaiming/MSRA initialization**: for ReLU networks, initialize weights as
  `W ~ N(0,1) · sqrt(2/D_in)` — this keeps activation scale (mean/std) stable across
  layers, avoiding vanishing/exploding activations at the start of training.

**Training recipe:**
- **Image normalization**: subtract the per-channel mean and divide by the per-channel
  std (3 numbers for RGB), precomputed over the dataset — used by almost all modern
  models, an image-specific case of standardization (see
  [[Data Preprocessing for Neural Networks]]).
- **Data augmentation**: apply label-preserving transforms to training images (horizontal
  flips, random crops, contrast/brightness jitter) so the model sees more effective
  variety without collecting more data. Especially effective on small datasets like
  CIFAR; less critical for very large ones like ImageNet.
- **Transfer learning**: start from a model pretrained on a large dataset (e.g.
  ImageNet). Earlier layers are more generic (reusable), later layers more
  task-specific. Strategy depends on target dataset size/similarity:
  - little data + similar dataset → freeze conv layers, retrain only the final
    classifier layer.
  - little data + very different dataset → try another model or collect more data.
  - lots of data → finetune all layers (regardless of similarity), or train from scratch
    if data is abundant and very different.
- **Choosing hyperparameters** (a 6-step recipe): (1) check the initial loss is
  sane, (2) overfit a small sample to verify the model *can* learn, (3) find a learning
  rate that makes loss drop within ~100 iterations (try 1e-1 … 1e-5), (4) coarse grid
  search over hyperparameters for 1-5 epochs, (5) refine the grid and train longer,
  (6) inspect loss/accuracy curves.
- **Reading train/val accuracy curves**: still rising → train longer; big train/val gap
  → overfitting (add [[Regularization]] or more data); little/no gap but plateaued →
  underfitting (train longer or use a bigger model).

## Related

- [[Module 1 - Deep Models CNN to RNN]]
- [[Convolutional Neural Networks]]
- [[Regularization]]
- [[Gradient Descent and Optimization]]
- [[Data Preprocessing for Neural Networks]]
