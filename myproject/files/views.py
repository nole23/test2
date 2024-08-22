from rest_framework.views import APIView
from files.services import FileService
from common.webCommon import ResponsObject
from common.webCommon import decode_body

# Create your views here.



class File(APIView):
    fileService = FileService()

    def __init__(self):
        self.res = ResponsObject()

    def post(self, request):
        repositoryData = dict(request.POST)
        
        res = self.fileService.addNewFile(repositoryData)
        self.res.addItem(res)
        return self.res.createResponse(status=200)

    def put(self, request):
        data = decode_body(request.body)

        res = self.fileService.updateFile(data)
        self.res.addItem(res)
        return self.res.createResponse(status=200)

    def delete(self, _, id):
        res = self.fileService.removeFile(id)
        self.res.addItem(res)
        return self.res.createResponse(status=200)