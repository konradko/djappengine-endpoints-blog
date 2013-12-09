# Blog on djappengine with API on Google Cloud Enpoints

Example: <http://djae-endpoints-blog.appspot.com>

* Setup for Google App Engine with [djappengine](https://github.com/potatolondon/djappengine/)
* API on Google Cloud Enpoints created with [endpoints-proto-datastore](https://github.com/GoogleCloudPlatform/endpoints-proto-datastore)
* Supports [markdown](http://daringfireball.net/projects/markdown) syntax for article content
* Uses [Pure](http://purecss.io/) responsive CSS modified blog layout

## Requirements

Google Appengine Python SDK 1.8.5+

To run API explorer on local dev environment you need [this patch](https://gist.github.com/littleq0903/7681603) applied to google_appengine/google/appengine/api/logservice/logservice_stub.py ([Google App Engine Issue 10285](https://code.google.com/p/googleappengine/issues/detail?id=10285))

## Installation

**Locally**:

    git clone https://github.com/konradko/djappengine-endpoints-blog.git
    cd djappengine-endpoints-blog
    ./serve.sh

Visit <http://localhost:8080> to see it running or <http://localhost:8080/_ah/api/explorer> to explore the API.

**Appspot**:

1. Set up an app on <http://appengine.google.com>
2. Replace app name:

        sed -i '' 's/djae-blog/myappid/' app.yaml settings.py

3. Deploy:

    appcfg.py update .

## Running tests

    python manage.py test blog