from iplugin import IPlugin

class SamplingPlugin(IPlugin):
    def __init__(self):
        self.description = 'Sampling Plugins'
        self.topics = ['Sample']

    def execute(self, topic, args):
        """This is the
        method that our framework will call
        """
        print(f'Topic: {topic} Argument: {args}')

        if topic == "Sample":
            return self.sample(args)
        
        raise Exception (f'Topic: {topic} has no mapping function')


    def sample(self, args):
        print(f'Sampling: {args}')

        return args[2:3]

