from flask import Response
from flask import current_app, request
import json

"""
chaosmonkey.api.hal.link
==============

Implements the ``HAL`` Link specification.
"""

VALID_LINK_ATTRS = [
    'name',
    'title',
    'type',
    'deprecation',
    'profile',
    'templated',
    'hreflang'
]


class Collection(list):
    """Build a collection of ``HAL`` link objects.

    Example:
        >>> from chaosmonkey.api.hal.link import Collection, Link
        >>> l = Collection(
        ...     Link('foo', 'http://foo.com'),
        ...     Link('bar', 'http://bar.com'))
        >>> print l.to_dict()
        ... {
        ...     '_links': {
        ...         'foo': {
        ...             'href": "http://foo.com'
        ...         },
        ...         'bar': {
        ...             'href': 'http://bar.com'
        ...         }
        ...     }
        ... }
    """

    def __init__(self, *args):
        """Initialise a new ``Collection`` object.

        Example:
            >>> l = Collection(
            ...     Link('foo', 'http://foo.com'),
            ...     Link('bar', 'http://bar.com'))

        Raises:
            TypeError: If a link is not a ``chaosmonkey.api.hal.Link`` instance
        """

        for link in args:
            if not isinstance(link, Link):
                raise TypeError(
                    '{0} is not a valid chaosmonkey.api.hal.Link instance'.format(link))

            self.append(link)

    def to_dict(self):
        """Returns the Python ``dict`` representation of the ``Collection``
        instance.

        Example:
            >>> from chaosmonkey.api.hal.link import Collection, Link
            >>> l = Collection(
            ...     Link('foo', 'http://foo.com'),
            ...     Link('bar', 'http://bar.com'))
            >>> l.to_dict()
            ... {'_links': {'bar': {'href': 'http://bar.com'},
            ... 'foo': {'href': 'http://foo.com'}}}

        Returns:
            dict
        """

        links = {}

        for link in self:
            if link.rel in links.keys():
                if isinstance(links[link.rel], dict):
                    links[link.rel] = [links[link.rel]]
                links[link.rel].append(link.to_dict()[link.rel])
            else:
                links.update(link.to_dict())

        return {
            '_links': links
        }

    def to_json(self):
        """Returns the ``JSON`` representation of the instance.

        Example:
            >>> from chaosmonkey.api.hal.link import Collection, Link
            >>> l = Collection(
            ...     Link('foo', 'http://foo.com'),
            ...     Link('bar', 'http://bar.com'))
            >>> l.to_json()
            ... '{"_links":
                    {
                        "foo": {"href": "http://foo.com"},
                        "bar": {"href": "http://bar.com"}
                    }
                }'

        Returns:
            str: The ``JSON`` representation of the instance
        """

        return json.dumps(self.to_dict())


class Link(object):
    """Build ``HAL`` specification ``_links`` object.

    Example:
        >>> from chaosmonkey.api.hal.link import Link
        >>> l = Link('foo', 'http://foo.com/bar')
        >>> print l.to_json()
        ... '{"foo": {"href": "http://foo.com/bar"}}'
        >>> l.title = 'Foo'
        >>> print l.to_json()
        ... '{"foo": {"href": "http://foo.com/bar", "name": "Foo"}}'

    """

    def __init__(self, rel, href, **kwargs):
        """Initialise a new ``Link`` object.

        Args:
            rel (str): The links ``rel`` or name
            href (str): The URI to the resource

        Keyword Args:
            name (str): The links name attribute, optional
            title (str): The links title attribute, optional
            type (str): The links type attribute, optional
            deprecation (str): The deprecation attribute, optional
            profile (str): The profile  attribute, optional
            templated (bool): The templated attribute, optional
            hreflang (str): The hreflang attribute, optional
        """

        self.rel = rel
        self.href = href

        for attr in VALID_LINK_ATTRS:
            if attr in kwargs:
                setattr(self, attr, kwargs.pop(attr))

    def to_dict(self):
        """Returns the Python ``dict`` representation of the ``Link`` instance.

        Example:
            >>> from chaosmonkey.api.hal.link import Link
            >>> l = Link('foo', 'http://foo.com')
            >>> l.to_dict()
            ... {'foo': {'href': 'http://foo.com'}}

        Returns:
            dict
        """

        # Minimum viable link
        link = {
            'href': self.href
        }

        # Add extra attributes if they exist
        for attr in VALID_LINK_ATTRS:
            if hasattr(self, attr):
                link[attr] = getattr(self, attr)

        return {
            self.rel: link
        }

    def to_json(self):
        """Returns the ``JSON`` encoded representation of the ``Link`` object.

        Example:
            >>> from chaosmonkey.api.hal.link import Link
            >>> l = Link('foo', 'http://foo.com', name='Foo')
            >>> print l.to_json()
            ... '{"foo": {"href": "http://foo.com", "name": "Foo"}}'

        Returns:
            str: The ``JSON`` encoded object
        """
        return json.dumps(self.to_dict())


