class Attack:
    """
    Base class for attacks. Every attack must extend from this class
    """

    ref = None      #: **string** Unique identifier for the attack. Must be module_name.AttackClass
    schema = None   #: **dict** Valid jsonSchema to validate the attack attributes in the API
    #: **dict** example for using when calling add plan endpoint
    example = None

    def __init__(self, attack_config):
        self.attack_config = attack_config

    def run(self):
        """
        This method is called by an executor to perform the actual attack.
        You can access the self.attack_config that holds the configuration
        used when calling the endpoint to plan the attacks.
        """
        raise NotImplementedError("Attacks should implement this!")

    @staticmethod
    def to_dict():
        """
        You should implement to_dict to return an Attack._to_dict(ref, schema, example)
        using the attack attributes

        Example::

            @staticmethod
            def to_dict():
                return Attack._to_dict(
                    TerminateEC2Instance.ref,
                    TerminateEC2Instance.schema,
                    TerminateEC2Instance.example
                )
        """

        raise NotImplementedError("Attacks should implement this!")

    @staticmethod
    def _to_dict(ref, schema, example):
        return {
            "ref": ref,
            "schema": schema,
            "example": example,
        }
