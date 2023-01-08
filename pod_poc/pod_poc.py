from .lib.qr_gen import generate_qr
from .lib.orders import process_form
from .lib.confirm import mk_log_dir, log_delivery, get_log

import os

from flask import (Flask, request, render_template,
                    make_response, send_from_directory,
                    redirect, url_for, session)

host = "127.0.0.1"
port = 8080
pod = Flask(__name__)

@pod.route("/")
def index():
    return render_template("landing_page.html")

@pod.route("/order", methods=["GET", "POST"])
def order():
    return render_template("order.html")

@pod.route("/delivery_note", methods=["POST"])
def delivery_note():
    try:
        order = process_form(request.form)
    except:
        return render_template("order.html")
    site = f"http://{host}:{port}/confirm/{order['id']}"
    qr = generate_qr(site)
    return render_template("delivery_note.html", item=order, qr=qr, order_id=site)

@pod.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        try:
            order_number = int(request.form["string"])
            return redirect(f"/confirm/{order_number}")
        except:
            return render_template("search_order.html")
    else:
        return render_template("search_order.html")

@pod.route("/confirm/<order_number>", methods=["GET", "POST"])
def confirm(order_number=None):
    if request.method == "POST":
        if request.form.get("delivered"):
            log_delivery(order_number)
            return redirect(url_for("success"))
        else:
            return render_template("confirm_delivery.html", order_number=order_number)
    else:
        return render_template("confirm_delivery.html", order_number=order_number)

@pod.route("/success")
def success():
    return render_template("success.html")

@pod.route("/list")
def list():
    csvfiles = get_log()
    return render_template("list.html", csvfiles=csvfiles)

@pod.route("/list/<name>")
def download(name):
    path = os.path.join(os.getcwd(), "log")
    return send_from_directory(path, name, as_attachment=True)

@pod.route("/list/raw/<name>")
def raw(name):
    path = os.path.join(os.getcwd(), "log", name)
    with open(path) as fh:
        contents = [line for line in fh.readlines()]
    return render_template("raw.html", raw=contents)

def main():
    # This allows us to use a plain HTTP callback
    # ~ os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"

    # Runs web application
    # add threaded=True
    mk_log_dir()
    pod.run(debug=True, host="0.0.0.0", port=port) #ssl_context='adhoc'

if __name__ == "__main__":
    main()
