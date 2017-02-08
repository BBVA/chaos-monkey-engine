import logging
import base64
import paramiko
import io
import random
from chaosmonkey.attacks.attack import Attack
from chaosmonkey.drivers import EC2DriverFactory


class RunScript(Attack):
    """
    Run a script in a VM, selected by the filters passed to the cloud client,
    through a SSH connection established using the given certificate.
    """

    ref = "run_script:RunScript"

    schema = {
        "type": "object",
        "properties": {
            "ref": {"type": "string"},
            "args": {
                "type": "object",
                "properties": {
                    "region": {"type": "string"},
                    "filters": {
                        "type": "object",
                        "properties": {
                            "tag:Name": {"type": "string"}
                        }
                    },
                    "local_script": {"type": "string"},
                    "remote_script": {"type": "string"},
                    "ssh": {
                        "type": "object",
                        "properties": {
                            "user": {"type": "string"},
                            "pem": {"type": "string"}
                        },
                        "required": ["user", "pem"]
                    }
                },
                "required": ["ssh", "local_script", "remote_script", "filters", "region"]
            }
        }
    }

    example = {
        "ref": ref,
        "args": {
            "region": "eu-west-1",
            "local_script": "/attacks/scripts/s_burncpu.sh",
            "remote_script": "/tmp/s_burncpu.sh",
            "filters": {
                "tag:Name": "playground-asg"
            },
            "ssh": {
                "user": "ec2-user",
                "pem": "BASE64_STRING_PEM"
            }
        }
    }

    filters = {}
    script = ""

    def __init__(self, attack_config):
        super(RunScript, self).__init__(attack_config)

        self.log = logging.getLogger(__name__)

        region = self.attack_config.get("region", None)
        self.driver = EC2DriverFactory(region=region).get_driver()

        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def run(self):
        """
        Run a script through ssh on a random instance from the collection if instances
        which satisfies the filter constraints
        """
        nodes = self._get_nodes(self.attack_config.get("filters"))
        random.seed()
        node = random.choice(nodes)

        ssh_config = self.attack_config.get("ssh")
        user = ssh_config.get("user")
        pem = ssh_config.get("pem")

        local_script = self.attack_config.get("local_script")
        remote_script = self.attack_config.get("remote_script")

        self._run_script(node.private_ips[0], user, local_script, remote_script, pem)

    def _get_nodes(self, filters):
        """
        Return the nodes matching the filters
        """
        if filters is None:
            raise ValueError("You must specify a valid filter to list nodes")

        if "instance-state-name" not in filters:
            filters["instance-state-name"] = "running"

        self.log.info("Get nodes with filter: %r ", filters)
        nodes = self.driver.list_nodes(ex_filters=filters)
        return nodes

    def _run_script(self, host, user, local_script, remote_script, pem):
        """
        Copy a script to a remote host and exec it.
        """
        self.log.info("running %s in node %s", local_script, host)

        pem_decoded = base64.b64decode(pem).decode()
        pkey = paramiko.RSAKey.from_private_key(file_obj=io.StringIO(pem_decoded))

        try:
            # get attack script paths

            self.log.info("connect ssh client to %s with user %s", host, user)
            self.ssh_client.connect(host, username=user, pkey=pkey)
            self._ssh_upload_script(local_script, remote_script)
            self.log.info("Executing remote script")
            # avoid file descriptors open while executing the script
            # http://unix.stackexchange.com/questions/30400/execute-remote-commands-completely-detaching-from-the-ssh-connection
            self.log.info("Execute command %s", remote_script)
            stdin, stdout, stderr = self.ssh_client.exec_command(remote_script, get_pty=True)
            self.log.info("script executed\nstdout: %s", stdout.readlines())
            self.log.info("script executed\nstderr: %s", stderr.readlines())
        except Exception as e:
            self.log.info(e)
        finally:
            self.ssh_client.close()

    def _ssh_upload_script(self, local_script, remote_script):
        """
        Uploads a local file to the host to the remote file
        """
        self.log.info("remove previous script")
        self.ssh_client.exec_command("rm " + remote_script)
        trans = self.ssh_client.get_transport()
        sftp = paramiko.SFTPClient.from_transport(trans)
        self.log.info("put from %s to %s", local_script, remote_script)
        sftp.put(local_script, remote_script)
        self.log.info("make remote script +x")
        self.ssh_client.exec_command("chmod u+x " + remote_script)
        sftp.close()

    @staticmethod
    def to_dict():
        return Attack._to_dict(RunScript.ref, RunScript.schema, RunScript.example)
