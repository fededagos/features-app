PLOTS_FOLDER_URL = "dashboard_plots/"

USE_FEATURES_SELECTION = True

TEMPORAL_FEATURES = [
    "mfr",
    "mifr",
    "med_isi",
    "mode_isi",
    "prct5ISI",
    "entropy",
    "CV2_mean",
    "CV2_median",
    "CV",
    "IR",
    "Lv",
    "LvR",
    "LcV",
    "SI",
    "SKW",
    "acg_burst_vs_mfr",
    "acg_oscill_vs_mfr",
]

WAVEFORM_FEATURES = [
    "relevant_channel",
    "trough_voltage",
    "trough_t",
    "peak_voltage",
    "peak_t",
    "repolarisation_t",
    "depolarisation_t",
    "peak_50_width",
    "trough_50_width",
    "onset_t",
    "onset_amp",
    "wvf_width",
    "peak_trough_ratio",
    "tau_recovery",
    "multiplicative_a_recovery" "recovery_slope",
    "repolarisation_slope",
    "depolarisation_slope",
    "spatial_decay_24um",
    "dendritic_comp_amp",
]

C4_COLORS = {
    "PkC_ss": [28, 120, 181],
    "PkC_cs": [0, 0, 0],
    "MLI": [224, 85, 159],
    "MFB": [214, 37, 41],
    "GrC": [42, 161, 73],
    "GoC": [56, 174, 62],
    "laser": [96, 201, 223],
    "drug": [239, 126, 34],
    "background": [244, 242, 241],
    "MLI_A": [224, 85, 150],
    "MLI_B": [220, 80, 160],
}

LAB_CORRESPONDENCE = {
    "Hausser data": "hausser",
    "Hull data": "hull",
    "Combined mouse data": "combined_mouse",
    "Lisberger data (macaque)": "lisberger",
    "All data": "all",
}


SELECTED_FEATURES = {
    "mfr": "Mean FR (Hz)",
    "mifr": "Mean inst. FR (Hz)",
    "CV": "CV",
    "CV2_mean": "CV2",
    "LcV": "Log CV",
    "IR": "Instantaneous irregularity",
    "entropy": "Entropy (bits/s)",
    "Lv": "Local variation",
    "LvR": "Revised local variation",
    "acg_burst_vs_mfr": "Burst ratio",
    "SKW": "ISI skewness",
    "trough_voltage": "Depolarisation amplitude (\u03bcV)",
    "peak_voltage": "Repolarisation amplitude (\u03bcV)",
    "wvf_width": "Waveform width (ms)",
    "peak_trough_ratio": "Peak-trough ratio",
    "tau_recovery": "Recovery slope (\u03bcV/ms)",
    "spatial_decay_24um": "Spatial decay (%/24\u03bcm)",
}
