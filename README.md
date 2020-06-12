# Messenger Builder

Custom metrics parser for MessengerUp clients in the field

## Getting Started

This application is intended as a Docker image where a self terminating container is created when a new build is required to be made.

This requires a client interface or scheduled task that instructs the creation of the build after port discovery and assignment of a port number that is included as an environment variable. This project does not contain a `.env` file independent of the variables passed in the command set.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

