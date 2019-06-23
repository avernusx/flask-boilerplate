from marshmallow import fields, Schema


class TestSchema(Schema):
    id = fields.UUID(dump_only=True)
    test = fields.String(required=True)