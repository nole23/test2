import json
from django.http import HttpResponse
#region ResponsObject

def decode_body(body):
    data_unicode = body.decode('utf-8')
    return json.loads(data_unicode)

def decode_post(data):
    return json.loads(data)

class Object1():
    def __init__(self, key, value):
        self.key = key
        self.value = value

class ResponsObject():
    def __init__(self):
        self.responseObject = {}

    def addItem(self, key):
        self.responseObject = key

    def createResponse(self, status):
        response = HttpResponse(json.dumps(
            self.responseObject), content_type="application/json", status=status)
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
    
    def decode_body(self, body):
        data_unicode = body.decode('utf-8')
        return json.loads(data_unicode)

    def listProjectUserSerialize(self, data, isIssue=False):
        rd = []
        
        for each in data:
            rd.append({
                'id': str(each.project.id),
                'projectName': str(each.project.name),
                'type': str(each.project.typeProject),
                'typeLanguage': each.project.typeLanguage,
                'typeLicense': each.project.typeLicense,
                'dateOfModifide': str(each.project.dateCreate),
                'descriotion': str(each.project.description)
            })
        return rd
    
    def projectUserSerialize(self, data):
        rd = {
                'id': str(data.id),
                'projectName': str(data.name),
                'type': str(data.typeProject),
                'typeLanguage': data.typeLanguage,
                'typeLicense': data.typeLicense,
                'dateOfModifide': str(data.dateCreate),
                'descriotion': str(data.description)
            }
        return rd
    
    def projectSerialize(self, data, issuesData, listProjectData):
        return {
            'id': str(data.id),
            'name': data.name,
            'description': data.description,
            'dateCreate': str(data.dateCreate),
            'dateClose': str(data.dateClose),
            'typeProject': data.typeProject,
            'rootTree': self.rootTreeSeriallize(data.rootTree.all()),
            'issue': self.issuesSerialize(issuesData) if issuesData != None else None,
            'listUser': self.listUserSerialize(listProjectData) if listProjectData != None else None
        }
    
    def issuesSerialize(self, data):
        rd = []
        for each in data:
            rd.append({
                'id': str(each.id),
                'name': each.name,
                'description': each.description,
                'status': each.status,
                'dateCreate': str(each.dateCreate),
                'user': self.userSerialize(each.user),
                'assigned': self.assignedSerialize(each.assigned.all()),
                'labels': each.labels
            })
        return rd
    
    def issueSerialize(self, data):
        return {
            'id': str(data.id),
            'name': data.name,
            'description': data.description,
            'status': data.status,
            'user': self.userSerialize(data.user),
            'dateCreate': str(data.dateCreate),
            'assigned': self.userFirstSerialize(data.assigned.all()),
            'labels': data.labels

        }
    
    def issuesCommentSerialize(self, data):
        rd = []
        for each in data:
            rd.append(self.issueCommentSerialize(each))
        return rd
    
    def issueCommentSerialize(self, data):
        return {
            'id': str(data.id),
            'comment': data.comment,
            'issue': self.issueSerialize(data.issue),
            'user': self.userSerialize(data.user),
            'dateCreate': str(data.dateCreate),
            'typeComment': data.typeComment
        }
    
    def userFirstSerialize(self, data):
        dt = []
        for each in data:
            dt.append({
                'id': str(each.id),
                'firstName': each.firstName,
                'lastName': each.lastName,
                'username': each.username
            })
        return dt
    
    def assignedSerialize(self, data):
        rd = []
        for each in data:
            rd.append({
                'id': str(each.id),
                'firstName': each.firstName,
                'lastName': each.lastName,
                'username': each.username
            })
        return rd
    
    def listUserSerialize(self, data, notList=False):
        if notList == False:
            rd = []
            for each in data:
                rd.append({
                    'user': self.userSerialize(each.user),
                    'role': self.roleSerialize(each.role)
                })
            return rd
        else:
            return {
                'user': self.userSerialize(data.user),
                'role': self.roleSerialize(data.role)
            }
    
    def roleSerialize(self, data):
        return {
            'roleName': data.role_name
        }
    
    def rootTreeSeriallize(self, data, types=None):
        if types is None:
            rd = []
            for each in data:
                rd.append({
                    'id': str(each.id),
                    'nameBranch': each.nameBranch,
                    'dateCreate': str(each.dateCreate),
                    'userCreate': self.userSerialize(each.userCreate),
                    'files': self.serializeFiles(each.files.all(), each.nameBranch, None, each.userCreate.username),
                    'childrenFolder': self.serializeFolders(each.childrenFolder.all(), each.nameBranch, each.userCreate.username)
                })
            return rd
        else:
            return {
                'id': str(data.id),
                'nameBranch': data.nameBranch,
                'dateCreate': str(data.dateCreate),
                'userCreate': self.userSerialize(data.userCreate),
                'files': self.serializeFiles(data.files.all(), data.nameBranch, None, data.userCreate.username),
                'childrenFolder': self.serializeFolders(data.childrenFolder.all(), data.nameBranch, data.userCreate.username)
            }
    
    def serializeFiles(self, data, node, folder, username):
        dt = []
        for each in data:
            dt.append({
                'id': str(each.id),
                'name': each.name,
                'cover': self.read_file(username, node, folder, each.cover),
                'dateCreate': str(each.dateCreate),
                'user': self.userSerialize(each.user)
            })
        return dt
    
    def serializeFolders(self, data, branch, user_create):
        dt = []
        for each in data:
            dt.append({
                'id': str(each.id),
                'nameNode': each.name_node,
                'dateCreate': str(each.date_create),
                'userCreate': self.userSerialize(each.user_create),
                'files': self.serializeFiles(each.files.all(), branch, each.name_node, user_create),
                'childrenFolder': self.serializeFolders(each.childrenFolder.all(), branch, user_create)
            })
        return dt
        
    def userSerialize(self, data):
        return {
            'id': str(data.id),
            'firstName': data.firstName,
            'lastName': data.lastName,
            'username': data.username
        }
    
    def usersSerialize(self, data):
        us = []
        for each in data:
            us.append(self.userSerialize(each))
        return us
    
    def read_file(self, user, branch, folder, name_file):
        file_data = None
        file_location = 'media/' + name_file.name

        try:
            with open(file_location, 'r') as f:
                file_data = f.read()
        except IOError:
            # handle file not exist case here
            return str('null')
        return file_data
    
# endregion
    
class AuthSerialize():

    def userInformation(self, data):
        return {
            'image': data.imageLink if data is not None and data.imageLink else ""
        }

    def userSerialize(self, data):
        return {
            'id': str(data.id),
            'firstName': data.firstName,
            'lastName': data.lastName,
            'username': data.username,
            'userInformation': self.userInformation(data.userInformation)
        }

    def loginSerialize(self, user, jwt):
        return {
            'user': self.userSerialize(user),
            'jwt': jwt
        }
