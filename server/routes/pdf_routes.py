from flask import Blueprint, jsonify
from server.chat.create_embeddings import create_embeddings_for_pdf



bp = Blueprint("pdf", __name__, url_prefix="/api/pdfs")

@bp.route("/", methods=["POST"])
def embed_pdf():
    create_embeddings_for_pdf("server/static/pdf/2022_Statistical_Annex_Final__508_Compliant-revised.pdf")
    return jsonify({"message": "Embedding complete"})
