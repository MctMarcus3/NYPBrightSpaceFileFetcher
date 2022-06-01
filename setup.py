from setuptools import setup

setup(
    name="NYPLMSFileFetcher",
    version="0.1",
    packages=["uff"],
    entry_points={
        "console_scripts": ['NYPLMSFileFetcher=uff.uforafilefetcher:run'],
    }, install_requires=[
        "requests==2.25.1",
        "beautifulsoup4==4.9.3",
        "tqdm==4.60.0",
        "inquirer==2.7.0",
        "selenium==4.0.0",
        "webdriver-manager==3.4.2",
        "pathvalidate==2.4.1",
        "pyotp==2.6.0",
        "pyOpenSSL>=0.14"
    ]
)
