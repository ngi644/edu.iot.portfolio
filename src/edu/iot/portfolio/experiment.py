# encoding: utf-8

__author__ = 'nagai'

from plone.dexterity.content import Item, Container
from zope.interface import implements
from Products.CMFCore.utils import getToolByName


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

    def get_experimental_list(self):
        """
        単元のデータから実験リストを取得
        :return:
        """
        unit = self.get_unit()
        if unit.experimental_list:
            return unit.experimental_list
        return []

    def get_graphs(self, experimental_title=None, uid=None, group_num=None):
        """

        :return:
        """
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
