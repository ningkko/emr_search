from setuptools import setup, find_packages

setup(

    name="engine",
    version="1.0",
    description="A search tool for medical records.",
    author="Ningkko",
    author_email="makiasagawa@gmail.com",
    packages=find_packages(),
    install_requires=["whoosh", "jieba"],
    url='https://github.com/ningkko/emr_search',
    entry_points='''
        [console_scripts]
        emr=engine.emr
    '''

)
