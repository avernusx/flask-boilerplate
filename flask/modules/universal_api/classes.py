from flask import request
from flask_restful import Resource
from sqlalchemy import or_
from database import database


def get_instance(model, slug):
    '''Поиск сущности по айди или символьному коду'''
    args = [model.id == slug]

    if hasattr(model, 'slug'):
        args.append(model.slug == slug)

    instance = database.session.query(model).filter(or_(*args)).first()

    return instance


def update_instance(model, instance, data):
    '''Обновление сущности по словарю'''
    for field, value in data.items():
        attribute = getattr(model, field)
        if hasattr(attribute, 'mapper'):
            pass
        elif value != getattr(instance, field):
            setattr(instance, field, value)

    return instance


class UniversalInstanceAPI(Resource):
    def get(self, slug):
        schema = self.schema()
        instance = get_instance(self.model, slug)

        if not instance:
            return {
                'message': 'Instance not found'
            }, 404

        return schema.dump(instance).data, 200


    def post(self):
        schema = self.schema()
        data = schema.load(request.get_json())
        
        if data.errors:
            return data.errors, 400

        instance = self.model(**data.data)
        database.session.add(instance)
        database.session.commit()

        return schema.dump(instance).data, 200


    def patch(self, slug):
        schema = self.schema()

        data = schema.load(request.get_json())
        
        if data.errors:
            return data.errors, 400

        instance = get_instance(self.model, slug)

        if not instance:
            return {
                'message': 'Instance not found'
            }, 404

        instance = update_instance(self.model, instance, data.data)
        database.session.add(instance)
        database.session.commit()

        return schema.dump(instance).data, 200


    def delete(self, slug):
        schema = self.schema()
        instance = get_instance(self.model, slug)

        if not instance:
            return {
                'message': 'Instance not found'
            }, 404

        database.session.delete(instance)
        database.session.commit()

        return { 'message': 'Instance deleted' }, 200


class UniversalListAPI(Resource):
    def get(self):
        arguments = request.args.copy()

        schema = self.schema()
        query = database.session.query(self.model)

        page = int(arguments.get('page')) if 'page' in arguments else 1
        per_page = int(arguments.get('per_page')) if 'per_page' in arguments else 20

        total = query.count()
        paginated = query.paginate(page, per_page)

        return {
            'items': schema.dump(paginated.items, many=True).data,
            'pages': paginated.pages,
            'page': page,
            'per_page': per_page,
            'total': total
        }, 200