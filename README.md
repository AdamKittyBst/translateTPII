# TranslateTPII

Develop a local Python GUI application that translates Chinese text to English or Indonesian, prioritizing local vector database and using remote Google or OpenAI API as backup, with results saved locally for future use.

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy trans

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading).

## Deployment

The following details how to deploy this application.

## 文件结构

- `main.py`: 主应用程序入口，负责启动整个应用。
- `gui/`: 存放与用户界面相关的代码。
  - `app.py`: Tkinter GUI的主要实现代码。
  - `widgets.py`: 自定义的Tkinter小部件（widgets）代码。
- `assets/`: 存放应用需要使用的图片、图标等资源文件。
- `translation/`: 存放与翻译相关的代码。
  - `translator.py`: 负责调用翻译API，处理翻译任务的代码。
  - `history.py`: 管理历史翻译记录的代码。
  - `keyword_table.py`: 管理关键字表的代码。
- `local_db/`: 存放本地向量数据库相关的代码。
  - `db_operations.py`: 对本地向量数据库的增删改查操作。
- `files/`: 存放用户选择的文件和翻译后的文件。
- `translated_files/`: 存放翻译后的文件。
- `requirements.txt`: 用于记录项目所需的依赖库及其版本。

