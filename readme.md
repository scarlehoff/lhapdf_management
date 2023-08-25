Management library for LHAPDF

This a pure-python LHAPDF management library to download, list and load PDFs.
At the moment it cannot do any interpolation or perform anything that would need a complete LHAPDF installation.


# Install

It can be installed from pypi with a simple command

```
  pip install lhapdf-management
```

# Features

At the moment is very bare-bones and includes only:

## Update

Updates the local reference index

```
  lhapdf_management update
```

If no installation of LHAPDF is found, the program will fail to do anything, as creating the `LHAPDF` directory is not the business of the management module.
In order to run lhapdf-management and make it believe that LHAPDF already exist a possibility is to populate the `LHAPDF_DATA_PATH` environment variable, i.e.,

```bash
LHAPDF_DATA_PATH=$(python -c 'from pathlib import Path ; from sys import prefix ; print(Path(prefix) / "share" / "LHAPDF")' ; lhapdf-management update
```

It is possible to create the directory in the "best guess location" doing `lhapdf_management update --init`

## List

Lists all available PDFs

```
  lhapdf_management list [PATTERNS ...] [--installed] [--codes]
```

## Install

Installs a given PDF

```
  lhapdf_management install <pdf_name> [--upgrade] [--keep]
```

## Open a PDF

It can also be used to programatically get an object pointing to all the right parts of a PDF.
No interpolation will be provided by this script at this point and when/if it is ever provided
will be done by importing the normal `python` interface of LHAPDF (and so at that point LHAPDF
will need to be installed)

```python
  from lhapdf_management.pdfsets import PDF
  from lhapdf_management.configuration import get_lhapdf_datapath
  data_path = get_lhapdf_datapath()
  pdf = PDF(data_path / "NNPDF31_nnlo_as_0118")
  grids = pdf.get_member_grids(0)
```

## Programatically use the interface

A very useful feature of this library is the possibility of using everything programatically.
The three given interfaces (install, list and update) take as input the same arguments
as the script interface.

```python
  from lhapdf_management import pdf_install, pdf_list, pdf_update
  list_of_pdfs = pdf_list("--installed")
  pdf_install("NNPDF31_nnlo_as_0118")
```

## Download all PDFs matching pattern

There are some arguments that have been modified for simplicity as their behaviour can also
be obtained by other means.
For instance, in order to download all PDFs matching a certain pattern one can write the
following short bash script:

```bash
  for pdf in $(lhapdf_management list NNPDF31*)
  do
    lhapdf_management install ${pdf} --upgrade
  done
```

# TODO
While this script can (if needed) be used as is, there are a number of features missing to be compatible with the `lhapdf`.
The list of features that are currently missing with respect to the previous script are:

- list ``--outdated``
- install ``--dryrun``