class Self(Link):
    """A class to create the required ``self`` link  from the current
    request URL.
    """

    def __init__(self, **kwargs):
        """Initialises a new ``Self`` link instance. Accepts the same
        Keyword Arguments as :class:`.Link`.

        Additional Keyword Args:
            external (bool): if true, force link to be fully-qualified URL, defaults to False

        See Also:
            :class:`.Link`
        """

        url = request.url
        external = kwargs.get('external', False)
        if not external and current_app.config['SERVER_NAME'] is None:
            url = request.url.replace(request.host_url, '/')

        return super(Self, self).__init__('self', url, **kwargs)


class BaseDocument(object):
    """Constructs a ``HAL`` document.
    """

    def __init__(self, data=None, links=None, embedded=None):
        """Base ``HAL`` Document. If no arguments are provided a minimal viable
        ``HAL`` Document is created.

        Keyword Args:
            data (dict): Data for the document
            links (chaosmonkey.api.hal.link.Collection): A collection of ``HAL`` links
            embedded: TBC

        Raises:
            TypeError: If ``links`` is not a :class:`chaosmonkey.api.hal.link.Collection`
        """

        self.data = data
        self.embedded = embedded or {}
        self.links = links or Collection()

    @property
    def links(self):
        return self._links

    @links.setter
    def links(self, value):
        if not isinstance(value, Collection):
            if isinstance(value, (list, set, tuple)):
                value = Collection(*value)
            else:
                raise TypeError('links must be a {0} or {1} instance'.format(
                                Collection, list))
        self._links = value

    @property
    def embedded(self):
        return self._embedded

    @embedded.setter
    def embedded(self, value):
        if not isinstance(value, dict):
            raise TypeError('embedded must be a {0} instance'.format(dict))
        self._embedded = value

    def to_dict(self):
        """Converts the ``Document`` instance into an appropriate data
        structure for HAL formatted documents.

        Returns:
            dict: The ``HAL`` document data structure
        """

        document = {}

        # Add Data to the Document
        if isinstance(self.data, dict):
            document.update(self.data)

        # Add Links
        if self.links:
            document.update(self.links.to_dict())

        # Add Embedded: Embedded API TBC
        if self.embedded:
            embedded = {}
            for n, v in self.embedded.items():
                if isinstance(v, list):
                    embedded[n] = []
                    for item in v:
                        embedded[n].append(item.to_dict() if not isinstance(item, dict) else item)
                else:
                    embedded[n] = v.to_dict()

            document.update({
                '_embedded': embedded
            })

        return document

    def to_json(self):
        """Converts :class:`.Document` to a ``JSON`` data structure.

        Returns:
            str: ``JSON`` document
        """

        return json.dumps(self.to_dict())


class Document(BaseDocument):
    """Constructs a ``HAL`` document.
    """

    def __init__(self, data=None, links=None, embedded=None, external_self=False):
        """Initialises a new ``HAL`` Document instance. If no arguments are
        provided a minimal viable ``HAL`` Document is created.

        Keyword Args:
            data (dict): Data for the document
            links (chaosmonkey.api.hal.link.Collection): A collection of ``HAL`` links
            embedded: TBC
            external_self: use a fully-qualified link for self

        Raises:
            TypeError: If ``links`` is not a :class:`chaosmonkey.api.hal.link.Collection`
        """
        super(Document, self).__init__(data, links, embedded)
        self.links.append(Self(external=external_self))


