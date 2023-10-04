# Real-Time Event Prediction

Symbolic time intervals (STIs) are a powerful way to represent time-series data or real-life events with varying duration, such as traffic light timing or medical treatments. STIs can be used to uniformly represent heterogeneous multivariate temporal data (time point values, instantaneous events, or time intervals), including both event-driven measurements (e.g., traffic accidents) and manual measurements (e.g., blood tests).
Temporal abstraction can be used to uniformly represent such heterogeneous multivariate temporal data using STIs. 
Frequent time intervals-related patterns (TIRPs) can be discovered from the STI data, which have proven to be valuable for knowledge discovery, as well as for use as features in classification and prediction tasks.

This repository includes implementation of our study that proposes a novel method for real-time event prediction using STIs.
Our method builds on our previous work on the continuous prediction of a single TIRP completion.
The completion of a TIRP can be inferred by calculating the probability of observing the remaining part of the pattern, given its observed part at a specific time.
We also implemented an extension of the single TIRP completion model to be capable of estimating the TIRP's completion occurrence time, in addition to the completion probability.
By continuously aggregating multiple completion models for TIRPs that end with an event of interest, we learn a continuous event prediction model that is capable of estimating the event's occurrence probability and time.
A model that leverages multiple TIRPs is expected to generalize better than a model that uses a single TIRP.