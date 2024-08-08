# Kernel Evaluation
We are currently evaluating the [Flow2](https://www.kernel.com/products) by Kernel as a potential new neuroimaging device to acquire hyperscanning data for the [Consortium for Interacting Minds](https://www.interactingminds.com/)

This website will share information with members of our community about how to acquire and analyze data.

## Time Domain Functional Near Infrared Spectroscopy (TD-fNIRS)
TD fNIRS uses time gating to discriminate the photons arriving to the detector as a function of their time of flight. As photons traveling longer distances are more likely to have reached deeper layers of the tissue, TD-fNIRS has increased sensitivity to the brain hemodynamics when longer-traveling photons are selected. However, this advantage over CW fNIRS is limited in real instrumentation by the instrument response function (IRF), which causes a broadening of the distribution of times of flight (DTOF), complicating the inter- pretation of the time gates. Moment analysis of the DTOF,13 which is relatively immune to the IRF,14 has been proposed as an alternative to time gates analysis in TD-fNIRS. Higher statistical moments of the DTOF present increased sensitivity to deeper tissue layers compared to signal intensity changes as the kernel for the moment calculation grows as a function of the time of flight.15

A common way to summarize information from time-of-flight histograms is to compute the first three moments of the histogram corresponding to the total counts (sum), mean time-of-flight (first moment), and variance of the times of flight (second central moment) (13, 27, 28). Moments have a convenient property: the moments of the DTOF can be obtained from calculating the moments of the TPSF and of the IRF straightforwardly (27). Accordingly, with Flow2, system drift in the DTOF moments can be corrected for, using the internal IRF detector. 

using coarse time gates: here, we first deconvolve the measured IRF from the measured DTOFs, and coarsen the data to 500ps gates (0-500ps, 500-1000ps, etc

Within each module, one dedicated detector at the center of the module assumes the role of an on-board IRF detector. This detector captures light, transmitted via a waveguide from the source optical path, yielding a per-pulse waveform that temporally corresponds to each pulse from each respective wavelength. The programmable integration time for constructing histograms on each detector spans from 1ms to 800ms, with the current configuration set at 3.5ms. Each histogram collected contains signals from only one wavelength. This means our histogram sampling rate is 285.7 Hz, and considering both wavelengths, the system is able to complete spectroscopic measurements at a rate of 142.9 Hz. To avoid optical crosstalk, all lasers are not enabled at the same time. This temporal multiplexing enables lasers in an 38-state pattern, completing a full cycle of data collection for all modules and wavelengths every 76 histograms, corresponding to a system sampling frequency of 3.76 Hz. In the full headset configuration, one source operates at 7.52 Hz, which is a frequency fast enough to accurately capture pulse rate, a complementary measure to the optical properties. This temporal multiplexing provides the additional benefit of bringing the average power per source down to a level that classifies as a class 1 laser device according to the United States Food and Drug Administration Federal Laser Product Performance Standard Code of Federal Regulations Title 21 Section 1040.10 (US FDA FLPPS 21CFR1040.10).

A critical performance metric of a time-domain optical measurement system is the IRF. The IRF is a measure of the uncertainty associated with each timestamp recorded and is reflected in the histogram of accumulated events, when used in time-correlated single-photon counting (TCSPC) applications, as a smearing or broadening of the desired signal being measured.

Each component in the system plays a pivotal role in shaping the system’s IRF, with the laser and detectors emerging as the predominant influencers. The IRF is primarily shaped by the design specifics of the detector process, the laser driver circuitry, and the laser itself. Moreover, the IRF characteristics of these active components exhibit dependencies on the temperature and operating voltages of the electronics and optoelectronics, factors subject to temporal variations and fluctuations during a measurement.

A crucial element in the updated Flow2 module design is the incorporation of a dedicated reference IRF detector within each module (Fig. 1F). This detector is the exact same design as detectors employed in measuring signals from the scalp but is strategically isolated to capture light directly emitted from the lasers without traveling through tissue. This isolation provides a reliable estimate for both the IRF contribution from the detector (owing to its identical design and similar process as the signal-measuring detectors) and the IRF contribution originating from the laser. This IRF measurement is recorded continuously, at the same rate as that of the other detectors.

## Resources
- https://github.com/GriffithsLab/kernel-flow-tools
- https://openfnirs.org/community/
- mne discussion about snirf compatibility https://github.com/mne-tools/mne-python/pull/9661
- pysnirf2 https://github.com/BUNPC/pysnirf2/tree/main

## Development
- going to need something to create BIDS formatted fNIRS datasets
- going to need to write a data importer for nltools

```{tableofcontents}
```
