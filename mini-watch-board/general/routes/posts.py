from flask import Blueprint, redirect, render_template, request, url_for
from post_rules import validate_post
from repositories import posts as repository

posts_bp = Blueprint("posts", __name__)


def not_found():
    return render_template("error.html", message="게시글을 찾을 수 없습니다."), 404


@posts_bp.get("/")
def index():
    return render_template("index.html", posts=repository.list_posts())


@posts_bp.get("/board/<int:post_id>")
def detail(post_id):
    post = repository.find_post(post_id)
    if post is None:
        return not_found()
    return render_template("detail.html", post=post)


@posts_bp.route("/board/new", methods=["GET", "POST"])
def new():
    if request.method == "GET":
        return render_template("new.html", title="", body="")
    title, body, error = validate_post(request.form.get("title"), request.form.get("body"))
    if error:
        return render_template("new.html", title=title, body=body, error=error), 400
    post_id = repository.create_post(title, body)
    return redirect(url_for("posts.detail", post_id=post_id), code=303)


@posts_bp.route("/board/<int:post_id>/edit", methods=["GET", "POST"])
def edit(post_id):
    post = repository.find_post(post_id)
    if post is None:
        return not_found()
    if request.method == "GET":
        return render_template("edit.html", post=post, title=post["title"], body=post["body"])
    title, body, error = validate_post(request.form.get("title"), request.form.get("body"))
    if error:
        return render_template("edit.html", post=post, title=title, body=body, error=error), 400
    updated = repository.update_post(post_id, title, body)
    if updated is None:
        return not_found()
    return redirect(url_for("posts.detail", post_id=post_id), code=303)


@posts_bp.route("/board/<int:post_id>/delete", methods=["GET", "POST"])
def delete(post_id):
    if request.method == "POST":
        if repository.delete_post(post_id) is None:
            return not_found()
        return redirect(url_for("posts.index"), code=303)
    post = repository.find_post(post_id)
    if post is None:
        return not_found()
    return render_template("delete.html", post=post)
