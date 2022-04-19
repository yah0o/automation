import asyncio

from copy import copy
from urllib.parse import quote

from capi_lib_python.aio import AIOClient
from capi_lib_python.exceptions import CAPIResponseError


contracts = {
    'api_key': '410ab756-627d-4c93-b556-4a42359d3e1f',
    'app_id': 'nprs',
    'path': 'contracts',
    'message_bus': {
        'host': 'breeder-wgt1.wgns.iv',
        'port': 5672,
        'username': 'wgt1-platform',
        'password': 'wgt1-platform',
        'vhost': '/wgt1-platform',
    },
    'timeout': 10,
    'names': ['external-events.v1.receipt-created'],
}


def check_response(responses):
    names = copy(contracts['names'])
    for resp in responses:
        if isinstance(resp, CAPIResponseError):
            continue
        for name in resp['serving_contracts']:
            if name in names:
                names.remove(name)
    if names:
        return 0
    return 1


async def check():
    client = AIOClient(
        contracts['app_id'],
        amqp_url='amqp://%s:%s@%s:%d/%s' % (
            contracts['message_bus']['username'],
            contracts['message_bus']['password'],
            contracts['message_bus']['host'],
            contracts['message_bus']['port'],
            quote(contracts['message_bus']['vhost'], safe='')
        ),
        contracts_path=contracts['path'],
        loop=asyncio.get_event_loop(),
        auth='api-key:%s' % contracts['api_key'],
    )

    try:
        roll_call_result = await asyncio.wait_for(
            client.collect(
                'system.v1.roll-call',
                {'reason': 'nprs monitoring'},
                predicate=check_response
            ),
            timeout=20,
        )
        print(roll_call_result)
    except Exception as e:
        return 0
    return check_response(roll_call_result)


async def func():
    if await check():
        print('Finished!', 'success')
    else:
        print('Finished!', 'failed')


loop = asyncio.get_event_loop()
loop.run_until_complete(func())