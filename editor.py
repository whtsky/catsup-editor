#coding=utf-8

import os
import tornado.httpserver
import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpclient
import tornado.escape
from tornado.options import define, options

define("port", default=7777, help="run on the given port", type=int)
define("posts_path", default="~/catsup/_posts", help="path to posts.")
define("webhook_url", help="your blog's webhook url.")
define("password")


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('editor.html')
        
    def post(self):
        assert self.get_argument('password') == options.password
        filename = self.get_argument('filename')
        content = self.get_argument('content')

        fpath = os.path.join(options.posts_path, filename)
        open(fpath, 'w').write(content)
        
        request = tornado.httpclient.HTTPRequest(options.webhook_url, "POST", body='miao')
        http_client = tornado.httpclient.AsyncHTTPClient()
        http_client.fetch(request, None)
        

if __name__ == '__main__':
    base_path = os.path.dirname(__file__)
    conf_path = os.path.join(base_path, "editor.conf")
    tornado.options.parse_config_file(conf_path)
    tornado.options.parse_command_line()
    application = tornado.web.Application([
            (r'/', MainHandler),
        ], debug=True,
        static_path=os.path.join(base_path, 'static'),
        template_path=os.path.join(base_path, 'template')
    )
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()