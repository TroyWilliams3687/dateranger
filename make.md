# Make

The makefiles are the reason for this repository. They provide functionality in a common way across different python repositories. It makes that using a command like `make venv` will construct the virtual environment and install all the requirements. It means that `make test` will run pytest (if installed).

For the `Makefile` to work properly, we have to define the `Makefile.env`. This file should not be stored in the repository, add it to `.gitignore` (if you use the template in this repo, it is already there). `Makefile.env` stores the path to the Python binaries that you want to use. This means it is possible to use different versions of Python if you want in a way that is transparent and flexible (at least I think so). There are two sample files, one for Linux (bash) and one for windows. Rename the appropriate one and set the path correctly.

- `Makefile.env`
- `Makefile.env.sample`
- `Makefile.env.win.sample`

>NOTE: If you have lots of repositories and they require different versions of python, you can use a symbolic link in the repositories to point them to the correct file.

```bash
$ ln -s ~/repositories/env\ files/Makefile3.10.1.env Makefile.env
```

>NOTE: Once you create a symbolic link, you can copy it around to the different folders.

Once the `Makefile.env` is properly configured it is time to add the rest of the makefiles. For a basic Python repository, you should use the following 3 makefiles:

- `Makefile`
    - This is the root Makefile. It defines a lot of the commands and it includes (imports) the other more specialized makefiles.

- `Makefile.python`
    - This is Python specific commands around constructing and managing the virtual environments.
    - It is simply included into the main Makefile.

- `Makefile.python.build`
    - This Python specific commands around testing and linting.
    - It is simply included into the main Makefile.

Optionally, you can include these makefiles to provide more specialized support. You can also create your own.

- `Makefile.docker`
- `Makefile.jupyter`

>NOTE: The `Makefile` support files are located in the `./mf_support` folder to clean up the repo of the root. They do tend to add noise that isn't necessary.

## `mf_support`

This folder contains the support files required by the `Makefile` in the repository. You should maintain copies of the support files so the repository can stand on its own.


## Basic Commands


Help:

```bash
$ make
```

Delete `.venv` and other python folders (caches and temp folders):

```bash
$ make remove
```

Build virtual environment (`.venv`):

```bash
$ make venv
```

Launch virtual environment:

```bash
$ make shell
```

Run unit tests:

```bash
$ make test
```