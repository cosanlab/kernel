
# Measurement
Here are details about the signals that are being measured and how they are currently being preprocessed by Kernel.

- **Moments** provide the time courses for each channel:
    - 0th moment: integral (# photons, from 0 to ~1e7),
    - 1st moment: mean time of flight (mean time of flight, in picoseconds is on the order of 1000)
    - 2nd moment: variance of time-of-flight (variance of time of flight, in picoseconds^2 is on the order of 100000)
- **Hb/Moments** includes an analysis indicating concentration of HbO (oxyhemoglobin) and HbR (deoxyhemoglobin) using the modified Beer–Lambert law. 
- **Gating** - Time Gating
- **Reconstruction** - High Density - Diffustion Optical Tomography (HD-DOT)


## Relative changes in HbO and HbR concentrations (moments method)
The data preprocessing procedures details are available in [Castillo et al., 2023](https://www.nature.com/articles/s41598-023-38258-8). Initially, we applied a channel selection method based on histogram shape criteria (14). Subsequently, histograms derived from the chosen channels were utilized to calculate the moments of the DTOFs, specifically focusing on the sum, mean, and variance moments. The alterations in preprocessed DTOF moments were then translated into changes in absorption coefficients for each wavelength, employing the sensitivities of the various moments to absorption coefficient changes, as outlined in (13). To determine these sensitivities, a 2-layer medium with a superficial layer of 12 mm thickness was employed. Utilizing a finite element modeling (FEM) forward model from NIRFAST (58, 59), the Jacobians (sensitivity maps) for each moment were integrated within each layer to assess sensitivities. The changes in absorption coefficients at each wavelength were further converted into alterations in oxyhemoglobin and deoxyhemoglobin concentrations (HbO and HbR, respectively), employing the extinction coefficients for the respective wavelengths and the modified Beer–Lambert law (mBLL (60)). The HbO/HbR concentrations underwent additional preprocessing through a motion correction algorithm known as Temporal Derivative Distribution Repair (TDDR (61)). To address spiking artifacts arising from baseline shifts during TDDR, they were identified and rectified using cubic spline interpolation (62). Lastly, data detrending was performed using a moving average with a 100-second kernel, and short channel regression was employed to eliminate superficial physiological signals from brain activity (63), utilizing short within-module channels with a source-detector separation (SDS) of 8.5 mm.

## Absolute concentrations of HbO and HbR (curve fitting method)
The DTOF results from convolving the time-resolved TPSF with the IRF. Utilizing Flow2’s online IRF measurements, we employed a curve fitting technique to extract the absolute optical properties of the tissue beneath. Generating candidate TPSFs through an analytical solution of the diffusion equation for a homogeneous semi-infinite medium, we convolved these with the known IRF and compared them with the recorded DTOF. The search for optical properties was carried out using the Levenberg-Marquardt algorithm, focusing on fitting within the range spanning from 80% of the peak on the rising edge to 0.1% of the peak on the falling edge, with a refractive index set to 1.4. These absorption coefficient estimates were then converted to HbO and HbR concentrations. A single value for HbO and HbR was obtained by computing the median value across well-coupled long, within-module channels (SDS=26.5mm) of two prefrontal modules.

## DOT reconstruction algorithm
A finite element model (FEM) of the adult head was developed based on the unbiased non-linear averages of the MNI 152 database (49). The atlas was segmented to 5 tissue types of skin, skull, CSF, gray and white matter and discretized into linear tetrahedral elements using NIRFASTSlicer, giving rise to 413,403 nodes and 2,465,366 elements. Optical properties of each tissue layer at each wavelength (690 nm and 905 nm) were assigned based on published values of the adult head (29). The coordinates for each of the 40 modules containing the optical sources and detectors were determined and identified on the surface of the FEM and the time-resolved light propagation model was solved using the diffusion approximation to the light transport equation throughout the domain (58). The Jacobians (sensitivity functions that map a change in measured data due to a change in optical properties) for the time-resolved data (TPSF) for each optical parameter (μa and μs′) were calculated using the adjoint theorem (64) at each wavelength and then interpolated to a uniform voxel grid (also known as reconstruction basis) spanning the entire model, with a resolution of 4 × 4 × 4 mm. The use of lower resolution reconstruction basis is crucial for DOT as the problem is highly under-determined: that is the number of measurements is much lower than the number of unknowns. While a high resolution FEM mesh is needed for the calculation of the time-resolved light propagation to ensure numerical accuracy, a much lower voxel resolution is needed to better improve the stability of the inverse problem.

The time-resolved Jacobian for each optical property was then mapped to each data-type (intensity, mean time of flight and variance) which was then normalized with respect to their corresponding data. A Moore–Penrose pseudoinverse with Tikhonov regularization was used to calculate an approximation of the inverse of the Jacobian to perform a single step linear recovery of the optical properties (29) using the same functional data as outlined earlier. Note that we downsampled the data to 1Hz before performing reconstruction. The recovered changes in the μa within each voxel were mapped to changes to oxy/deoxy hemoglobin for further processing using the same GLM model described above. Lastly, in addition to GLM analyses, we performed an epoched analysis. Here, we considered different ROIs given the task: voxels within 10 mm of the left motor area with the maximum GLM contrast for the finger tapping task and voxels within 10 mm of the left auditory region with maximum GLM contrast for the passive auditory task. The time course of these ROIs were then epoched and aggregated within each block type for further visualization (Fig. 7).
  
## Reconstruction Preprocessing
- Data conditioning (calibration correction)
- Data processing (Filtering, De-trending)
- Select good channels based on channel quality check
- Convert to log contrast
- Select histogram bins with contrast
- Load atlas head mesh
- Run forward model to get TPSFs, fluences, and Jacobians
- Perform Jacobian normalization and regularization
- Crop to valid channels and histogram bins
- Invert Jacobian
- Use fully processed data together with inverse Jacobian to generate reconstruction of mu_a and mu_s' per wavelength
- Use extinction coefficients to generate 3D map of HbO and HbR
- Note that we are performing reconstruction using a linearized model (as developed in the attached paper), which provides estimates of relative changes in HbO and HbR (not yet absolute estimates).
- We do the reconstruction on the full time-domain data using histograms. We've invested heavily in developing our reconstruction pipelines to fully utilize our data and are constantly working to improve its accuracy and performance so that it scales well. Our objective is to provide our customers with the best volumetric data that can then be analyzed in any NIfTI-compatible SW.
