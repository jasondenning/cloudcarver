from setuptools import setup

requirements = [
    'boto',
    'requests',
    'pyyaml',
]

setup(name="CloudCarver",
      version="0.01",
      description="Stuff",
      author="Jason Denning",
      packages=['cloudcarver']
)
