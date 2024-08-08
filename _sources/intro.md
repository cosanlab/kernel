# Kernel Evaluation
We are currently evaluating the [Flow2](https://www.kernel.com/products) by Kernel as a potential new neuroimaging device to acquire hyperscanning data for the [Consortium for Interacting Minds](https://www.interactingminds.com/)

This website will share information with members of our community about how to acquire and analyze the data. We recommend reading the Kernel preprint on the [validation](https://www.biorxiv.org/content/10.1101/2024.04.30.591765v1.abstract) and [reliability](https://www.nature.com/articles/s41598-024-68555-9) of the Flow2 system.

## Time Domain Functional Near Infrared Spectroscopy (TD-fNIRS)
Time-Domain Near-Infrared Spectroscopy (TD-NIRS) is an advanced non-invasive technique used to measure the optical properties of biological tissues, primarily for medical and physiological studies. Near-infrared light can penetrate several centimeters into biological tissues, making TD-NIRS suitable for monitoring deep tissue and brain activities. TD-fNIRS systems use short pulses of light and detectors capable of measuring single photons to capture a distribution of times of flight (DTOF) of photons. This fine-grained measurement capability allows TD-fNIRS systems to measure absolute optical properties of the underlying tissue including the absorption (μa) and reduced scattering (μs′) coefficients, instead of only measuring relative changes in light intensity like continuous wave (CW) systems. The increased information from TD-fNIRS systems also allows for advanced signal processing methods to more heavily weight photons that arrive late in the DTOF in order to emphasize data from deeper in the head (i.e., from the brain). TD-fNRIS  allows for the quantification of absolute concentrations of chromophores, such as oxyhemoglobin and deoxyhemoglobin. This provides precise measurements of tissue oxygenation and hemodynamics.

### Principle of Operation:

TD-fNIRS systems use short pulses of light and detectors capable of measuring single photons to capture a distribution of times of flight (DTOF) of photons. This fine-grained measurement capability allows TD-fNIRS systems to measure absolute optical properties of the underlying tissue including the absorption (μa) and reduced scattering (μs′) coefficients, instead of only measuring relative changes in light intensity like continuous wave (CW) systems. The increased information from TD-fNIRS systems also allows for advanced signal processing methods to more heavily weight photons that arrive late in the DTOF in order to emphasize data from deeper in the head (i.e., from the brain).

### Quantitative Information:

TD fNIRS uses time gating to discriminate the photons arriving to the detector as a function of their time of flight. As photons traveling longer distances are more likely to have reached deeper layers of the tissue, TD-fNIRS has increased sensitivity to the brain hemodynamics when longer-traveling photons are selected. However, this advantage over CW fNIRS is limited in real instrumentation by the instrument response function (IRF), which causes a broadening of the distribution of times of flight (DTOF), complicating the inter- pretation of the time gates. Moment analysis of the DTOF, which is relatively immune to the IRF, has been proposed as an alternative to time gates analysis in TD-fNIRS. Higher statistical moments of the DTOF present increased sensitivity to deeper tissue layers compared to signal intensity changes as the kernel for the moment calculation grows as a function of the time of flight.

A common way to summarize information from time-of-flight histograms is to compute the first three moments of the histogram corresponding to the total counts (sum), mean time-of-flight (first moment), and variance of the times of flight (second central moment). Moments have a convenient property: the moments of the DTOF can be obtained from calculating the moments of the TPSF and of the IRF straightforwardly. Accordingly, with Flow2, system drift in the DTOF moments can be corrected for, using the internal IRF detector. However, the instrument response function (IRF) can complicate data interpretation in TD-fNIRS. To address this, moment analysis of the distribution of times of flight (DTOF) has been proposed as an alternative to time gates analysis. Higher statistical moments of the DTOF show increased sensitivity to deeper tissue layers.

![flow2](images/flow2.png)


## Flow 2

![dtof](images/DTOF.png)

## Resources

We recommend reading the Kernel preprint on the [validation](https://www.biorxiv.org/content/10.1101/2024.04.30.591765v1.abstract) and [reliability](https://www.nature.com/articles/s41598-024-68555-9) of the Flow2 system.

- https://github.com/GriffithsLab/kernel-flow-tools
- https://openfnirs.org/community/
- mne discussion about snirf compatibility https://github.com/mne-tools/mne-python/pull/9661
- pysnirf2 https://github.com/BUNPC/pysnirf2/tree/main

## Development
- going to need something to create BIDS formatted fNIRS datasets
- going to need to write a data importer for nltools

```{tableofcontents}
```
