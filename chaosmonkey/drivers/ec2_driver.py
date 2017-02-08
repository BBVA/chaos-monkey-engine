import os
import logging
import requests
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver


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
        self.log = logging.getLogger(__name__)
        self.IAM_METADATA_URL = "http://169.254.169.254/latest/meta-data/iam/security-credentials"

        # First check if AWS_IAM_ROLE is defined
        aws_iam_role = os.environ.get("AWS_IAM_ROLE", None)
        if aws_iam_role is not None:
            # Get credentials from IAM role
            self.aws_ak, self.aws_sk, self.token = \
                self._get_aws_credentials_from_iam_role(aws_iam_role)
        else:
            # Get credentials from environment variables
            self.log.debug('getting AWS credentials from environment variables AWS_ACCESS_KEY_ID, '
                           'AWS_SECRET_ACCESS_KEY and AWS_DEFAULT_REGION')
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
        self.log.debug("get AWS credentials from IAM_METADATA (%s)", url)
        response = requests.get(url)
        response.raise_for_status()
        resp_json = response.json()
        aws_ak = resp_json.get("AccessKeyId")
        aws_sk = resp_json.get("SecretAccessKey")
        aws_token = resp_json.get("Token")
        return aws_ak, aws_sk, aws_token
