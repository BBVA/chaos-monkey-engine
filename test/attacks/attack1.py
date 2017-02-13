from chaosmonkey.attacks.attack import Attack


class Attack1(Attack):

    schema = {}
    example = {}
    ref = "attack1:Attack1"

    def __init__(self, attack_config):
        super(Attack1, self).__init__(attack_config)

    def run(self):
        pass

    @staticmethod
    def to_dict():
        return Attack._to_dict(
            Attack1.ref,
            Attack1.schema,
            Attack1.example
        )
