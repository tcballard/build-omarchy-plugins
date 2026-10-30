import json


MAX_BYTES = 16 * 1024


def read_request(stream):
    payload = stream.read(MAX_BYTES + 1)
    if len(payload) > MAX_BYTES:
        raise ValueError("Request exceeds 16 KiB")
    try:
        request = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, ValueError, RecursionError):
        raise ValueError("Invalid request") from None
    if not isinstance(request, dict) or set(request) != {"text"}:
        raise ValueError("Expected one text field")
    if not isinstance(request["text"], str) or "\x00" in request["text"]:
        raise ValueError("Invalid text")
    try:
        request["text"].encode("utf-8")
    except UnicodeEncodeError:
        raise ValueError("Invalid text") from None
    return request["text"]
