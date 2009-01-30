from django.http import HttpResponse
from django.template import loader, Context, RequestContext
from pdb import set_trace

class TemplateResponse(HttpResponse):

    def set_template(self, value):
#        if not value:
#            set_trace()
#        assert(value and 'template argument must not be None')
        print 'New template value for %s is: %s' % (repr(self), value)
        #set_trace()
        self._real_template = value
    def get_template(self):
        return self._real_template

    _template = property(get_template, set_template)

#    def _get_context(self):
#        return self._context
#    def _set_context(self, value):
#        print 'NEW CONTEXT: ', value
#        self._context = value
#        if value is None:
#            set_trace()
    #context = property(_get_context, _set_context)

    def __init__(self, template, context, *args, **kwargs):
        assert(template and 'template argument must not be None')
        assert(context.get('base_template', None) and 'base_template not given in the context')
        self._template = template
        self._context = context
        self.rendered = False
        print 'INIT ', self._context
        super(TemplateResponse, self).__init__(*args, **kwargs)
        assert(self._context.get('base_template', None) and 'base_template not given in the context')
    
    def resolve_template(self, template):
        # Template can be a template object, path-to-template or list of paths
        if isinstance(template, (list, tuple)):
            return loader.select_template(template)
        elif isinstance(template, basestring):
            return loader.get_template(template)
        else:
            return template
    
    def resolve_context(self, context):
        # Context can be a dictionary or a context object
        if isinstance(context, Context):
            return context
        else:
            return Context(context)
    
    def render(self):
        if not self._template:
            set_trace()
        assert(self._template and 'please, setup template to render')

        template = self.resolve_template(self._template)
        assert(template and 'template not found')

        context = self.resolve_context(self._context)
        try:
            return template.render(context)
        except Exception, e:
            raise
            #set_trace()
    
    def bake(self):
        """
        The template is baked the first time you try to do something with the
        response - access response.content, for example. This is a bit ugly, 
        but is necessary because Django middleware frequently expects to be 
        able to over-write the content of a response.
        """
        if not self.rendered:
            print 'BAKE ', self._context
            self._set_content(self.render())
            self.rendered = True
    
    def __iter__(self):
        self.bake()
        return super(TemplateResponse, self).__iter__()
    
    def _get_content(self):
        self.bake()
        return super(TemplateResponse, self)._get_content()
    
    def _set_content(self, value):
        return super(TemplateResponse, self)._set_content(value)
    
    content = property(_get_content, _set_content)

class RequestTemplateResponse(TemplateResponse):
    
    def __init__(self, request, template, context, *args, **kwargs):
        self.request = request
        assert(template)
        base_template = context.get('base_template')
        print base_template
        set_trace()
        super(RequestTemplateResponse, self).__init__(
            template, context, *args, **kwargs
        )
    
    def resolve_context(self, context):
        if isinstance(context, Context):
            return context
        else:
            return RequestContext(self.request, context)

# Less verbose alias:
render = RequestTemplateResponse
