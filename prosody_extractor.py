import numpy as np
import pandas as pd
import librosa
import parselmouth
from parselmouth.praat import call

# ---------------------------------------------------------
# Helper small functions
# ---------------------------------------------------------

def rms_energy(y):
    return np.mean(y**2)

def db_from_amplitude(amplitude, ref=1.0):
    with np.errstate(divide='ignore'):
        return 20.0 * np.log10(np.maximum(amplitude, 1e-12) / ref)

def voiced_mask_from_pitch(pitch_object):
    times = pitch_object.xs()
    voiced = ~np.isnan(pitch_object.selected_array['frequency'])
    return times, voiced

def formant_stats(sound, n_points=150):
    formant = sound.to_formant_burg(time_step=0.01, max_number_of_formants=5, maximum_formant=5500)
    duration = sound.get_total_duration()
    times = np.linspace(0, duration, n_points)

    f1, f2, f3 = [], [], []
    for t in times:
        try:
            f1.append(formant.get_value_at_time(1, t))
            f2.append(formant.get_value_at_time(2, t))
            f3.append(formant.get_value_at_time(3, t))
        except:
            f1.append(np.nan); f2.append(np.nan); f3.append(np.nan)

    return np.array(f1), np.array(f2), np.array(f3)

# ---------------------------------------------------------
# Main Prosodic Extraction Function
# ---------------------------------------------------------

def extract_prosodic_features(audio_path, sr_target=16000, silence_db=30):
    y, sr = librosa.load(audio_path, sr=sr_target)
    duration = len(y) / sr

    snd = parselmouth.Sound(y, sampling_frequency=sr)

    # Energy
    rms = librosa.feature.rms(y=y)[0]
    energy = np.mean(rms)
    power = rms_energy(y)

    # Pitch
    pitch = snd.to_pitch(time_step=0.01, pitch_floor=50, pitch_ceiling=500)
    pitch_vals = pitch.selected_array["frequency"]
    voiced = pitch_vals[~np.isnan(pitch_vals)]

    min_pitch = np.nanmin(pitch_vals) if voiced.size else np.nan
    max_pitch = np.nanmax(pitch_vals) if voiced.size else np.nan
    mean_pitch = np.nanmean(voiced) if voiced.size else np.nan
    pitch_sd = np.nanstd(voiced) if voiced.size else np.nan
    pitch_abs = max_pitch - min_pitch if voiced.size else np.nan
    pitch_quant = np.nanpercentile(voiced, 50) if voiced.size else np.nan

    # Intensity
    intensity = snd.to_intensity(time_step=0.01)
    intensity_vals = intensity.values.T.flatten()
    intensityMin = float(np.nanmin(intensity_vals))
    intensityMax = float(np.nanmax(intensity_vals))
    intensityMean = float(np.nanmean(intensity_vals))
    intensitySD = float(np.nanstd(intensity_vals))

    # Formants
    f1_vals, f2_vals, f3_vals = formant_stats(snd)
    fmean1 = float(np.nanmean(f1_vals))
    fmean2 = float(np.nanmean(f2_vals))
    fmean3 = float(np.nanmean(f3_vals))
    f1STD = float(np.nanstd(f1_vals))
    f2STD = float(np.nanstd(f2_vals))
    f3STD = float(np.nanstd(f3_vals))

    # Spectral
    S = np.abs(librosa.stft(y + 1e-12))
    flatness = float(np.mean(librosa.feature.spectral_flatness(S=S)[0]))
    zcr = float(np.mean(librosa.feature.zero_crossing_rate(y)[0]))

    # Loudness
    loudness = float(db_from_amplitude(np.mean(rms)))

    # Jitter / Shimmer
    try:
        pointProcess = call(snd, "To PointProcess (periodic, cc)", 75, 500)
        jitter = call(pointProcess, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
        shimmer = call([snd, pointProcess], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, True, False)
    except:
        jitter = np.nan
        shimmer = np.nan

    # Unvoiced frames
    _, voiced_mask = voiced_mask_from_pitch(pitch)
    percentUnvoiced = 100 * np.sum(~voiced_mask) / len(voiced_mask) if len(voiced_mask) else np.nan

    # Voice breaks
    numVoiceBreaks = int(np.sum((voiced_mask[:-1] == True) & (voiced_mask[1:] == False))) if len(voiced_mask) else 0
    PercentBreaks = float(100 * numVoiceBreaks / len(voiced_mask)) if len(voiced_mask) else np.nan

    # Pauses
    nonsilent = librosa.effects.split(y, top_db=silence_db)
    pauses = []
    if nonsilent.size > 0:
        segs = nonsilent / sr
        for i in range(len(segs) - 1):
            gap = segs[i+1, 0] - segs[i, 1]
            if gap > 0.01:
                pauses.append(gap)

    numPause = len(pauses)
    maxDurPause = float(np.max(pauses)) if pauses else 0.0
    avgDurPause = float(np.mean(pauses)) if pauses else 0.0
    TotDurPause3 = float(np.sum(pauses)) if pauses else 0.0
    iInterval = float(np.mean(pauses) * 1000) if pauses else 0.0
    speakRate = float(len(nonsilent) / duration) if duration > 0 else np.nan

    # Rising/Falling pitch events (simple version)
    numRising = 0
    numFall = 0
    MaxRising3 = 0.0
    MaxFalling3 = 0.0
    AvgTotRis3 = 0.0
    AvgTotFall3 = 0.0

    # Build feature dictionary (38 features)
    features = {
        "duration": duration,
        "energy": energy,
        "power": power,
        "min_pitch": min_pitch,
        "max_pitch": max_pitch,
        "mean_pitch": mean_pitch,
        "pitch_sd": pitch_sd,
        "pitch_abs": pitch_abs,
        "pitch_quant": pitch_quant,
        "intensityMin": intensityMin,
        "intensityMax": intensityMax,
        "intensityMean": intensityMean,
        "intensitySD": intensitySD,
        "fmean1": fmean1,
        "fmean2": fmean2,
        "fmean3": fmean3,
        "f1STD": f1STD,
        "f2STD": f2STD,
        "f3STD": f3STD,
        "jitter": jitter,
        "shimmer": shimmer,
        "meanPeriod": (1000.0 / mean_pitch) if mean_pitch and mean_pitch > 0 else np.nan,
        "percentUnvoiced": percentUnvoiced,
        "numVoiceBreaks": numVoiceBreaks,
        "PercentBreaks": PercentBreaks,
        "speakRate": speakRate,
        "numPause": numPause,
        "maxDurPause": maxDurPause,
        "avgDurPause": avgDurPause,
        "TotDurPause:3": TotDurPause3,
        "iInterval": iInterval,
        "MaxRising:3": MaxRising3,
        "MaxFalling:3": MaxFalling3,
        "AvgTotRis:3": AvgTotRis3,
        "AvgTotFall:3": AvgTotFall3,
        "numRising": numRising,
        "numFall": numFall
    }

    return pd.Series(features)

# ---------------------------------------------------------
# Extract from Streamlit audio bytes
# ---------------------------------------------------------

def extract_from_bytes(audio_bytes):
    import tempfile
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name
    return extract_prosodic_features(tmp_path)
