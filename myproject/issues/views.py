from rest_framework.views import APIView
from issues.service import IssueService
from common.webCommon import ResponsObject
from common.webCommon import decode_body, decode_post
import json

# Create your views here.
class Issues(APIView):
    issueService = IssueService()

    def __init__(self):
        self.res = ResponsObject()

    def get(self, _, status, nameUser, params, id):
        repository = self.issueService.findIssue(status, nameUser, params, id)
        self.res.addItem(repository)

        return self.res.createResponse(status=200)
    
    def post(self, request):
        repositoryData = decode_body(request.body)
        data = {
            "name": repositoryData["name"],
            "description": repositoryData["description"],
            "id": repositoryData["id"],
            "labels": repositoryData["labels"]
        }

        res = self.issueService.createNewIssue(repositoryData['user'], data)
        self.res.addItem(res)
        
        return self.res.createResponse(status=200)
    
    def put(self, request):
        res = self.issueService.closeIssue(request.data['data']['id'], request.data['user'])
        
        self.res.addItem(res)
        return self.res.createResponse(status=200)

class IssuesGet(APIView):
    issueService = IssueService()

    def __init__(self):
        self.res = ResponsObject()

    def get(self, _, id):
        res = self.issueService.getCommentByIssue(id)

        self.res.addItem(res)
        return self.res.createResponse(status=200)
    
    def put(self, request):
        res = self.issueService.assignedToIssue(request.data['user'], request.data['data'])
        
        self.res.addItem(res)
        return self.res.createResponse(status=200)

class IssuesComment(APIView):
    issueService = IssueService()

    def __init__(self):
        self.res = ResponsObject()

    def post(self, request):
        res = self.issueService.createNewComment(request.data['user'], request.data['data'])

        self.res.addItem(res)
        return self.res.createResponse(status=200)
    
    def put(self, request):
        res = self.issueService.editIssue(request.data['user'], request.data['data'])

        self.res.addItem(res)
        return self.res.createResponse(status=200)

class IssuesLanles(APIView):
    issueService = IssueService()

    def __init__(self):
        self.res = ResponsObject()
    
    def put(self, request):
        res = self.issueService.updateLabels(request.data['issueId'], request.data['label'], request.data['userId'])
        self.res.addItem(res)
        return self.res.createResponse(status=200)