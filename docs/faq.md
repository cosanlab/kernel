# FAQ
These are answers to questions from Kernel Support
 
## Details about the nifti reconstruction
***What is the sampling frequency of the reconstructed data?***

> the data is resampled to 1hz before source reconstruction.

***How does the start and stop correspond to the experiment?***

> There is a field in the nifti header, `toffset`, which indicates the time of the first volume, with the same reference as the events. Note that the recording is cropped to 1s before the `start_experiment` trigger and 1s after the `end_experiment` trigger as part of the export.


## Details about the SNIRF file:
- ***How does the start and stop correspond to the experiment?***

> The pipeline also crops data to 1s before the `start_experiment` event and 1s after the `end_experiment` event. The timestamps of the nirs data are in the nirs/data/time key, and are using the same reference as the timestamps in the events (the first entry in the nirs/stim/data key).

***How are bad channels treated? Can we remove channels that are nans?***

> Yes, you can remove the NaNs. The SNIRF format, or maybe it’s Homer, requires (or required at some point) that all channels be present. Since some channels are rejected by our pipeline (not enough light), we fill them with NaNs in the SNIRF export.

***Is there any way to get access to the signal quality of each sensor similar to the subject setup calibration?***

> If you download SNIRF: Moments and look at the first moment, it corresponds to the intensity of the light for each channel (as the number of photons received during the 3.5ms integration period), which is a first order measure of signal quality. Note that longer channels get less photons, but are more sensitive to brain activity because the photons travel deeper on average.

***Is there any way to get ROI locations of each module beyond just the 3D coordinates?***

> The 3D coordinates are mapped to a MNI atlas. They are on the scalp so obviously won’t fall inside typically MNI atlas ROIs, but you can find the nearest ROI as a first order approximation. Of course, location of the optodes on the MNI head is approximate and won’t be anatomically correct for all subjects, depending on how you place the helmet, their head size, etc. We have been doing more work with localizing optodes on individualized head models, but we are not supporting this type of pipeline in Portal yet.

***Is there any possibility of getting MNE to natively support TD SNIRF files? I saw a thread on their Github, but after a couple of years it seems like the PR has been closed and was never merged.***

> Yes, there was some progress a while back, but it stalled. Until now it hasn’t been a priority for us, but as we are shipping more systems we may have to just do it, if nobody else in the community steps up to do it.

## Preprocessing
***Is there any where to get more details about the preprocessing that has been done to each of the different files beyond the details in the Flow2 preprints? I found references to community.kernel.com, but this page doesn't seem to work anymore.***

> We’re actually in the process of moving the contents of that (defunct) page to our Kernel docs. In short:
> - SNIRF: Moments. This is a fairly raw output, minimally preprocessed
> - Trim the data to the events (1s before first, 1s after last)
> - Remove bad channels (based on shape of histogram, counts)
> - Remove histogram noise floor (“dark counts”)
> - Compute moments (sum, mean and variance of the time-of-flight histograms)
> - SNIRF: Hb Moments. This is a more processed output. We continue the processing:
> - Convert moment changes to hb changes, using a 2-layer slab (12mm scalp) and sensitivities from a FEM model
> - Motion artifact correction: using TDDR, followed by cubic spline interpolation of remaining spikes
> - Global Superficial signal regression, using signal from short channels (8mm)
> - SNIRF: Gated. This is destined to people who want to try something else than moments (time gates, or curve fitting) for their analysis. It starts like SNIRF: Moments, then instead of converting to moments: Deconvolution (using FFT) of the real-time IRF from the histograms Reconstruction. This is as described in our recent biorxiv preprint. We use the moments, then downsample to 1Hz, and solve an inverse problem using Tikhonov regularization to constrain the solution.
> - Note that these pipelines are subject to change (which we will track in release notes), as we find better ways to process the signal.

***Is there a canonical HRF function for HbO or HbR that you recommend for GLM style analyses? Or should we just be using the standard fMRI HRF?***

> We’ve been using the standard glover HRF provided by nilearn. Our take is that for block designs it doesn’t matter too much, it’s close enough. We haven’t explored using other HRFs.

***Do you have any recommendations for plotting heatmaps of the Reconstructed data?*** 

> Just use your favorite fMRI visualization software for the NIfTI reconstructions. This is in MNI space. Can paint on the surface too.

***Is there an API for accessing web portal?***

> here's a fast way to download all the SNIRF files from a study via https://docs.kernel.com/docs/downloading-datasets and running the script within the zip file.
> 
> Exposing our API is on our roadmap and we can see if we can prioritize it. Just to clarify, you are looking for:
> - List all dataset ids and metadata in a study
> - Given a dataset id, submit a pipeline
> - Given a pipeline run id, get its status
> - Given a pipeline run id, download its outputs
