"""Python. Improved.

Extended objects and common utilities for Python.
"""


class qlist(list):
    """A queryable list with optional collection listening and list insertion validation\conditioning."""

    # todo: implement strict querying - if getattr doesn't find an attribute raise an error instead of a false match
    # todo: implement querying beyond a single attribute in distinct(), like filter() does
    # todo: implement group by functions in filter()
    # todo: implement sum(), max(), min() - not to be confused with the filter methods _sum(), _max(), etc.

    group_funcs = ['_any', '_all', '_none', '_count', '_sum', '_max', '_min']

    def __init__(self, seq=(), strict_querying=False, listener=None, before_add=None):
        super(qlist, self).__init__(seq)
        self.strict_querying = strict_querying
        self.listener = listener
        self.before_add = before_add

    #===================================================================================================================
    # public methods that modify the list
    #===================================================================================================================
    def insert(self, index, p_object):
        # condition and validate object (casting, cleanup, etc, testing)
        if self.before_add is not None:
            p_object, abort = self.before_add(p_object, False)
        # insert into list
        super(qlist, self).insert(index, p_object)
        # inform listener of addition
        if self.listener is not None:
            self.listener([p_object], "added")

    def append(self, p_object):
        # condition and validate object (casting, cleanup, etc, testing)
        if self.before_add is not None:
            p_object, abort = self.before_add(p_object, False)
        # append to list
        super(qlist, self).append(p_object)
        # inform listener of addition
        if self.listener is not None:
            self.listener([p_object], "added")

    def extend(self, iterable):
        # condition and validate object (casting, cleanup, etc, testing)
        if self.before_add is not None:
            p_object, abort = self.before_add(iterable, True)
        # extend list
        super(qlist, self).extend(iterable)
        # inform listener of addition
        if self.listener is not None:
            self.listener(iterable, "added")

    def contract(self, iterable, ignore_notinlist=True):
        # contract list
        for obj in iterable:
            try:
                super(qlist, self).remove(obj)
            except ValueError, e:
                if not ignore_notinlist:
                    raise e
                else:
                    iterable.remove(obj)
        # inform listener of addition
        if self.listener is not None:
            self.listener(iterable, "removed")

    def remove(self, value):
        # remove from list
        super(qlist, self).remove(value)
        # inform listener of removal
        if self.listener is not None:
            self.listener([value], "removed")

    def pop(self, index=-1):
        # pop from list
        obj = super(qlist, self).pop(index)
        # inform listener of removal
        if self.listener is not None:
            self.listener([obj], "removed")
        # return popped object
        return obj

    def clear(self):
        removelist = self[:]
        while len(self) > 0:
            super(qlist, self).pop()
        # inform listener of removal
        if self.listener is not None:
            self.listener(removelist, "removed")

    #===================================================================================================================
    # public methods that return another qlist
    #===================================================================================================================
    def flip(self):
        copy_ = qlist(self[:])
        copy_.reverse()
        return copy_

    def sort(self, *args, **kwargs):
        from operator import attrgetter
        ordered_list = qlist()
        try:
            if len(args) == 0:
                ordered_list.extend(sorted(self, **kwargs))
            else:
                ordered_list.extend(sorted(self, key=attrgetter(*args), **kwargs))
        except AttributeError:
            if self.strict_querying:
                raise AttributeError
            else:
                return self
        return ordered_list

    def top(self, top):
        filtered_list = qlist()
        i = 0
        for obj in self:
            filtered_list.append(obj)
            i += 1
            if i == top:
                break
        return filtered_list

    def filter(self, **kwargs):

        # todo: decide on the possible benefits of creating a dummy object to use in place of None to know when
        #       a value is actually None and when a getattr fails to find it.

        filtered_list = qlist()
        first_result =  kwargs.pop('__first_result', False)

        for obj in self:
            match = True
            for key, value in kwargs.iteritems():
                match = self._compare(obj, value, key.split('__'))
                if not match:
                    break

            if match:
                if first_result:
                    return obj
                else:
                    filtered_list.append(obj)

        if first_result:
            return None
        else:
            return filtered_list

    def distinct(self, attribute=None):

        if len(self) == 0:
            return self

        #if attribute is None then distinct on self, else distinct on attribute
        distinct_list = qlist()
        col = self

        #test if attribute is a collection, if so, switch obj to this and return distinct list
        if attribute is not None:
            attr = getattr(self[0], attribute, None)
            if attr is None:
                return None
            else:
                if hasattr(attr, '__iter__'):
                    for obj in self:
                        attr = getattr(obj, attribute, None)
                        if attr is None:
                            return None
                        else:
                            for item in attr:
                                if item not in distinct_list:
                                    distinct_list.append(item)
                    return distinct_list

        if attribute is None:
            for obj in col:
                if obj not in distinct_list:
                    distinct_list.append(obj)
        else:
            distinct_values = []
            for obj in self:
                attr = getattr(obj, attribute, None)
                if attr is not None and attr not in distinct_values:
                    distinct_values.append(attr)
                    distinct_list.append(obj)
        return distinct_list

    #===================================================================================================================
    # public methods that return a specific object in the qlist
    #===================================================================================================================
    def get(self, **kwargs):
        #kwargs['__first_result'] = True
        return self.filter(__first_result=True, **kwargs)

    #===================================================================================================================
    # private methods
    #===================================================================================================================
    def _compare(self, obj, value, address, position=0, func=None):
        if func is None:
            func = self._equals

        # push through the address finding the object we're going to use in comparison
        for i in range(position, len(address)):

            try_func = None

            # check if the last in the address is a function
            if i > 0:
                try_func = getattr(self, '_{}'.format(address[i]), None)
                if try_func is not None:
                    func = try_func
                    # if it's a func and not the end, it must be a group connector
                    if i != len(address) - 1:
                        return func(obj, value, address, i+1)

            if try_func is None:
                obj = getattr(obj, address[i], None)
                if obj is None and value is not None:
                    return False

        # handle case where we end with a group connector and implicitly assume the equals func
        if func.func_name in self.group_funcs:
            return func(obj, value, address, len(address))
        else:
            return func(obj, value)

    #===================================================================================================================
    # private methods - filter operators
    #===================================================================================================================
    def _startswith(self, obj, compare):
        value = str(obj).lower()
        compare = str(compare).lower()
        if len(compare) > len(value):
            return False
        if compare == value[0:len(compare)]:
            return True
        else:
            return False

    def _endswith(self, obj, compare):
        value = str(obj).lower()
        compare = str(compare).lower()
        if len(compare) > len(value):
            return False
        if compare == value[-len(compare)]:
            return True
        else:
            return False

    def _contains(self, obj, compare):
        value = str(obj).lower()
        compare = str(compare).lower()
        if compare in value:
            return True
        else:
            return False

    def _in(self, obj, compare):

        if hasattr(obj, '__iter__') and hasattr(compare, '__iter__'):
            # is any in list in list
            a = set(obj)
            b = set(compare)
            if len(a & b) > 0:
                return True
            else:
                return False
        elif hasattr(compare, '__iter__'):
            # object is contained in list
            if obj in compare:
                return True
            else:
                return False
        else:
            # str is contained in str
            obj = str(obj).lower()
            compare = str(compare).lower()
            if obj in compare:
                return True
            else:
                return False

    def _notin(self, obj, compare):

        if hasattr(obj, '__iter__'):
            # is any in list in list
            a = set(obj)
            b = set(compare)
            if len(a & b) == 0:
                return True
            else:
                return False
        else:
            # is str in list
            if obj in compare:
                return False
            else:
                return True

    def _equals(self, obj, compare):
        if obj is None and compare is None:
            return True
        if obj is None or compare is None:
            return False

        return obj == compare

    def _lt(self, obj, compare):
        if obj is None and compare is None:
            return True
        if obj is None or compare is None:
            return False

        return obj < compare

    def _gt(self, obj, compare):
        if obj is None and compare is None:
            return True
        if obj is None or compare is None:
            return False

        return obj > compare

    def _lte(self, obj, compare):
        if obj is None and compare is None:
            return True
        if obj is None or compare is None:
            return False

        return obj <= compare

    def _gte(self, obj, compare):
        if obj is None and compare is None:
            return True
        if obj is None or compare is None:
            return False

        return obj >= compare

    #===================================================================================================================
    # private methods - group by functions
    #===================================================================================================================
    def _count(self, obj, compare, address, position):
        if self._compare(len(obj), compare, address, position):
            return True

        return False

    def _sum(self, obj, compare, address, position):

        sum = 0
        pos = position
        follow_attribute = False
        if len(address) > position:
            try_func = getattr(self, '_{}'.format(address[position]), None)
            if try_func is None:
                follow_attribute = True
                pos += 1

        max = None
        if not follow_attribute:
            # max on obj
            for item in obj:
                sum += item
        else:
            # max on obj attribute
            for item in obj:
                attr = getattr(item, address[position], None)
                if attr is None:
                    return False
                sum += attr

        return  self._compare(sum, compare, address, pos)

    def _max(self, obj, compare, address, position):

        pos = position
        follow_attribute = False

        if len(address) > position:
            try_func = getattr(self, '_{}'.format(address[position]), None)
            if try_func is None:
                follow_attribute = True
                pos += 1

        max = None
        if not follow_attribute:
            # max on obj
            for item in obj:
                if max is None or max < item:
                    max = item
        else:
            # max on obj attribute
            for item in obj:
                attr = getattr(item, address[position], None)
                if attr is None:
                    return False
                if max is None or max < attr:
                    max = attr

        return self._compare(max, compare, address, pos)

    def _min(self, obj, compare, address, position):

        follow_attribute = False
        pos = position

        if len(address) > position:
            try_func = getattr(self, '_{}'.format(address[position]), None)
            if try_func is None:
                follow_attribute = True
                pos += 1

        max = None
        if not follow_attribute:
            # max on obj
            for item in obj:
                if min is None or min > item:
                    min = item
        else:
            # max on obj attribute
            for item in obj:
                attr = getattr(item, address[position], None)
                if attr is None:
                    return False
                if min is None or min > attr:
                    min = attr

        return self._compare(min, compare, address, pos)

    #===================================================================================================================
    # private methods - group by to filter operator connections (think of having statements in sql)
    #===================================================================================================================
    def _any(self, obj, compare, address, position):
        for item in obj:
            if self._compare(item, compare, address, position):
                return True

        return False

    def _all(self, obj, compare, address, position):
        for item in obj:
            if not self._compare(item, compare, address, position):
                return False

        return True

    def _none(self, obj, compare, address, position):
        for item in obj:
            if self._compare(item, compare, address, position):
                return False

        return True