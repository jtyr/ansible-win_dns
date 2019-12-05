from __future__ import (absolute_import, division, print_function)


def ammend_records(data, auto):
    ptrs = []

    for d in data:
        if 'type' in d and d['type'] == 'A' and auto:
            # Create PTR record
            ptr = dict(d)

            zone = ptr['zone']
            name = ptr['name']

            ptr['type'] = 'PTR'
            ptr['zone'] = '.'.join(
                ptr['value'].split('.')[::-1][1:]) + '.in-addr.arpa'
            ptr['name'] = ptr['value'].split('.')[-1]
            ptr['value'] = "%s.%s" % (name, zone)

            # Add missing dot
            if not ptr['value'].endswith('.'):
                ptr['value'] += '.'

            ptrs.append(ptr)
        elif 'type' in d and d['type'] == 'CNAME':
            # Add missing dot
            if not d['value'].endswith('.'):
                d['value'] += '.'

    return data + ptrs


class FilterModule(object):
    def filters(self):
        return {
            'ammend_records': ammend_records,
        }
