# encoding: utf-8

__author__ = 'nagai'


from Products.Five.browser import BrowserView
from edu.iot.portfolio.interfaces import IExperiment, IMeasuredData
from zope.interface import implementer
from zope.interface import implements
from Products.CMFCore.utils import getToolByName
import json
from plone import api


@implementer(IExperiment)
class ExperimentView(BrowserView):
    """

    """

    def __init__(self, context, request):
        super(ExperimentView, self).__init__(context, request)


@implementer(IExperiment)
class ExperimentNewGraphView(BrowserView):
    """

    """

    def __init__(self, context, request):
        super(ExperimentNewGraphView, self).__init__(context, request)

    def get_param(self):
        context = self.context
        device_uid = self.request.get('uid', '')
        params = context.get_params(device_uid)
        if params:
            sc = '''
            <script type="text/javascript">
            let app_id = '{}.mlkcca.com';
            let app_ds = '{}';
            let app_key = '{}';
            let app_pass = '{}';
            let device_id = '{}';
            </script>
            '''.format(params['app_id'], params['datastore'],
                       params['api_key'], params['api_secret'],
                       params['device_id'])
            return sc
        return u''

    def get_experimental_title(self):
        return self.request.form.get('e', u'')

    def get_group_num(self):
        return self.request.form.get('g', u'')


@implementer(IExperiment)
class ExperimentAddGraph(BrowserView):

    def __init__(self, context, request):
        super(ExperimentAddGraph, self).__init__(context, request)

    def __call__(self):
        context = self.context
        self.request.RESPONSE.setHeader('Content-Type', 'application/json')
        group_num = self.request.form.get('g', u'')
        experimental_title = self.request.form.get('e', u'')
        data = self.request.form.get('d', u'')
        m_obj = api.content.create(
            type='MeasuredData',
            title=u'{}班 のデータ'.format(group_num),
            container=context)
        m_obj.group_num = group_num
        m_obj.experimental_title = experimental_title
        m_obj.data = data
        m_obj.reindexObject()
        return json.dumps({'result': True})


@implementer(IExperiment)
class ExperimentMeasuredGraphView(BrowserView):

    def __init__(self, context, request):
        super(ExperimentMeasuredGraphView, self).__init__(context, request)

    def get_experimental_title(self):
        return self.request.form.get('e', u'')

    def _get_value(self, data, posi):
        if len(data) > posi:
            return str(data[posi])
        return u'null'

    def _get_label_name(self, group_num, ex_title, filter):
        if filter:
            return u'"{}班"'.format(group_num)
        else:
            return u'"{}: {}班"'.format(ex_title, group_num)

    def get_dataset(self):
        ex_title = self.request.form.get('e', u'')
        uid = self.request.form.get('uid', u'')
        graphs = [x for x in self.context.get_graphs(ex_title, uid) if json.loads(x.data)]
        data_set = []
        values = []
        labels = [self._get_label_name(x.group_num, x.experimental_title, ex_title) for x in graphs]
        data_set.append(u'[{}]'.format(u','.join([u'"time"'] + labels)))
        max_size = 0
        for g in graphs:
            dl = [x['value']['temp'] for x in json.loads(g.data)]
            if len(dl) > max_size:
                max_size = len(dl)
            values.append(dl)
        for num in range(max_size):
            data_row = [str(num * 30)]
            for v in values:
                data_row.append(self._get_value(v, num))
            data_set.append(u'[{}]'.format(u','.join(data_row)))

        sc = '''
            <script type="text/javascript">
            var data_set = [{}];
            </script>
            '''.format(u','.join(data_set))

        return sc






@implementer(IMeasuredData)
class MeasuredDataView(BrowserView):
    """

    """

    def __init__(self, context, request):
        super(MeasuredDataView, self).__init__(context, request)

