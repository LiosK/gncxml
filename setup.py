# vim: set fileencoding=utf-8 :

from setuptools import setup

setup(
        name="gncxml",
        version="0.3.1",
        description="Extract entries from GnuCash data file to pandas.DataFrame.",
        long_description="Extract entries from GnuCash data file to pandas.DataFrame.",
        author="LiosK",
        author_email="contact@mail.liosk.net",
        url="https://github.com/LiosK/gncxml",
        scripts=["scripts/gncxml"],
        packages=["gncxml"],
        install_requires=["pandas"],
        classifiers=[
            "License :: OSI Approved :: Apache Software License",
            "Programming Language :: Python :: 3 :: Only",
            "Topic :: Office/Business :: Financial",
            "Topic :: Software Development :: Libraries :: Python Modules",
            ],
        )
