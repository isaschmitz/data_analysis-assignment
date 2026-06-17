# Table of contents
1. [Introduction](#introduction)
2. [Characterize the data in time domain](#characterize-the-data-time-domain)
    - [Introduction to the time series](#introduction-to-the-time-series)
    - [Properties of the time series](#properties-of-the-time-series)
3. [The Spectrum](#the-spectrum-frequency-domain)
    - [Welch's power spectrum](#welchs-power-spectrum)
        - [Dominant Timescales](#dominant-timescales)
        - [Parseval Ratio](#parseval-ratio)
4. [Apply a filter](#apply-a-filter)
    - [Filter design](#filter-design)
    - [Comparison to boxcar](#comparison-to-boxcar)
    - [Welch's spectrum with filtered times series](#welch-spectrum-with-filtered-time-series)
5. [Conclusion](#conclusion)
6. [Sources](#sources)




# Introduction
This report aims to characterize the meridional ovetrurning at the OSNAP East location between Greenland and Scotland. The dataset was loaded using the AMOCatlas package and includes both OSNAP East and West and their respective components like meidional heat- and freshwater transport as well as a variable denoting the maximum of the overturnng streamfunction in sigma_theta coordinates. The latter (MOC_EAST_SIGMA0) is the one analyzed in this assignment, where 0 denotes the reference level used for the calculations. 
![Filter](../figures/image.png)

# Characterize the data (time domain)

## Introduction to the time series 
OSNAP (Overturning in the subpolar North ALtnatic) is an observational program which provides information about transport and hydrographic esimates between 2014 and 2022.

## Properties of the time series 
The timeseries of the MOC at OSNAP-East begins 2014-08-01 at 12pm and ends in 2022-07-01 also at 12pm, which results in a record length of 7 years and 11 months. We have a monthly resolution, which can be seen when comparing consecutive timesteps. The sample is always given at the first day of the month at 12pm. 

Our timeseries has no missing values, which was determined by summing all NaNs present and printing them (0) and also summing all values which are extremely large (0), which is sometimes used as a filler for missing values. Therefore no gap-handling method was needed or applied. As linear interpolation was used when handling the input data for this transport estimate, it would probably also be my choice if this dataset would have had gaps. 

The MOC timeseries is centered around a mean strength of 16.4 Sv with a standard deviation of 2.9 Sv. The amplitude ranges from 10.4 Sv as a minimum strength which was observed in ______ up to 23.7 Sv, which was seen in ____.
![Histogram MOC](../figures/hist_moc_osnap_east.png)
*Figure 1: Histrogram of MOC OSNAP-East*

In figure 1, we see the histrogram of the amplitude distribution of the MOC strength. Surprisingly it is relatively nomally distributed, although we only have monthly values for a ~8 year record. The most values lie in the 14 Sv bin, whcih is probably why the mean is around 16 Sv, although we have so many higher values as well. Interestingly there are no measurements which fall into the 20 or 22 Sv bin, whch makes the histogram appear discontinued. 

# The spectrum (frequency domain) 

## Welch's power spectrum
Here we now translate our timeseries into frequency space to determine spectral properties. What is important for this analysis is a continuos time axis, so if there would have been any gaps in the dataset a linear interpolation would be necessary.

After that the periodogram can be calculated. The default window chosen for this is boxcar. Other windows would be a better choice to prevents leakage as we now have less sidelobes and a more tapered distribution. the boxcar window is great for time domain, and hann is good for frequency domain and tukey is kind of middle of the road, so okay in time- and in frequency domain. 

THe next thing that is important is to define the segment length. We only have monthly data, which sets the maximum length of our segments to be 96, which results in year-long segments. If this is our segment length we would naturally choose the overlap to be half of the segment length, so 48. In this figure different segment lengths and their respective overlap are shown. 

![Welch unfilt](../figures/welch_unfilt.png)

This figure aims to illustrate the differences when choosing segment lenghts and what signals you can still capture with which segment lenght. If I needed to choose how many segments to take, I would probably opt for the 2 year long segments. It best represents the structure of the priodogram, while making it smoother, to easily capture the dominant timescales.
### Dominant timescales
Here, the dominant timescales fall into the frequency of 1/year which highlights a stronger annual variability. In addition to that there is also a peak visible at a freqency of 1/3 months. This could be due to monthly variability or data artifacts from 3 monthly ARGO obvservations. (????)
There is no rolloff seen in this periodogram, probably because we do not have any signal which are more frequent than on monthly timescales. 


### Parseval ratio
The parseval ratio is a good way to determine if your spectral analysis shows the same as the time analysis. Here we compare the variance of our parameter x. In the time domain we take the variance using numpy (np.var(x)) and in frequency domain we sum our power spectral density and multiply by our timestep length. If both of these parameters are equal we are doing a good job. Therefore we look at the ratio of both, which should be 1. Here our variance in the time domain is 8.364, in the periodogram it is 8.339  and in welch it is 7.485, which gives a parseval ratio of 0.997 if we consider time domain and periodogram. If we compare our time domain to our Welch spectrum we get 0.873. 
### Chi-squared confidence interval and degrees of freedom 
In order to be more confident in our visualized periodogram/ Welch spectrum we can also calculate the chi² confidence interval. This confidence interval is determined by our degrees of freedom, which are twice our number of averaged segments. This means, if we average 4 sections, our dof's would be 8 nd this would determine our confidence interval. 

# Apply a filter 
Now as previously mentioned the timeseries is already in a monthly resolution with a possible 3 month filter applied. (Unfortunately i could not find any record on this, but if I do apply a 3 month filter the timeseries stays exactly the same).

## Filter design 
Because it is hard to analyse seasonal variability if you only have monthly resolution and the timeseries is with ~8 years fairly short, I chose a 12 month filter to visualize the annual variability and filter out any seasonal changes we might have.
 
![Filter](../figures/osnap_moc_filtered.png)

## Comparison to boxcar
I specifically chose the 12 month window to be able to see the annual variability and see the dominant timescale of 1 year. This is greatly represented when I filtered the timeseries with the tukey filter, seen in blue. The peaks and troughs seen in the original data are still present in the tukey-filtered timeseries. 
If we now compare this to a boxcar filter of the same length applied to the same dataset, seen in orange, we stark differences in how the annual varaibility is represented. The nice peaks and troughs, shown in the tukey-filtered timeseries are not visible anymore in the boxar timeseries. In addition to that the tukey-timeseries is able to capture changes on smaller timescales as well. For example in the beginning of 2020 and 2021 the MOC seems to spike in strength, whereas betgween those spikes it's strength returns back closer to the mean. The tukey-filtered timeseries shows this change best: it shows both peaks and the return to the wekaer state, whereas the boxcar filter shows the maximum to be at exactly the time where the MOC was actually back to the mean and does not capture the two strong events at all. 
Furthermore the tukey-filtered timeseries looks smoother in general, which makes a visual analysis easier than for the boxcar-filtered timeseries. 

## Welch spectrum with filtered time series
As previously stated the original timeseries has no rolloff period. But if I apply a 12 month filter, the rolloff is visible. 

![Welch_filt](../figures/welch_filt.png)

You can see that the Welch spectrum now deviates from the original raw periodogram, which is what we expect for filtered timeseries. 

# Conclusion
All in all the MOC at OSNAP EAST has a mean strength of 16.4 +- 2.9 Sv in the 7 years and 11 month of data available from August of 2014 to July of 2022. If we perfrom a spectral analysis the dominant timescales we frind are located around 1 year and 3 months, which hints at a strong yearly signal. Filtering our timeseries with the right filter also highlights those yearly variations. 


# Sources
- Emery & Thomson, Data Analysis Methods in Physical Oceanography, Ch. 5 (§5.6 Spectral
analysis; §5.10 Digital filters)
- AMOCatlas: https://github.com/AMOCcommunity/AMOCatlas 
- Lecture deck and starter code (code/spectra_filtering, code/make_figures.py)