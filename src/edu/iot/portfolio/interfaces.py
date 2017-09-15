# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from edu.iot.portfolio import _
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from plone.autoform import directives
from plone.supermodel.directives import fieldset
from plone.supermodel.directives import primary
from plone.supermodel import model
from plone.autoform import directives as form
from z3c.relationfield.schema import RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.app.z3cform.widget import RelatedItemsFieldWidget

from edu.iot.syllabus.interfaces import IUnit
from edu.iot.devicemanage.interfaces import IDevice


class IEduIotPortfolioLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IPortfolio(model.Schema):
    """

    """

    year = schema.Int(
        title=_(u'Year'),
        required=True,
    )

    grade = schema.TextLine(
        title=_(u'Grade'),
        required=True,
    )

    klassname = schema.TextLine(
        title=_(u'Class name'),
        required=True,
    )


class IReport(model.Schema):
    """

    """


class IExperiment(model.Schema):
    """
    実験のインターフェイス
    """

    unit = RelationChoice(
        title=_(u"Unit"),
        vocabulary='plone.app.vocabularies.Catalog',
        required=False,
    )

    form.widget(
        'unit',
        RelatedItemsFieldWidget,
        vocabulary='plone.app.vocabularies.Catalog',
    )


class IMeasuredData(model.Schema):
    """

    """

    group_num = schema.TextLine(
        title=_(u'Group number'),
        required=False,
    )

    experimental_title = schema.TextLine(
        title=_(u'Experimental Title'),
        required=False,
    )

    data = schema.Text(
        title=_(u'Data'),
        required=False,
    )

    start = schema.TextLine(
        title=_(u'Start date'),
        required=False,
    )

    end = schema.TextLine(
        title=_(u'End date'),
        required=False,
    )

