# encoding: utf-8

__author__ = 'nagai'


from Products.Five.browser import BrowserView
from edu.iot.portfolio.interfaces import IExperiment, IMeasuredData
from zope.interface import implementer
from zope.interface import implements
from Products.CMFCore.utils import getToolByName
import json
import datetime
from plone import api
import decimal


def round_harf_even(num, q='.1'):
    """
    banker's rounding
    """
    d_num = decimal.Decimal(num).quantize(decimal.Decimal(q), rounding=decimal.ROUND_HALF_EVEN)
    return float(d_num)


def step_round(x, base=5):
    return base * round(float(x)/base)


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
        memo = self.request.form.get('m', u'')
        m_obj = api.content.create(
            type='MeasuredData',
            title=u'{}班 のデータ'.format(group_num),
            container=context)
        m_obj.group_num = group_num
        m_obj.experimental_title = experimental_title
        m_obj.data = data
        m_obj.memo = memo
        m_obj.reindexObject()
        return json.dumps({'result': True})


@implementer(IExperiment)
class ExperimentMeasuredGraphView(BrowserView):

    def __init__(self, context, request):
        super(ExperimentMeasuredGraphView, self).__init__(context, request)

    def get_experimental_title(self):
        return self.request.form.get('e', u'')

    def get_group_title(self):
        g_num = self.request.form.get('g', u'')
        if g_num:
            return u'【 {}班 】'.format(g_num)
        return u''

    def _get_value(self, data, posi):
        if len(data) > posi:
            return u'{0:.1f}'.format(data[posi])
        return u'null'

    def _get_label_name(self, group_num, ex_title, filter_e, filter_g):
        if filter_e:
            return u'{}班'.format(group_num)
        elif filter_g:
            return u'{}'.format(ex_title)
        else:
            return u'{}: {}班'.format(ex_title, group_num)

    def _get_datasets(self, m_key='temp'):
        ex_title = self.request.form.get('e', u'')
        g_num = self.request.form.get('g', u'')
        uid = self.request.form.get('uid', u'')
        graphs = [x for x in self.context.get_graphs(ex_title, uid, g_num) if json.loads(x.data)]
        review_set = []
        labels = [self._get_label_name(x.group_num, x.experimental_title, ex_title, g_num) for x in graphs]
        data_list = []
        for i, g in enumerate(graphs):
            g_x = []
            g_y = []
            for posi, m_data in enumerate(json.loads(g.data)):
                now_time = datetime.datetime.fromtimestamp(m_data['timestamp'] / 1000)
                if posi < 1:
                    total_sec = 0
                    now_sec = 0
                else:
                    tdl = now_time - past_timestamp
                    now_sec = step_round(tdl.seconds)
                    print(now_sec)
                total_sec += now_sec
                g_x.append(round_harf_even(total_sec / 60.0, '.01'))
                g_y.append(round_harf_even(m_data['value'][m_key]))
                past_timestamp = now_time

            data_list.append(dict(x=g_x, y=g_y, name=labels[i], type='scatter',
                                  mode='lines+markers',
                                  marker=dict(symbol='circle', size=4)))
            review_set.append(dict(title=labels[i], memo=g.memo))

        return data_list, review_set

    def get_dataset(self):

        data_set, review_set = self._get_datasets()
        sc = '''
            <script type="text/javascript">
            var data_json = '{}';
            </script>
            '''.format(json.dumps(data_set))
        return sc

    def get_comments(self):
        data_set, review_set = self._get_datasets()
        return review_set



@implementer(IMeasuredData)
class MeasuredDataView(BrowserView):
    """

    """

    def __init__(self, context, request):
        super(MeasuredDataView, self).__init__(context, request)

