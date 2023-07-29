PLOTS_FOLDER_URL = "dashboard_plots/"

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
    "recovery_slope",
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
