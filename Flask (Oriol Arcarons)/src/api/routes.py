from flask import jsonify, request 
from src.config.db import sessionobj
from src.models.book import Book

def init_api_routes(app):
    
    @app.route('/api/books', methods=['GET'])
    def get_books():
        books = sessionobj.query(Book).all() 
        return jsonify([
            {
                'id': b.id, 
                'title': b.title, 
                'author': b.author,
                'price': float(b.price) 
            } for b in books
        ]) 
    @app.route('/api/books/<int:id>', methods=['GET'])
    def get_book(id):
        book = sessionobj.query(Book).get(id)
        
        if not book:
            return jsonify({"error": "Libro no encontrado"}), 404
            
        return jsonify({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'price': float(book.price)
        })

    @app.route('/api/books', methods=['POST'])
    def post_book():
        data = request.get_json() 
        new_book = Book(title=data['title'], author=data['author'], price=data['price'])
        sessionobj.add(new_book)
        sessionobj.commit() 
        return jsonify({'message': 'Libro creado'}), 201 

    @app.route('/api/books/<int:id>', methods=['PUT'])
    def update_book(id):
        book = sessionobj.query(Book).get(id)
        if not book:
            return jsonify({"error": "No encontrado"}), 404 
        data = request.get_json()
        book.title = data.get('title', book.title)
        sessionobj.commit()
        return jsonify({'message': 'Actualizado'}), 200 

    @app.route('/api/books/<int:id>', methods=['DELETE'])
    def delete_book(id):
        book = sessionobj.query(Book).get(id)
        if book:
            sessionobj.delete(book)
            sessionobj.commit()
            return '', 204 
        return jsonify({"error": "No encontrado"}), 404 