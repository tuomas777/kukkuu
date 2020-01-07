def update_object(obj, data):
    if not data:
        return
    for k, v in data.items():
        setattr(obj, k, v)
    obj.save()
