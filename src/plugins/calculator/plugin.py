from iplugin import IPlugin

class CalculatorPlugin(IPlugin):
    def __init__(self):
        self.description = 'Calculator'
        self.topics = ['Add', 'Subtract']

    def execute(self, topic, args):
        """This is the method that our framework will call
        """
        print(f'Topic: {topic} Argument: {args}')

        if topic == "Add":
            return self.add(args)
        
        if topic == "Subtract":
           return self.subtract(args) 
        
        raise Exception (f'Topic: {topic} has no mapping function')

    def add(self, args):
        count  = 0

        for index in range(0, len(args)):
            count += args[index]
        
        return count

    def subtract(self, args):
        count  = 0

        for index in range(0, len(args)):
            count -= args[index]
        
        return count

       