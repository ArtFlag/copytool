# copytool

A simple script to copy the provided path in a target folder and optionally start an HTTP server.
It can be useful when you need to spin up a website whose content is built from various repos, in various output
folders.

```console
Usage: copytool.py [OPTIONS]

Options:
  -t, --target TEXT  The target folder that will contain the provided paths.
                     [required]
  -p, --path TEXT    A path to a folder to be copied to the target path.
                     [required]
  -s, --serve        Starts a local webserver from the target folder.
  --help             Show this message and exit.
```

## Usage

### Setting up the virtual environment

1. This project uses [poetry](https://github.com/sdispater/poetry),
   [install it](https://poetry.eustace.io/docs/#installation).
1. From `copytool`:

   ```console
   poetry install
   ```

### Running the script

```console
poetry run python3 copytool.py <options>
```

### Examples

- Merging two folders (`source1` and `source2`) into `webserver` and running a server from it:

  ```console
  poetry run python3 copytool.py -t webserver -p source1 -p source2 --serve
  ```

- Copy a folder (`source`) into `webserver`:

  ```console
  poetry run python3 copytool.py -t webserver -p source
  ```
