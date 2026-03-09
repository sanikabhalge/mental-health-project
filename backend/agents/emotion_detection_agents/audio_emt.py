import librosa
import numpy as np
import io
import tempfile
import os


def analyze_audio_emotion(audio_data, sr=22050):
    """
    Analyze emotion from audio bytes or file path using spectral features.

    Returns:
        dict: { emotion: str, confidence: float }
    """
    temp_file = None
    try:
        # ── Load audio ────────────────────────────────────────────────────
        if isinstance(audio_data, bytes):
            try:
                y, sr = librosa.load(io.BytesIO(audio_data), sr=sr)
            except Exception:
                with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as tmp:
                    temp_file = tmp.name
                    tmp.write(audio_data)
                y, sr = librosa.load(temp_file, sr=sr)
        elif isinstance(audio_data, str):
            y, sr = librosa.load(audio_data, sr=sr)
        else:
            y = np.array(audio_data)

        if len(y) == 0:
            return {"emotion": "neutral", "confidence": 50.0}

        # ── Feature extraction ────────────────────────────────────────────

        # FIX: librosa.feature.energy() removed in 0.10+ → use rms()
        rms    = librosa.feature.rms(y=y)[0]
        energy = float(np.mean(rms))

        zcr = float(np.mean(librosa.feature.zero_crossing_rate(y)[0]))

        spec_centroid = float(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)[0]))

        pitches, _ = librosa.piptrack(y=y, sr=sr)
        pitch_vals  = pitches[pitches > 0]
        mean_pitch  = float(np.mean(pitch_vals)) if len(pitch_vals) > 0 else 0.0

        print(f"[Audio] energy={energy:.4f}, zcr={zcr:.4f}, "
              f"centroid={spec_centroid:.1f}, pitch={mean_pitch:.1f}")

        # ── Emotion scoring ───────────────────────────────────────────────
        scores = {
            "angry":   energy * 2.5 + zcr * 10.0 + (0.3 if mean_pitch > 200 else 0),
            "sad":     (1 - min(energy * 5, 1)) * 1.5 + (1 - min(zcr * 20, 1)) * 1.5
                       + (0.4 if spec_centroid < 2000 else 0),
            "happy":   (energy * 3.0 if 0.05 < energy < 0.4 else 0)
                       + (spec_centroid / 10000 * 2.0 if spec_centroid > 3000 else 0),
            "calm":    (1 - min(energy * 5, 1)) + (1 - min(zcr * 20, 1))
                       + (0.5 if 1000 < spec_centroid < 3000 else 0),
            "fearful": (energy * zcr * 15.0 if energy > 0.05 and zcr > 0.05 else 0)
                       + (0.2 if mean_pitch > 150 else 0),
            "neutral": 0.3,
        }

        total = sum(scores.values()) or 1.0
        normalized = {k: (v / total) * 100 for k, v in scores.items()}

        best_emotion     = max(normalized, key=normalized.get)
        best_confidence  = round(normalized[best_emotion], 2)

        print(f"[Audio] → {best_emotion} ({best_confidence}%)")
        return {"emotion": best_emotion, "confidence": best_confidence}

    except Exception as e:
        print(f"[Audio] Error: {e}")
        return {"emotion": "neutral", "confidence": 0.0}
    finally:
        if temp_file and os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except Exception:
                pass


def analyze_audio(audio_data):
    """Main entry point for audio emotion analysis."""
    return analyze_audio_emotion(audio_data)