# TODO: Is this useful? Is the concept of a "connection" something we want in this library?
# - I think yes, so that it'll be easier to apply Stitch (and other extras) if needed
# - The fact of the matter is that no one runs singer taps in isolation, outside of an orchestration context.
def get_config():
    return {"my": "config"}
