from setuptools import setup

setup(
    name='learning_text_transformer',
    version='0.1.0',
    description='learning_text_transformer',
    long_description="some long desc",
    author='Maintained by Ian Ozsvald',
    author_email='ian@ianozsvald.com',
    url='https://github.com/ianozsvald/',
    license='MIT',
    #packages=['company_database_builder', 'company_database_builder/tests', 'company_database_builder/config'],
    packages=['engine', 'engine/tests']
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
