from Products.Five.browser import BrowserView
from edu.iot.portfolio.interfaces import IPortfolio
from zope.interface import implementer
from zope.interface import implements
from Products.CMFCore.utils import getToolByName
import json
import datetime
from plone import api

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


@implementer(IPortfolio)
class PortfolioSampleView(BrowserView):
    """

    """

    def __init__(self, context, request):
        super(PortfolioSampleView, self).__init__(context, request)



@implementer(IPortfolio)
class PortfolioSearchView(BrowserView):
    """

    """

    def __init__(self, context, request):
        super(PortfolioSearchView, self).__init__(context, request)


    def search_keyword(self):
        context = self.context
        cur_path = '/'.join(context.getPhysicalPath())
        keyword = self.request.form.get('key', u'')
        base_query = {}
        portal_catalog = getToolByName(self, 'portal_catalog')
        base_query['portal_type'] = ('Experiment', )
        base_query['path'] = {'query': cur_path, 'depth': 1}
        base_query['SearchableText'] = [keyword,]
        
        items = portal_catalog(base_query)
        return items
