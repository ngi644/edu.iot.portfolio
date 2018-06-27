# encoding: utf-8

__author__ = 'nagai'

from plone.dexterity.content import Item, Container
from zope.interface import implements
from Products.CMFCore.utils import getToolByName

from Acquisition import aq_inner
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from zope.security import checkPermission
from zc.relation.interfaces import ICatalog


class Experiment(Container):
    """A experiment class"""

    def get_unit(self):
        """
        単元データの取得
        :return:
        """
        return self.unit.to_object

    def get_params(self, uid):

        portal_catalog = getToolByName(self, 'portal_catalog')
        base_query = {}
        base_query['UID'] = uid
        results = portal_catalog(base_query)
        if results:
            device_obj = results[0].getObject()
            return device_obj.get_params()
        return {}

    def get_devices(self):
        """
        デバイスの一覧取得
        :return:
        """
        portal_catalog = getToolByName(self, 'portal_catalog')
        base_query = {}
        base_query['portal_type'] = ('Device',)
        devices = portal_catalog(base_query)
        return devices

    def get_group_list(self):
        """
        単元のデータから班のリストを返す
        :return:
        """
        unit = self.get_unit()
        if unit.group_count:
            return [x+1 for x in range(unit.group_count)]
        return []

    def get_valid_group_list(self):
        """
        データのある班のみ返す。
        :return:
        """
        g_list = []
        for ex in self.get_experimental_list():
            for g in self.get_group_list():
                r = self.get_graphs(experimental_title=ex, group_num=str(g))
                if r:
                    g_list.append(g)
        return list(set(g_list))

    def get_valid_group_list_per_exp(self, ex_title=None):
        """
        特定の実験においてデータのある班のみ返す。
        :return:
        """
        g_list = []
        if not ex_title:
            ex_title = self.REQUEST.form.get('e', u'')
        for g in self.get_group_list():
            r = self.get_graphs(experimental_title=ex_title, group_num=str(g))
            if r:
                g_list.append(g)
        return list(set(g_list))

    def get_experimental_list(self):
        """
        単元のデータから実験リストを取得
        :return:
        """
        unit = self.get_unit()
        if unit.experimental_list:
            return unit.experimental_list
        return []

    def get_graphs(self, experimental_title=None, uid=None, group_num=None, other_obj=None):
        """

        :return:
        """
        if other_obj:
            cur_path = '/'.join(other_obj.getPhysicalPath())
        else:
            cur_path = '/'.join(self.getPhysicalPath())
        base_query = {}
        portal_catalog = getToolByName(self, 'portal_catalog')
        base_query['portal_type'] = ('MeasuredData',)
        base_query['path'] = {'query': cur_path, 'depth': 1}
        base_query['sort_on'] = 'group_num'
        #base_query['sort_order'] = 'reverse'
        if experimental_title:
            base_query['experimental_title'] = experimental_title
        if uid:
            base_query['UID'] = uid
        if group_num:
            base_query['group_num'] = group_num
        graphs = portal_catalog(base_query)
        return graphs

    def get_other_experiment(self):
        """
        同じUnitの実験を検索する
        :return: experiment list
        """
        #import pdb;pdb.set_trace()
        results = self.back_references(self.unit.to_object, 'unit')
        return results

    def back_references(self, source_object, attribute_name):
        """
        Return back references from source object on specified attribute_name
        """
        catalog = getUtility(ICatalog)
        intids = getUtility(IIntIds)
        result = []
        for rel in catalog.findRelations(dict(to_id=intids.getId(aq_inner(source_object)),
                                              from_attribute=attribute_name)):
            obj = intids.queryObject(rel.from_id)
            if obj is not None and checkPermission('zope2.View', obj):
                if obj.UID() != self.UID():
                    result.append(obj)
        return result
