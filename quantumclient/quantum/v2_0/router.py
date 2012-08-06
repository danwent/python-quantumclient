# Copyright 2012 OpenStack LLC.
# All Rights Reserved
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#
# vim: tabstop=4 shiftwidth=4 softtabstop=4

import logging

from quantumclient.quantum.v2_0 import CreateCommand
from quantumclient.quantum.v2_0 import DeleteCommand
from quantumclient.quantum.v2_0 import ListCommand
from quantumclient.quantum.v2_0 import UpdateCommand
from quantumclient.quantum.v2_0 import ShowCommand
from quantumclient.quantum.v2_0 import QuantumCommand


class ListRouter(ListCommand):
    """List routers that belong to a given tenant."""

    resource = 'router'
    log = logging.getLogger(__name__ + '.ListRouter')
    _formatters = {}


class ShowRouter(ShowCommand):
    """Show information of a given router."""

    resource = 'router'
    log = logging.getLogger(__name__ + '.ShowRouter')


class CreateRouter(CreateCommand):
    """Create a router for a given tenant."""

    resource = 'router'
    log = logging.getLogger(__name__ + '.CreateRouter')

    def add_known_arguments(self, parser):
        parser.add_argument(
            '--admin_state_down',
            default=True, action='store_false',
            help='Set Admin State Up to false')
        parser.add_argument(
            'name', metavar='name',
            help='Name of router to create')

    def args2body(self, parsed_args):
        body = {'router': {
            'name': parsed_args.name,
            'admin_state_up': parsed_args.admin_state_down, }, }
        if parsed_args.tenant_id:
            body['router'].update({'tenant_id': parsed_args.tenant_id})
        return body


class DeleteRouter(DeleteCommand):
    """Delete a given router."""

    log = logging.getLogger(__name__ + '.DeleteRouter')
    resource = 'router'


class UpdateRouter(UpdateCommand):
    """Update router's information."""

    log = logging.getLogger(__name__ + '.UpdateRouter')
    resource = 'router'

class AddInterfaceRouter(QuantumCommand):
    """Use add_interface action on a given router."""

    api = 'network'
    log = logging.getLogger(__name__ + '.AddInterfaceRouter')
    resource = 'router'

    def get_parser(self, prog_name):
        parser = super(AddInterfaceRouter, self).get_parser(prog_name)
        parser.add_argument(
            'router_id', metavar='router_id',
            help='ID of the router')
        parser.add_argument(
            'subnet_id', metavar='subnet_id',
            help='ID of the subnet for the interface')
        return parser

    def run(self, parsed_args):
        self.log.debug('run(%s)' % parsed_args)
        quantum_client = self.get_client()
        quantum_client.format = parsed_args.request_format
        #TODO(danwent): handle passing in port-id
        quantum_client.add_interface_router(parsed_args.router_id,
                                     {'subnet_id': parsed_args.subnet_id})
        #TODO(danwent): print port ID that is added
        print >>self.app.stdout, (
            _('Added interface to router %s') % parsed_args.router_id)
        return


