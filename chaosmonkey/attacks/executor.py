import logging
import chaosmonkey.engine.cme_manager as CMEManager

log = logging.getLogger(__name__)


def execute(attack_config=None, plan_id=None):
    """
    This func is executed for every job stored in the scheduler.
    Receive in kwargs all attack configuration used when creating
    the executor that indicates which attack and configuration should be
    used to do the actual attack.

    :param attack_config: **Dict** with attack configuration
    :param plan_id: **String** plan id for the plan containing the executor
    """
    attack_class = CMEManager.manager.attacks_store.get(attack_config.get('ref'))

    if attack_class is None:
        msg = '[PlanID %s] Attack ref %s not loaded in the store ' \
              % (plan_id, attack_config.get('ref'))
        log.debug(msg)
        raise ValueError(msg)

    attack_instance = attack_class(attack_config.get("args"))
    attack_instance.run()
