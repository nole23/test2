from rest_framework.views import APIView
from common.webCommon import ResponsObject
from statistic.service import StatisticService

# Create your views here.
class Statistic(APIView):
    statistic = StatisticService()

    def __init__(self):
        self.res = ResponsObject()

    def get(self, _, id):
        statis = self.statistic.getStatistic(id)
        
        self.res.addItem(statis)
        return self.res.createResponse(status=200)