from obspy import read
import streamlit as st
import allantools
import numpy as np

file = st.file_uploader("Upload file", type=["seed", "mseed"])

if file is not None:
    stream = read(file)
    component = st.selectbox("Component", ["Z", "X", "Y"])
    
    stream = stream.select(component=component)
    stream
    convert = st.checkbox("Convert to Acceleration")
    if convert:
        titan_gain = st.number_input("Titan Gain", value=8.16, step=0.01)
    if convert:
        # g = seed_data * (1e-6)/(1.6*9.80665*4.08)
        stream[0].data = stream[0].data * (1e-6)/(1.6*9.80665*titan_gain)
    # choose the first trace
    # tr = st[0]
    st.title("Filtering")
    st.header("Choose the type of filter from the dropdown menu")
    # filter_name = st.selectbox("Filter Type", ["bandpass", "bandstop", "lowpass", "highpass", "lowpass_cheby_2", "lowpass_fir", "remez_fir"])
    filter_name = st.selectbox("Filter Type", ["None", "lowpass", "highpass", "lowpass_cheby_2"])

    filter_freq = st.number_input("Filter Frequency", value=1.0, step=0.1)

    # filter the trace using lowwpass filter cheby 2
    # tr_filt = tr.copy()
    # tr_filt.filter("lowpass_cheby_2", freq=0.1)
    if filter_name != "None":
        stream.filter(filter_name, freq=filter_freq)

    # plot the raw and filtered data
    # tr.plot()
    # tr_filt.plot()
    fig = stream.plot()
    st.pyplot(fig)

    st.title("Allan Deviation")
    # Show tau only 10e-1 onwards
    taus = np.logspace(-1, 3, 100)
    a = allantools.Dataset(data=stream[0].data, rate=stream[0].stats.sampling_rate, data_type="freq", taus=taus)
    a.compute("adev")

    fig = allantools.Plot()
    fig.plot(a, errorbars=True, grid=True)
    fig.ax.set_xlabel("tau (s)")
    fig.ax.set_title(f"Allan Deviation - Filter: {filter_name}, Frequency: {filter_freq}")
    st.pyplot(fig.fig)

