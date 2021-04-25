"""
Copyright (c) Footprint  Team.

This is the Configuration file that has all the required configurations 
used by the JupyterHub Server. We are using the FargateSpawner class to
create the Spawners which will create tasks in the ECS cluster.

Resources will be managed by the ECS cluster and each user will get 
a specific amount of resource before they login to the server.

Note: 
To change the configs just edit the environment variable.
"""

# ===================================================================================================
# Importing the libraries
import sys
import yaml
from fargatespawner import FargateSpawner
from fargatespawner import FargateSpawnerEC2InstanceProfileAuthentication

# Create the configuration object
config = yaml.load(open("./config.yaml"), Loader=yaml.FullLoader)
# ===================================================================================================


# ===================================================================================================
# ----------------------------------------------------------------------------------------
# Authentication Class Initialization
# ----------------------------------------------------------------------------------------
# Setting the spawner class for JupyterHub
c.JupyterHub.spawner_class = FargateSpawner
# Setting up the authentication class for FargateSpawner
c.FargateSpawner.authentication_class = FargateSpawnerEC2InstanceProfileAuthentication
# ===================================================================================================


# ===================================================================================================
# ----------------------------------------------------------------------------------------
# Authentication for Login
# ----------------------------------------------------------------------------------------

# Authentication configs for the JupyterHub
# ===== Native authenticator =====
c.JupyterHub.authenticator_class = 'nativeauthenticator.NativeAuthenticator'
c.JupyterHub.admin_access = True
c.NativeAuthenticator.admin_users = set(["admin", "daniel"])
c.Authenticator.enable_signup = True
c.Authenticator.allowed_failed_logins = 3
c.Authenticator.seconds_before_next_try = 600
c.Authenticator.check_common_password = True
c.Authenticator.minimum_password_length = 10
c.Authenticator.ask_email_on_signup = True
# ===================================================================================================


# ===================================================================================================
# ----------------------------------------------------------------------------------------
# Server Option Form
# ----------------------------------------------------------------------------------------
# Creating the form to get the server configuration from the user
c.FargateSpawner.options_form = """
<div class="form-group">
    <label for="resources">Select the suitable configuration for your Notebook instance</label>
    <select name="resources" size="9" class="form-control">
        <option value="512_1024" selected>0.5 CPU & 1GB RAM</option>
        <option value="512_2048">0.5 CPU & 2GB RAM</option>
        <option value="512_4096">0.5 CPU & 4GB RAM</option>
        <option value="1024_2048">1 CPU & 2GB RAM</option>
        <option value="1024_4096">1 CPU & 4GB RAM</option>
        <option value="1024_8192">1 CPU & 8GB RAM</option>
        <option value="2048_4096">2 CPU & 4GB RAM</option>
        <option value="2048_8192">2 CPU & 8GB RAM</option>
        <option value="2048_16384">2 CPU & 16GB RAM</option>
    </select>
</div><br>
<div class="alert alert-light">
    <p><strong>Note: </strong><br>
        1. The above selection will launch a machine with the selected configuration. <br>
        2. There are some Data Science libraries that are preinstalled within your Notebook's kernel. <br>
        3. You can install python libraries as you require using the JupyterHub console.
    </p>
</div>
"""
# ===================================================================================================


# ===================================================================================================
# ----------------------------------------------------------------------------------------
# Fargate Spawner Configurations
# ----------------------------------------------------------------------------------------
c.FargateSpawner.aws_region = config['FARGATESPAWNER_AWS_REGION']
c.FargateSpawner.aws_ecs_host = config['FARGATESPAWNER_AWS_ECS_HOST']
c.FargateSpawner.notebook_port = 8888
c.FargateSpawner.notebook_scheme = "http"
# ===================================================================================================


# ===================================================================================================
# ----------------------------------------------------------------------------------------
# Fargate Spawner task run configs.
# This will help to run the task for each user in the ECS cluster
# ----------------------------------------------------------------------------------------
# The get_run_task_args argument must a callable that takes the spawner 
# instance as a parameter, and returns a dictionary that is passed to the RunTask API call.
# NOTE: MAKE CHANGES IN THE .env FILE
c.FargateSpawner.get_run_task_args = lambda spawner: {
    'cluster': config['CLUSTER_NAME'],
    'taskDefinition': config['CLUSTER_TASK_DEFINITION'],
    'overrides': {
        # 'taskRoleArn': 'arn:aws:iam::123456789012:role/notebook-task',
        'containerOverrides': [{
            'command': spawner.cmd + [
                '--NotebookApp.notebook_dir=/home',
                '--NotebookApp.default_url=/lab'
            ],
            'environment': [
                {
                    'name': name,
                    'value': value,
                } for name, value in spawner.get_env().items()
            ],
            'name': config['CLUSTER_NAME'],
        }],
        'cpu':spawner.user_options['resources'][0].split('_')[0],
        'memory': spawner.user_options['resources'][0].split('_')[1],
    },
    'count': 1,
    'launchType': 'FARGATE',
    'networkConfiguration': {
        'awsvpcConfiguration': {
            'assignPublicIp': config['ASSIGN_PUBLIC_IP'],
            'securityGroups': config['SECURITY_GROUPS'],
            'subnets': config['SUBNETS'],
        },
    },
    'platformVersion': config['PLATFORM_VERSION']
}
# ===================================================================================================


