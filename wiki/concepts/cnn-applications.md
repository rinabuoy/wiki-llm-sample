---
title: CNN Applications
type: concept
tags:
- cnn
- computer-vision
- applications
aliases: []
sources:
- sources/module-1-deep-models-cnn-to-rnn.md
created: '2026-07-21'
updated: '2026-07-21'
---

## Definition

Downstream computer-vision tasks built on top of [[Convolutional Neural Networks|CNN]]
feature extraction.

## Discussion

- **Classification**: CNN outputs a single label/probability for the whole image.
  Example cited: a CNN-based system for breast cancer screening outperformed expert
  radiologists at detecting cancer from mammograms (including catching cases radiologists
  missed), per an international Nature evaluation.
- **Object detection**: output a class label *and* a bounding box `(x,y,w,h)` per object
  in the image. A naive sliding-window approach (run a CNN classifier over every possible
  box scale/position) is intractable — too many candidate regions. **Faster R-CNN**
  solves this with a **Region Proposal Network** that proposes candidate regions directly
  from shared conv feature maps, followed by RoI pooling and a classifier.
- **Semantic segmentation**: predict a class label per *pixel*, not per image. A **Fully
  Convolutional Network (FCN)** uses only convolutional layers with a downsampling path
  (encoder) then an upsampling path (decoder, via transposed convolutions —
  `tf.keras.layers.Conv2DTranspose` / `torch.nn.ConvTranspose2d`) to go from a full-res
  input to a full-res per-pixel prediction map.
- **Autoencoders**: a CNN encoder compresses an image down to a small latent vector `h`,
  and a mirrored decoder (using transposed convolutions) reconstructs the original image
  from it — trained to minimize reconstruction error, no labels needed.
- **End-to-end autonomous navigation**: multiple camera views (+ optional route map) are
  each passed through conv layers, flattened, concatenated, and fed through dense layers
  to directly output a probabilistic steering control distribution
  `P(θ|I,M) = Σ φᵢ N(μᵢ,σᵢ²)` — trained end-to-end without any human labeling.
- **OCR via Convolutional Recurrent Neural Networks (CRNN)**: convolutional layers
  extract a feature-map sequence from a text image, a deep bidirectional LSTM (see
  [[Recurrent Neural Networks and Sequence Modeling]]) models per-frame character
  distributions along that sequence, and a transcription layer decodes them into the
  final predicted text string.

## Related

- [[Module 1 - Deep Models CNN to RNN]]
- [[Convolutional Neural Networks]]
- [[CNN Architectures and Training]]
- [[Recurrent Neural Networks and Sequence Modeling]]
