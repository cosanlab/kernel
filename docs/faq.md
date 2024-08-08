# Questions for Kernel
- Is reconstruction resampled to 1hz?
- Is reconstruction start on the onset of 'start_experiment' and end at the end of the experiment? (start_experiment duration)
- In the SNIRF file, do the block onsets correpond to start of experiment?  or the start of the recording?
- How are bad channels treated?
- Is there any way to get the signal quality from each sensor from calibration?
- Is there any way to get ROI locations of each module?

ur answers are below. Glad to see you are having fun with the device!
 
1) Nifti Reconstruction:
- is the nifti reconstruction resampled to 1hz?

Yes, the data is resampled to 1hz before source reconstruction.

- how does the start and stop correspond to the experiment? It seems like the starting time corresponds to the starting time of the experiment, not the recording.

There is a field in the nifti header, `toffset`, which indicates the time of the first volume, with the same reference as the events. Note that the recording is cropped to 1s before the `start_experiment` trigger and 1s after the `end_experiment` trigger as part of the export.

- do you have any recommendations for how to deal with the signal inhomogeneities across channels? We are finding that the PFC channels have a lot of variance, but not the sensorimotor channels, which probably has to do with the dark hair color of our participant.

I’m not entirely sure I understand the question, which mentions channels yet is nested under the NIfTI reconstruction heading.

2) SNIRF file:
- unlike the reconstruction file, I'm assuming that the start time corresponds to the start of the data recording and that each event time corresponds to the onset of the recording?

The pipeline also crops data to 1s before the `start_experiment` event and 1s after the `end_experiment` event. The timestamps of the nirs data are in the nirs/data/time key, and are using the same reference as the timestamps in the events (the first entry in the nirs/stim/data key).

- how are bad channels treated? I've just been removing channels that are nans.

Yes, you can remove the NaNs. The SNIRF format, or maybe it’s Homer, requires (or required at some point) that all channels be present. Since some channels are rejected by our pipeline (not enough light), we fill them with NaNs in the SNIRF export.

- is there any way to get access to the signal quality of each sensor similar to the subject setup calibration?

If you download SNIRF: Moments and look at the first moment, it corresponds to the intensity of the light for each channel (as the number of photons received during the 3.5ms integration period), which is a first order measure of signal quality. Note that longer channels get less photons, but are more sensitive to brain activity because the photons travel deeper on average.

- Is there any way to get ROI locations of each module beyond just the 3D coordinates?

The 3D coordinates are mapped to a MNI atlas. They are on the scalp so obviously won’t fall inside typically MNI atlas ROIs, but you can find the nearest ROI as a first order approximation. Of course, location of the optodes on the MNI head is approximate and won’t be anatomically correct for all subjects, depending on how you place the helmet, their head size, etc. We have been doing more work with localizing optodes on individualized head models, but we are not supporting this type of pipeline in Portal yet.

- is there any possibility of getting MNE to natively support TD SNIRF files? I saw a thread that Julien commented on their Github, but after a couple of years it seems like the PR has been closed and was never merged.

Yes, there was some progress a while back, but it stalled. Until now it hasn’t been a priority for us, but as we are shipping more systems we may have to just do it, if nobody else in the community steps up to do it.

4) Is there any where to get more details about the preprocessing that has been done to each of the different files beyond the details in the Flow2 preprints? I found references to community.kernel.com, but this page doesn't seem to work anymore.

We’re actually in the process of moving the contents of that (defunct) page to our Kernel docs. In short:
SNIRF: Moments. This is a fairly raw output, minimally preprocessed
Trim the data to the events (1s before first, 1s after last)
Remove bad channels (based on shape of histogram, counts)
Remove histogram noise floor (“dark counts”)
Compute moments (sum, mean and variance of the time-of-flight histograms)
SNIRF: Hb Moments. This is a more processed output. We continue the processing:
Convert moment changes to hb changes, using a 2-layer slab (12mm scalp) and sensitivities from a FEM model
Motion artifact correction: using TDDR, followed by cubic spline interpolation of remaining spikes
Global Superficial signal regression, using signal from short channels (8mm)
SNIRF: Gated. This is destined to people who want to try something else than moments (time gates, or curve fitting) for their analysis. It starts like SNIRF: Moments, then instead of converting to moments:
     4. Deconvolution (using FFT) of the real-time IRF from the histograms
Reconstruction. This is as described in our recent biorxiv preprint. We use the moments, then downsample to 1Hz, and solve an inverse problem using Tikhonov regularization to constrain the solution.
I hope this helps. Note that these pipelines are subject to change (which we will track in release notes), as we find better ways to process the signal.

5) is there a canonical HRF function for HbO or HbR that you recommend for GLM style analyses? Or should we just be using the standard fMRI HRF?

We’ve been using the standard glover HRF provided by nilearn. Our take is that for block designs it doesn’t matter too much, it’s close enough. We haven’t explored using other HRFs.

6) Do you have any recommendations for plotting heatmaps of the Reconstructed data? I've just been averaging over the z-dimension, but that doesn't seem to be the most ideal.

Just use your favorite fMRI visualization software for the NIfTI reconstructions. This is in MNI space. Can paint on the surface too.