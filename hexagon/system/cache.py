def no_caching_interceptor(r):
    r.headers["Cache-Control"] = "no-cache, no-store, max-age=0"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r


def no_caching(app):
    app.after_request(no_caching_interceptor)
