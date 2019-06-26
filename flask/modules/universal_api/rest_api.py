def rest(blueprint, route):
    def wrapper(cls):
        api = cls()
        blueprint.route(route, methods=['GET'])(api.listing)
        blueprint.route(route, methods=['POST'])(api.create)
        blueprint.route(route + '/<string:id>', methods=['GET'])(api.view)
        blueprint.route(route + '/<string:id>', methods=['PUT', 'PATCH'])(api.update)
        blueprint.route(route + '/<string:id>', methods=['DELETE'])(api.delete)
    return wrapper