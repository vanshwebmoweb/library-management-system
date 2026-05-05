from rest_framework.negotiation import DefaultContentNegotiation


class CustomContentNegotiation(DefaultContentNegotiation):

    def select_renderer(self, request, renderers, format_suffix=None):
        for renderer in renderers:
            if renderer.media_type == 'application/json':
                return renderer, renderer.media_type
        return super().select_renderer(request, renderers, format_suffix)

