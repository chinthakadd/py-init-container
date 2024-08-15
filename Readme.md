
## Motivation

To build a simple init container that we can use docker and kubernetes environments which can perform health checks
against infrastructure components that live outside the premise of our deployment environment.

These health checks rely on the same application configuration details and try to establish plain connections and make sure
that connectivity can be established. Such init containers are specially useful kubernetes deployments which has many external
infrastructure dependencies.

## To install the packages required

```shell
pipenv install
```

## How to run

- Refer to settings.toml to configure the health checks of each component
- Start Docker Compose from Install Folder
- Run app.py