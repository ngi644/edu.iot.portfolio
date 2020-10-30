# encoding: utf-8

__author__ = 'nagai'


from Products.Five.browser import BrowserView
from edu.iot.portfolio.interfaces import IExperiment, IMeasuredData, IPortfolio
from zope.interface import implementer
from zope.interface import implements
from Products.CMFCore.utils import getToolByName
import json
import datetime
from plone import api
import decimal
import urllib
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


def round_harf_even(num, q='.1'):
    """
    banker's rounding
    """
    d_num = decimal.Decimal(num).quantize(decimal.Decimal(q), rounding=decimal.ROUND_HALF_EVEN)
    return float(d_num)


def step_round(x, base=5):
    return base * round(float(x)/base)


@implementer(IPortfolio)
class PortfolioView(BrowserView):
    """

    """

    def __init__(self, context, request):
        super(PortfolioView, self).__init__(context, request)


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


    template_mlkcca = ViewPageTemplateFile('templates/experiment_new_graph_view.pt')
    template_fb = ViewPageTemplateFile('templates/experiment_new_graph_fb_view.pt')

    def __init__(self, context, request):
        super(ExperimentNewGraphView, self).__init__(context, request)

    def __call__(self):

        device_uid = self.request.get('uid', '')
        cloud_type = self.context.get_params(device_uid).get('cloud_type', 'Milkcocoa')

        if cloud_type == 'Firebase':
            return self.template_fb()
        else:
            return self.template_mlkcca()


    def get_param(self):
        context = self.context
        device_uid = self.request.get('uid', '')
        params = context.get_params(device_uid)
        if params:
            if params['cloud_type'] == 'Milkcocoa':
                sc = '''
                <script type="text/javascript">
                let app_id = '{}.mlkcca.com';
                let app_ds = '{}';
                let app_key = '{}';
                let app_pass = '{}';
                let device_id = '{}';
                let device_name = '{}';
                </script>
                '''.format(params['app_id'], params['datastore'],
                           params['api_key'], params['api_secret'],
                           params['device_id'], params['device_name'])
            if params['cloud_type'] == 'Firebase':
                sc = '''
                <script type="text/javascript">
                let apiKey = '{}';
                let authDomain = '{}';
                let databaseURL = '{}';
                let storageBucket = '{}';
                let fb_projectId = '{}';
                let messagingSenderId = '{}';
                let device_id = '{}';
                let device_name = '{}';
                </script>
                '''.format(params['fb_apiKey'], params['fb_authDomain'],
                           params['fb_databaseURL'], params['fb_projectId'], params['fb_storageBucket'],
                           params['fb_messagingSenderId'],
                           params['device_id'], params['device_name'])
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

    def _get_other_label_name(self, group_num, ex_title, ext_obj, filter_e=None):
        """

        :param group_num:
        :param ex_title:
        :param ext_obj:
        :return:
        """
        nl = []
        if ext_obj:
            if self.context.__parent__.title != ext_obj.__parent__.title:
                nl.append(u'{}|'.format(ext_obj.__parent__.title))
            nl.append('{}年度{}{} {}班|'.format(ext_obj.year, ext_obj.grade, ext_obj.klassname, group_num))
            if not filter_e:
                nl.append(ex_title)
        return u''.join(nl)

    def _get_obj_by_uid(self, uid=None):
        """

        :param uid:
        :return:
        """
        base_query = {}
        portal_catalog = getToolByName(self, 'portal_catalog')
        if uid:
            base_query['UID'] = uid
            return portal_catalog(base_query)[0].getObject()
        return None

    def _get_datasets(self, m_key='temp'):
        ex_title = self.request.form.get('e', u'')
        g_num = self.request.form.get('g', u'')
        uid = self.request.form.get('uid', u'')
        o_g_num = self.request.form.get('og', u'')
        o_uid = self.request.form.get('ouid', u'')
        o_euid = self.request.form.get('oeuid', u'')
        if o_euid:
            other_obj = self._get_obj_by_uid(o_euid)
            other_search = True
        else:
            other_obj = None
            other_search = False
        graphs = [x for x in self.context.get_graphs(ex_title, uid, g_num) if json.loads(x.data)]
        if other_search:
            other_graphs = [x for x in self.context.get_graphs(ex_title, o_uid, o_g_num, other_obj) if json.loads(x.data)]
        else:
            other_graphs = []
        review_set = []
        main_labels = [self._get_label_name(x.group_num, x.experimental_title, ex_title, g_num) for x in graphs]
        other_labels = [self._get_other_label_name(x.group_num, x.experimental_title, other_obj, ex_title).replace('|', '<br>') for x in other_graphs]
        labels = main_labels + other_labels
        data_list = []
        for i, g in enumerate(graphs + other_graphs):
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

    def get_other_link(self, oeuid, og):
        """

        :param g_uid:
        :param g_:
        :return:
        """

        ex_title = self.request.form.get('e', u'')
        g_num = self.request.form.get('g', u'')
        uid = self.request.form.get('uid', u'')
        o_uid = self.request.form.get('ouid', u'')
        qs = urllib.urlencode(dict(e=ex_title,
                                    g=g_num,
                                    uid=uid,
                                    og=og,
                                   oeuid=oeuid,
                                   ouid=o_uid))
        return '{}/measured_view?{}'.format(self.context.absolute_url(), qs)


@implementer(IMeasuredData)
class MeasuredDataView(BrowserView):
    """

    """

    def __init__(self, context, request):
        super(MeasuredDataView, self).__init__(context, request)




