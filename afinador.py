import streamlit as st
import numpy as np
import sounddevice as sd
import scipy.fftpack

# Frecuencias estándar de las cuerdas de guitarra (EADGBE)
guitar_notes = {
    "E2": 82.41,
    "A2": 110.00,
    "D3": 146.83,
    "G3": 196.00,
    "B3": 246.94,
    "E4": 329.63
}

def detect_frequency(audio, samplerate):
    fft = np.abs(scipy.fftpack.fft(audio))
    freqs = scipy.fftpack.fftfreq(len(fft), 1/samplerate)
    peak_idx = np.argmax(fft[:len(fft)//2])
    peak_freq = abs(freqs[peak_idx])
    return peak_freq

def closest_note(freq):
    closest = min(guitar_notes.items(), key=lambda item: abs(item[1] - freq))
    return closest

st.title("🎸 Afinador de guitarra en Streamlit")
st.write("Toca una cuerda y presiona grabar para detectar la nota.")

duration = st.slider("Duración de grabación (segundos)", 1, 5, 2)

if st.button("🎙️ Grabar"):
    st.write("Grabando...")
    audio = sd.rec(int(duration * 44100), samplerate=44100, channels=1)
    sd.wait()
    st.write("Procesando...")

    audio = audio.flatten()
    freq = detect_frequency(audio, 44100)
    note, standard_freq = closest_note(freq)

    st.write(f"🔍 Frecuencia detectada: `{freq:.2f} Hz`")
    st.write(f"🎵 Nota más cercana: `{note}` ({standard_freq} Hz)")

    if abs(freq - standard_freq) < 2:
        st.success("✅ ¡Está afinada!")
    elif freq < standard_freq:
        st.warning("📉 Muy baja. Ajusta hacia arriba.")
    else:
        st.warning("📈 Muy alta. Ajusta hacia abajo.")
