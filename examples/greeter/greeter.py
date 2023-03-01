class Greeter:
    def greet(self, name:str, greeting:str='hi there'):
        """
        Greet someone by name.

        :param name: The name of the person to be greeted.
        :param greeting: The greeting message to use.
        """
        print(f'{greeting}, {name}')
