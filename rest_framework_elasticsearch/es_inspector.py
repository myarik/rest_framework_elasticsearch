# -*- coding: utf-8 -*-
# http://www.django-rest-framework.org/topics/3.7-announcement/#customizing-api-docs-schema-generation
try:
    from rest_framework.schemas import AutoSchema
except ImportError:
    EsAutoSchema = type("EsAutoSchema", tuple(), dict())
else:
    from rest_framework.schemas.utils import is_list_view

    class EsAutoSchema(AutoSchema):
        """Elasticsearch inspector for APIView.
        Responsible for per-view instrospection and schema generation.
        """
        def get_es_filter_fields(self, path, method):
            fields = []
            for filter_backend in self.view.es_filter_backends:
                fields += filter_backend().get_schema_fields(self.view)
            return fields

        def get_filter_fields(self, path, method):
            fields = super(EsAutoSchema, self).get_filter_fields(path, method)
            fields += self.get_es_filter_fields(path, method)
            return fields

        def get_es_pagination_fields(self, path, method):
            view = self.view
            if not is_list_view(path, method, view):
                return []

            pagination = getattr(view, 'es_pagination_class', None)
            if not pagination:
                return []

            return pagination().get_schema_fields(view)

        def get_pagination_fields(self, path, method):
            fields = super(EsAutoSchema, self).get_pagination_fields(path, method)
            fields += self.get_es_pagination_fields(path, method)
            return fields


try:
    from rest_framework.schemas.openapi import AutoSchema
except ImportError:
    EsOpenApiAutoSchema = type("EsAutoSchema", tuple(), dict())
else:
    class EsOpenApiAutoSchema(AutoSchema):
        def _get_filter_parameters(self, path, method):
            parameters = super(EsOpenApiAutoSchema, self)._get_filter_parameters(path, method)

            for filter_backend in self.view.es_filter_backends:
                parameters += filter_backend().get_schema_operation_parameters(self.view)
            return parameters

        def _get_pagninator(self):
            pagination_class = getattr(self.view, 'es_pagination_class', None)
            if pagination_class:
                return pagination_class()

            return super(EsOpenApiAutoSchema, self)._get_pagninator()
