# vim: set fileencoding=utf-8 :

from setuptools import setup

setup(
        name="gncxml",
        version="0.1.3",
        description="Extract entries in GnuCash data file as pandas.DataFrame.",
        long_description="Extract entries in GnuCash data file as pandas.DataFrame.",
        author="LiosK",
        author_email="contact@mail.liosk.net",
        url="https://github.com/LiosK/gncxml",
        scripts=["scripts/gncxml"],
        packages=["gncxml"],
        install_requires=["pandas"],
        license="MIT License",
        classifiers=[
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3 :: Only",
            "Topic :: Office/Business :: Financial",
            "Topic :: Software Development :: Libraries :: Python Modules",
            ],
        )
