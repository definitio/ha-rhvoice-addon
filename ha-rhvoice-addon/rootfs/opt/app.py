#!/usr/bin/env python3
# pylint: disable=import-error

import os
from shlex import quote
from urllib import parse

from flask import Flask, request, make_response, Response, stream_with_context
from markupsafe import escape
from rhvoice_wrapper import TTS

try:
    from rhvoice_tools.text_prepare import text_prepare
except ImportError as err:
    print(f"Warning! Preprocessing disable: {err}")

    def text_prepare(text, stress_marker=False, debug=False):
        del debug, stress_marker
        return text


DEFAULT_VOICE = "anna"

FORMATS = {
    "wav": "audio/wav",
    "mp3": "audio/mpeg",
    "opus": "audio/ogg",
    "flac": "audio/flac",
}
DEFAULT_FORMAT = "mp3"

app = Flask(__name__, static_url_path="")


def voice_streamer(text, voice, format_, sets):
    # pylint: disable=used-before-assignment
    with tts.say(text, voice, format_, None, sets or None) as read:
        for chunk in read:
            yield chunk


def chunked_stream(stream):
    b_break = b"\r\n"
    for chunk in stream:
        yield format(len(chunk), "x").encode() + b_break + chunk + b_break
    yield b"0" + b_break * 2


def set_headers():
    if CHUNKED_TRANSFER:  # pylint: disable=used-before-assignment
        return {"Transfer-Encoding": "chunked", "Connection": "keep-alive"}
    return None


@app.route("/say")
@app.route("/rhasspy", methods=["POST"])
def say():
    # https://rhasspy.readthedocs.io/en/latest/text-to-speech/#remote
    if request.path == "/rhasspy" and request.method == "POST":
        text = request.get_data(as_text=True)
        format_ = "wav"
    else:
        text = " ".join(
            [x for x in parse.unquote(request.args.get("text", "")).splitlines() if x]
        )
        format_ = request.args.get("format", DEFAULT_FORMAT)
    voice = request.args.get("voice", DEFAULT_VOICE)

    if voice not in SUPPORT_VOICES:  # pylint: disable=used-before-assignment
        return make_response(
            f"Unknown voice: '{escape(voice)}'. Support: {', '.join(SUPPORT_VOICES)}.",
            400,
        )
    if format_ not in FORMATS:
        return make_response(
            f"Unknown format: '{escape(format_)}'. Support: {', '.join(FORMATS)}.",
            400,
        )
    if not text:
        return make_response("Unset 'text'.", 400)

    text = quote(text_prepare(text))
    sets = _get_sets(request.args)
    stream = voice_streamer(text, voice, format_, sets)
    if CHUNKED_TRANSFER:
        stream = chunked_stream(stream)
    return Response(
        stream_with_context(stream), mimetype=FORMATS[format_], headers=set_headers()
    )


@app.route("/info")
def info():
    return make_response(
        {
            "DEFAULT_VOICE": DEFAULT_VOICE,
            "FORMATS": FORMATS,
            "DEFAULT_FORMAT": DEFAULT_FORMAT,
            "SUPPORT_VOICES": list(SUPPORT_VOICES),
            "rhvoice_wrapper_voices_info": tts.voices_info,
            "rhvoice_wrapper_voice_profiles": tts.voice_profiles,
            "rhvoice_wrapper_api_version": tts.api_version,
            "rhvoice_wrapper_library_version": tts.lib_version,
            "rhvoice_wrapper_thread_count": tts.thread_count,
            "rhvoice_wrapper_process": tts.process,
            "rhvoice_wrapper_cmd": tts.cmd,
        }
    )


def _normalize_set(val):  # 0..100 -> -1.0..1
    try:
        return max(0, min(100, int(val))) / 50.0 - 1
    except (TypeError, ValueError):
        return 0.0


def _get_sets(args):
    keys = {
        "rate": "absolute_rate",
        "pitch": "absolute_pitch",
        "volume": "absolute_volume",
    }
    return {keys[key]: _normalize_set(args[key]) for key in keys if key in args}


def _get_def(any_, test, def_=None):
    if test not in any_ and len(any_):
        return def_ if def_ and def_ in any_ else next(iter(any_))
    return test


def _check_env(word: str) -> bool:
    return word in os.environ and os.environ[word].lower() not in [
        "no",
        "disable",
        "false",
        "",
    ]


if __name__ == "__main__":
    tts = TTS()

    CHUNKED_TRANSFER = _check_env("CHUNKED_TRANSFER")
    print(f"Chunked transfer encoding: {CHUNKED_TRANSFER}")

    formats = tts.formats
    DEFAULT_FORMAT = _get_def(formats, DEFAULT_FORMAT, "wav")
    FORMATS = {key: val for key, val in FORMATS.items() if key in formats}

    SUPPORT_VOICES = tts.voices
    DEFAULT_VOICE = _get_def(SUPPORT_VOICES, DEFAULT_VOICE)
    SUPPORT_VOICES = set(SUPPORT_VOICES)

    print(f"Threads: {tts.thread_count}")
    app.run(host="0.0.0.0", port=8080, threaded=True)
    tts.join()
