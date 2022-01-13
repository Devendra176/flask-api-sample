from flask_restx import reqparse
import werkzeug

class ParserArgument():
    def __init__(self):
        self.reqparse  = reqparse.RequestParser()
        super(ParserArgument,self).__init__()

    def for_login_argument(self):
        login_parser = self.reqparse
        login_parser.add_argument('email', type=str, location='form',required=True)
        login_parser.add_argument('password', type=str, location='form',required=True)
        return login_parser

    def for_put_argument(self):
        for_put = self.reqparse
        for_put.add_argument('password', type=str, 
                            location='form',required=True, 
                            help='enter existing password')
        for_put.add_argument('new_password', type=str, location='form',required=True)
        for_put.add_argument('confirm_new_password', type=str, location='form',required=True)
        return for_put
        
    def for_delete_account_arg(self):
        for_delete_account_arg = self.reqparse
        for_delete_account_arg.add_argument('password', type=str, 
                                            location='form',required=True,
                                            help='enter password for confirmation')
        return for_delete_account_arg

    def for_upload_file(self):
        for_upload_file = self.reqparse
        for_upload_file.add_argument('file',
                         type=werkzeug.datastructures.FileStorage, 
                         location='files', 
                         required=True, 
                         help='Upload file of extenstion .jpg, .png,.jpeg'
                        )
        return for_upload_file
    
    def for_profile_pic_arg(self):
        for_profile_pic_arg = self.reqparse
        for_profile_pic_arg.add_argument('img',
                         type=werkzeug.datastructures.FileStorage, 
                         location='files', 
                         required=True, 
                         help='Upload file of extenstion .jpg, .png,.jpeg'
                        )
        return for_profile_pic_arg
