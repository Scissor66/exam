from marshmallow import Schema, fields


class Addition(Schema):
    uuid = fields.String(required=True)
    amount = fields.Integer(load_only=True, missing=0)
    balance = fields.Integer(dump_only=True)
    status = fields.Boolean(dump_only=True)


class CommonRequest(Schema):
    addition = fields.Nested(Addition)


class CommonResponse(CommonRequest):
    status = fields.Integer()
    result = fields.Boolean()
    description = fields.String()
