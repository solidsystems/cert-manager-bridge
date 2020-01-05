from setuptools import setup, find_packages


# Used for installing test dependencies directly
tests_require = [
    'flake8',
    'mock',
    'nose',
    'nose-timer',
    'coverage<4.1',
]

setup(
    name='cert-manager-bridge',
    version='1.0.0',
    description="Bridge API for cert-manager",
    author="Jacob Alheid",
    author_email="shakefu@gmail.com",
    packages=find_packages(exclude=['test', 'test_*', 'fixtures']),
    install_requires=[
        'configargparse>=0.14.1',
        'flask',
        'pytool',
        'pyyaml',
        'requests',
        'waitress',
        ],
    test_suite='nose.collector',
    tests_require=tests_require,
    # For installing test dependencies directly
    extras_require={'test': tests_require},
    url="https://github.com/solidsystems/cert-manager-bridge/",
    entry_points={
        'console_scripts': [
            ],
        },
)

