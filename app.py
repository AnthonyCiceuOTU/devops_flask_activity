from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/hello", methods=["GET"])
def hello():
    """Simple health-style endpoint returning a greeting."""
    return jsonify(message="Hello, World!")


@app.route("/echo", methods=["POST"])
def echo():
    """Echo back any JSON payload sent in the request body.

    Returns the same payload with HTTP 201 Created.
    """
    data = request.get_json(force=True, silent=True) or {}
    return jsonify(data), 201


# Very small in-memory "store" just for demo purposes.
# In a real app this would be a database or external service.
items = {}


@app.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id: int):
    """Create or update an item in the in-memory store.

    Body should be JSON, e.g. {"name": "example"}.
    Returns the stored item along with its id.
    """
    payload = request.get_json(force=True, silent=True) or {}
    items[item_id] = payload
    response = {"id": item_id, "data": payload}
    return jsonify(response), 200


@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id: int):
    """Delete an item from the in-memory store if it exists."""
    if item_id in items:
        deleted = items.pop(item_id)
        return jsonify({"id": item_id, "deleted": deleted}), 200

    return jsonify({"error": "Item not found"}), 404


if __name__ == "__main__":
    # Debug mode for local development only.
    app.run(debug=True)