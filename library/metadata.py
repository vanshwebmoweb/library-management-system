from rest_framework.metadata import SimpleMetadata


class CustomMetadata(SimpleMetadata):

    def determine_metadata(self, request, view):
        metadata = super().determine_metadata(request, view)

        metadata['api_version'] = '1.0.0'
        metadata['contact'] = 'vansh@gmail.com'
        metadata['documentation'] = 'http://127.0.0.1:8000/api/schema/swagger-ui/'

        return metadata