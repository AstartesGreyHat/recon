#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <portaudio.h>
#include <alsa/asoundlib.h>
#include <jack/jack.h>  // Agregar la cabecera de JACK

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

// Manejador de errores silencioso para ALSA (ya agregado anteriormente)
static void silent_alsa_error_handler(const char *file, int line, const char *function, int err, const char *fmt, ...) {
    // No se hace nada para suprimir los mensajes de ALSA
}

static void silent_jack_error(const char *msg) {
    // No se hace nada para suprimir los mensajes de JACK
}

static int beep(double frequency, double duration, int sample_rate) {
    PaError err;
    PaStream *stream;
    
    // Configurar ALSA y JACK para suprimir mensajes de error
    snd_lib_error_set_handler(silent_alsa_error_handler);
    jack_set_error_function(silent_jack_error);
    
    err = Pa_Initialize();
    if (err != paNoError) {
        return 0;
    }
    
    err = Pa_OpenDefaultStream(&stream,
                                 0,            // no input channels
                                 1,            // mono output
                                 paFloat32,    // 32-bit floating point output
                                 sample_rate,
                                 paFramesPerBufferUnspecified,
                                 NULL,         // sin callback, usar API bloqueante
                                 NULL);
    if (err != paNoError) {
        Pa_Terminate();
        return 0;
    }
    
    err = Pa_StartStream(stream);
    if (err != paNoError) {
        Pa_CloseStream(stream);
        Pa_Terminate();
        return 0;
    }
    
    int total_frames = (int)(duration * sample_rate);
    float *buffer = (float*) malloc(sizeof(float) * total_frames);
    if (!buffer) {
        Pa_StopStream(stream);
        Pa_CloseStream(stream);
        Pa_Terminate();
        return 0;
    }
    
    for (int i = 0; i < total_frames; i++) {
        double t = (double)i / sample_rate;
        buffer[i] = 0.5f * sin(2 * M_PI * frequency * t);
    }
    
    err = Pa_WriteStream(stream, buffer, total_frames);
    if (err != paNoError) {
        free(buffer);
        Pa_StopStream(stream);
        Pa_CloseStream(stream);
        Pa_Terminate();
        return 0;
    }
    
    free(buffer);
    err = Pa_StopStream(stream);
    if (err != paNoError) {
        Pa_CloseStream(stream);
        Pa_Terminate();
        return 0;
    }
    Pa_CloseStream(stream);
    Pa_Terminate();
    return 1;
}

// Las funciones exportadas se mantienen igual:
#ifdef __cplusplus
extern "C" {
#endif

int beep_function(double frequency, double duration, int sample_rate) {
    return beep(frequency, duration, sample_rate);
}

void error_beep() {
    beep(2500.0, 0.3, 44100);
    beep(2000.0, 0.5, 44100);
    beep(2500.0, 0.3, 44100);
    beep(2000.0, 0.5, 44100);
    beep(2500.0, 0.3, 44100);
    beep(2000.0, 0.5, 44100);
    beep(2500.0, 0.3, 44100);
    beep(2000.0, 0.5, 44100);
}

void done_beep() {
    // Implementar si se requiere algún sonido de finalización.
}

#ifdef __cplusplus
}
#endif
