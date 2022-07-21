# Copyright 2018 TNG Technology Consulting GmbH, Unterföhring, Germany
# Licensed under the Apache License, Version 2.0 - see LICENSE.md in project root directory

import logging

from xml.sax.saxutils import escape

log = logging.getLogger()


class Todo:
    def __init__(self, file_path, line_number, content):
        self.file_path = file_path
        self.line_number = line_number
        self.content = content
        self.is_valid = True
        self.error_reason = None
        self.is_ignored = False
        self.ignored_reason = None

    def __str__(self):
        return 'Todo in file ' + self.file_path + ':' + str(self.line_number) + ' | ' + self.content

    def mark_as_valid(self):
        self.is_valid = True
        self.error_reason = None

    def mark_as_invalid(self, error_reason):
        self.is_valid = False
        self.error_reason = error_reason

    def mark_as_ignored(self, ignored_reason):
        self.is_ignored = True
        self.ignored_reason = ignored_reason

    def print(self, show_valid=False):
        if not show_valid and self.is_valid:
            return

        log.error('[REASON]   %s' % self.error_reason)
        if self.is_ignored:
            log.error('[IGNORED]  %s' % self.ignored_reason)
        log.error('[FILE]     %s' % self.file_path)
        log.error('[LINE]     %s' % self.line_number)
        log.error('[CONTENT]  %s' % self.content)


    def print_xml(self, xml_file):
        status_ignored = ' status="ignored"' if self.is_ignored else ''
        if self.is_valid:
            xml_file.write('\t<testcase classname="{}" name="line {}"{} />\n'.format(self.file_path, self.line_number, status_ignored))
        else:
            xml_file.write('\t<testcase classname="{}" name="line {}"{} >\n'.format(self.file_path, self.line_number, status_ignored))
            xml_file.write('\t\t<failure message="{}">{}</failure>\n'.format(self.error_reason, escape(self.content)))
            xml_file.write('\t</testcase>\n')
