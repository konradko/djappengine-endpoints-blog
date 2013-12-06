# Blog on djappengine

Example: <http://djae-blog-test.appspot.com>

* Setup for Google App Engine with [djappengine](https://github.com/potatolondon/djappengine/)
* Supports [markdown](http://daringfireball.net/projects/markdown) syntax for article content
* Uses [Pure](http://purecss.io/) responsive CSS modified blog layout

## Requirements

Google Appengine Python SDK 1.7.5+

## Installation

**Locally**:

    git clone https://github.com/konradko/djappengine-blog.git
    cd djappengine-blog
    ./serve.sh

**Appspot**:

1. Set up an app on <http://appengine.google.com>
2. Replace app name:

        sed -i '' 's/djae-blog/myappid/' app.yaml settings.py

3. Deploy:

    appcfg.py update .

## Running tests

    python manage.py test blog