# ===================================================================================================
# ----------------------------------------------------------------------------------------
# JupyterHub(Application) configuration
# ----------------------------------------------------------------------------------------

## The ip or hostname for proxies and spawners to use for connecting to the Hub.
c.JupyterHub.hub_ip = '0.0.0.0'
## The internal port for the Hub process.
c.JupyterHub.hub_port = 8081

## The ip or hostname for proxies and spawners to use for connecting to the Hub.
# This will be the IP address of the machine in which the docker container is running
c.JupyterHub.hub_connect_ip = config['HUB_CONNECT_IP']

#  This is the address on which the proxy will bind. Sets protocol, ip, base_url
#  Default: 'http://:8000'
c.JupyterHub.bind_url = 'https://:8000'

## Set the log level by value or name.
#  Choices: any of [0, 10, 20, 30, 40, 50, 'DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL']
#  Default: 30
c.JupyterHub.log_level = 'DEBUG'

# ## Duration (in seconds) to determine the number of active users.
# #  Default: 1800
# c.JupyterHub.active_user_window = 1800

# Company Logo file that will be displayed in the JupyterHub
c.JupyterHub.logo_file = config['LOGO_FILE_NAME']

# This helps in creating multiple servers per User.
# It is use to manage named servers via the user home page.
c.JupyterHub.allow_named_servers = True

# The number of named servers per user can be limited by this setting
# Maximum users that can use the server
c.JupyterHub.named_server_limit_per_user = int(config['MAX_NUMBER_OF_USERS'])

## Interval (in seconds) at which to update last-activity timestamps.
c.JupyterHub.last_activity_interval = 60

## url for the database. e.g. `sqlite:///jupyterhub.sqlite`
#  Default: 'sqlite:///jupyterhub.sqlite'
c.JupyterHub.db_url = "mysql+pymysql://{}:{}@{}:{}/{}".format(
    config['RDS_SQL_DB_USERNAME'], 
    config['RDS_SQL_DB_PASSWORD'],
    config['RDS_SQL_DB_ENDPOINT'], 
    config['RDS_SQL_DB_PORT'],
    config['RDS_SQL_DB_NAME']
)

## log all database transactions. This has A LOT of output
#  Default: False
c.JupyterHub.debug_db = False
c.JupyterHub.upgrade_db = False
c.JupyterHub.reset_db = False

## List of service specification dictionaries.
# This will check if the user is active or inactive
c.JupyterHub.services = [
    {
        'name': 'idle-culler',
        'admin': True,
        'command': [
            sys.executable, '-m', 
            'jupyterhub_idle_culler', 
            '--timeout=1800'
        ],
    }
]
# ===================================================================================================


# ===================================================================================================
# ----------------------------------------------------------------------------------------
# Spawner(LoggingConfigurable) configuration
# ----------------------------------------------------------------------------------------

## The command used for starting the single-user server.
c.Spawner.cmd = ['start-notebook.sh']

## List of environment variables for the single-user server to inherit from the
#  JupyterHub process.
#  Default: ['PATH', 'PYTHONPATH', 'CONDA_ROOT', 'CONDA_DEFAULT_ENV', 
#           'VIRTUAL_ENV', 'LANG', 'LC_ALL', 'JUPYTERHUB_SINGLEUSER_APP']
c.Spawner.env_keep = ['LANG', 'LC_ALL']

## The default URL for users when they arrive (e.g. when user directs to "/")
c.Spawner.default_url = '/lab'

## The default users directory
# c.Spawner.notebook_dir = '/'

## Timeout (in seconds) before giving up on a spawned HTTP server
c.Spawner.http_timeout = 300

## Timeout (in seconds) before giving up on starting of single-user server.
c.Spawner.start_timeout = 300

## Enable debug-logging of the single-user server
c.Spawner.debug = True
# ===================================================================================================


# ===================================================================================================
# ----------------------------------------------------------------------------------------
# HTTP proxy configurations
# ----------------------------------------------------------------------------------------

# Initializing the proxy class
c.JupyterHub.proxy_class = 'jupyterhub.proxy.ConfigurableHTTPProxy'

# Ths is for enabling the Debug mode
c.ConfigurableHTTPProxy.debug = True

# Whether to shutdown the proxy when the Hub shuts down.
c.JupyterHub.cleanup_proxy = False

# This tells the hub to not stop servers when the hub restarts 
# (this is useful even if you don’t run the proxy separately)
c.JupyterHub.cleanup_servers = False

# This tells the hub that the proxy should not be started (because you start it yourself)
c.ConfigurableHTTPProxy.should_start = False

# Should be set to a token for authenticating communication with the proxy.
c.ConfigurableHTTPProxy.auth_token = config['HTTP_PROXY_AUTH_TOKEN']

# Should be set to the URL which the hub uses to connect to the proxy’s API
c.ConfigurableHTTPProxy.api_url = config['HTTP_PROXY_API_URL']
# ===================================================================================================


# ===================================================================================================
# Function to get the username from the email
def get_username(spawner):
    username = spawner.user.name
    return username

# Getting user name and Notebook user from the Spawner environment
c.Spawner.environment = {
    "USER_ID": get_username,
    "NB_USER": get_username,
    "CHOWN_HOME":"yes"
}
# ===================================================================================================