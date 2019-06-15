#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals
from logging import getLogger

from . import variables as v
from . import utils
###############################################################################

LOG = getLogger('PLEX.migration')


def check_migration():
    LOG.info('Checking whether we need to migrate something')
    last_migration = utils.settings('last_migrated_PKC_version')
    if last_migration == v.ADDON_VERSION:
        LOG.info('Already migrated to PKC version %s' % v.ADDON_VERSION)
        # Ensure later migration if user downgraded PKC!
        utils.settings('last_migrated_PKC_version', value=v.ADDON_VERSION)
        return

    if not utils.compare_version(last_migration, '1.8.2'):
        LOG.info('Migrating to version 1.8.1')
        # Set the new PKC theMovieDB key
        utils.settings('themoviedbAPIKey',
                       value='19c90103adb9e98f2172c6a6a3d85dc4')

    if not utils.compare_version(last_migration, '2.0.25'):
        LOG.info('Migrating to version 2.0.24')
        # Need to re-connect with PMS to pick up on plex.direct URIs
        utils.settings('ipaddress', value='')
        utils.settings('port', value='')

    if not utils.compare_version(last_migration, '2.7.6'):
        LOG.info('Migrating to version 2.7.5')
        from .library_sync.sections import delete_files
        delete_files()

    if not utils.compare_version(last_migration, '2.8.3'):
        LOG.info('Migrating to version 2.8.2')
        from .library_sync import sections
        sections.clear_window_vars()
        sections.delete_videonode_files()

    utils.settings('last_migrated_PKC_version', value=v.ADDON_VERSION)
