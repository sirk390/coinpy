from coinpy.lib.serialization.scripts.serialize import ScriptSerializer

def cached_serialized_size(script):
    if script.serialized_size is None:
        script.serialized_size = ScriptSerializer().get_size(script)
    return script.serialized_size
