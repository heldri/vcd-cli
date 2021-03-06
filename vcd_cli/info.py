# vCloud CLI 0.1
#
# Copyright (c) 2014 VMware, Inc. All Rights Reserved.
#
# This product is licensed to you under the
# Apache License, Version 2.0 (the "License").
# You may not use this product except in compliance with the License.
#
# This product may include a number of subcomponents with
# separate copyright notices and license terms. Your use of the source
# code for the these subcomponents is subject to the terms and
# conditions of the subcomponent's license, as noted in the LICENSE file.
#

import click
from pyvcloud.vcd.client import QueryResultFormat
from pyvcloud.vcd.client import RESOURCE_TYPES
from pyvcloud.vcd.utils import to_camel_case
from pyvcloud.vcd.utils import to_dict
from tabulate import tabulate
from vcd_cli.utils import restore_session
from vcd_cli.utils import stderr
from vcd_cli.utils import stdout
from vcd_cli.utils import tabulate_names
from vcd_cli.vcd import vcd


@vcd.command(short_help='show resource details')
@click.pass_context
@click.argument('resource_type',
                metavar='[resource-type]',
                required=False)
@click.argument('resource-id',
                metavar='[resource-id]',
                required=False)
def info(ctx, resource_type, resource_id):
    """Display details of a resource in vCloud Director.

\b
    Description
        Display details of a resource with the provided type and id.
        Resource type is not case sensitive. When invoked without a resource
        type, list the available types. Admin resources are only allowed when
        the user is the system administrator.
\b
    Examples
        vcd info task ffb96443-d7f3-4200-825d-0f297388ebc0
            Get details of task by id.
\b
        vcd info vapp c48a4e1a-7bd9-4177-9c67-4c330016b99f
            Get details of vApp by id.
\b
    See Also
        Several 'vcd' commands provide the id of a resource, including the
        'vcd search' command.
    """
    try:
        if resource_type is None or resource_id is None:
            click.secho(ctx.get_help())
            click.echo('\nAvailable resource types:')
            click.echo(tabulate(tabulate_names(RESOURCE_TYPES, 4)))
            return
        restore_session(ctx)
        client = ctx.obj['client']
        q = client.get_typed_query(to_camel_case(resource_type,
                                                 RESOURCE_TYPES),
                                   query_result_format=QueryResultFormat.
                                   ID_RECORDS,
                                   qfilter='id==%s' % resource_id)
        records = list(q.execute())
        if len(records) == 0:
            raise Exception('not found')
        elif len(records) > 1:
            raise Exception('multiple found')
        result = to_dict(records[0], resource_type)
        stdout(result, ctx, show_id=True)
    except Exception as e:
        import traceback
        traceback.print_exc()
        stderr(e, ctx)
