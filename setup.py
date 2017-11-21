# vim: set fileencoding=utf-8 :

from setuptools import setup

setup(
        name="gncxml",
        version="0.1.1",
        description="Extract entries from GnuCash data file",
        author="LiosK",
        author_email="contact@mail.liosk.net",
        url="https://github.com/LiosK/gncxml",
        scripts=["scripts/gncxml"],
        packages=["gncxml"],
        install_requires=["pandas"],
        )
