.. _extending:

Extending the Chaos Mokey Engine
================================

Adding Custom Planners
**********************

You can create your own planners to fit your needs. A planner is just a python class that receives some properties and and attack configuration. Based on this properties the planner schedule executors that execute attacks.

To create your custom planner, just create your module in the planners folder, and add a class that implements the Planner interface (:meth:`chaosmonkey.planners.planner`).

Internally the engine uses `apscheduler <http://apscheduler.readthedocs.io/>`_ to schedule jobs (*executors*) to be executed sometime in the future.

Your planner class must have three mandatory properties (ref, schema and example) and two mandatory methods (``plan`` and ``to_dict``)::

    from chaosmonkey.planners import Planner

    class MyPlanner(Planner):

        ref = "my_planner:MyPlanner"
        schema = {
            "type": "object",
            "properties": {
                "ref": {"type": "string"},
                "args": {
                    "type": "object",
                    "properties": {
                        "date": {"type": "string"}
                    }
                }
            }
        }
        example = {
            "ref": "my_planner:MyPlanner",
            "args": {
                "date": "2016-06-21T15:30"
            }
        }

        def plan(self, planner_config, attack_config):
                """
                planner_config and attack_config are json/dicts passed to the endpoint
                when executing this planner.

                The plan method must call self._add_job to schedule attacks in a date.
                This date should be calculated based on planner_config variables.
                The executor config is passed as a parameter to the add_job, and it will
                be passed to the attack executor when the scheduler executes a job to execute
                the attack.
                """
                self._add_job(attack_date, "Job Name", attack_config)

        @staticmethod
        def to_dict():
            return Planner._to_dict(MyPlanner.ref, MyPlanner.schema, MyPlanner.example)


Adding Custom Attacks
*********************

You can create your own attacks. An attack is a Python class that receive some properties and execute an attacks based on the properties.

To create your custom attack, just create your module in the attacks folder, and add a class that implements the Attack interface (:meth:`chaosmonkey.attacks.attack`)

Your attack class must have three mandatory properties (ref, schema and example) and two mandatory methods (run and to_dict)::

    from chaosmonkey.attacks import Attack

    class MyAttack(Attack):

        ref = "my_attack:MyAttack"

        schema = {
            "type": "object",
            "properties": {
                "ref": {"type": "string"},
                "name": {"type": "string"}
            }
        }

        example = {
            "ref": "my_attack:MyAttack",
            "name": "attack1"
        }

        def __init__(self, attack_config):
            super(MyAttack, self).__init__(attack_config)

        def run(self):
            """
            This method is called to perform the actual attack. You can access the self.attack_config
            that holds the dict/json used when calling the endpoint to plan the attacks.
            """
            pass

        @staticmethod
        def to_dict():
            return Attack._to_dict(MyAttack.ref, MyAttack.schema, MyAttack.example)

Adding Custom Drivers
*********************

In order to interact with the cloud provider, you can use `apache-libcloud <https://libcloud.apache.org/>`_, which is included as a dependency, to get some level of abstraction and reusability. The Chaos Monkey Engine provides with one driver out-of-the-box, the :meth:`chaosmonkey.drivers.EC2DriverFactory`, that can be reused in your attacks or serve as inspiration::

  class EC2DriverFactory:
      """
      Driver factory to get a libcloud driver with appropriate credentials for AWS provider
      You can provide credentials by either:

      * Setting AWS_IAM_ROLE in env variables
      * Setting AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY in env variables

      You can provide the region to connect by either:

      * Provide it at instantiation time
      * Setting AWS_DEFAULT_REGION in env variables
      """

      def __init__(self, region=None):
          """
          Initialize an EC2 driver factory for a certain AWS region

          :param region: The AWS region to operate within
          :type region: string
          """

          self.IAM_METADATA_URL = "http://169.254.169.254/latest/meta-data/iam/security-credentials"

          # First check if AWS_IAM_ROLE is defined
          aws_iam_role = os.environ.get("AWS_IAM_ROLE", None)
          if aws_iam_role is not None:
              # Get credentials from IAM role
              self.aws_ak, self.aws_sk, self.token = self._get_aws_credentials_from_iam_role(aws_iam_role)
          else:
              # Get credentials from environment variables
              self.aws_ak = os.environ.get('AWS_ACCESS_KEY_ID')
              self.aws_sk = os.environ.get('AWS_SECRET_ACCESS_KEY')
              self.region = region if region is not None else os.environ.get("AWS_DEFAULT_REGION")

      def get_driver(self):
          """
          Return a Libcloud driver for AWS EC2 Provider

          :return: Compute driver
          :type driver: Libcloud compute driver
          """
          return (get_driver(Provider.EC2))(self.aws_ak, self.aws_sk, region=self.region)


      def _get_aws_credentials_from_iam_role(self, role):
          """
          With a valid IAM_ROLE make a request to the AWS metadata server to
          get temporary credentials for the role

          :param role: The IAM role to use
          :type role: string
          """
          url = "/".join((self.IAM_METADATA_URL, role))
          log.info("get aws credentials from AWS_IAM_ROLE (%s)", url)
          response = requests.get(url)
          response.raise_for_status()
          resp_json = response.json()
          aws_ak = resp_json.get("AccessKeyId")
          aws_sk = resp_json.get("SecretAccessKey")
          aws_token = resp_json.get("Token")
          return aws_ak, aws_sk, aws_token

