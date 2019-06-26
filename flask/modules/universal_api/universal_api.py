'''CRUD-операции с сущностью'''
from flask import request
from flask_restful import Resource
from sqlalchemy import or_
from database import database


def get_instance_query(model, slug):
    '''Поиск сущности по айди или символьному коду'''
    args = [model.id == slug]

    if hasattr(model, 'slug'):
        args.append(model.slug == slug)

    query = database.session.query(model).filter(or_(*args))

    return query


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
    '''Класс базовых операций'''
    def view(self, slug):
        '''Получить сущность'''
        schema = self.schema()

        instance = get_instance(self.model, slug).first()

        if not instance:
            return {
                'message': 'Instance not found'
            }, 404

        # patch instance with custom data, check different conditions, user rights, etc
        try:
            dispatcher.emit(
                'before_instance_get',
                self.model,
                {
                    'instance': instance
                }
            )
        except UniversalApiException as e:
            return { 'error': e.message }, e.code

        return schema.dump(instance).data, 200


    def create(self):
        '''Создать сущность'''
        schema = self.schema()
        data = schema.load(request.get_json())
        
        if data.errors:
            return data.errors, 400

        # pathing input data, checking different conditions, user rights, etc
        try:
            dispatcher.emit(
                'before_instance_create',
                self.model,
                {
                    'instance': instance,
                    'data': data.data
                }
            )
        except UniversalApiException as e:
            return { 'error': e.message }, e.code

        instance = self.model(**data)
        database.session.add(instance)
        database.session.commit()

        # creating associated resources, related models, other stuff
        instance = dispatcher.emit(
            'after_instance_create',
            self.model,
            {
                'instance': instance
            }
        )

        return schema.dump(instance).data, 200


    def update(self, slug):
        '''Update instance'''
        schema = self.schema()

        data = schema.load(request.get_json())
        
        if data.errors:
            return data.errors, 400

        instance = get_instance(self.model, slug).first()

        if not instance:
            return {
                'message': 'Instance not found'
            }, 404

        # pathing input data, checking different conditions, user rights, etc
        try:
            dispatcher.emit(
                'before_instance_update',
                self.model,
                {
                    'instance': instance,
                    'data': data.data
                }
            )
        except UniversalApiException as e:
            return { 'error': e.message }, e.code

        instance = update_instance(self.model, instance, data)
        database.session.add(instance)
        database.session.commit()

        return schema.dump(instance).data, 200


    def delete(self, slug):
        '''Delete instance'''
        schema = self.schema()
        instance = get_instance(self.model, slug).first()

        if not instance:
            return {
                'message': 'Instance not found'
            }, 404

        # check different conditions, user rights, etc
        try:
            dispatcher.emit(
                'before_instance_delete',
                self.model,
                {
                    'instance': instance
                }
            )
        except UniversalApiException as e:
            return { 'error': e.message }, e.code

        database.session.delete(instance)
        database.session.commit()

        # cleaning up the mess, removing associated resources, etc
        dispatcher.emit(
            'after_instance_delete',
            self.model,
            {
                'instance': instance
            }
        )

        return { 'message': 'Instance deleted' }, 200


    def listing(self):
        '''Список сущностей'''
        arguments = request.args.copy()

        schema = self.schema()
        query = database.session.query(self.model)

        dispatcher.emit(
            'before_list',
            self.model,
            {
                'query': query
            }
        )

        page = int(arguments.get('page')) if 'page' in arguments else 1
        per_page = int(arguments.get('per_page')) if 'per_page' in arguments else 20

        total = query.count()
        paginated = query.paginate(page, per_page)

        dispatcher.emit(
            'after_list',
            self.model,
            {
                'items': paginated.pages
            }
        )

        return {
            'items': schema.dump(paginated.items, many=True).data,
            'pages': paginated.pages,
            'page': page,
            'per_page': per_page,
            'total': total
        }, 200