from flask import Blueprint

from flask_restx import Api, Resource,Namespace


api = Namespace('view', description='first api')


class ViewApi(Resource):

    def get(self):
        return {'response':{'items':'get method'}}

    def post(self):
        return {'response':self.response}

api.add_resource(ViewApi,'/viewmethod')