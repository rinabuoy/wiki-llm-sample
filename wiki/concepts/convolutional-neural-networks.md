---
title: Convolutional Neural Networks
type: concept
tags:
- neural-networks
- cnn
- computer-vision
aliases:
- CNN
sources:
- sources/module-1-deep-models-cnn-to-rnn.md
created: '2026-07-21'
updated: '2026-07-21'
---

## Definition

A convolutional neural network replaces the dense matrix multiply of a
[[Linear Models as Neural Network Layers|linear layer]] with a **convolution operation**:
a small learned filter (kernel) is slid over a 2D (or multi-channel) input, computing a
Hadamard product (element-wise multiply, `A∘B`) at each position and summing the result
into one output pixel, producing a **feature map**: `Y = g(W ⊙ P)` for a patch `P` under
the filter, generalized to `feature_map = input ⊛ filter`.

## Discussion

- **Filters as feature detectors**: different filter weights produce different feature
  maps from the same image — e.g. a sharpen kernel `[[0,-1,0],[-1,5,-1],[0,-1,0]]` or edge
  detection kernels highlight different structure. A conv layer learns many such filters
  in parallel.
- **Spatial arrangement of the output volume** — layer shape is `h × w × d` where `d`
  (depth) = number of filters. Key hyperparameters: **kernel size** (`K_H × K_W`),
  **number of filters** (`C_out`), **padding** (`P`), **stride** (`S`, the filter's step
  size). Given input `C_in × H × W`:
  - Weight matrix: `C_out × C_in × K_H × K_W`; bias vector: `C_out`.
  - Output size: `C_out × H' × W'` where `H' = (H − K + 2P)/S + 1` (same for `W'`).
  - Common settings: `K=3,P=1,S=1` (3×3 conv, preserves size — "same" padding is
    `P=(K−1)/2`); `K=1,P=0,S=1` (1×1 conv); `K=3,P=1,S=2` (downsample by 2).
  - **Receptive field**: the locations in the input image that a given output node is
    path-connected to.
  - Parameter count example: 10 filters of 5×5 over a 3-channel input = `10×(3·5·5+1
    bias) = 760` learnable parameters, `768K` multiply-add FLOPs.
- **Padding**: zero-pad the input border so the filter can be centered on edge pixels
  (and to control output size).
- **Strided convolutions**: moving the filter by more than 1 pixel per step downsamples
  the output directly.
- **Non-linearity**: ReLU (`g(z)=max(0,z)`) is applied pixel-by-pixel after every
  convolution — without it, stacked convolutions would still just be linear (see
  [[Linear Models as Neural Network Layers]]).
- **Pooling** (e.g. max-pool with a 2×2 filter, stride 2): downsamples feature maps
  further, giving reduced dimensionality and *spatial invariance* (small shifts in the
  input don't change the pooled output much).
- **Transposed convolution (deconvolution)**: runs the convolution "in reverse" to
  *upsample* a smaller feature map back to a larger spatial size — used in segmentation
  and autoencoder decoders.
- **A full CNN** = stacked (convolution → non-linearity → pooling) blocks for feature
  extraction, followed by a flattening operation and fully-connected layers (an MLP) to
  produce final scores.
- **Normalization of activations** stabilizes training: Batch Norm, Layer Norm, Instance
  Norm, and Group Norm differ only in which axes (N, C, H, W) statistics are computed
  over. LayerNorm's recipe: normalize per-sample (`μ,σ` over the feature dim), then
  apply *learned* scale/shift parameters `γ, β`: `y = γ(x−μ)/σ + β`.

## Related

- [[Module 1 - Deep Models CNN to RNN]]
- [[Linear Models as Neural Network Layers]]
- [[CNN Architectures and Training]]
- [[CNN Applications]]
