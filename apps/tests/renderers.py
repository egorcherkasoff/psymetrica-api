import json

# возможно стоит перейти на станларный renderer
from rest_framework.renderers import JSONRenderer


class TestJSONRenderer(JSONRenderer):
    charset = "utf-8"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context["response"].status_code
        errors = data.get("errors", None)
        if errors is not None:
            return super(TestJSONRenderer, self).render(data)
        return json.dumps({"status_code": status_code, "test": data})


class TestsJSONRenderer(JSONRenderer):
    charset = "utf-8"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context["response"].status_code
        errors = data.get("errors", None)
        if errors is not None:
            return super(TestsJSONRenderer, self).render(data)
        return json.dumps({"status_code": status_code, "tests": data})
