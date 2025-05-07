# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request
import logging
import chardet
from models.user import AppUser
from services.csv_service import process_csv_row
from database import db
import pandas as pd

csv_bp = Blueprint('csv', __name__)

logging.basicConfig(
    filename='import.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

@csv_bp.route('/upload-csv', methods=['POST'])
def upload_csv():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No CSV file provided!"}), 400
        file = request.files['file']
        if not file.filename.endswith('.csv'):
            return jsonify({"error": "File must be a CSV!"}), 400

        user_id = request.form.get('user_id', 1)
        try:
            user_id = int(user_id)
        except ValueError:
            return jsonify({"error": "Invalid user ID provided!"}), 400

        user = db.session.get(AppUser, user_id)
        if not user:
            return jsonify({"error": f"User with ID {user_id} does not exist!"}), 404

        raw_data = file.read()
        detected = chardet.detect(raw_data)
        encoding = detected['encoding'] or 'utf-8'
        file.stream.seek(0)

        try:
            df = pd.read_csv(file.stream, encoding=encoding)
        except UnicodeDecodeError:
            file.stream.seek(0)
            try:
                df = pd.read_csv(file.stream, encoding='utf-8')
            except Exception:
                return jsonify({"error": "Failed to decode CSV file!"}), 400

        if df.empty:
            return jsonify({"error": "Uploaded CSV file is empty or invalid!"}), 400

        for _, row in df.iterrows():
            process_csv_row(row, user_id)

        return jsonify({"message": "CSV processed successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error processing CSV: {str(e)}")
        return jsonify({"error": f"Error processing CSV: {str(e)}"}), 500