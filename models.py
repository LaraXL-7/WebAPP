from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # 'admin' o 'user'

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    vida_util = db.Column(db.String(20), nullable=False)
    unidad = db.Column(db.String(50), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    descripcion = db.Column(db.String(200))

class Movimiento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # 'entrada' o 'salida'
    cantidad = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    trabajador = db.Column(db.String(150))  # Solo relevante para movimientos de salida
    producto = db.relationship('Producto', backref=db.backref('movimientos', lazy=True))

class Herramienta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    vida_util = db.Column(db.String(20), nullable=False)
    unidad = db.Column(db.String(50), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    proyecto = db.Column(db.String(200), nullable=True)
    area_colocacion = db.Column(db.String(200), nullable=True)
    persona_asignada = db.Column(db.String(200), nullable=True)

    # Relación con MovimientoHerramienta (sin backref duplicado)
    movimientos = db.relationship('MovimientoHerramienta', backref='herramienta', cascade="all, delete-orphan", lazy=True)


class MovimientoHerramienta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    herramienta_id = db.Column(db.Integer, db.ForeignKey('herramienta.id'), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # 'entrada' o 'salida'
    cantidad = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    trabajador = db.Column(db.String(150))  # Solo relevante para movimientos de salida

    # No se necesita backref aquí si ya está en el modelo de Herramienta


class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    unidad = db.Column(db.String(50), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    proyecto = db.Column(db.String(200))  # Nueva columna para el Proyecto
    area_colocacion = db.Column(db.String(200))  # Nueva columna para el Área de Colocación
    movimientos = db.relationship('MovimientoMaterial', backref='material', cascade="all, delete-orphan", lazy=True)


class MovimientoMaterial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey('material.id'), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # 'entrada' o 'salida'
    cantidad = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    trabajador = db.Column(db.String(150))  # Solo relevante para movimientos de salida

