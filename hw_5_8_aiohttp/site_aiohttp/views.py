from aiohttp import web

from main import app
from serializer import AdSerializer
from models import Ad, User


async def get_ads(request):
    ads = await Ad.query.gino.all()
    resp = {'count': len(ads), 'items': [ad.to_dict() for ad in ads]}

    return web.json_response(resp, status=200)


async def get_ad(request):
    ad_id = request.match_info['ad_id']
    ad = await Ad.get(int(ad_id))
    ad_data = ad.to_dict()
    return web.json_response(ad_data, status=200)


async def post_ad(request):
    ad_data = await request.json()

    user = await User.get(int(ad_data['id_owner']))
    if user is None:
        return web.json_response({'error': 'Not Found Owner'}, status=404)

    ad_serialized = AdSerializer(**ad_data)
    ad_data = ad_serialized.dict()
    new_ad = await Ad.create(**ad_data)
    return web.json_response(new_ad.to_dict(), status=200)


async def put_ad(request):
    ad_id = request.match_info['ad_id']

    ad = await Ad.get(int(ad_id))

    if ad is None:
        return web.json_response({'error': 'Not Found Ad'}, status=404)
    else:
        ad_data = await request.json()

        await ad.update(title=ad_data['title'], text=ad_data['text'], id_owner=ad_data['id_owner']).apply()

        return web.json_response(ad.to_dict(), status=200)


async def delete_ad(request):
    ad_id = request.match_info['ad_id']

    ad = await Ad.get(int(ad_id))

    if ad is None:
        return web.json_response({'error': 'Not Found Ad'}, status=404)
    else:
        await ad.delete()

        return web.json_response({}, status=200)

app.add_routes([web.get('/ads/', get_ads)])
app.add_routes([web.get('/ads/{ad_id}', get_ad)])
app.add_routes([web.post('/ads/', post_ad)])
app.add_routes([web.put('/ads/{ad_id}', put_ad)])
app.add_routes([web.delete('/ads/{ad_id}', delete_ad)])