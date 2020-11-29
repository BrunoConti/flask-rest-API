from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    views = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name={name}, likes={likes}, views={views})"

video_post_args = reqparse.RequestParser()
video_post_args.add_argument("name", type=str, help="Name of the Video", required=True)
video_post_args.add_argument("likes", type=int, help="Likes of the Video", required=True)
video_post_args.add_argument("views", type=int, help="Views of the Video", required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the Video")
video_update_args.add_argument("likes", type=int, help="Likes of the Video")
video_update_args.add_argument("views", type=int, help="Views of the Video")

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'likes': fields.Integer,
    'views': fields.Integer
}

class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Could not find that video!")
        return result,200

    @marshal_with(resource_fields)
    def post(self, video_id):
        args = video_post_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(404, message="That video already exist!")
        video = VideoModel(id=video_id, name=args['name'], likes=args['likes'], views=args['views'])
        db.session.add(video)
        db.session.commit()
        return video, 200

    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="That video does not exist!")
        
        if args["name"]:
            result.name = args["name"]
        if args["likes"]:
            result.likes = args["likes"]
        if args["views"]:
            result.views = args["views"]

        db.session.commit()

    def delete(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="That video does not exist!")
        db.session.delete(result)
        db.session.commit()
        return "", 201

api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True)