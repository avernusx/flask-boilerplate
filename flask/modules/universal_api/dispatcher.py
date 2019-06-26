'''Диспетчер событий универсального апи'''
class Dispatcher():
    '''Диспетчер событий универсального апи'''
    events = {}

    def on(self, event, model, callback):
        '''
        Подписаться на событие
        '''
        if event not in self.events:
            self.events[event] = {}

        if model not in self.events[event]:
            self.events[event][model] = []

        self.events[event][model].append(callback)


    def emit(self, event, model, callback_kwargs={}):
        '''
        Испустить событие
        '''
        for callback in self.events[event][model]:
            callback(**callback_kwargs)

        if 'any' in self.events[event]:
            for callback in self.events[event]['any']:
                callback(**callback_kwargs)
           