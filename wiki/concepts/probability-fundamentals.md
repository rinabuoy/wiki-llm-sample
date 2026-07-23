---
title: Probability Fundamentals
type: concept
tags:
- probability
- foundations
aliases: []
sources:
- sources/module-1-the-basics.md
created: '2026-07-22'
updated: '2026-07-22'
---

## Definition

Probability formalizes uncertainty: a **sample space** `Ω` is the set of all possible
outcomes of an experiment, an **event** `A` is a subset of `Ω`, and `P(A) ∈ [0,1]` is the
likelihood of that event (0 = impossible, 1 = certain).

## Discussion

**Conditional probability & independence**

- `P(A|B) = P(A∩B) / P(B)` — the probability of `A` given `B` has occurred (restricts
  the sample space to outcomes where `B` happens).
- Two events are **independent** iff `P(A∩B) = P(A)P(B)`, equivalently `P(A|B) = P(A)`.

**Random variables**

- A random variable `X` numerically describes the outcome of an experiment. **Discrete**
  variables (dice, counts) take countable values, described by a **PMF** (probability
  mass function). **Continuous** variables (height, time) take any value in an interval,
  described by a **PDF** (probability density function). The **CDF** (cumulative
  distribution function) gives `P(X ≤ x)` in either case.
- **Expected value** `E[X]` (a.k.a. `μ`) is the long-run average / "center of mass":
  discrete `E[X] = Σ x·P(X=x)`, continuous `E[X] = ∫ x·f(x) dx`.
- **Variance** `Var(X) = E[(X−E[X])²] = E[X²] − (E[X])²`.

**Core distributions**

- **Bernoulli(p)** — single trial, two outcomes (success/failure). `E[X]=p`,
  `Var(X)=p(1−p)`.
- **Binomial(n,p)** — number of successes in `n` independent Bernoulli trials.
  `P(X=k) = C(n,k) pᵏ(1−p)ⁿ⁻ᵏ`. `E[X]=np`, `Var(X)=np(1−p)`.
- **Categorical / Multinoulli(p₁,...,p_k)** — single trial with `k` possible outcomes
  (generalizes Bernoulli); `Σ pᵢ = 1`.
- **Gaussian (Normal)(μ,σ²)** — continuous, symmetric bell curve; `f(x) =
  (1/(σ√2π))·e^(−½((x−μ)/σ)²)`. ~68/95/99.7% of mass falls within 1/2/3 standard
  deviations of `μ`.

**Bayes' Rule**

`P(A|B) = P(B|A)P(A) / P(B)` — updates a **prior** `P(A)` into a **posterior** `P(A|B)`
given a **likelihood** `P(B|A)` and the **marginal** `P(B)`. Classic use case: a spam
filter combines `P(Spam)` (prior) with `P("Free"|Spam)` (likelihood) to get
`P(Spam|"Free")` (posterior).

## Related

- [[Module 1 - The Basics]]
- [[Descriptive Statistics]]
- [[Loss Functions]] — cross-entropy loss is derived from likelihood under Bernoulli/
  Categorical output distributions