class Embedded(BaseDocument):
    """Constructs a ``HAL`` embedded.

    Example:
        >>> document = Document(
        >>>     embedded={
        >>>         'orders': Embedded(
        >>>             embedded={'details': Embedded(
        >>>                 data={'details': {}}
        >>>             )},
        >>>             links=link.Collection(
        >>>                 Link('foo', 'www.foo.com'),
        >>>                 Link('boo', 'www.boo.com')
        >>>             ),
        >>>             data={'total': 30},
        >>>         )
        >>>     },
        >>>     data={'currentlyProcessing': 14}
        >>> )
        >>> document.to_json()
        ... {
                "_links": {
                    "self": {"href": "/entity/231"}
                },
                "_embedded": {
                    "orders": {
                        "_embedded": {
                            "details": {"details": {}}
                        },
                        "total": 30,
                        "_links": {
                            "foo": {"href": "www.foo.com"},
                            "boo": {"href": "www.boo.com"}
                        }
                    }
                },
                "currentlyProcessing": 14
            }
    """

    def to_dict(self):
        """Converts the ``Document`` instance into an appropriate data
        structure for HAL formatted documents.

        Returns:
            dict: The ``HAL`` document data structure
        """
        if isinstance(self.data, (list, tuple, set)):
            data = []

            for item in self.data:
                if isinstance(item, BaseDocument):
                    data.append(item.to_dict())
                else:
                    data.append(item)
            return data

        return super(Embedded, self).to_dict()


class HAL(object):
    """Enables Flask-HAL integration into Flask Applications, either by the
    Application Factory Pattern or directly into an already created Flask
    Application instance.

    This will set a custom ``response_class`` for the Application which
    handles the conversion of a ``HAL`` document response from a
    view into it's ``JSON`` representation.
    """

    def __init__(self, app=None, response_class=None):
        """Initialise Flask-HAL with a Flask Application. Acts as a proxy
        to :meth:`chaosmonkey.api.hal.HAL.init_app`.

        Example:
            >>> from flask import Flask
            >>> from chaosmonkey.api.hal import HAL
            >>> app = Flask(__name__)
            >>> HAL(app=app)

        Keyword Args:
            app (flask.app.Flask): Optional Flask application instance
            response_class (class): Optional custom ``response_class``
        """

        if app is not None:
            self.init_app(app, response_class=response_class)

    def init_app(self, app, response_class=None):
        """Initialise Flask-HAL with a Flask Application. This is designed to
        be used with the Flask Application Factory Pattern.

        Example:
            >>> from flask import Flask
            >>> from chaosmonkey.api.hal import HAL
            >>> app = Flask(__name__)
            >>> HAL().init_app(app)

        Args:
            app (flask.app.Flask): Flask application instance

        Keyword Args:
            response_class (class): Optional custom ``response_class``
        """

        # Set the response class
        if response_class is None:
            app.response_class = HALResponse
        else:
            app.response_class = response_class


class HALResponse(Response):
    """A custom response class which overrides the default Response class
    wrapper.

    Example:
        >>> from flask import Flask()
        >>> from chaosmonkey.api.hal import HALResponse
        >>> app = Flask(__name__)
        >>> app.response_class = HALResponse
    """

    @staticmethod
    def force_type(rv, env):
        """Called by ``flask.make_response`` when a view returns a none byte,
        string or unicode value. This method takes the views return value
        and converts into a standard `Response`.

        Args:
            rv (chaosmonkey.api.hal.document.Document): View return value
            env (dict): Request environment

        Returns:
            flask.wrappers.Response: A standard Flask response
        """

        if isinstance(rv, Document):
            return Response(
                rv.to_json(),
                headers={
                    'Content-Type': 'application/hal+json'
                })

        return Response.force_type(rv, env)
