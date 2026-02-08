"""
APSchedule 安裝設定檔
"""
from setuptools import setup, find_packages
from pathlib import Path

# 讀取 README
readme_file = Path(__file__).parent / 'README.md'
long_description = readme_file.read_text(encoding='utf-8') if readme_file.exists() else ''

setup(
    name='apschedule',
    version='1.0.0',
    description='簡易排程系統 - 基於 APScheduler',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='APSchedule Team',
    packages=find_packages(),
    install_requires=[
        'APScheduler==3.10.4',
        'PyYAML==6.0.1',
    ],
    extras_require={
        'dev': [
            'pytest==7.4.3',
            'pytest-cov==4.1.0',
            'pytest-mock==3.12.0',
        ],
    },
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)


















