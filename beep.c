#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <portaudio.h>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

// Función interna para reproducir un tono usando PortAudio.
static int beep(double frequency, double duration, int sample_rate) {
    PaError err;
    PaStream *stream;

    err = Pa_Initialize();
    if (err != paNoError) {
        fprintf(stderr, "PortAudio error (Initialize): %s\n", Pa_GetErrorText(err));
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
        fprintf(stderr, "PortAudio error (OpenDefaultStream): %s\n", Pa_GetErrorText(err));
        Pa_Terminate();
        return 0;
    }

    err = Pa_StartStream(stream);
    if (err != paNoError) {
        fprintf(stderr, "PortAudio error (StartStream): %s\n", Pa_GetErrorText(err));
        Pa_CloseStream(stream);
        Pa_Terminate();
        return 0;
    }

    int total_frames = (int)(duration * sample_rate);
    float *buffer = (float*) malloc(sizeof(float) * total_frames);
    if (!buffer) {
        fprintf(stderr, "Error: No se pudo asignar memoria para el buffer\n");
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
        fprintf(stderr, "PortAudio error (WriteStream): %s\n", Pa_GetErrorText(err));
        free(buffer);
        Pa_StopStream(stream);
        Pa_CloseStream(stream);
        Pa_Terminate();
        return 0;
    }

    free(buffer);
    err = Pa_StopStream(stream);
    if (err != paNoError) {
        fprintf(stderr, "PortAudio error (StopStream): %s\n", Pa_GetErrorText(err));
        Pa_CloseStream(stream);
        Pa_Terminate();
        return 0;
    }
    Pa_CloseStream(stream);
    Pa_Terminate();
    return 1;
}

// Para que estas funciones sean visibles desde otros lenguajes (como Python)
// envolvemos las declaraciones con extern "C" si se compila en C++
// (Si compilas como C, no es necesario, pero se recomienda para compatibilidad).
#ifdef __cplusplus
extern "C" {
#endif

// Función exportada para reproducir un beep.
// Devuelve 1 en éxito y 0 en error.
int beep_function(double frequency, double duration, int sample_rate) {
    return beep(frequency, duration, sample_rate);
}

// Función exportada para reproducir la secuencia de error.
void error_beep() {
    // Secuencia de beeps de error.
    beep(2500.0, 0.3, 44100);
    beep(2000.0, 0.5, 44100);
    beep(2500.0, 0.3, 44100);
    beep(2000.0, 0.5, 44100);
    beep(2500.0, 0.3, 44100);
    beep(2000.0, 0.5, 44100);
    beep(2500.0, 0.3, 44100);
    beep(2000.0, 0.5, 44100);
}

// Función exportada para indicar "done". Por ahora, no hace nada.
void done_beep() {
    // Implementar si se requiere algún sonido de finalización.
}

#ifdef __cplusplus
}
#endif
