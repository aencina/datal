from core.shortcuts import render_to_response
from core.http import get_domain_by_request
from core.daos.datastreams import DataStreamDBDAO
from core.daos.visualizations import VisualizationDBDAO


def sitemap(request):
    import datetime

    language = request.auth_manager.language
    account = request.account
    params = request.GET

    domain = get_domain_by_request(request)
    now = datetime.datetime.now()
    dss = DataStreamDBDAO().query(account_id=account.id, language=language, filters_dict=dict(status=[3]))[0]
    vss = VisualizationDBDAO().query(account_id=account.id, language=language, filters_dict=dict(status=[3]))[0]

    return render_to_response('sitemap.xml', locals(), mimetype="application/xml")
