from rest_framework.metadata import SimpleMetadata
from rest_framework.schemas.openapi import AutoSchema


class APIMetadata(SimpleMetadata):
    """Extended metadata generator."""
    def get_field_info(self, field):
        field_info = super().get_field_info(field)

        # Add extra validators using the OpenAPI schema generator
        validators = {}
        AutoSchema()._map_field_validators(field, validators)
        extra_validators = ['format', 'pattern']
        for validator in extra_validators:
            if validators.get(validator, None):
                field_info[validator] = validators[validator]

        # Add additional data from serializer
        field_info['initial'] = field.initial
        field_info['field_name'] = field.field_name
        field_info['write_only'] = field.write_only

        return field_info

    # >> > import json
    # >> > from your_app.serializers import UserSerializer
    # >> > metadata_generator = APIMetadata()
    # >> > metadata = metadata_generator.get_serializer_info(UserSerializer())
    # >> > with open('User.json', 'w') as json_file:
    #     ...
    #     json.dump(metadata, json_file, indent=2, sort_keys=True)