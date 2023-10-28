from drf_yasg.inspectors import SwaggerAutoSchema


class CustomAutoSchema(SwaggerAutoSchema):
    def get_tags(self, operation_keys=None):
        tags = super().get_tags(operation_keys)

        if operation_keys and operation_keys[1] == 'customer':
            tags = ['customer']
        elif operation_keys and operation_keys[1] == 'organization':
            tags = ['organization']
        elif operation_keys and operation_keys[1] == 'showcase':
            tags = ['showcase']
        elif operation_keys and operation_keys[1] == 'base':
            tags = ['base']
        elif operation_keys and operation_keys[1] == 'authentication':
            tags = ['authentication']

        return tags


SWAGGER_SETTINGS = {
    'DEFAULT_AUTO_SCHEMA_CLASS': CustomAutoSchema
}
