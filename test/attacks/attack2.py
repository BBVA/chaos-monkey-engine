from chaosmonkey.attacks.attack import Attack


class Attack2(Attack):

    schema = {}
    example = {}
    ref = "attack2:Attack2"

    def __init__(self, attack_config):
        super(Attack2, self).__init__(attack_config)

    def run(self):
        pass

    @staticmethod
    def to_dict():
        return Attack._to_dict(
            Attack2.ref,
            Attack2.schema,
            Attack2.example
        )
