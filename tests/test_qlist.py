from hoomanpy import qlist


class DummyModel(object):
    def __init__(self, name, order):
        self.name = name
        self.order = order
        self.status = "active"
        self.tags = []


def get_test_obj(listener=None):
    """Returns a qlist for testing

    :returns: Returns a qlist for testing
    :rtype: hoomanpy.qlist
    """

    ql = qlist(listener=listener)

    for i in range(0, 10):
        ql.append(DummyModel('Object #{}'.format(i), i + 1))

    ql[2].status = "inactive"
    ql[4].status = "inactive"
    ql[6].status = "inactive"
    ql[3].status = "in progress"
    ql[5].status = "in progress"
    ql[7].status = "in progress"

    ql[0].tags.extend(['pop', 'rock', 'groovy', 'music'])
    ql[1].tags.extend(['pop', 'rock', 'groovy', 'music'])
    ql[2].tags.extend(['pop', 'rock', 'groovy', 'music'])

    ql[3].tags.extend(['country', 'live', 'depressing', 'music'])
    ql[4].tags.extend(['country', 'live', 'depressing', 'music'])
    ql[5].tags.extend(['country', 'live', 'depressing', 'music'])

    ql[6].tags.extend(['folk', 'indie', 'hipster', 'music'])
    ql[7].tags.extend(['folk', 'indie', 'hipster', 'music'])
    ql[8].tags.extend(['folk', 'indie', 'hipster', 'music'])

    return ql


def test_listener():

    def listening(changelist, change):
        test_listener.lastchangelist = changelist
        test_listener.lastchange = change

    ql = get_test_obj(listener=listening)

    test_listener.lastchange = ''
    test_listener.lastchangelist = []

    # insert listener
    obj = DummyModel('New Object', 0)
    ql.insert(0, obj)
    assert test_listener.lastchange == 'added' and len(test_listener.lastchangelist) == 1 \
        and test_listener.lastchangelist[0] is obj

    # append listener
    obj = DummyModel('New Object', 0)
    ql.append(obj)
    assert test_listener.lastchange == 'added' and len(test_listener.lastchangelist) == 1 \
        and test_listener.lastchangelist[0] is obj

    # extend listener
    ql.extend([DummyModel('A', 0), DummyModel('B', 0)])
    assert test_listener.lastchange == 'added' and len(test_listener.lastchangelist) == 2 \
        and test_listener.lastchangelist[0] is not test_listener.lastchangelist[1]

    # pop listener
    obj = ql.pop()
    assert test_listener.lastchange == 'removed' and len(test_listener.lastchangelist) == 1 \
        and test_listener.lastchangelist[0] is obj

    # remove listener
    obj = ql[0]
    ql.remove(obj)
    assert test_listener.lastchange == 'removed' and len(test_listener.lastchangelist) == 1 \
        and test_listener.lastchangelist[0] is obj


def test_filter():

    ql = get_test_obj()

    # test filtering basic property
    assert len(ql.filter(status='active')) == 4

    # test 'less than' filter operator
    assert len(ql.filter(order__lt=5)) == 4

    # test 'less than or equal to' filter operator
    assert len(ql.filter(order__lte=5)) == 5

    # test 'greater than' filter operator
    assert len(ql.filter(order__gt=5)) == 5

    # test 'greater than or equal to' filter operator
    assert len(ql.filter(order__gte=5)) == 6

    # test 'in' filter operator on a non-collection property
    assert len(ql.filter(status__in=['inactive', 'in progress'])) == 6

    # test 'notin' filter operator on a non-collection property
    assert len(ql.filter(status__notin=['inactive', 'in progress'])) == 4

    # test 'in' filter operator on a collection property
    #assert ql.filter(tags__in=['indie', 'hipster']).count() == 6

    # test 'count' grouping operator
    assert len(ql.filter(tags__count=4)) == 9
    assert len(ql.filter(tags__count=0)) == 1

    # test filter operators in conjunction grouping operators
    assert len(ql.filter(tags__count__gt=0)) == 9

if __name__ == '__main__':
    test_listener()

    #
    #
    #
    # for action in dl.DataAccess.actions.filter(status__in=m.Action.active_statuses).sort('name').sort('status'):
    #     self.print_line('{}, {}', action.status, action.name)
    #
    # self.print_line("\n{:=^70}\n".format(" test max by attribute "))
    # for plan in dl.DataAccess.plans.filter(actions__max__order=1):
    #     self.print_line(plan.name)
    #
    # self.print_line("\n{:=^70}\n".format(" test max by object "))
    #
    # class testdummy(object):
    #     def __init__(self, name, numbers):
    #         self.name = name
    #         self.numbers = numbers
    #
    # from hoomanpy import qlist
    # a = qlist()
    # a.append(testdummy('a', range(0, 100)))
    # a.append(testdummy('b', range(0, 90)))
    #
    # for obj in a.filter(numbers__max__lt=100):
    #     self.print_line(obj.name)
    #
    # self.print_line("\n{:=^70}\n".format(" test distinct "))
    # for tag in dl.DataAccess.actions.distinct('tags').sort().flip():
    #     self.print_line(tag)
    #
    # self.print_line("\n{:=^70}\n".format(" test multiple collection connectors ending with implicit equals "))
    # for plan in dl.DataAccess.plans.filter(actions__any__tags__any='music'):
    #     self.print_line(plan.name)
    #
    # self.print_line("\n{:=^70}\n".format(" test multiple collection connectors ending with explicit equals "))
    # for plan in dl.DataAccess.plans.filter(actions__any__tags__any__equals='music'):
    #     self.print_line(plan.name)
    #
    # self.print_line("\n{:=^70}\n".format(" test multiple collection connectors ending with explicit startswith "))
    # for plan in dl.DataAccess.plans.filter(actions__any__tags__any__startswith='m'):
    #     self.print_line(plan.name)
    #
    # self.print_line("\n{:=^70}\n".format(" test single collection connector with attribute of collection "))
    # for plan in dl.DataAccess.plans.filter(actions__any__order=1):
    #     self.print_line(plan.name)
    #
    # self.print_line("\n{:=^70}\n".format(" test against positive None "))
    # for plan in dl.DataAccess.plans.filter(parent=None):
    #     self.print_line(plan.name)
    #
    # self.print_line("\n{:=^70}\n".format(" test count "))
    # for plan in dl.DataAccess.plans.filter(actions__count=0):
    #     self.print_line(plan.name)
    #
    # self.print_line("\n{:=^70}\n".format(" test sum "))
    # for plan in dl.DataAccess.plans.filter(actions__sum__order__gt=2):
    #     self.print_line(plan.name)
    #
    # self.print_line("\n{:=^70}\n".format(" test sum "))
    # for plan in dl.DataAccess.plans.filter(actions__sum__order__lte=2):
    #     self.print_line(plan.name)

#import pytest
#@pytest.fixture(scope='module', params=['1', '2', '3'])
# def test_answer(business_object):
#     assert business_object.func(3) == 5
#
# def test_has_a(business_object):
#     assert hasattr(business_object, 'a')
#
# def test_value_of_a_is_1(business_object):
#     assert business_object.a == '1'